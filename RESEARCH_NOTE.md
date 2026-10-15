# The Six-Trap Conjecture

## Definition, finite evidence, partial results, and open challenge

**Adrien Washington**  
Founder, President & CEO of Seltlox  
Version 1.0 · 2026

**AI-assisted mathematical development and computation.**

### Abstract

We study the integer map `T(n)=n+D(n)-D(n+1)` for `n>=2`, where `D(n)` is the largest positive proper divisor of `n`. Six explicitly verified periodic cycles are recorded, and the Six-Trap Conjecture asserts that every starting integer eventually reaches one of them. A saved exact-arithmetic census classifies all **999,999,999** starting values from 2 through 1,000,000,000 into the same six cycles, with zero unclassified starts and zero cap hits. Separately, an internal computer-assisted arithmetic-family argument reports a lower-natural-density bound `Q50 ≈ 0.8695739413707237` for starts that fall below their original value within 50 moves. Neither result proves universal six-cycle capture. The project is AI-assisted and has not received external mathematical review or end-to-end proof-assistant formalization. No exact predecessor was identified in the searches preserved in Master V2; historical originality remains unverified.

## 1. Exact definition and conjecture

For an integer `n>=2`, let `D(n)` be its largest positive divisor strictly smaller than `n`. Equivalently, `D(n)=n/p(n)`, where `p(n)` is the least prime divisor of `n`.

```text
T(n) = n + D(n) - D(n+1).
```

Both divisor functions are evaluated at the original `n` before the move.

**Conjecture.** Every integer `n>=2` has some iterate in

```text
{2, 3286, 4210, 5182, 54214, 127330}.
```

The six values are minimum representatives of six registered periodic cycles. The conjecture is unresolved.

## 2. The six registered cycles

The six periods are 1, 5, 9, 3, 4, and 64, for a total of **86 distinct cycle states**. The complete state-by-state register is in `SIX_CYCLES.md` and `data/census_billion/cycles.csv`.

| Minimum | Period | Maximum cycle state | Starts reaching it in the billion census |
|---:|---:|---:|---:|
| 2 | 1 | 2 | 948,084,782 |
| 3,286 | 5 | 7,063 | 19,551,309 |
| 4,210 | 9 | 14,849 | 25,946,998 |
| 5,182 | 3 | 8,983 | 4,372,632 |
| 54,214 | 4 | 106,891 | 350,595 |
| 127,330 | 64 | 4,546,157 | 1,693,683 |

The last column is a finite-range census count, not a claim about limiting basin density.

## 3. Elementary structure

The following are internal hand proofs preserved in Master V2.

### 3.1 Domain preservation

For `n>=2`, `D(n)>=1` and `D(n+1)<=(n+1)/2`, so

```text
T(n) >= (n+1)/2.
```

Since `T(n)` is an integer, `T(n)>=2`. Also `T(n)<=3n/2-1`.

### 3.2 Unique fixed point

If `T(n)=n`, then `D(n)=D(n+1)`. This common value divides both consecutive integers and therefore equals 1. Hence `n` and `n+1` are both prime, forcing `n=2`. Conversely, `T(2)=2`.

### 3.3 Opposite one-step motion by parity

For odd `n>=3`, `D(n)<=n/3` and `D(n+1)=(n+1)/2`, hence

```text
T(n) <= (5n-3)/6 < n.
```

For even `n>=4`, `D(n)=n/2` and `D(n+1)<=(n+1)/3`, hence

```text
T(n) >= (7n-2)/6 > n.
```

Thus odd states decrease in one step while even states above 2 increase. This does not imply eventual descent.

### 3.4 No exact period-two cycle

Any two-cycle would alternate an even `e>=4` and an odd `o>e`. Let `p` be the least prime divisor of `e+1` and `q` the least prime divisor of `o`. The exact branch equations are

```text
E_p(x) = ((3p-2)x - 2)/(2p),
O_q(x) = ((q+2)x - q)/(2q).
```

Eliminating `o` yields

```text
e = 2[pq+q+2] / [6p-pq-2q-4].
```

Positivity implies `q<6`, so `q` is 3 or 5. The `q=3` reduction leaves only an algebraic candidate whose claimed `p` is not the actual least prime divisor of `e+1`; the `q=5` reduction yields no prime `p`. Therefore no exact two-cycle exists.

## 4. Why easy global descent is impossible

For every integer `k>=1`, the seed `n0=2+6^k` satisfies

```text
T^j(2+6^k) = 2 + 7^j 6^(k-j),    0 <= j <= k.
```

Every one of the first `k` moves is strictly increasing. Consequently:

- no universal constant `C` can bound every orbit by `C` times its initial value; and
- no fixed number of moves guarantees descent below the start for all sufficiently large seeds.

This is a family of **finite** growing prefixes, not one infinite escaping orbit.

## 5. Finite census through one billion

The retained exact-arithmetic census reports complete classification of every integer from **2 through 1,000,000,000 inclusive**: **999,999,999 starting values**.

The principal saved result is:

```text
cycles discovered: 6
unclassified starts: 0
cap hits: 0
map evaluations before memoized-tail reuse: 1,495,346,614
sum of individual stopping times: 152,725,996,715
```

Here stopping time means the number of map applications before **first entry into any state of the eventual cycle**, not travel to the minimum representative.

The longest transient in this finite interval is **623 moves**, first attained by seed **804,497,890**. The largest orbit height in the interval is **172,413,150,234,659**, reached from seed **789,535,970** at step 125; that seed first enters the fixed-point cycle at step 382. Its peak/start ratio is approximately **218,372.761705**.

