# Evaluation

## Files

- `formulas.tsv`: the benchmark formulas (F1–F14, F3b, and the families
  R1–R8 and N1–N8), in the syntax of `mtl2tba` and in the syntax of CASAAL
  (`~` marks a CASAAL encoding that is not equivalent: CASAAL has no hatted
  operators).  R1 is F1 with renamed propositions.
- `run_full_eval.sh`: builds the tool and runs `mtl2tba -stats` on every
  formula (Linux/WSL, requires Spot, dune, menhir): five runs per formula
  (`REPS`), limit 300 s per run (`LIMIT`), peak memory (`/usr/bin/time`),
  times of the Spot, optimization, and export stages, the verified check
  `init_free`, and one run with Spot option `-B --small` instead of `-B -D`.
  Writes `ours_runs.tsv` (every run), `ours_results.tsv` (medians, via
  `summarize_runs.py`), `spot_small.tsv`, `machine.txt`, and the automata in
  `out/`.
- `run_casaal.py`: runs CASAAL (Windows executable) on every formula; writes
  `casaal_results.tsv`.  With `--exclusive`, the formula is conjoined with
  `[](!(a /\ b))` for every pair of distinct propositions, so that CASAAL
  reads at most one proposition per position, the event semantics of
  `mtl2tba` (common semantic domain); writes `casaal_exclusive.tsv`.
- `make_tables.py`: joins the results into `results.tsv` and the LaTeX tables
  `results_table.tex` (Table 5 of the article), `scaling_table.tex`, and
  `formulas_table.tex` (supplementary material).
- `boundary_tests.tsv`, `run_boundary_tests.sh`, `check_boundaries.py`:
  implementation checks at strict and non-strict boundaries and with
  overlapping activations.  The tool translates the negation of a safety
  requirement; `check_boundaries.py` simulates the exported automaton on
  finite timed words, with clocks starting at 0 as in UPPAAL, and checks that
  the accepting sink (violation) is reached exactly when expected.  These
  checks validate the implementation; they do not replace the proof.
- `init_comparison.tsv`: measures with and without the option `-init`.
- `check_initial_values.py`: the same condition as the verified check
  `init_free`, on the dot files (kept for reference).
- `setup_wsl.sh`: one-time installation of Spot, OCaml, dune, and menhir in
  WSL Ubuntu.

## Steps

1. Windows PowerShell as administrator: `wsl --install -d Ubuntu`, reboot,
   open Ubuntu once and create the Linux user.
2. In Ubuntu, from this folder: `sudo bash setup_wsl.sh`
3. In Ubuntu: `bash run_full_eval.sh` (about one hour, most of it in the
   instances that reach the limit), then `bash run_boundary_tests.sh`
4. On Windows: `python run_casaal.py <casaal folder>` and
   `python run_casaal.py --exclusive <casaal folder>`
5. `python make_tables.py`

The machine and the versions used for the article are in `machine.txt`.
