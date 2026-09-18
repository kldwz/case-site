#!/usr/bin/env bash
cd /Users/hxw/codebuddy/case-site
BEFORE=$(ls src/content/cases/*.md | wc -l | tr -d ' ')
echo "[$(date)] START cases=$BEFORE"
echo "[$(date)] === import 100 ==="
python3 pipeline/_import_more.py 100
echo "[$(date)] import step done (exit=$?)"
echo "[$(date)] === append tsv ==="
python3 pipeline/append_trustmrr_tsv.py
echo "[$(date)] === build ==="
ASTRO_BASE=/case-site/ npx astro build
echo "[$(date)] build exit=$?"
echo "[$(date)] === git add ==="
git add src/content/cases cases.tsv public/cases pipeline/trustmrr_slugs.txt
echo "[$(date)] === git commit ==="
git commit -m "TrustMRR 补充导入：新增副业/独立产品案例（Stripe/Polar/RevenueCat 等验证营收）" || echo "nothing to commit"
echo "[$(date)] === git push (proxy retry) ==="
for i in 1 2 3 4 5 6; do
  if git -c http.proxy=http://127.0.0.1:1082 -c https.proxy=http://127.0.0.1:1082 push origin main 2>&1; then echo "PUSH_OK via proxy"; break; fi
  if git push origin main 2>&1; then echo "PUSH_OK direct"; break; fi
  echo "push attempt $i failed, wait 15s"; sleep 15
done
AFTER=$(ls src/content/cases/*.md | wc -l | tr -d ' ')
echo "[$(date)] DONE before=$BEFORE after=$AFTER added=$((AFTER-BEFORE))"
