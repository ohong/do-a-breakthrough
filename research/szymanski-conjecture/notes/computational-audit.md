# Hostile computational audit

Date: 2026-07-23

## Verdict

The unrestricted Boolean multicommodity-flow formula in `code/routing.py` is
**exactly equivalent** to the contract's directed arc-disjoint routing problem,
under the contract's explicit convention that a fixed point uses a zero-arc
path. I found no soundness or completeness defect in the encoding, and no
stored SAT witness fails independent validation.

The recorded `unknown` for `q5-high-distance-random-a` is not an infeasibility
result. It has now been superseded, for that single candidate only, by a
separate constructive shortest-path packing certificate:
`results/2026-07-23-exact-routing/audit-q5-high-distance-random-a-shortest-path-search-240s.json`.
That certificate routes all 32 demands using 136 distinct directed arcs, equal
to the total Hamming-distance lower bound. It therefore proves this candidate
SAT for unrestricted routing as well. It does not prove anything about the
remaining `32!` permutations.

Accordingly, all 84 structured batch candidates are now known routable: the
original batch files establish 83 SAT candidates, and the independent path
certificate establishes the one candidate for which the original 20-second run
was `unknown`. The original saved batch summary must remain reported as 83 SAT
and 1 unknown, because it faithfully records that original time-limited run.

## Encoding audit

For an active commodity `s -> t`, every selected arc is Boolean. The model
imposes `out - in = 1` at `s`, `-1` at `t`, and `0` elsewhere, while each
commodity has at most one selected incoming and one selected outgoing arc at
each vertex.

This forces `(out,in)=(1,0)` at `s`, `(0,1)` at `t`, and either `(0,0)` or
`(1,1)` at any other vertex. Its support is consequently one directed
`s`-to-`t` component plus zero or more directed cycles. The target is
reachable from the source: otherwise summing balance over the source-reachable
set gives net outflow one although, by definition, no selected arc leaves that
set. Deleting cycles and all unused support leaves an arc-disjoint simple
`s`-to-`t` path. The per-directed-arc cardinality constraint preserves global
capacity after this deletion.

Specific hostile checks:

- **Fixed points:** excluded from variables and represented as `[s]`; they use
  no directed arcs, matching the stated zero-length convention.
- **Flow cycles and branching:** separate cycles are harmless and removable.
  Branching and merging are excluded by the per-commodity degree caps.
- **Endpoints:** the balance equation plus the caps forces exactly the required
  source and target degrees, rather than merely allowing a net imbalance.
- **Arc orientation:** `(u,v)` and `(v,u)` are separately enumerated and have
  separate capacity constraints. This matches a bidirected cube, not an
  undirected edge-capacity model.
- **Extraction:** the implementation's reachability search yields a simple
  path; removing other selected arcs cannot create a cross-commodity collision.
  Its post-extraction validator checks endpoints, cube adjacency, simplicity,
  optional shortestness, and global directed-arc uniqueness.

The `--shortest-only` restriction is correctly implemented as strictly
distance-decreasing arcs. It is a sound calibration subproblem, not an
encoding of unrestricted routing.

## Independent certificate verification

I added `code/independent_verify.py`. Its certificate mode imports neither
`routing.py` nor Z3: it parses JSON with the standard library, reconstructs cube
adjacency, checks the permutation and redundant distance/capacity metadata,
checks every endpoint and fixed point, checks simplicity and (where declared)
shortestness, and rejects every repeated directed arc.

Command, from `research/szymanski-conjecture/code/`:

```sh
python3 independent_verify.py certificates ../results/2026-07-23-exact-routing \
  --output ../results/2026-07-23-exact-routing/audit-certificate-verification.json
```

Result: all 83 SAT `*.result.json` certificates passed, and the same 83 SAT
records embedded in `summary.json` also passed. Of 85 stored result files, the
other two are exactly the 20-second and 120-second records for the same Q5
permutation, both `unknown` with `reason_unknown: "timeout"`; neither carries a
path certificate. The machine used Python 3.14.6 and Z3 Python package 4.15.4.

## Independent Q5 attempt

The initially attempted alternate decision encoding used QF_FD Boolean degree
constraints, coordinate-major arc creation, demand-descending commodity order,
and no arithmetic flow sums. It is an equivalent formulation: sources have
out-degree one/in-degree zero, targets the reverse, and other vertices have
equal Boolean in/out degree, all with degree at most one. On the Q5 instance,
the first eager `qffd` tactic attempt terminated on this host before emitting a
result. A later direct `SolverFor("QF_FD")` run completed its 240-second limit
as `unknown` with `reason_unknown: "timeout"`, stored at
`results/2026-07-23-exact-routing/audit-q5-high-distance-random-a-qffd-240s.json`.
Neither event is evidence of infeasibility. The retained script uses the direct
QF_FD engine for small reproducible checks.

I then used a genuinely different whole-path formulation: enumerate every
shortest coordinate-order path for each demand, dynamically select the demand
with the fewest currently arc-disjoint path options, choose a low-frequency
arc option, and restart if stuck. It is a bounded constructive search, so a
failure would be inconclusive, while a returned path family is a proof of SAT.

Command, from `research/szymanski-conjecture/code/`:

```sh
python3 independent_verify.py path-search \
  ../results/2026-07-23-exact-routing/q5-high-distance-random-a.instance.json \
  --timeout-seconds 240 --seed 1989 \
  --output ../results/2026-07-23-exact-routing/audit-q5-high-distance-random-a-shortest-path-search-240s.json
```

It found a SAT certificate in trial 1 after 0.030414 seconds. Independent
certificate checking reports 32 sources and 136 used directed arcs. The path
length distribution is seven paths of length 2, one of length 3, one of length
4, and 23 of length 5. Their total is 136, exactly the independently computed
Hamming-distance lower bound, so every path is shortest. This also verifies
the JSON certificate without invoking the original solver.

Focused regression command:

```sh
python3 -m unittest -v test_routing.py
```

All 8 tests passed in 0.20 seconds.

## Defects and result changes

No encoding, extraction, capacity, endpoint, or saved-SAT-certificate defect
was found. The material correction is evidentiary: the notes call the seeded
Q5 mutation A unresolved because its original Z3 runs timed out. The original
timeout records remain honestly `unknown`, but the new independent path
certificate proves that instance routable. The overall conjecture remains
unresolved, and the bounded experiment still supplies neither an unrestricted
UNSAT certificate nor exhaustive coverage of Q5.
