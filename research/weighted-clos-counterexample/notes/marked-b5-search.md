# Route B5 marked \(3/5,2/5\) search

Date: 2026-07-23

Status: **exhaustive \(2\times2\) control completed; no counterexample**

## Exact finite contract

An endpoint cell contains separate heavy and light multiplicities. Heavy edges
have weight \(3/5\), light edges have weight \(2/5\). The retained domain
enforces:

1. B.1 at every vertex: \(h(v)\le3\) and
   \(\ell(v)\le6-h(v)\);
2. connectedness and no isolated vertices;
3. some vertex has degree six;
4. B.5:
   \(\Delta(G[M])+\Delta(G-M)\ge7\);
5. if \(G\) is 6-regular, the heavy degree is nonconstant.

A five-colouring is SAT exactly when every vertex-colour receives at most two
edges and at most one of those edges is heavy. `SAT_5_COLOURING`,
`UNSAT_5_COLOURING`, and `UNKNOWN` refer to this exact CSP.

## Reproducible exhaustive run

Artifact:
`code/search_marked_b5.py`

Command:

```sh
python3 \
  research/weighted-clos-counterexample/code/search_marked_b5.py \
  --total-seconds 220 \
  --output /tmp/weighted-clos-marked-b5-2x2.json
```

The script enumerates the 22 possible `(heavy, light)` cell values satisfying
the per-cell consequence of B.1, hence scans all
\(22^4=234{,}256\) labelled \(2\times2\) multiplicity arrays before applying
the filters.

| Edges | Retained labelled | Symmetry-reduced | SAT five-colouring |
|---:|---:|---:|---:|
| 7 | 136 | 17 | 136 |
| 8 | 476 | 61 | 476 |
| 9 | 892 | 116 | 892 |
| 10 | 1,020 | 139 | 1,020 |
| 11 | 748 | 115 | 748 |
| 12 | 240 | 50 | 240 |
| **Total** | **3,512** | **498** | **3,512** |

The symmetry quotient uses independent row and column swaps and swapping the
two bipartitions. It is reporting-only: all 3,512 labelled retained instances
were separately coloured.

For each instance the program:

- expands parallel heavy and light edges as distinct edge IDs;
- constructs and verifies explicit local three-bin certificates;
- obtains a five-colouring by restricted-growth exact backtracking;
- independently checks the returned colouring against B.3.

The run visited 37,608 backtracking nodes in total, at most 13 for one
instance, and completed in 0.282 seconds. A deterministic rerun completed in
0.582 seconds with the same coverage digest:

```text
8e5c70a95e6f031636cacdf896fd7a92c4a0e2f1f5149251ec323730082a97d4
```

There were 3,512 `SAT_5_COLOURING`, zero `UNSAT_5_COLOURING`, and zero
`UNKNOWN`. No witness was emitted.

## Why the broader sampled run was stopped

A concurrent theory route identified a general construction that appears to
colour the entire marked B family: edge-colour the heavy bipartite subgraph
with at most three matchings; edge-colour the light subgraph with at most six
matchings; merge two light matching colours; then place the heavy matching
colours into three of the four unmerged light colours. An unmerged colour has
at most a heavy-light pair at a vertex, while the merged light colour has at
most two lights. Both loads are at most one.

That argument is recorded here as the reason not to spend the bounded budget
on \(2\times3\) or \(3\times3\) sampling. It should be independently audited
and written as a theorem before Route B is marked proved. The exhaustive
\(2\times2\) computation is corroboration, not evidence needed by that proof.

No claim is made beyond the exact \(2\times2\) frontier.
