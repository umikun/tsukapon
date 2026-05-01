#!/usr/bin/env python3
"""Daily Log standalone server.

ブラウザから http://127.0.0.1:8765 でアクセスできるダッシュボード。
Cowork を介さずに、ローカルに保存されている activity / clockify / Markdownファイル
の3ソースを統合表示する。

提供API:
  GET  /                           → ダッシュボードHTML (index.html)
  GET  /favicon.svg                → daily-log/oclock.svg をファビコンとして配信
  GET  /api/activity/YYYY-MM-DD    → その日のactivity JSONLをパースしたJSON
  GET  /api/clockify/YYYY-MM-DD    → その日のclockify JSON + _latest.json
  GET  /api/files/YYYY-MM-DD       → その日に編集されたTsukapon内の.mdファイル一覧
  GET  /api/commits/YYYY-MM-DD     → git-repos.json で指定したリポジトリの自分のコミット一覧
  GET  /api/memo/YYYY-MM-DD        → vault/Daily Log/memo/YYYY-MM-DD.md の本文を返す
  POST /api/memo/YYYY-MM-DD        → vault/Daily Log/memo/YYYY-MM-DD.md に上書き保存
  POST /api/save-md/YYYY-MM-DD     → 本文を vault/Daily Log/YYYY-MM-DD.md に上書き保存
  GET  /api/reminders              → reminders-cli で macOS Reminders を取得（全リスト読み取り）

Carrier: stdlib only (http.server, json, pathlib, datetime)
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

# --- config ---
HOME = Path.home()
VAULT_ROOT = HOME / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon"
BASE = VAULT_ROOT / "_ kiwami" / "tools" / "daily-log"
INDEX_HTML = BASE / "server" / "index.html"
ACTIVITY_DIR = BASE / "activity"
CLOCKIFY_DIR = BASE / "clockify"
REPORTS_DIR = VAULT_ROOT / "Daily Log"
MEMO_DIR = REPORTS_DIR / "memo"
FAVICON_PATH = BASE / "oclock.svg"
GIT_REPOS_CONFIG = BASE / "git-repos.json"
# 起動コピー側にも置いてあれば優先（launchdが叩く本体）
GIT_FETCHER_SCRIPT = (
    HOME / "bin/daily-log/git-fetcher.py"
    if (HOME / "bin/daily-log/git-fetcher.py").exists()
    else BASE / "git-fetcher.py"
)
GIT_FETCHER_STATE = Path("/tmp/daily-log-git-fetcher.json")

HOST = os.environ.get("DAILY_LOG_HOST", "127.0.0.1")
PORT = int(os.environ.get("DAILY_LOG_PORT", "8765"))

# .md スキャン時に無視するパス
EXCLUDE_DIRS = {".obsidian", ".claude", ".claudian", ".agents", ".trash", "node_modules"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class Handler(BaseHTTPRequestHandler):
    server_version = "DailyLog/1.0"

    # --- ルーティング ---
    def do_GET(self):  # noqa: N802
        url = urlparse(self.path)
        path = url.path

        if path in ("/", "/index.html"):
            self._serve_file(INDEX_HTML, "text/html; charset=utf-8")
            return
        if path in ("/favicon.svg", "/favicon.ico"):
            self._serve_file(FAVICON_PATH, "image/svg+xml")
            return
        if path == "/healthz":
            self._json({"ok": True, "time": datetime.now().astimezone().isoformat()})
            return
        if path.startswith("/api/activity/"):
            self._handle_activity(path[len("/api/activity/"):])
            return
        if path.startswith("/api/clockify/"):
            self._handle_clockify(path[len("/api/clockify/"):])
            return
        if path.startswith("/api/files/"):
            self._handle_files(path[len("/api/files/"):])
            return
        if path.startswith("/api/memo/"):
            self._handle_memo_get(path[len("/api/memo/"):])
            return
        if path.startswith("/api/commits/"):
            self._handle_commits(path[len("/api/commits/"):])
            return
        if path == "/api/fetch-status":
            self._handle_fetch_status()
            return
        if path == "/api/reminders":
            self._handle_reminders()
            return
        self.send_error(404, "Not found")

    def do_POST(self):  # noqa: N802
        url = urlparse(self.path)
        path = url.path
        if path.startswith("/api/save-md/"):
            self._handle_save_md(path[len("/api/save-md/"):])
            return
        if path.startswith("/api/memo/"):
            self._handle_memo_post(path[len("/api/memo/"):])
            return
        if path == "/api/fetch":
            self._handle_fetch()
            return
        self.send_error(404, "Not found")

    def do_OPTIONS(self):  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # --- ハンドラ ---
    def _handle_activity(self, date_key: str) -> None:
        if not self._validate_date(date_key):
            return
        samples: list[dict] = []
        path = ACTIVITY_DIR / f"{date_key}.jsonl"
        if path.exists():
            try:
                for line in path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        samples.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            except OSError as e:
                self._json({"error": f"read failed: {e}"}, status=500)
                return
        self._json({"date": date_key, "samples": samples})

    def _handle_clockify(self, date_key: str) -> None:
        if not self._validate_date(date_key):
            return
        result = {"latest": None, "day": None}
        latest_path = CLOCKIFY_DIR / "_latest.json"
        day_path = CLOCKIFY_DIR / f"{date_key}.json"
        if latest_path.exists():
            try:
                result["latest"] = json.loads(latest_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        if day_path.exists():
            try:
                result["day"] = json.loads(day_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        self._json(result)

    def _handle_files(self, date_key: str) -> None:
        if not self._validate_date(date_key):
            return
        try:
            target_date = datetime.strptime(date_key, "%Y-%m-%d").date()
        except ValueError:
            self.send_error(400, "Invalid date")
            return

        matched: list[dict] = []
        try:
            for md_file in VAULT_ROOT.rglob("*.md"):
                try:
                    if any(part in EXCLUDE_DIRS for part in md_file.parts):
                        continue
                    stat = md_file.stat()
                    mtime = datetime.fromtimestamp(stat.st_mtime)
                    if mtime.date() != target_date:
                        continue
                    rel = md_file.relative_to(VAULT_ROOT)
                    matched.append(
                        {
                            "date": mtime.strftime("%Y-%m-%d"),
                            "time": mtime.strftime("%H:%M"),
                            "path": str(rel),
                            "size": stat.st_size,
                        }
                    )
                except OSError:
                    continue
        except Exception as e:
            self._json({"error": str(e)}, status=500)
            return

        matched.sort(key=lambda f: f["time"], reverse=True)
        self._json({"date": date_key, "files": matched})

    def _handle_commits(self, date_key: str) -> None:
        if not self._validate_date(date_key):
            return
        try:
            target_date = datetime.strptime(date_key, "%Y-%m-%d").date()
        except ValueError:
            self.send_error(400, "Invalid date")
            return

        config = {"repos": [], "author_email": None}
        if GIT_REPOS_CONFIG.exists():
            try:
                raw = GIT_REPOS_CONFIG.read_text(encoding="utf-8")
                # `//` 行コメントを許可（先頭の空白に続く // から行末まで除去）
                stripped = re.sub(r"^\s*//.*$", "", raw, flags=re.MULTILINE)
                config = json.loads(stripped)
            except (OSError, json.JSONDecodeError) as e:
                self._json({"error": f"config read failed: {e}"}, status=500)
                return

        repo_paths = config.get("repos") or []
        ae = config.get("author_email")
        if ae is None:
            global_emails: list[str] = []
        elif isinstance(ae, str):
            global_emails = [ae] if ae.strip() else []
        elif isinstance(ae, list):
            global_emails = [s for s in ae if isinstance(s, str) and s.strip()]
        else:
            global_emails = []
        since = target_date.strftime("%Y-%m-%d 00:00:00")
        until = (target_date + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

        repos: list[dict] = []
        total = 0
        errors: list[str] = []
        for repo_path_str in repo_paths:
            repo_path = Path(repo_path_str).expanduser()
            entry: dict = {"path": str(repo_path), "name": repo_path.name, "commits": []}
            if not (repo_path / ".git").exists() and not repo_path.is_dir():
                entry["error"] = "not a git repo"
                repos.append(entry)
                continue
            emails = global_emails or [e for e in [self._git_user_email(repo_path)] if e]
            entry["author"] = ", ".join(emails) if emails else "(unknown)"
            if not emails:
                entry["error"] = "git user.email 未設定"
                repos.append(entry)
                continue
            commits, err = self._git_log_for_day(repo_path, emails, since, until)
            if err:
                entry["error"] = err
                errors.append(f"{repo_path.name}: {err}")
            entry["commits"] = commits
            total += len(commits)
            repos.append(entry)

        self._json({
            "date": date_key,
            "total": total,
            "repos": repos,
            "errors": errors,
        })

    @staticmethod
    def _git_user_email(repo_path: Path) -> str:
        try:
            out = subprocess.check_output(
                ["git", "-C", str(repo_path), "config", "user.email"],
                text=True, stderr=subprocess.DEVNULL, timeout=5,
            ).strip()
            return out
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return ""

    @staticmethod
    def _git_log_for_day(repo_path: Path, emails: list[str], since: str, until: str) -> tuple[list[dict], str]:
        # 区切りに NUL を使って改行を含むメッセージにも対応
        sep = "\x1f"
        rec = "\x1e"
        # %S: そのコミットを到達した source ref（--source 必須）
        # %P: 親コミット一覧（マージ判定用、空白区切り）
        fmt = sep.join(["%H", "%h", "%cI", "%an", "%ae", "%S", "%P", "%s"]) + rec
        author_args: list[str] = []
        for em in emails:
            author_args.append(f"--author={em}")
        try:
            out = subprocess.check_output(
                [
                    "git", "-C", str(repo_path), "log",
                    *author_args,
                    f"--since={since}", f"--until={until}",
                    "--all", "--source",
                    f"--pretty=format:{fmt}",
                ],
                text=True, stderr=subprocess.PIPE, timeout=10,
            )
        except FileNotFoundError:
            return [], "git コマンドが見つかりません"
        except subprocess.TimeoutExpired:
            return [], "git log がタイムアウト"
        except subprocess.CalledProcessError as e:
            err_msg = (e.stderr or "").strip().splitlines()
            return [], err_msg[-1] if err_msg else "git log 失敗"

        commits: list[dict] = []
        # SHA → branch 候補集合（重複コミットでもローカル/リモート両方を保持）
        seen: dict[str, int] = {}
        for raw in out.split(rec):
            raw = raw.strip("\n")
            if not raw:
                continue
            parts = raw.split(sep)
            if len(parts) < 8:
                continue
            sha, short, iso, author_name, author_email, source_ref, parents_str, subject = parts[:8]
            branch = Handler._normalize_ref(source_ref)
            parents = parents_str.split() if parents_str else []
            is_merge = len(parents) >= 2
            merged_from = ""
            merged_into = ""
            if is_merge:
                merged_from, merged_into = Handler._parse_merge_subject(subject)
                # サブジェクトから抽出できなければ 2nd parent から逆引き
                if not merged_from and len(parents) >= 2:
                    merged_from = Handler._git_name_rev(repo_path, parents[1])
                # マージ先（current branch）はサブジェクト or branch から
                if not merged_into:
                    merged_into = branch
            if sha in seen:
                # 既出のコミットなら、ローカルブランチの方を優先して上書き
                idx = seen[sha]
                existing = commits[idx]["branch"]
                if Handler._branch_priority(branch) < Handler._branch_priority(existing):
                    commits[idx]["branch"] = branch
                continue
            seen[sha] = len(commits)
            commits.append({
                "sha": sha, "short": short, "datetime": iso,
                "author_name": author_name, "author_email": author_email,
                "branch": branch,
                "is_merge": is_merge,
                "merged_from": merged_from,
                "merged_into": merged_into,
                "subject": subject,
            })
        commits.sort(key=lambda c: c["datetime"])
        return commits, ""

    # マージコミットのサブジェクトから「merged_from」「merged_into」を抽出
    _MERGE_BRANCH_RE = re.compile(r"^Merge branch ['\"]([^'\"]+)['\"](?:\s+of\s+\S+)?(?:\s+into\s+(\S+))?")
    _MERGE_PR_RE = re.compile(r"^Merge pull request #(\d+) from ([^\s]+)")
    _MERGE_REMOTE_RE = re.compile(r"^Merge remote-tracking branch ['\"]([^'\"]+)['\"](?:\s+into\s+(\S+))?")
    # Bitbucket形式: "Merged in <branch> (pull request #<N>)"
    _MERGE_BITBUCKET_RE = re.compile(r"^Merged in (\S+)\s*\(pull request #(\d+)\)")
    # 簡易形式: "Merged <branch> into <branch>"
    _MERGE_SIMPLE_RE = re.compile(r"^Merged?\s+(\S+)(?:\s+into\s+(\S+))?")

    @staticmethod
    def _parse_merge_subject(subject: str) -> tuple[str, str]:
        """マージコミットのサブジェクトから (merged_from, merged_into) を抽出。"""
        s = (subject or "").strip()
        m = Handler._MERGE_BITBUCKET_RE.match(s)
        if m:
            return f"PR#{m.group(2)}: {m.group(1)}", ""
        m = Handler._MERGE_PR_RE.match(s)
        if m:
            # owner/branch → branch だけ取り出す
            from_path = m.group(2)
            from_branch = from_path.split("/", 1)[1] if "/" in from_path else from_path
            return f"PR#{m.group(1)}: {from_branch}", ""
        m = Handler._MERGE_REMOTE_RE.match(s)
        if m:
            return m.group(1), (m.group(2) or "")
        m = Handler._MERGE_BRANCH_RE.match(s)
        if m:
            return m.group(1), (m.group(2) or "")
        m = Handler._MERGE_SIMPLE_RE.match(s)
        if m and m.group(1) not in ("branch", "in", "pull"):
            return m.group(1), (m.group(2) or "")
        return "", ""

    @staticmethod
    def _git_name_rev(repo_path: Path, sha: str) -> str:
        """SHA から最も近いブランチ名を逆引き（refs/heads/* 限定）。"""
        try:
            out = subprocess.check_output(
                ["git", "-C", str(repo_path), "name-rev", "--name-only",
                 "--refs=refs/heads/*", "--no-undefined", sha],
                text=True, stderr=subprocess.DEVNULL, timeout=5,
            ).strip()
            # "main~3" のような形式を素のブランチ名に
            return out.split("~", 1)[0].split("^", 1)[0]
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return ""

    @staticmethod
    def _normalize_ref(ref: str) -> str:
        """source ref を表示用ブランチ名に整形。

        例: refs/heads/main → main
            refs/remotes/origin/feature/x → origin/feature/x
            refs/tags/v1.0 → tag:v1.0
        """
        ref = (ref or "").strip()
        if not ref:
            return ""
        if ref.startswith("refs/heads/"):
            return ref[len("refs/heads/"):]
        if ref.startswith("refs/remotes/"):
            return ref[len("refs/remotes/"):]
        if ref.startswith("refs/tags/"):
            return "tag:" + ref[len("refs/tags/"):]
        return ref

    @staticmethod
    def _branch_priority(branch: str) -> int:
        """重複コミットの代表ブランチを選ぶ優先度（小さいほど優先）。"""
        if not branch:
            return 99
        if branch.startswith("tag:"):
            return 30
        if "/" in branch:  # origin/main 等のリモート参照
            return 20
        return 10  # ローカルブランチ

    def _handle_memo_get(self, date_key: str) -> None:
        if not self._validate_date(date_key):
            return
        path = MEMO_DIR / f"{date_key}.md"
        content = ""
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
            except OSError as e:
                self._json({"error": f"read failed: {e}"}, status=500)
                return
        self._json({"date": date_key, "content": content})

    def _handle_memo_post(self, date_key: str) -> None:
        if not self._validate_date(date_key):
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            self._json({"error": "empty body"}, status=400)
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            content = payload.get("content", "")
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self._json({"error": f"invalid json: {e}"}, status=400)
            return
        if not isinstance(content, str):
            self._json({"error": "content must be string"}, status=400)
            return
        try:
            MEMO_DIR.mkdir(parents=True, exist_ok=True)
            target = MEMO_DIR / f"{date_key}.md"
            if content.strip() == "":
                if target.exists():
                    target.unlink()
                self._json({"ok": True, "path": None, "deleted": True})
                return
            target.write_text(content, encoding="utf-8")
        except OSError as e:
            self._json({"error": f"write failed: {e}"}, status=500)
            return
        self._json({"ok": True, "path": str(target.relative_to(VAULT_ROOT))})

    def _handle_fetch_status(self) -> None:
        """直近のfetch結果を返す（git-fetcher.pyが書き出す state ファイルを読む）。"""
        if not GIT_FETCHER_STATE.exists():
            self._json({"available": False})
            return
        try:
            data = json.loads(GIT_FETCHER_STATE.read_text(encoding="utf-8"))
            data["available"] = True
            self._json(data)
        except (OSError, json.JSONDecodeError):
            self._json({"available": False})

    def _handle_fetch(self) -> None:
        """git-fetcher.py を呼び出して結果を返す（同期実行）。"""
        if not GIT_FETCHER_SCRIPT.exists():
            self._json({"error": f"git-fetcher.py が見つかりません: {GIT_FETCHER_SCRIPT}"}, status=500)
            return
        try:
            proc = subprocess.run(
                ["/usr/bin/python3", str(GIT_FETCHER_SCRIPT), "--json"],
                capture_output=True, text=True, timeout=120,
            )
        except subprocess.TimeoutExpired:
            self._json({"error": "git-fetcher がタイムアウト (120s)"}, status=504)
            return
        except Exception as e:
            self._json({"error": f"git-fetcher 起動失敗: {e}"}, status=500)
            return
        try:
            payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
        except json.JSONDecodeError:
            payload = {"error": "invalid json from git-fetcher", "stdout": proc.stdout[:500]}
        self._json(payload)

    def _handle_reminders(self) -> None:
        """スナップショットファイル `_ kiwami/tools/daily-log/reminders-snapshot.json` を読む。

        macOS の TCC（プライバシー制御）の制約で、launchd-spawned daily-log-server から
        直接 reminders-cli / osascript を呼んでも Reminders DB へのアクセスが silently
        拒否される。回避策として、Terminal context（Claudian の Bash ツール経由 or 手動 cli）
        から定期的にスナップショットを書き出し、本サーバーはそれを読むだけにする。

        スナップショット書き込み元: `~/bin/daily-log/reminders-snapshot.sh`
        書き込みタイミング:
          - Claudian の `/show-reminders` 実行時（自動）
          - Claudian の `/sync-reminders` 実行時（自動）
          - ユーザーが Terminal から `~/bin/daily-log/reminders-snapshot.sh` を手動実行
          - launchd の com.user.reminders-snapshot エージェント（10分ごと、Aqua TCC を持つbashで実行）
        CLAUDE.md「⏰ 絶対ルール」読み取り権限に準拠（add/complete/delete/edit は呼ばない）。
        """
        snapshot_path = BASE / "reminders-snapshot.json"

        if not snapshot_path.exists():
            self._json({
                "available": False,
                "error": (
                    "リマインダーのスナップショットがまだありません。"
                    "Claudian で `/show-reminders` を一度実行するか、ターミナルから "
                    "`~/bin/daily-log/reminders-snapshot.sh` を実行してください。"
                ),
            })
            return

        try:
            with snapshot_path.open(encoding="utf-8") as f:
                snapshot = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            self._json({"available": False, "error": f"スナップショット読み込み失敗: {e}"}, status=500)
            return

        # スナップショットの鮮度チェック
        try:
            mtime = datetime.fromtimestamp(snapshot_path.stat().st_mtime).astimezone()
        except OSError:
            mtime = None

        # スナップショットフォーマットを期待する形に整形
        # スナップショット形式: { "fetched_at": ISO, "lists": { "<list>": [reminders...] } }
        reminders_by_list: dict[str, list[dict]] = snapshot.get("lists", {}) or {}
        for ln in reminders_by_list:
            for r in reminders_by_list[ln]:
                r.setdefault("list", ln)
                r.setdefault("isCompleted", False)

        # 期限3日以内（緊急枠）を抽出
        now = datetime.now().astimezone()
        urgent_cutoff = now + timedelta(days=3)
        urgent: list[dict] = []
        for list_name, items in reminders_by_list.items():
            for r in items:
                due_str = r.get("dueDate")
                if not due_str:
                    continue
                try:
                    due = datetime.fromisoformat(due_str.replace("Z", "+00:00"))
                    if due <= urgent_cutoff:
                        urgent.append({**r, "list": list_name})
                except (ValueError, AttributeError):
                    continue

        # 期限順ソート（期限なしは後ろ）
        def due_key(r: dict) -> tuple[int, str]:
            d = r.get("dueDate")
            return (0, d) if d else (1, "")

        for ln in reminders_by_list:
            reminders_by_list[ln].sort(key=due_key)
        urgent.sort(key=due_key)

        # 集計
        total_pending = sum(len(items) for items in reminders_by_list.values())
        overdue = sum(
            1 for items in reminders_by_list.values() for r in items
            if r.get("dueDate") and datetime.fromisoformat(
                r["dueDate"].replace("Z", "+00:00")
            ) < now
        )

        # 鮮度判定（30分以上前なら "stale" 表示）
        snapshot_fetched_at = snapshot.get("fetched_at") or (mtime.isoformat() if mtime else now.isoformat())
        stale_threshold = timedelta(minutes=30)
        is_stale = False
        if mtime is not None:
            is_stale = (now - mtime) > stale_threshold

        self._json({
            "available": True,
            "fetched_at": snapshot_fetched_at,
            "served_at": now.isoformat(),
            "stale": is_stale,
            "lists": reminders_by_list,
            "urgent": urgent,  # 期限3日以内（リスト横断）
            "summary": {
                "total_pending": total_pending,
                "overdue": overdue,
                "urgent": len(urgent),
                "list_count": len(reminders_by_list),
            },
        })

    def _handle_save_md(self, date_key: str) -> None:
        if not self._validate_date(date_key):
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            self._json({"error": "empty body"}, status=400)
            return
        try:
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            content = payload.get("content", "")
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self._json({"error": f"invalid json: {e}"}, status=400)
            return
        if not isinstance(content, str):
            self._json({"error": "content must be string"}, status=400)
            return
        try:
            REPORTS_DIR.mkdir(parents=True, exist_ok=True)
            target = REPORTS_DIR / f"{date_key}.md"
            target.write_text(content, encoding="utf-8")
        except OSError as e:
            self._json({"error": f"write failed: {e}"}, status=500)
            return
        self._json({"ok": True, "path": str(target.relative_to(VAULT_ROOT))})

    # --- helpers ---
    def _validate_date(self, date_key: str) -> bool:
        if not DATE_RE.match(date_key):
            self.send_error(400, "Invalid date format (YYYY-MM-DD)")
            return False
        return True

    def _serve_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(404, f"File not found: {path.name}")
            return
        try:
            data = path.read_bytes()
        except OSError as e:
            self.send_error(500, f"Read error: {e}")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    # 標準ログを抑制（必要なら自前で）
    def log_message(self, format, *args):  # noqa: A002
        pass


def main() -> int:
    if not INDEX_HTML.exists():
        print(
            f"[daily-log-server] WARN: {INDEX_HTML} が見つかりません。HTML未配置です。",
            file=sys.stderr,
        )
    try:
        server = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError as e:
        print(f"[daily-log-server] ERROR: ポート {PORT} が使用中です: {e}", file=sys.stderr)
        return 1

    print(f"[daily-log-server] http://{HOST}:{PORT} で起動 (PID={os.getpid()})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[daily-log-server] shutting down", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
