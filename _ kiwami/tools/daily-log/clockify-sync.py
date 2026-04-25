#!/usr/bin/env python3
"""Clockify 時間エントリ同期スクリプト (Daily Log用).

launchd から15分ごとに起動される想定。
- ~/.config/clockify-sync/api_key から API キーを読み込む
- Clockify API を叩いて直近（昨日〜明日UTC）の time entry を取得
- _ kiwami/tools/daily-log/clockify/YYYY-MM-DD.json に日付別保存
- Daily Log ダッシュボード (Cowork artifact: daily-log) がこのJSONを読み込んで表示

参考: Claudian-スキル一覧.md の「Daily Log（Cowork artifact）」セクション
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- config ---
HOME = Path.home()
KEY_FILE = HOME / ".config" / "clockify-sync" / "api_key"
VAULT_ROOT = HOME / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon"
OUT_DIR = VAULT_ROOT / "_ kiwami" / "tools" / "daily-log" / "clockify"
LOG_PREFIX = "[clockify-sync]"

API_BASE = "https://api.clockify.me/api/v1"
REQUEST_TIMEOUT = 20  # seconds
DAYS_BACK = 2
DAYS_FORWARD = 1


def log(msg: str) -> None:
    print(f"{LOG_PREFIX} {msg}", flush=True)


def err(msg: str) -> None:
    print(f"{LOG_PREFIX} ERROR: {msg}", file=sys.stderr, flush=True)


def read_api_key() -> str:
    if not KEY_FILE.exists():
        err(f"API key file not found: {KEY_FILE}")
        err(f"Create it with:")
        err(f"  mkdir -p '{KEY_FILE.parent}'")
        err(f"  echo 'YOUR_CLOCKIFY_API_KEY' > '{KEY_FILE}'")
        err(f"  chmod 600 '{KEY_FILE}'")
        sys.exit(1)
    key = KEY_FILE.read_text().strip()
    if not key:
        err(f"API key file is empty: {KEY_FILE}")
        sys.exit(1)
    return key


def api_get(path: str, api_key: str, params: dict | None = None) -> object:
    url = API_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"X-Api-Key": api_key, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        err(f"HTTP {e.code} on {path}: {body}")
        raise
    except urllib.error.URLError as e:
        err(f"Network error on {path}: {e.reason}")
        raise


def parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def simplify_entry(e: dict) -> dict:
    ti = e.get("timeInterval") or {}
    start_utc = parse_iso(ti.get("start"))
    end_utc = parse_iso(ti.get("end"))
    start_local = start_utc.astimezone() if start_utc else None
    end_local = end_utc.astimezone() if end_utc else None

    project = e.get("project") or {}
    tags = e.get("tags") or []

    return {
        "id": e.get("id"),
        "description": (e.get("description") or "").strip(),
        "start": start_local.isoformat() if start_local else None,
        "end": end_local.isoformat() if end_local else None,
        "duration_iso": ti.get("duration"),
        "project": project.get("name") or "",
        "project_color": project.get("color") or "",
        "tags": [t.get("name") for t in tags if t.get("name")],
        "billable": bool(e.get("billable")),
        "is_running": end_utc is None,
    }


def group_by_local_date(entries: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for e in entries:
        if not e.get("start"):
            continue
        local = datetime.fromisoformat(e["start"])
        key = local.strftime("%Y-%m-%d")
        grouped.setdefault(key, []).append(e)
    for key in grouped:
        grouped[key].sort(key=lambda x: x["start"] or "")
    return grouped


def main() -> int:
    api_key = read_api_key()

    log("Fetching user info...")
    user = api_get("/user", api_key)
    user_id = user["id"]
    ws_id = user["activeWorkspace"]
    log(f"user_id={user_id} workspace_id={ws_id}")

    now_utc = datetime.now(timezone.utc)
    start = (now_utc - timedelta(days=DAYS_BACK)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end = (now_utc + timedelta(days=DAYS_FORWARD)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    params = {
        "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hydrated": "true",
        "page-size": "500",
        "in-progress": "true",
    }
    log(f"Fetching time entries between {params['start']} and {params['end']}...")
    raw = api_get(f"/workspaces/{ws_id}/user/{user_id}/time-entries", api_key, params)
    if not isinstance(raw, list):
        err(f"Unexpected response shape: {type(raw).__name__}")
        return 2
    log(f"Got {len(raw)} entries")

    simplified = [simplify_entry(e) for e in raw]
    grouped = group_by_local_date(simplified)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    today_local = datetime.now().strftime("%Y-%m-%d")
    if today_local not in grouped:
        grouped[today_local] = []

    written = 0
    for date_key, entries_for_date in grouped.items():
        out_path = OUT_DIR / f"{date_key}.json"
        payload = {
            "date": date_key,
            "synced_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "workspace_id": ws_id,
            "user_id": user_id,
            "entries": entries_for_date,
        }
        out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        log(f"Wrote {out_path.name} ({len(entries_for_date)} entries)")
        written += 1

    (OUT_DIR / "_latest.json").write_text(
        json.dumps(
            {
                "synced_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "workspace_id": ws_id,
                "user_id": user_id,
                "files_written": written,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    log("Done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
