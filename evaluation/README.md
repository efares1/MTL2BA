# Evaluation

- `formulas.tsv`: the 23 benchmark formulas, in the syntax of `mtl2tba` and
  in the syntax of CASAAL (`~` marks a CASAAL encoding that is not
  equivalent: CASAAL has no hatted operators).
- `run_tool_eval.sh`: runs `mtl2tba -stats` on every formula (Linux/WSL,
  requires Spot, dune, menhir); writes `ours_results.tsv` and the automata
  in `out/`.
- `run_casaal.py`: runs CASAAL (Windows executable) on every formula; writes
  `casaal_results.tsv`.
- `make_tables.py`: joins both into `results.tsv` and the LaTeX table
  `results_table.tex`.
- `results.md`: summary of the observations.
- `setup_wsl.sh`: one-time installation of Spot, OCaml, dune, and menhir in
  WSL Ubuntu.

## Steps

1. Windows PowerShell as administrator: `wsl --install -d Ubuntu`, reboot,
   open Ubuntu once and create the Linux user.
2. In Ubuntu, from this folder: `sudo bash setup_wsl.sh`
3. In Ubuntu: `bash run_tool_eval.sh`
4. On Windows: `python run_casaal.py <casaal folder>`
5. `python make_tables.py`

## Time origin and `-init`

The results of `ours_results.tsv` are obtained without the option `-init`.
`init_comparison.tsv` gives the measures of every formula with and without
`-init`.  `check_initial_values.py` checks, on the automata of `out/`, that
the initial location has no invariant and that no clock is read before it has
been reset, so that acceptance does not depend on the initial clock values:

    python check_initial_values.py out

It reports F8, whose only clock is a restart clock tested by a lower bound
before its first reset (a larger initial value only helps such a test).
