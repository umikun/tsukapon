#!/bin/bash
# スキル・機能ファイルが変更されたら、Claudian-スキル一覧.md の更新をClaudeに促すhook
# PostToolUse (Write|Edit) から呼ばれる想定

input=$(cat)
path=$(echo "$input" | python3 -c 'import sys,json
try:
    d = json.load(sys.stdin)
    print(d.get("tool_input", {}).get("file_path", ""))
except Exception:
    print("")
')

# 対象ファイルのパターン
# - .claude/commands/*.md (カスタムスキル)
# - LaunchAgents/*.plist (launchd自動化)
# - ~/bin/*.sh (シェル自動化)
# - .mcp.json (MCPサーバー設定)
case "$path" in
    *".claude/commands/"*.md | \
    *"LaunchAgents/"*.plist | \
    */bin/*.sh | \
    *".mcp.json")
        cat <<EOF
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"⚠️ CLAUDE.md ルール発動: スキル・自動化ファイルが変更されました ($path)。タスク完了前に Claudian-スキル一覧.md を必ず更新し、完了報告に『📋 スキル一覧を更新しました』を含めてください。"}}
EOF
        ;;
esac

exit 0
