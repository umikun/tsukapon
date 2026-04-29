#!/usr/bin/env python3
"""Daily Log analytics engine.

activity/YYYY-MM-DD.jsonl のみから集計する分析モジュール。
Clockify は実時間と乖離があるため使用しない（2026-04-29 ユーザー判断）。

CLI 使い方:
    python3 analytics.py daily 2026-04-29           # 日次サマリー（JSON）
    python3 analytics.py daily today                # 今日のサマリー
    python3 analytics.py weekly 2026-W18            # 週次サマリー（JSON）
    python3 analytics.py weekly current             # 今週のサマリー
    python3 analytics.py focus-peaks 2026-04-29     # 集中ピーク時間帯
    python3 analytics.py file-times 2026-04-29      # ファイル別時間
    python3 analytics.py note-time 2026-W18         # note記事執筆時間（週次）
    python3 analytics.py hourly-heatmap 2026-W18    # 時間帯別カテゴリ分布
    python3 analytics.py distraction-patterns --days 7  # 脱線パターン検出

Python から:
    from analytics import load_day, summarize_day, summarize_week
    s = summarize_day("2026-04-29")
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

# --- paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
ACTIVITY_DIR = SCRIPT_DIR / "activity"
CONFIG_PATH = SCRIPT_DIR / "activity-config.json"
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent  # _ kiwami/tools/daily-log → vault root

# --- constants ---
SAMPLE_INTERVAL_MIN = 1  # 1サンプル = 1分（activity-tracker は60秒ごと）
DEFAULT_FOCUS_PEAK_MIN_MINUTES = 30  # 連続focus N分以上を「ピーク」と呼ぶ
DEFAULT_PEAK_GAP_TOLERANCE_MIN = 2   # ピーク内で許容する非focus分（小さなトイレ離席等）


# ============================================================
# データ読み込み
# ============================================================

def load_config() -> dict:
    """activity-config.json を読む。"""
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_day(target_date: str) -> list[dict]:
    """指定日の activity JSONL を読み込む。

    Args:
        target_date: "YYYY-MM-DD" or "today" or "yesterday"

    Returns:
        records list. 空ならファイル不在。
    """
    target_date = _resolve_date(target_date)
    path = ACTIVITY_DIR / f"{target_date}.jsonl"
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def load_range(start_date: str, end_date: str) -> dict[str, list[dict]]:
    """期間内の各日の records を返す。"""
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    out: dict[str, list[dict]] = {}
    cur = start
    while cur <= end:
        key = cur.strftime("%Y-%m-%d")
        out[key] = load_day(key)
        cur += timedelta(days=1)
    return out


def _resolve_date(s: str) -> str:
    if s == "today":
        return date.today().strftime("%Y-%m-%d")
    if s == "yesterday":
        return (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    return s


def _parse_date(s: str) -> date:
    return datetime.strptime(_resolve_date(s), "%Y-%m-%d").date()


def _iso_week_to_range(iso_week: str) -> tuple[date, date]:
    """'2026-W18' or 'current' → (Mon, Sun) の date タプル。"""
    if iso_week == "current":
        today = date.today()
        year, week, _ = today.isocalendar()
    else:
        m = re.match(r"^(\d{4})-W(\d{1,2})$", iso_week)
        if not m:
            raise ValueError(f"invalid ISO week: {iso_week}")
        year, week = int(m.group(1)), int(m.group(2))
    monday = date.fromisocalendar(year, week, 1)
    sunday = monday + timedelta(days=6)
    return monday, sunday


# ============================================================
# 集計プリミティブ
# ============================================================

def summarize_categories(records: list[dict]) -> dict[str, int]:
    """カテゴリ別の分（=サンプル数）を返す。"""
    c = Counter()
    for r in records:
        c[r.get("cat", "unknown")] += SAMPLE_INTERVAL_MIN
    return dict(c)


def summarize_apps(records: list[dict], top_n: int = 10) -> list[tuple[str, int, str]]:
    """アプリ別時間ランキング。返り値: [(app, minutes, dominant_cat), ...]"""
    by_app: dict[str, Counter] = defaultdict(Counter)
    for r in records:
        app = r.get("app", "unknown") or "unknown"
        cat = r.get("cat", "unknown")
        by_app[app][cat] += SAMPLE_INTERVAL_MIN
    rows = []
    for app, cat_counter in by_app.items():
        total = sum(cat_counter.values())
        dominant = cat_counter.most_common(1)[0][0]
        rows.append((app, total, dominant))
    rows.sort(key=lambda x: x[1], reverse=True)
    return rows[:top_n]


# Obsidian title: "<file> - <vault> - Obsidian X.Y.Z"
OBSIDIAN_TITLE_RE = re.compile(r"^(.+?)\s+-\s+[^-]+\s+-\s+Obsidian")
# Cursor / VSCode: "<file> — <project>" or "<file> - <project>"
CURSOR_TITLE_RE = re.compile(r"^(.+?)\s+[—-]\s+")


def extract_file_from_title(app: str, title: str) -> str | None:
    """ウィンドウタイトルからファイル名を抽出。取れなかったら None。"""
    if not title:
        return None
    if app == "Obsidian":
        m = OBSIDIAN_TITLE_RE.match(title)
        if m:
            return m.group(1).strip()
    if app in ("Cursor", "Antigravity", "Code", "Visual Studio Code"):
        m = CURSOR_TITLE_RE.match(title)
        if m:
            return m.group(1).strip()
    return None


def summarize_files(records: list[dict], top_n: int = 15) -> list[tuple[str, int, str]]:
    """ファイル別時間（Obsidian/Cursor等の編集対象）。
    返り値: [(file, minutes, app), ...]"""
    by_file: dict[tuple[str, str], int] = defaultdict(int)
    for r in records:
        if r.get("cat") != "focus":
            continue
        app = r.get("app", "")
        title = r.get("title", "") or ""
        fname = extract_file_from_title(app, title)
        if fname:
            by_file[(fname, app)] += SAMPLE_INTERVAL_MIN
    rows = [(f, m, a) for (f, a), m in by_file.items()]
    rows.sort(key=lambda x: x[1], reverse=True)
    return rows[:top_n]


def find_focus_peaks(
    records: list[dict],
    min_minutes: int = DEFAULT_FOCUS_PEAK_MIN_MINUTES,
    gap_tolerance: int = DEFAULT_PEAK_GAP_TOLERANCE_MIN,
) -> list[dict]:
    """連続focus時間帯を抽出。

    gap_tolerance 分以下の途切れは同じピーク内とみなす。
    返り値: [{"start": "09:30", "end": "11:15", "minutes": 105, "top_app": "Obsidian"}, ...]
    """
    if not records:
        return []
    sorted_recs = sorted(records, key=lambda r: r.get("ts", ""))
    peaks: list[dict] = []
    cur_start: str | None = None
    cur_end: str | None = None
    cur_app_counter: Counter = Counter()
    gap = 0

    for r in sorted_recs:
        ts = r.get("ts", "")
        cat = r.get("cat", "")
        if cat == "focus":
            if cur_start is None:
                cur_start = ts
            cur_end = ts
            cur_app_counter[r.get("app", "?")] += 1
            gap = 0
        else:
            if cur_start is not None:
                gap += 1
                if gap > gap_tolerance:
                    minutes = _ts_diff(cur_start, cur_end) + 1
                    if minutes >= min_minutes:
                        peaks.append({
                            "start": cur_start,
                            "end": cur_end,
                            "minutes": minutes,
                            "top_app": cur_app_counter.most_common(1)[0][0] if cur_app_counter else "?",
                        })
                    cur_start = None
                    cur_end = None
                    cur_app_counter = Counter()
                    gap = 0

    # 末尾処理
    if cur_start is not None and cur_end is not None:
        minutes = _ts_diff(cur_start, cur_end) + 1
        if minutes >= min_minutes:
            peaks.append({
                "start": cur_start,
                "end": cur_end,
                "minutes": minutes,
                "top_app": cur_app_counter.most_common(1)[0][0] if cur_app_counter else "?",
            })

    peaks.sort(key=lambda p: p["minutes"], reverse=True)
    return peaks


def _ts_diff(start: str, end: str) -> int:
    """HH:MM 形式の差分を分で返す。"""
    sh, sm = map(int, start.split(":"))
    eh, em = map(int, end.split(":"))
    return (eh * 60 + em) - (sh * 60 + sm)


def hourly_heatmap(records: list[dict]) -> dict[int, dict[str, int]]:
    """時間帯別（0-23時）のカテゴリ分布。
    返り値: {hour: {cat: minutes}}"""
    out: dict[int, Counter] = defaultdict(Counter)
    for r in records:
        ts = r.get("ts", "")
        if ":" not in ts:
            continue
        hour = int(ts.split(":")[0])
        out[hour][r.get("cat", "unknown")] += SAMPLE_INTERVAL_MIN
    return {h: dict(c) for h, c in out.items()}


# ============================================================
# 高レベル: 日次・週次サマリー
# ============================================================

def summarize_day(target_date: str) -> dict:
    """日次サマリー（人間可読＋プログラム可読）。"""
    target_date = _resolve_date(target_date)
    records = load_day(target_date)
    if not records:
        return {"date": target_date, "empty": True, "minutes_tracked": 0}

    cats = summarize_categories(records)
    apps = summarize_apps(records, top_n=10)
    files = summarize_files(records, top_n=15)
    peaks = find_focus_peaks(records)
    heatmap = hourly_heatmap(records)
    total = sum(cats.values())
    focus_min = cats.get("focus", 0)

    # 集中度スコア = focus / (focus + distraction + other)（idle除外）
    productive_total = focus_min + cats.get("distraction", 0) + cats.get("other", 0)
    focus_ratio = (focus_min / productive_total * 100) if productive_total else 0

    return {
        "date": target_date,
        "minutes_tracked": total,
        "categories": cats,
        "focus_ratio_pct": round(focus_ratio, 1),
        "top_apps": [{"app": a, "minutes": m, "cat": c} for a, m, c in apps],
        "top_files": [{"file": f, "minutes": m, "app": a} for f, m, a in files],
        "focus_peaks": peaks,
        "hourly_heatmap": heatmap,
    }


def summarize_week(iso_week: str) -> dict:
    """週次サマリー。曜日別 + 集計値。"""
    monday, sunday = _iso_week_to_range(iso_week)
    week_label = f"{monday.isocalendar().year}-W{monday.isocalendar().week:02d}"
    days_data = load_range(monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d"))

    by_day: dict[str, dict] = {}
    total_cats: Counter = Counter()
    all_records: list[dict] = []
    for d, recs in days_data.items():
        if not recs:
            by_day[d] = {"empty": True}
            continue
        cats = summarize_categories(recs)
        by_day[d] = {
            "weekday": _parse_date(d).strftime("%a"),
            "minutes_tracked": sum(cats.values()),
            "categories": cats,
        }
        for k, v in cats.items():
            total_cats[k] += v
        all_records.extend(recs)

    # 曜日別ヒートマップ
    weekday_heatmap: dict[str, dict[int, dict[str, int]]] = {}
    for d, recs in days_data.items():
        if not recs:
            continue
        wd = _parse_date(d).strftime("%a")
        weekday_heatmap[wd] = hourly_heatmap(recs)

    apps = summarize_apps(all_records, top_n=10)
    files = summarize_files(all_records, top_n=20)
    peaks = find_focus_peaks(all_records, min_minutes=30)

    productive_total = total_cats.get("focus", 0) + total_cats.get("distraction", 0) + total_cats.get("other", 0)
    focus_ratio = (total_cats.get("focus", 0) / productive_total * 100) if productive_total else 0

    return {
        "iso_week": week_label,
        "range": {"start": monday.strftime("%Y-%m-%d"), "end": sunday.strftime("%Y-%m-%d")},
        "totals": {
            "minutes_tracked": sum(total_cats.values()),
            "categories": dict(total_cats),
            "focus_ratio_pct": round(focus_ratio, 1),
        },
        "by_day": by_day,
        "weekday_hourly_heatmap": weekday_heatmap,
        "top_apps": [{"app": a, "minutes": m, "cat": c} for a, m, c in apps],
        "top_files": [{"file": f, "minutes": m, "app": a} for f, m, a in files],
        "focus_peaks": peaks[:10],
    }


# ============================================================
# SNS運用 連携: note執筆時間 / 脱線パターン検出
# ============================================================

NOTE_FILE_RE = re.compile(r"note-(\d{8})")
THREAD_FILE_RE = re.compile(r"(\d{8}).*thread|thread.*(\d{8})", re.IGNORECASE)


def note_writing_time(iso_week: str) -> dict:
    """週次のnote記事執筆時間（titleに 'note-YYYYMMDD' を含む focus 時間）。"""
    monday, sunday = _iso_week_to_range(iso_week)
    days_data = load_range(monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d"))

    by_article: dict[str, int] = defaultdict(int)
    by_day: dict[str, int] = defaultdict(int)
    total = 0
    for d, recs in days_data.items():
        for r in recs:
            if r.get("cat") != "focus":
                continue
            title = r.get("title", "") or ""
            m = NOTE_FILE_RE.search(title)
            if not m:
                continue
            article_date = m.group(1)  # YYYYMMDD
            by_article[f"note-{article_date}"] += SAMPLE_INTERVAL_MIN
            by_day[d] += SAMPLE_INTERVAL_MIN
            total += SAMPLE_INTERVAL_MIN

    return {
        "iso_week": iso_week,
        "total_minutes": total,
        "by_article": dict(sorted(by_article.items(), key=lambda x: x[1], reverse=True)),
        "by_day": dict(sorted(by_day.items())),
    }


def detect_distraction_patterns(days: int = 7, min_occurrences: int = 3) -> list[dict]:
    """直近N日の脱線パターン検出（自己改善ループ用）。

    「同じ時間帯（hour）に同じアプリで脱線」を min_occurrences 回以上検出したら返す。
    """
    end = date.today()
    start = end - timedelta(days=days - 1)
    days_data = load_range(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

    # (hour, app) → 出現日数（同じ日に複数あっても 1日 1カウント）
    counter: dict[tuple[int, str], set] = defaultdict(set)
    for d, recs in days_data.items():
        for r in recs:
            if r.get("cat") != "distraction":
                continue
            ts = r.get("ts", "")
            if ":" not in ts:
                continue
            hour = int(ts.split(":")[0])
            app = r.get("app", "?")
            counter[(hour, app)].add(d)

    patterns = []
    for (hour, app), days_set in counter.items():
        if len(days_set) >= min_occurrences:
            patterns.append({
                "hour": hour,
                "app": app,
                "occurred_days": sorted(days_set),
                "occurrence_count": len(days_set),
            })
    patterns.sort(key=lambda p: p["occurrence_count"], reverse=True)
    return patterns


# ============================================================
# CLI
# ============================================================

def _print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily Log analytics")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_daily = sub.add_parser("daily", help="日次サマリー")
    p_daily.add_argument("date", help="YYYY-MM-DD or 'today' / 'yesterday'")

    p_weekly = sub.add_parser("weekly", help="週次サマリー")
    p_weekly.add_argument("week", help="YYYY-Wnn or 'current'")

    p_peaks = sub.add_parser("focus-peaks", help="集中ピーク時間帯")
    p_peaks.add_argument("date", help="YYYY-MM-DD or 'today'")
    p_peaks.add_argument("--min-minutes", type=int, default=30)

    p_files = sub.add_parser("file-times", help="ファイル別時間")
    p_files.add_argument("date", help="YYYY-MM-DD or 'today'")

    p_note = sub.add_parser("note-time", help="note記事執筆時間（週次）")
    p_note.add_argument("week", help="YYYY-Wnn or 'current'")

    p_heat = sub.add_parser("hourly-heatmap", help="時間帯別カテゴリ分布")
    p_heat.add_argument("week", help="YYYY-Wnn or 'current'")

    p_dist = sub.add_parser("distraction-patterns", help="脱線パターン検出")
    p_dist.add_argument("--days", type=int, default=7)
    p_dist.add_argument("--min-occurrences", type=int, default=3)

    args = parser.parse_args()

    if args.cmd == "daily":
        _print_json(summarize_day(args.date))
    elif args.cmd == "weekly":
        _print_json(summarize_week(args.week))
    elif args.cmd == "focus-peaks":
        recs = load_day(args.date)
        _print_json(find_focus_peaks(recs, min_minutes=args.min_minutes))
    elif args.cmd == "file-times":
        recs = load_day(args.date)
        rows = summarize_files(recs, top_n=20)
        _print_json([{"file": f, "minutes": m, "app": a} for f, m, a in rows])
    elif args.cmd == "note-time":
        _print_json(note_writing_time(args.week))
    elif args.cmd == "hourly-heatmap":
        s = summarize_week(args.week)
        _print_json(s["weekday_hourly_heatmap"])
    elif args.cmd == "distraction-patterns":
        _print_json(detect_distraction_patterns(days=args.days, min_occurrences=args.min_occurrences))
    return 0


if __name__ == "__main__":
    sys.exit(main())
