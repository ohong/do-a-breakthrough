# Hostile theory audit

Date: 2026-07-23

Scope: `contract.md`, `notes/solver-theory.md`, and
`notes/coordinator-observations.md`. This is a correctness audit, not a
literature or novelty audit. `proved/pass` below means that the stated argument
can be made self-contained using elementary graph theory. Computation was used
only to reconstruct finite certificates, never as the proof of a general claim.

## High-impact findings

- The explicit \(Q_3\) routing and both restricted-induction obstruction
  certificates are correct. They refute the one-crossing portal and cycle-flip
  Beneš embeddings, not Szymanski's conjecture.
- The single-cycle theorem through \(k=d+1\) survives, including
  \(d=1,k=2\) and \(k=d+1\). Its general hub-fan lemma must say that the fan
  paths intersect only at the hub. The current phrase “pairwise internally
  vertex-disjoint” is too ambiguous for the proof.
- The ordered-closed-trail equivalence and the cube boundary equality
  classification survive.
- The coordinator's proposed universal Beneš claim is now false by the later
  \(Q_3\) certificate. The assertion that mere connectedness of the
  pairwise-intersection graph is false is plausible but is not accompanied by a
  cube counterexample and remains unverified as written.
- No audited artifact proves or disproves the full conjecture.

## Numbered verdict

1. **Contract/source identification: `unverified`.** The normalized
   mathematical statement is internally coherent: the quantifiers are
   \(d\geq1\), every permutation, directed paths, and directed-arc rather than
   vertex disjointness. This audit did not re-open the primary sources, so the
   claims that this is exactly the surviving sourced formulation and that the
   result is known through \(d=4\) are not independently certified here.
   **Repair:** retain the existing source audit as a separate dependency and do
   not promote this item from source-tested to proved without the cited texts.

2. **Cycle deletion for routing walks: `proved/pass`.** If a directed walk with
   distinct endpoints repeats a vertex, delete the closed segment between two
   occurrences. Iteration terminates at a simple directed path, preserves the
   endpoints, and only removes arcs. Fixed points are handled separately by
   empty paths. This justifies the contract's proposed simple-path reduction.

3. **Coordinator Lemma 1 and its saturation corollary: `proved/pass`.** For
   each coordinate, pathwise signed crossing counts sum to zero, while every
   \(0\to1\) demand contributes at least one \(0\to1\) traversal. Hence
   \(p_i=q_i=c_i+r_i\), with \(0\leq r_i\leq 2^{d-1}-c_i\). Also
   \(\sum_v\operatorname{dist}(v,\sigma(v))=2\sum_i c_i\), which gives the
   displayed total-length identity. If \(c_i=2^{d-1}\), all arcs in both
   directions of dimension \(i\) are used, and no request can recross that
   coordinate.

4. **Slack identity and the \(S=0,2\) classification: `proved/pass`.**
   With \(\rho=A\circ\sigma\),
   \(\operatorname{dist}(v,\rho(v))=
   d-\operatorname{dist}(v,\sigma(v))\) pointwise. A nonidentity permutation
   moves at least two vertices. Thus total slack two forces exactly two moved
   vertices, each at distance one, hence one adjacent transposition. No
   quantifier or parity assumption is missing.

5. **Standard antipodal routing and adjacent tail switches:
   `proved/pass`.** At step \(j\), translation of the start vertex makes the
   used arcs exactly all directed arcs of coordinate \(j\), once each. For
   \(b=a\oplus e_j\), \(B_a\) immediately after flipping \(j\) and \(B_b\)
   immediately before flipping \(j\) are at the same vertex. Swapping suffixes
   gives the required targets. In one recombined walk the two opposite
   \(j\)-arcs form an immediate two-arc closed segment. After deleting it, the
   remaining sequence flips every other coordinate at most once, so it is
   genuinely a path. Disjoint adjacent transpositions use disjoint base-path
   pairs, so simultaneous switches preserve global arc disjointness even if
   different pairs share vertices.

6. **Common-vertex tail switching: `proved/pass`, with an omitted finishing
   sentence.** Permuting suffixes of all base paths meeting a common vertex
   preserves the global multiset of used arcs and implements the corresponding
   endpoint permutation. The recombined objects may repeat vertices.
   **Exact repair:** say explicitly that they are arc-disjoint directed trails
   and invoke item 2 on each trail. Shared vertices are allowed by the contract.

7. **Prefix-chain description: `proved/pass`.** A base path \(B_v\) passes
   through \(x\) at stage \(j\) exactly when \(v=x\oplus M_j\). The \(M_j\)
   are distinct, giving precisely the stated \(d+1\) starts.

