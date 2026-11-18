# Explicit periodic witness

## Instance

Let the graph be the four-cycle `a-b-c-d-a` with a leaf `e` adjacent to `a`.
The bipartition is

```text
{a,c} | {b,d,e}.
```

Sources `c` and `e` send simultaneously in round 1. Edge `ab` has transit time
two in both directions. Edges `bc`, `cd`, `da`, and `ae` have transit time one.

For round `r`, let:

- `D_r` be the set of directed messages delivered at original graph vertices
  in round `r`;
- `F_r` be the set of directed messages currently in the sole internal tick of
  `ab`, to be delivered in round `r+1`.

For transit time two, the full state is `S_r=(D_r,F_r)`.

## Certificate

| Round | `D_r`, delivered in this round | `F_r`, still in transit |
|---:|---|---|
| 1 | `c->b, c->d, e->a` | empty |
| 2 | `a->d, d->a` | `a->b, b->a` |
| 3 | `a->b, a->e, b->a, d->c` | `a->b` |
| 4 | `a->b, a->d, a->e, b->c, c->b` | empty |
| 5 | `c->d, d->c` | empty |
| 6 | `c->b, d->a` | empty |
| 7 | `a->e` | `a->b, b->a` |
| 8 | `a->b, b->a` | empty |
| 9 | `a->d, a->e, b->c` | empty |
| 10 | `c->d, d->c` | empty |

Thus

```text
S_5 = ({c->d, d->c}, empty) = S_10.
```

The update from a full state is deterministic. The nonempty five-round block
from round 5 through round 9 therefore repeats forever, proving nontermination.

## Transition audit

- Round 1: the two sources send to all neighbors.
- Round 2: `a`, having received only from `e`, sends toward `b` and `d`;
  `b`, having received only from `c`, sends toward `a`; `d`, having received
  only from `c`, sends toward `a`. The two sends on `ab` are still in transit.
- Round 3: the two in-transit messages arrive. The round-2 delivery `d->a`
  also makes `a` send another delayed message toward `b`, while `a->d` makes
  `d` send toward `c`.
- Round 4: the remaining delayed `a->b` arrives. The other sends follow
  directly from the round-3 receiver sets.
- Rounds 5-10 follow by the same rule. In round 7, sends in both directions on
  `ab` are in transit. They arrive in round 8 and pass rather than cancel.

No inference relies on message identities or multiplicities. At most one copy
of a given directed edge-message is launched in any round.
