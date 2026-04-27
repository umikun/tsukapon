#!/usr/bin/env python3
"""git-repos.json で指定された全リポジトリを並列 fetch するユーティリティ。

呼び出し方:
  python3 git-fetcher.py            # テキストログ
  python3 git-fetcher.py --json     # JSON結果を stdout に出力（API用）

挙動:
  - 各リポジトリで `git fetch --all --prune --quiet` を最大15秒で実行
  - 並列実行（最大4並列）
  - 失敗してもexit 0（launchdを止めないため）
  - 結果を /tmp/daily-log-git-fetcher.json に保存（UIから最終実行時刻を読む用）
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

HOME = Path.home()
VAULT_ROOT = HOME / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon"
GIT_REPOS_CONFIG = VAULT_ROOT / "_ kiwami" / "tools" / "daily-log" / "git-repos.json"
STATE_PATH = Path("/tmp/daily-log-git-fetcher.json")

FETCH_TIMEOUT = 15
MAX_WORKERS = 4


def load_repos() -> list[str]:
    if not GIT_REPOS_CONFIG.exists():
        return []
    try:
        raw = GIT_REPOS_CONFIG.read_text(encoding="utf-8")
        stripped = re.sub(r"^\s*//.*$", "", raw, flags=re.MULTILINE)
        config = json.loads(stripped)
    except (OSError, json.JSONDecodeError):
        return []
    repos = config.get("repos") or []
    return [str(p) for p in repos if isinstance(p, str)]


# 認証絡みの典型的なエラーパターン（kind="auth" として分類）
_AUTH_ERROR_PATTERNS = (
    "could not read Password",
    "Device not configured",
    "Authentication failed",
    "remote: Invalid username or password",
    "fatal: Authentication",
    "Permission denied (publickey)",
    "fatal: Could not read from remote repository",
)


def classify_error(err: str) -> str:
    """エラー文字列を 'auth' / 'fail' に分類。"""
    if not err:
        return "fail"
    for pat in _AUTH_ERROR_PATTERNS:
        if pat in err:
            return "auth"
    return "fail"


def fetch_one(repo_path_str: str) -> dict:
    repo_path = Path(repo_path_str).expanduser()
    # kind: "ok" | "auth" | "fail"  (auth = 認証要設定で実害なし、fail = 実エラー)
    result: dict = {"path": str(repo_path), "name": repo_path.name, "ok": False, "kind": "fail", "error": ""}
    if not repo_path.exists():
        result["error"] = "repo not found"
        return result
    if not (repo_path / ".git").exists():
        result["error"] = "not a git repo"
        return result
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_path), "fetch", "--all", "--prune", "--quiet"],
            capture_output=True, text=True, timeout=FETCH_TIMEOUT,
        )
        if proc.returncode == 0:
            result["ok"] = True
            result["kind"] = "ok"
        else:
            err = (proc.stderr or proc.stdout or "").strip().splitlines()
            result["error"] = err[-1] if err else f"exit {proc.returncode}"
            result["kind"] = classify_error(result["error"])
    except FileNotFoundError:
        result["error"] = "git not found"
    except subprocess.TimeoutExpired:
        result["error"] = f"timeout ({FETCH_TIMEOUT}s)"
    except Exception as e:
        result["error"] = str(e)
    return result


def fetch_all() -> dict:
    started_at = datetime.now().astimezone()
    repos = load_repos()
    results: list[dict] = []
    if repos:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            futures = {ex.submit(fetch_one, p): p for p in repos}
            for f in as_completed(futures):
                results.append(f.result())
    finished_at = datetime.now().astimezone()
    summary = {
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_sec": round((finished_at - started_at).total_seconds(), 2),
        "total": len(results),
        "ok": sum(1 for r in results if r["kind"] == "ok"),
        "auth": sum(1 for r in results if r["kind"] == "auth"),
        "failed": sum(1 for r in results if r["kind"] == "fail"),
        "results": sorted(results, key=lambda r: r["name"]),
    }
    try:
        STATE_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass
    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="stdoutにJSONを出力")
    args = ap.parse_args()
    summary = fetch_all()
    if args.json:
        json.dump(summary, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(f"[git-fetcher] {summary['finished_at']} "
              f"total={summary['total']} ok={summary['ok']} auth={summary['auth']} failed={summary['failed']} "
              f"({summary['duration_sec']}s)")
        for r in summary["results"]:
            mark = {"ok": "✓", "auth": "🔑", "fail": "✗"}.get(r["kind"], "?")
            extra = "" if r["kind"] == "ok" else f" ({r['error']})"
            print(f"  {mark} {r['name']}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