8. **“Connected pairwise-intersection graph does not suffice”:
   `unverified`.** Ordered switches do make connectedness alone suspicious, but
   the observation gives no explicit set of cube base paths, connected
   intersection graph, and unattainable endpoint permutation. A generic
   one-use switching-network warning is not yet a counterexample inside this
   specific hypercube construction. **Repair:** provide such a concrete cube
   certificate, or weaken the text to “connectedness has not been shown to
   suffice.”

9. **Directed metric inequality: `proved/pass`.** For nonnegative arc lengths,
   each commodity path costs at least its directed shortest-path distance, and
   arc disjointness bounds the total route cost by \(\sum_a\ell(a)\). Therefore
   a strict reverse inequality proves integral and even fractional
   infeasibility. A metric supported on one directed cut reduces to item 30,
   and nonnegative sums of such cut inequalities also pass by summation. The
   claim that no violating metric is currently known is a search-status
   statement and is `unverified` by this audit.

10. **Skew-product closure: `proved/pass`.** Phase one routes
    \(\alpha_y\) inside each \(Q_p\)-fiber. Bijection of every \(\alpha_y\)
    leaves exactly one commodity with each first coordinate in every
    \(y\)-fiber, so phase two copies the routing of \(\tau\) in fixed-first-
    coordinate fibers. The phases use disjoint coordinate blocks. Their
    concatenation is a path: the first phase stays at one \(y\), the second at
    its phase-one endpoint \(x'\), and a simple phase-one path reaches \(x'\)
    only at its end.

11. **Beneš sufficient induction lemma: `proved/pass`; proposed universal
    satisfiability: `false`.** Alternating colors give one commodity of each
    lane at every input and output pair. A swapped pair uses both orientations
    of its physical matching edge, so the exact conflict condition is
    \(\neg(A_z\wedge B_z)\). Each component flip complements one literal state
    at all its incident pair vertices, making every condition a 2-CNF clause.
    If the formula is satisfiable, the two lower-dimensional lane permutations
    concatenate without arc conflict. However, item 16 below refutes the
    coordinator's later claim that some coordinate always has a satisfiable
    instance. **Repair:** mark only the conditional lemma proved and retire the
    universal induction target.

12. **Portal induction criterion A1: `proved/pass`.** Distinct sources and
    targets define a partial permutation. Matching unused sources to unused
    targets extends it to a full permutation of the half; discarding filler
    paths preserves arc disjointness. Half-cube arcs and the chosen cut arcs
    lie in disjoint dimension sets.

13. **One-crossing counting rigidity A2: `proved/pass`.** In either half the
    number of nonempty subrequests is \(N+m-a-b\), so partial-permutation
    feasibility forces \(a+b\geq m\). Summing the two halves requires at least
    one empty endpoint segment for each of the \(2m\) crossing requests.
    Nonadjacent crossing endpoints forbid two empty segments on one request,
    hence every request has exactly one and is \(F\) or \(L\). The derangement
    hypothesis is used exactly to keep all internal requests nonempty.

14. **Portal obstruction A3: `proved/pass`.** All eight displayed requests
    have Hamming distance two. For coordinate \(0\), the internal requests
    force \(3\) to be \(F\), \(5\) to be \(L\), and then \(2\) to be \(F\);
    the last two induced requests collide at target \(7\). For coordinate
    \(1\), they force \(3=L\), \(6=F\), and \(4=L\), after which two induced
    requests collide at source \(4\). For coordinate \(2\), request
    \(7\to1\) collides with internal \(3\to0\) if \(F\), and with internal
    \(6\to5\) if \(L\). This is a complete hand certificate. Independent
    enumeration found zero feasible choices among respectively \(64,64,16\)
    \(F/L\) assignments.

15. **Explicit routing of the A3 permutation: `proved/pass`.** Every
    consecutive pair in the eight displayed vertex sequences is a cube edge,
    every sequence has the stated source and target, and the 16 directed arcs
    are distinct. Opposite orientations of an undirected edge are correctly
    treated as different capacities.

16. **Beneš obstruction A4: `proved/pass`.** For each coordinate, the quotient
    multigraph in the table is one connected 2-regular bipartite multigraph,
    hence one cycle. The displayed commodity coloring
    \(c=(0,1,1,0,1,0,0,1)\) is alternating at every input and output pair and
    gives
    \[
    A=B=(0,1,1,0).
    \]
    This orientation conflicts at indices \(1,2\); its only complement
    conflicts at \(0,3\). Thus both cycle flips fail for every coordinate.
    An independent reconstruction found zero satisfying flips for all three
    coordinates. The certificate concerns only this restricted embedding.

