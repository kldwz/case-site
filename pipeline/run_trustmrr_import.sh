#!/usr/bin/env bash
# TrustMRR import driver: fetch all .md -> generate cases -> append tsv
# -> astro build -> commit -> push (via proxy 1082, retried).
# All steps resumable. Run in background.
set -u
mkdir -p pipeline/logs
cd "$(dirname "$0")/.."   # -> case-site root

echo "[$(date)] === fetch (pass 1) ==="
python3 pipeline/fetch_trustmrr.py --workers 5
echo "[$(date)] === fetch (mop-up pass) ==="
python3 pipeline/fetch_trustmrr.py --workers 5

echo "[$(date)] === generate ==="
python3 pipeline/gen_trustmrr.py --all --workers 6

echo "[$(date)] === append tsv ==="
python3 pipeline/append_trustmrr_tsv.py

echo "[$(date)] === build ==="
ASTRO_BASE=/case-site/ npx astro build
echo "[$(date)] build exit=$?"

echo "[$(date)] === commit ==="
git add -A
git commit -m "TrustMRR 导入：收入案例（Stripe/Polar/RevenueCat 等验证营收）" || echo "nothing to commit"

echo "[$(date)] === push (retry) ==="
for i in 1 2 3 4 5; do
  echo "push attempt $i"
  if git -c http.proxy=http://127.0.0.1:1082 -c https.proxy=http://127.0.0.1:1082 push origin main 2>&1; then
    echo "PUSH_OK via proxy"; break
  fi
  if git push origin main 2>&1; then
    echo "PUSH_OK direct"; break
  fi
  sleep 15
done

echo "[$(date)] === DONE. cases: $(ls src/content/cases/*.md | wc -l) ==="
