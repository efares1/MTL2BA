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
- `run_casaal.py`: runs CASAAL (Windows executable) on every formula (option
  `--runs=5`: median of five runs, used for the article); writes
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
- `run_weak_eval.sh`: primed configurations, translated with the option
  `-weak` of the tool, which replaces the Until of the clauses of
  upper-bounded hatted Until by a weak until (proved:
  `MTL_to_exported_correct_weak_with`); writes `weak_runs.tsv` and
  `weak_results.tsv`.  `spot_weak.py` is the earlier text-level experiment,
  kept for reference; it gives the same sizes.
- `run_spot_validation.sh`: translation validation of the Spot step, the only
  hypothesis of the end-to-end theorem.  The tool runs unchanged, with
  `-spot spot_tee.sh`, a wrapper that calls `ltl2tgba` with the arguments of
  the tool and keeps the clocked-LTL formula T(f) and the LBTT automaton; an
  independent translator, ltl2ba 1.3 (Gastin and Oddoux), translates T(f)
  after a common renaming of the atoms, and `autfilt --equivalent-to` checks
  that both automata accept the same propositional words.  The numbers of
  states and transitions read by the tool are compared with those of
  `autfilt`.  ltl2ba must be compiled with enlarged formula buffers (see the
  header of the script), since T(f) exceeds 4096 characters on N7 and N8.
  Result (`spot_validation.tsv`): equivalent on the 28 configurations other
  than R6 to R8; on R6 and R7 the equivalence check exceeds 600 s, and on R8
  Spot does not answer within 300 s.
- `run_interface_check.sh`: check of the trusted interface with Spot (option
  `-check` of the tool): Spot reads the same formula from the text given to
  `ltl2tgba` and from a second, independent prefix printer of T(f), and the
  automaton built by the reader is equivalent to the raw output of Spot
  (`autfilt --equivalent-to`).  Result (`interface_check.tsv`): both checks
  pass on the 30 configurations where Spot answers (all but R8).
- `tf_sizes.tsv`: size of the formula T(f) given to Spot (characters, atoms).
- `run_acceptance_eval.sh`: size of the automaton returned by Spot for every
  configuration, with Until or weak until in the upper-bounded clauses, and
  with state-based (`-B`, used by the tool), transition-based (`-b`), and
  transition-based generalized (`--tgba`) Büchi acceptance; writes
  `acceptance_results.tsv`.
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
