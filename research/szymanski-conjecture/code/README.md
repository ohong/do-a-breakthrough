# Exact routing checker

This directory contains a dependency-free (apart from the installed Z3 Python
module) exact feasibility checker for directed arc-disjoint permutation routing
in the bidirected hypercube.

Vertices are JSON integers `0..2^d-1`; bit `i` is coordinate `i`. An instance is:

```json
{"dimension": 3, "permutation": [7, 6, 5, 4, 3, 2, 1, 0]}
```

Run an unrestricted check:

```sh
python3 check.py instance.json --timeout-seconds 20 --output result.json
```

Add `--shortest-only` only for the calibration variant. Add
`--smt2 model.smt2` to retain the precise formula. Exit status 2 means Z3
returned `unknown`; SAT and UNSAT both use exit status 0 because both are valid
decision outcomes.

Reproduce the documented experiments from this directory:

```sh
python3 -m unittest -v test_routing.py
python3 run_experiments.py \
  --output-dir ../results/2026-07-23-exact-routing \
  --timeout-seconds 20
python3 metric_search.py \
  --dimension 5 --samples 2000 --seed 1989 \
  --output ../results/2026-07-23-exact-routing/metric-search.json
```

`routing.py` explains the binary-flow equivalence and independently validates
every extracted witness. `run_experiments.py` stops immediately and retains
SMT-LIB if an unrestricted UNSAT result appears. Such a result would still be
unaudited until checked with a genuinely independent encoding.
