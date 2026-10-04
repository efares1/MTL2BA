#!/bin/bash
# Primed configurations (experiment): the Until of the clauses of
# upper-bounded hatted Until is replaced by a weak until before Spot
# (spot_weak.py, given to mtl2tba through -spot); the tool is unchanged.
# Run in WSL after run_full_eval.sh (which builds the tool):
#     bash run_weak_eval.sh        # 5 runs per formula, limit 300 s
# Writes weak_runs.tsv, weak_results.tsv (medians), and the automata in out_weak/.
HERE="$(cd "$(dirname "$0")" && pwd)"
EXE=~/mtl2tba_eval/_build/default/src/mtl2tba.exe
REPS=${REPS:-5}
LIMIT=${LIMIT:-300}
W="$HERE/spot_weak.py"
chmod +x "$W"
mkdir -p "$HERE/out_weak"
HDR=$("$EXE" -stats-header)
printf 'id\trun\tstatus\tmem_kb\t%s\n' "$HDR" > "$HERE/weak_runs.tsv"
: > /tmp/weak.log
grep -v '^#' "$HERE/formulas.tsv" | while IFS=$'\t' read -r id desc ours cas; do
  [ -z "$id" ] && continue
  # only the configurations where the rewriting changes the formula
  rm -f /tmp/weak.log
  (cd /tmp && SPOT_WEAK_LOG=/tmp/weak.log timeout 60 "$EXE" -stats -nopdf -spot "$W" -o probe "$ours" > /dev/null 2>&1)
  n=$(awk '{print $4}' /tmp/weak.log 2>/dev/null | head -1)
  if [ -z "$n" ] || [ "$n" = "0" ]; then
    # the probe may time out on large instances: inspect the formula directly
    case $id in R*) ;; *) echo "$id: unchanged"; continue;; esac
  fi
  for r in $(seq 1 "$REPS"); do
    line=$(cd "$HERE/out_weak" && /usr/bin/time -f '%M' -o /tmp/mem.txt \
             timeout "$LIMIT" "$EXE" -stats -nopdf -spot "$W" -o "$id" "$ours" 2>/dev/null)
    code=$?
    mem=$(tail -1 /tmp/mem.txt)
    if [ $code -eq 0 ]; then st=ok; elif [ $code -eq 124 ]; then st=timeout; else st=error; fi
    printf "%s'\t%s\t%s\t%s\t%s\n" "$id" "$r" "$st" "$mem" "$line" >> "$HERE/weak_runs.tsv"
    echo "$id' run $r: $st"
    [ "$st" = ok ] || break
  done
done
python3 "$HERE/summarize_runs.py" weak_runs.tsv weak_results.tsv
