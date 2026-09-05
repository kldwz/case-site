#!/bin/bash
# run_daily.sh - 每日案例流水线：抓取 → 写文章 → 截图 → 构建 → 推送部署
# 用法：bash run_daily.sh   （launchd 每日定时调用）
# 日志：logs/daily_YYYY-MM-DD.log
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
DATE="$(date +%Y-%m-%d)"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/daily_$DATE.log"
FAILURE_SUMMARY="$ROOT/pipeline/failures/$DATE.md"

log() { echo "[$(date '+%H:%M:%S')] $*" >> "$LOG"; }

log "===== 每日流水线开始 $DATE ====="

# 1. 拉取候选（跳过已有去重，不 fresh）
log "步骤1: fetch 拉候选"
"$PY" pipeline/fetch.py >> "$LOG" 2>&1 || { log "!! fetch 失败"; exit 1; }

# 2. 写文章 + 截图 + 汇总表（重试兜底内建，失败记入 failures/）
log "步骤2: write_cases 生成文章/截图/汇总"
if [ -f "$ROOT/inbox/$DATE.json" ]; then
    "$PY" pipeline/write_cases.py --append >> "$LOG" 2>&1 || { log "!! write_cases 失败"; exit 1; }
else
    log "  跳过：无 inbox/$DATE.json（可能无新候选）"
fi

# 3. 构建静态站
log "步骤3: astro build"
npx astro build >> "$LOG" 2>&1 || { log "!! build 失败"; exit 1; }

# 4. 提交并推送（触发 GitHub Actions 部署）
log "步骤4: git commit + push"
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "daily: $DATE 案例更新" >> "$LOG" 2>&1 || { log "!! commit 失败"; exit 1; }
    # 清除代理变量：本机代理对 git CONNECT 隧道不稳定（503），直连更可靠
    env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
        git push >> "$LOG" 2>&1 || { log "!! push 失败"; exit 1; }
    log "  已推送"
else
    log "  无变更，跳过提交"
fi

# 5. 失败汇总提示
if [ -f "$FAILURE_SUMMARY" ]; then
    log "!! 有 $DATE 失败案例待人工补写：$FAILURE_SUMMARY"
fi

log "===== 每日流水线完成 $DATE ====="
echo "完成，日志：$LOG"
