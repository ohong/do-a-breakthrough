# Audit of the cycle-termination proof

This note is secondary to the direct five-node counterexample. The answer to
Open Problem 2 does not require Theorem 4.3 to be false.

## Smaller cycle witness

Take the four-cycle in cyclic order `0-2-1-3-0`, sources `{0,1,2}`, and transit
time two on edge `0-2`. All other edges have transit time one.

Its full state in round 4 is

```text
deliveries = {1->3, 3->1}
in transit = empty.
```

The same full state recurs in round 9. This gives a period-five orbit on an
edge-weighted cycle, contrary to Theorem 4.3 of the primary paper.

## Apparent proof defect

The proof expands a weighted cycle by placing tick nodes on delayed edges. It
defines a relation on sources:

```text
v ~ w iff there exists m such that v+m = w-m
        and the meeting point v+m is an original graph node.
```

The paper calls this relation transitive. From witnesses

```text
v+m' = w-m'
w+m'' = z-m'',
```

it adds offsets to obtain

```text
v+(m'+m'') = z-(m'+m'').
```

That equality is valid modulo the expanded cycle length, but it does not show
that the new meeting point is an original graph node rather than an internal
tick. The latter condition is part of the definition of `~`.

For the four-cycle witness, the expanded cycle has positions

```text
0, tick, 2, 1, 3
```

modulo five. Original-node positions are `{0,2,3,4}`, and source positions are
`{0,2,3}`. Direct calculation gives `0 ~ 3` and `3 ~ 2`, but not `0 ~ 2`,
because the unique midpoint of 0 and 2 is the tick at position 1. Hence `~` is
not transitive on this instance.

The subsequent equivalence-class counting argument, beginning with equation
(20), therefore does not apply.

## Claim strength

The state table and the failed-transitivity calculation have been independently
reproduced twice. This is still a proposed correction to a peer-reviewed
theorem and needs review by the authors or another expert before public claims.

