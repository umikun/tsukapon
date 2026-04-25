#!/usr/bin/env python3
"""Activity Tracker for Daily Log.

launchd から60秒ごとに起動される想定。
- 最前面アプリ名・ウィンドウタイトル・アイドル秒を取得
- activity-config.json に従ってカテゴリ分類
- activity/YYYY-MM-DD.jsonl に1行ずつ append-only で記録

Daily Log ダッシュボード (Cowork artifact: daily-log) がこのJSONLを読み込み、
- 活動タイムライン（カテゴリ色で1日を可視化）
- カテゴリ別時間集計
- 15分以上連続した「脱線」セッションのアラート
を表示する。

必要なmacOS権限:
- アクセシビリティ（System Events にウィンドウタイトル取得を許可）
- 画面収録は不要（スクリーンショットは撮らない）
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
VAULT_ROOT = HOME / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon"
BASE_DIR = VAULT_ROOT / "_ kiwami" / "tools" / "daily-log"
ACTIVITY_DIR = BASE_DIR / "activity"
CONFIG_FILE = BASE_DIR / "activity-config.json"

# AppleScript: 最前面アプリ名 + ウィンドウタイトルを改行区切りで返す
APPLESCRIPT = """
try
  tell application "System Events"
    set frontApp to name of first application process whose frontmost is true
    set frontTitle to ""
    try
      tell process frontApp
        set frontTitle to name of front window
      end tell
    end try
    return frontApp & linefeed & frontTitle
  end tell
on error errMsg
  return "unknown" & linefeed & ""
end try
"""


def get_idle_seconds() -> int:
    """HIDIdleTime (ナノ秒) を秒に変換して返す."""
    try:
        out = subprocess.check_output(
            ["ioreg", "-c", "IOHIDSystem"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        for line in out.splitlines():
            if '"HIDIdleTime"' in line:
                parts = line.strip().split("=")
                if len(parts) == 2:
                    try:
                        return int(parts[1].strip()) // 1_000_000_000
                    except ValueError:
                        pass
    except Exception:
        pass
    return 0


def get_front_app_and_title() -> tuple[str, str]:
    """最前面アプリ名とウィンドウタイトルを取得."""
    try:
        out = subprocess.check_output(
            ["osascript", "-e", APPLESCRIPT],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).rstrip("\n")
        parts = out.split("\n", 1)
        app = (parts[0] if parts else "").strip() or "unknown"
        title = (parts[1] if len(parts) > 1 else "").strip()
        return app, title
    except Exception:
        return "unknown", ""


def categorize(app: str, idle_s: int, config: dict) -> str:
    """アプリ名とアイドル秒からカテゴリを決定."""
    idle_threshold = config.get("idle_threshold_seconds", 180)
    if idle_s >= idle_threshold:
        return "idle"
    for cat_key, cat_info in config.get("categories", {}).items():
        for known_app in cat_info.get("apps", []):
            if app == known_app:
                return cat_key
    return "other"


def main() -> int:
    # 設定読み込み
    try:
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(
            f"[activity-tracker] ERROR: Config not found: {CONFIG_FILE}",
            file=sys.stderr,
        )
        return 1
    except json.JSONDecodeError as e:
        print(
            f"[activity-tracker] ERROR: Invalid JSON in {CONFIG_FILE}: {e}",
            file=sys.stderr,
        )
        return 1

    idle_s = get_idle_seconds()
    app, title = get_front_app_and_title()
    cat = categorize(app, idle_s, config)

    now = datetime.now().astimezone()
    ts_short = now.strftime("%H:%M")
    date_key = now.strftime("%Y-%m-%d")

    ACTIVITY_DIR.mkdir(parents=True, exist_ok=True)
    out_file = ACTIVITY_DIR / f"{date_key}.jsonl"

    line = json.dumps(
        {
            "ts": ts_short,
            "app": app,
            "title": title,
            "idle": idle_s,
            "cat": cat,
        },
        ensure_ascii=False,
    )

    with out_file.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