17. **Adaptive multi-crossing claim A-U1 and the one-defect auxiliary lemma:
    `unverified`.** Neither a decomposition producing a strictly simpler
    request class nor routability of every one-defect partial permutation is
    proved. The text correctly avoids using either as a theorem. The separate
    \(Q_1\) forbidden-arc strengthening is `proved/pass`: requests
    \(0\to0,0\to1\) force \(0\to1\).

18. **Ordered-closed-trail equivalence B1: `proved/pass`.** Concatenating the
    routed paths around each permutation cycle gives a closed directed trail
    with the designated path junctions as marked occurrences. Extra unmarked
    occurrences of terminals do not alter the cyclic order of the marks.
    Conversely, splitting at the marks gives arc-disjoint terminal-to-terminal
    trails; item 2 converts each to a path using only a subset of its arcs.
    The requirement that trails for distinct permutation cycles be jointly
    arc-disjoint preserves the original existential quantifier.

19. **Path-order criterion B2: `repairable gap`.** The claim is true, but the
    proof says to route \(x_k\to x_1\) along “all of \(R\)” in reverse.
    The hypothesis does not say that \(x_1,x_k\) are the endpoints of \(R\), so
    all of \(R\) need not start and end correctly. This is the earliest invalid
    literal instruction. **Exact repair:** replace \(R\) by its subpath from
    \(x_1\) to \(x_k\), or say “along the \(x_1\)-to-\(x_k\) subpath of \(R\)
    in reverse.” The forward terminal subpaths partition that same subpath, so
    the repaired proof is complete.

20. **Every single 3-cycle B3: `proved/pass`.** The coordinatewise-majority
    discrepancy sets are pairwise disjoint. Shortest branches supported on
    those sets meet only at the majority vertex, and every branch edge is used
    once in each direction. Empty branches cause no problem, including when
    one terminal equals the majority.

21. **General hub-fan lemma B4: `repairable gap`.** The proof needs the
    stronger fan property
    \[
    V(R_j)\cap V(R_\ell)=\{r\}\quad(j\ne\ell),
    \]
    not merely disjoint sets of internal vertices under the weakest reading of
    “internally vertex-disjoint.” Under that weak reading, take the bidirected
    graph with edges \(rx_1,rx_2,x_1x_3\), cycle
    \((x_1\,x_2\,x_3\,r)\), and branches
    \(R_1=r x_1\), \(R_2=r x_2\), \(R_3=r x_1x_3\). Their interior sets are
    \(\varnothing,\varnothing,\{x_1\}\), but the cut
    \(\{x_1,x_3\}\) has only the outgoing arc \(x_1\to r\), while both demands
    \(x_1\to x_2\) and \(x_3\to r\) must leave it. The permutation is not
    routable. **Exact repair:** define an \(r\)-to-\(X\) fan as paths that
    pairwise intersect only at \(r\), and use that as B4's hypothesis. With
    this wording, its branch-orientation proof is correct.

22. **Single-cycle theorem B5 through \(d+1\): `proved/pass` after the B4
    wording repair.** The induction really proves that deleting at most
    \(d-1\) vertices leaves \(Q_d\) connected. If both halves lose at most
    \(d-2\), induction connects each and more than \(d-1\) matching edges
    ensure one survives. Otherwise all deletions lie in one half; the intact
    half connects every surviving vertex of the damaged half through its
    matching neighbor.

    In the augmented graph, an \(r\)-\(t\) separator excludes \(r,t\). Any set
    of fewer than \(|X|=k-1\leq d\) such vertices leaves \(Q_d\) connected and
    leaves at least one \(X\)-vertex adjacent to \(t\). Vertex Menger therefore
    gives \(k-1\) internally disjoint \(r\)-\(t\) paths. Their last neighbors
    of \(t\), and also their first \(X\)-vertices, are distinct; truncating at
    those first \(X\)-vertices gives all endpoints of \(X\) and paths meeting
    only at \(r\). The endpoint cases work: \(d=1,k=2\) gives one branch, and
    \(k=d+1\) uses exactly the \(d\) available branches.

23. **Sharpness of the one-hub mechanism and the multiple-fan warning:
    `proved/pass`.** Paths meeting only at a \(d\)-valent hub must use distinct
    first edges, so there can be at most \(d\) branches. Also, each fan routing
    uses both orientations of every supporting branch edge; two independently
    chosen fans sharing an undirected edge necessarily conflict. This is a
    limitation of the mechanism, not a nonroutability theorem for longer or
    multiple cycles.

