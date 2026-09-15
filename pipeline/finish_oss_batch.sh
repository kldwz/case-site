#!/bin/bash
# finish_oss_batch.sh - 回填 GitHub 精确数据 → 追加 tsv → 构建 → 提交推送
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
LOG="$ROOT/logs/oss_finish_$(date +%Y-%m-%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1
echo "[$(date)] 开始：回填 GitHub 数据（等待限流解除）"
"$PY" pipeline/patch_gh_stats.py
echo "[$(date)] 构建站点"
ASTRO_BASE=/case-site/ npx astro build
echo "[$(date)] 提交并推送"
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "开源变现线 +7 案例：Supabase/PostHog/Cal.com/Dub/Appwrite/Twenty/Plane" 
    PROXY="http://127.0.0.1:1082"
    git -c http.proxy="$PROXY" -c https.proxy="$PROXY" push \
        || git -c http.proxy= push \
        || { echo "[$(date)] !! push 失败"; exit 1; }
    echo "[$(date)] 已推送"
else
    echo "[$(date)] 无变更"
fi
echo "[$(date)] 完成"
