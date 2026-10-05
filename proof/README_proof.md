# MTL(0,inf) to timed Büchi automata: Coq development

Mechanized correctness of the translation of MTL(0,inf), with hatted
operators, into timed Büchi automata, of the relaxation and reset completion
of the Büchi automaton returned by the LTL-to-Büchi translator, and of the
post-processing toward UPPAAL; extraction of the code of the tool `mtl2tba`.

| File | Content |
|---|---|
| `MTL_to_TBA_Shared_Clock_Derived_Strict_Direct_Core.v` | syntax, semantics, clocked-LTL translation, Büchi and timed automata, relaxation, reset completion, LTL-to-Büchi axiom |
| `EncodingCorrect_Shared_Clock_Derived_Strict_Direct_Proof.v` | correctness of the encoding, end-to-end theorems `MTL_to_TBA_correct` and `MTL_to_TBA_correct_with` |
| `MTL_to_TBA_Invariants.v` | location invariants, invariant synthesis, backward propagation, tightening of guards |
| `MTL_to_TBA_Optimizations.v` | forward propagation, simplification, dead resets, merging of clocks, transitions, and states, normalization, iterated pipeline |
| `MTL_to_TBA_Export.v` | transition merging, elimination of disjunctive invariants and guards, `MTL_to_exported_correct` |
| `MTL_to_TBA_Initialization.v` | conventional clock initialization (clocks at 0 at time 0, as in UPPAAL): verified check `init_free` and theorem `MTL_to_exported_correct0_with` |
| `MTL_to_TBA_Simplify.v` | proved simplification `ltl_simp` of the clocked-LTL formula (trivial operands `true`/`false`) before the LTL-to-Büchi step, and the corresponding end-to-end theorems |
| `MTL_to_TBA_Symbolic.v` | symbolic automaton: merging of the transitions with the same source, target, and resets, with Boolean labels (sets of events and clock constraints); `MTL_to_symbolic_correct_with` and `MTL_to_symbolic_correct0_with` |
| `MTL_to_TBA_Negation.v` | negation normal form: `neg` and `neg_correct` (`msat w i (neg f) <-> ~ msat w i f`), `neg_well_formed`; the tool computes every negation of its input with the extracted `neg` |
| `MTL_to_TBA_Weak.v` | weak until in the clauses of upper-bounded hatted Until: `weak`, `weak_correct` (equivalence on clock-consistent extensions), and the end-to-end theorems `MTL_to_exported_correct_weak_with` and `MTL_to_exported_correct0_weak_with` (option `-weak` of the tool) |
| `MTL_to_TBA_Recur.v` | lower bounds under always-eventually and eventually-always: `recur` (rewrites `[]<>[>=d] p` into `[]<> p` and `<>[][>=d] p` into `<>[] p`, also with `>`), `recur_correct` (equivalence under time divergence), and the end-to-end theorems `MTL_to_exported_correct_recur_weak_with` (existential acceptance) and `MTL_to_exported_correct0_recur_weak_with` (clocks starting at 0, when `init_free` holds) of the default chain of the tool |
| `Extract_Optim.v` | extraction to `../tool/src/optim.ml` |
| `tools/prune_extraction.py` | removes the unused code of the real-number library from the extracted file |

## Build

    make          # compiles the Coq files (Rocq 9) and extracts ../tool/src/optim.ml
    make tool     # builds the tool ../tool/_build/default/src/mtl2tba.exe
    make zip      # builds mtl2tba.zip

The only project axiom is `LTL_TO_BUCHI_CORRECT`, the correctness of the
LTL-to-Büchi translator; `MTL_to_TBA_correct_with` takes it as a hypothesis
and uses no project axiom.  `Print Assumptions` at the end of the proof,
optimization, and export files lists the axioms of the standard library of
real numbers.