24. **Translation routing B6: `proved/pass`.** At each scheduled coordinate,
    the current vertex is a bijective translate of the source, so that stage
    uses every directed arc of that dimension exactly once. Different stages
    use different dimensions, and each path flips each support coordinate once.

25. **Direct-product routing B7: `proved/pass`.** Copies in phase one and
    phase two occupy disjoint fibers, while the phases use disjoint coordinate
    blocks. Bijection of \(\alpha\) makes the second-stage fiber indexing
    exact. The same no-repeated-vertex check as item 10 applies.

26. **Coordinate-transposition consequence: `proved/pass`.** On each
    \(2\)-face, the routes \(01\to00\to10\) and
    \(10\to11\to01\) use four distinct directed arcs and have the correct
    swapped targets. Disjoint coordinate transpositions are a direct product of
    these local permutations.

27. **Sequential composition counterexample B8: `proved/pass`.** In \(Q_1\),
    both copies of the bit flip have unique nonempty routings. Concatenating
    them makes each directed arc appear in both commodity walks. This refutes
    conflict-free concatenation of routed factors, while correctly leaving open
    a different direct routing of the composite identity.

28. **Arbitrary single-cycle trail B-U1: `unverified`.** The proved classes do
    not cover a prescribed cycle longer than \(d+1\). The statement that
    arbitrary packing of independently constructed cycle trails is
    theorem-strength is `proved/pass`: by item 18, that unrestricted packing
    is exactly the original conjecture, not an auxiliary simplification.

29. **Cube boundary inequality and equality classification C1:
    `proved/pass`.** The induction identity
    \[
    |\partial S|=|\partial A|+|\partial B|+|A\triangle B|
    \]
    is exact. In the \(a,b\leq M/2\) case, equality forces \(A=B\ne\varnothing\)
    and equality for both lower-dimensional boundaries; induction makes the
    common set a coordinate half. In the \(a>M/2>b\) case, equality in the
    complete chain forces \(a+b=M\), equality for \(B\), and \(b<M/2\).
    A nonempty \(B\) would then contradict the lower-dimensional equality
    classification, so \(B=\varnothing\) and \(A=V_{d-1}\). These are exactly
    the coordinate halves. Exhaustive enumeration for \(d\leq4\) corroborates
    the equality cases but is not needed by the proof.

30. **Automatic directed cut condition and equality C2: `proved/pass`.**
    Bijection gives
    \(r_\sigma(S)\leq\min(|S|,|V_d\setminus S|)\); item 29 bounds this by the
    outgoing cut capacity. Equality in the full chain forces the smaller side,
    hence both sides, to be a coordinate half. Then all sources in \(S\) target
    its complement, and bijection gives
    \(\sigma(S)=V_d\setminus S\). The converse is immediate.

31. **Consequences of a tight coordinate cut: `proved/pass`.** There are
    \(2^{d-1}\) demands in each direction and exactly that many directed cut
    arcs in each direction. Every such demand needs at least one correctly
    oriented crossing, so all capacity is already consumed. Thus every path
    crosses once, no recrossing is possible, and every directed cut arc is
    used. This uses arc capacity, not hidden vertex disjointness.

32. **Coordinate saturation C3: `proved/pass`.** Target-bit balance gives
    \(D_i=U_i\leq2^{d-1}\). Equality forces every source to flip bit \(i\);
    equality in the sum forces this in all coordinates, hence the antipodal
    translation, already routed by B6. The conclusion rules out only the
    stated global all-down-arcs saturation mechanism.

33. **Cut sufficiency C-U1: `unverified`.** The necessary cut inequalities do
    not supply integral multicommodity paths. The artifact correctly labels a
    cube-specific splitting-off theorem as missing and does not use it.

34. **Peeling a tight cut as a translation: `unverified`.** Tightness proves
    one-crossing rigidity but gives no arc-disjoint factorization or
    cancellation. The ledger correctly identifies that composing or removing a
    translation may reuse already saturated arcs. No repair is available
    without a new allocation theorem.

## Bottom line

After the two local wording repairs in B2 and B4, the strongest surviving
positive theorem is the single-cycle result for \(2\leq k\leq d+1\). The two
\(Q_3\) certificates decisively close the restricted one-crossing induction
routes. The remaining multi-crossing, arbitrary-long-cycle, multi-cycle packing,
and cut-sufficiency steps are genuinely unproved; none should be described as
near-complete.
