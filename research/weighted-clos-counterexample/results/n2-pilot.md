# Retired n=2 pilot

Date: 2026-07-23

## Why this route was retired

The project initially treated \(n=2\) as the first open finite frontier. A
second primary-source pass found the missed result of Ngo and Vu (2003):
\(m(2,r)=3\). This is exactly the three-colour bound predicted by
Chung--Ross at \(n=2\). The active open frontier was therefore corrected to
\(n=3\).

Primary source:
https://doi.org/10.1137/S0097539702408235

## Exact pilot results

These results are retained as tool controls, not evidence about the open
\(n=3\) case.

### Continuous rational CEGAR

The exact solver exhausted every connected canonical \(3\times3\) bipartite
multigraph topology with 8 or 9 edges and edge multiplicity at most 4:

- 486 topologies;
- 486 `UNSAT_TOPOLOGY`;
- no timeout or `UNKNOWN`;
- no witness;
- 95.353261 seconds with the mixed-weight restriction disabled.

Command:

```text
python3 code/search_cegar.py --mode survey \
  --left-min 3 --left-max 3 --right-min 3 --right-max 3 \
  --edge-min 8 --edge-max 9 --max-multiplicity 4 \
  --max-topologies 600 --topology-seconds 8 --total-seconds 240 \
  --solver-timeout-ms 8000 --max-iterations 20000 \
  --progress-every 1000 --no-enforce-mixed-weights \
  --output /tmp/weighted-clos-3x3-e8-e9-unrestricted.json
```

The initial default run also exhausted the same 486 topologies, but only in the
mixed heavy/light slice. It took 104.662447 seconds. That run must not be
described as unrestricted.

### Independent bounded-denominator enumeration

The discrete engine exhausted all 12 canonical connected \(2\times3\),
six-edge multigraph topologies of multiplicity at most 2 over

\[
\{2/3,1/3,1/2,3/4,1/4,3/5\}.
\]

It examined 99,838 symmetry-reduced assignments. Of these, 94,850 had exact
local bin number two, and all were three-colourable.

Partial broader runs checked another 100,000 assignments on the same topology
family and 214,967 assignments across \(3\times3\), seven-edge topologies. No
counterexample or unknown result occurred.

## Interpretation

The finite negative results are consistent with the known theorem. They do not
constitute a proof of that theorem because the topology and weight spaces were
bounded, and the Z3 `unsat` responses were not retained as independently
checkable proof objects.