The census report records mean stopping time 152.725997; median 148; 90th percentile 207; 99th percentile 271; and 99.9th percentile 332. Adjacent starts entered different cycles in 100,029,227 of 999,999,998 neighboring pairs in the tested interval.

### 5.1 Validation scope

A separately written internal verifier recomputed **120,057 selected starting-value classifications** and exported **113 complete record trajectories** comprising **25,225 witnessed transitions**. A separate Python audit checks aggregate identities and all 86 cycle edges by explicit proper-divisor enumeration.

This is **not** a second full billion-seed census, outside peer review, or proof-assistant certification.

### 5.2 What the census establishes

Every tested start from 2 through one billion reaches one of the same six cycles. Therefore, any additional finite cycle would have to have **every member above one billion**; otherwise a tested member would have been classified into that additional cycle rather than one of the registered six.

The census does **not** establish universal convergence, the absence of an escaping orbit beyond the tested range, or the absence of a hidden cycle entirely above one billion.

## 6. The 50-move forward-descent result

Define

```text
H50 = { n >= 2 : T^j(n) < n for some 1 <= j <= 50 }.
```

The preserved computer-assisted argument reports

```text
lower natural density(H50) >= Q50 > 0.86957394,
```

with

```text
Q50 = 1465497517150036500881632322460683852989669687076834714478473874462285105941798237166631226960041972312602350786713236795739/1685305236769110904458560286557724281112736457290136277951208019840411778367507660296252856676868304273502102196584448000000
```

and decimal value approximately **0.8695739413707237**.

### 6.1 Method in brief

The argument partitions starting integers into exact arithmetic families described by congruence restrictions. For a complete finite family, specifying each parity halves its natural density; this is a Chinese-remainder-theorem statement across starting integers, not a randomness assumption along one orbit.

The retained search produced **295,396 disjoint arithmetic families** of total density 1, including **56,178 direct descent certificates**. A prime-aware continuation treats unresolved even branches conservatively using finite CRT bounds on possible least-prime behavior. The remaining families are grouped into **415** coefficient classes. An exact dynamic program counts length-39 future parity words, absorbing a word once its certified cumulative coefficient is at most 1. The longest prefix before those 39 continuation moves is 11, giving a maximum window of 50 moves.

The main arithmetic uses exact integers and rational fractions. Floating point affects search priority/display, not certificate acceptance, density addition, or the exact final fraction.

### 6.2 What this does not say

The H50 result is **not**:

- a proof that 86.957% of integers reach one of the six cycles;
- a probability that the conjecture is true;
- a density-one theorem;
- a universal convergence proof; or
- permission to add its percentage to a different coverage bound without recomputing overlap.

The full supporting argument and saved certificate dependencies are included in `reports/H50_FORWARD_DESCENT_REPORT.md` and `data/h50_descent/`.

## 7. What remains open

The project has not:

- proved that all starting integers reach the six cycles;
- excluded every longer hidden cycle;
- proved that no orbit is unbounded;
- established universal variable-time descent;
- established density-one descent;
- found a successful global ranking function;
- completed an all-primes/all-lengths cycle classification; or
- certified historical originality.

A sufficient proof target, using the verified finite base, would be to prove that every `n>1,000,000,000` has some later iterate strictly smaller than `n`. Strong induction would then reduce every start to the finite classified base. That sufficient statement has **not** been proved.

## 8. Reproducibility

This release includes the exact C++ source retained for the billion census, the hardened reusable variant, a separately written verifier, the aggregate audit script, essential machine-readable billion outputs, the H50 search/continuation/checker code, the H50 certificate/frontier corpus, and the main continuation data.

See `REPRODUCE.md` for commands and resource notes. Checksums are in `CHECKSUMS_SHA256.txt`.

## 9. Creator and AI-assisted provenance

Six-Trap was created and directed by **Adrien Washington**. AI tools assisted with mathematical exploration, computation, code development, derivations, and adversarial testing. The project is released openly so its claims can be independently examined, reproduced, challenged, or disproved.

Seltlox is Adrien Washington's company and affiliation; it is not presented as the author or mathematical validator of the conjecture.

## 10. Originality status

No exact predecessor for this recurrence was identified in the searches preserved in Master V2. Those searches were incomplete and do not establish global historical originality. The correct claim is: **No exact predecessor identified in the searches performed; originality unverified.**

## 11. Open challenge

Find an escaping orbit. Find a seventh trap. Find a flaw in the computation. Prove the six traps are complete. Or discover something none of us have seen yet.

A seventh finite cycle is a conclusive counterexample if every exact transition is verified. A proved unbounded orbit is also a counterexample. A universal proof must cover the remaining infinite domain. A time limit, size limit, numerical average, or finite cutoff is not enough.

**We tried to kill it. Repeatedly. It survived. Now it's your turn.**

## Package references

- `CONJECTURE.md` - exact definition and conjecture.
- `SIX_CYCLES.md` - complete cycle register.
- `KNOWN_RESULTS.md` - selected result statements and elementary proofs.
- `reports/BILLION_CENSUS_REPORT.md` - preserved V2 finite-census report.
- `reports/H50_FORWARD_DESCENT_REPORT.md` - preserved V2 H50 report.
- `REPRODUCE.md` - verification and rerun instructions.
- `AI_AND_PROVENANCE.md` - creator/AI disclosure and public origin.
- `ORIGINALITY_AND_LIMITATIONS.md` - red-line boundaries and originality status.
- `CHALLENGE.md` - challenge mechanics.
