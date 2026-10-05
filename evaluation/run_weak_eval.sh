#!/bin/bash
# Primed configurations: the tool runs with the option -weak, which replaces
# the Until of the clauses of upper-bounded hatted Until by a weak until in
# the formula given to Spot (proved: MTL_to_exported_correct_weak_with).
# Run in WSL after run_full_eval.sh (which builds the tool):
#     bash run_weak_eval.sh        # 5 runs per formula, limit 300 s
# Writes weak_runs.tsv, weak_results.tsv (medians), and the automata in out_weak/.
HERE="$(cd "$(dirname "$0")" && pwd)"
EXE=~/mtl2tba_eval/_build/default/src/mtl2tba.exe
REPS=${REPS:-5}
LIMIT=${LIMIT:-300}
mkdir -p "$HERE/out_weak"
HDR=$("$EXE" -stats-header)
printf 'id\trun\tstatus\tmem_kb\t%s\n' "$HDR" > "$HERE/weak_runs.tsv"
grep -v '^#' "$HERE/formulas.tsv" | while IFS=$'\t' read -r id desc ours cas; do
  [ -z "$id" ] && continue
  # only the configurations where the option changes the formula given to Spot
  u=$(cd /tmp && timeout 60 "$EXE" -v -nopdf -spot false -o probe "$ours" 2>&1 | sed -n 's/^clocked LTL: //p')
  v=$(cd /tmp && timeout 60 "$EXE" -v -nopdf -weak -spot false -o probe "$ours" 2>&1 | sed -n 's/^clocked LTL: //p')
  if [ "$u" = "$v" ]; then echo "$id: unchanged"; continue; fi
  for r in $(seq 1 "$REPS"); do
    line=$(cd "$HERE/out_weak" && /usr/bin/time -f '%M' -o /tmp/mem.txt \
             timeout "$LIMIT" "$EXE" -stats -nopdf -weak -o "$id" "$ours" 2>/dev/null)
    code=$?
    mem=$(tail -1 /tmp/mem.txt)
    if [ $code -eq 0 ]; then st=ok; elif [ $code -eq 124 ]; then st=timeout; else st=error; fi
    printf "%s'\t%s\t%s\t%s\t%s\n" "$id" "$r" "$st" "$mem" "$line" >> "$HERE/weak_runs.tsv"
    echo "$id' run $r: $st"
    [ "$st" = ok ] || break
  done
done
python3 "$HERE/summarize_runs.py" weak_runs.tsv weak_results.tsv
