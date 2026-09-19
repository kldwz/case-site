#!/bin/bash
cd /Users/hxw/codebuddy/case-site
LOG=pipeline/_regenrich_retry_log.txt
echo "RETRY START $(date) count=$(wc -l < pipeline/_regenrich_retry.txt)" > "$LOG"
n=0; ok=0; fail=0
while read s; do
  n=$((n+1))
  out=$(python3 pipeline/enrich_cases.py --slug "$s" --force 2>&1)
  if echo "$out" | grep -q "FAIL=0"; then ok=$((ok+1)); else fail=$((fail+1)); fi
  echo "$n $s ${out//$'\n'/ }" >> "$LOG"
done < pipeline/_regenrich_retry.txt
echo "RETRY DONE $(date) total=$n ok=$ok fail=$fail" >> "$LOG"
