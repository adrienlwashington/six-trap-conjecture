# Selected known results and their status

This file is deliberately selective. It exposes the central public-facing results from frozen Master V2 without turning the release into the full private research archive.

| Result | Status in Master V2 | Exact scope | Important limitation |
|---|---|---|---|
| Domain preservation | Internal hand proof | `T(n) >= 2` for every `n >= 2` | Says nothing about eventual capture |
| Unique fixed point | Internal hand proof | `2` is the only fixed point | Longer cycles exist |
| One-step direction | Internal hand proof | Odd `n >= 3` decrease; even `n >= 4` increase | Does not force global descent |
| No exact period two | Internal hand proof | No two-state cycle exists | Does not exclude longer cycles |
| Arbitrarily long initial growth | Internal hand proof | For every `k >= 1`, `2+6^k` rises for its first `k` moves | Different seed for each `k`; no escaping orbit |
| No constant excursion multiplier | Internal hand proof | No universal constant `C` bounds all orbit values by `C` times the seed | Seed-dependent bounds remain possible |
| Exact finite parity balance | Internal hand proof | Every fixed length-`L` parity word has natural density `2^-L` across starting integers | Not randomness along one infinite orbit |
| 50-move forward descent | Internal computer-assisted proof | Lower natural density at least `Q50 ≈ 0.8695739413707237` for starts descending below themselves within 50 moves | Not six-cycle capture, density one, or universal convergence |
| Billion census | Saved exhaustive computation | Every start 2 through 1,000,000,000 classified into the six registered cycles | Finite evidence only; not an infinite proof |

## Elementary proofs

### Domain preservation

For `n >= 2`, `D(n) >= 1` and `D(n+1) <= (n+1)/2`. Therefore

```text
T(n) >= (n+1)/2.
```

Since `T(n)` is an integer, `T(n) >= 2`. Also `T(n) <= 3n/2 - 1`.

### Unique fixed point

If `T(n)=n`, then `D(n)=D(n+1)`. The common value divides consecutive integers, so it must be 1. Therefore both `n` and `n+1` are prime. The only consecutive primes are 2 and 3, and indeed `T(2)=2`.

### Odd states decrease; even states above 2 increase

For odd `n >= 3`, `D(n) <= n/3` and `D(n+1)=(n+1)/2`, giving

```text
T(n) <= (5n-3)/6 < n.
```

For even `n >= 4`, `D(n)=n/2` and `D(n+1) <= (n+1)/3`, giving

```text
T(n) >= (7n-2)/6 > n.
```

### No exact period two

Any two-cycle would have an even state `e >= 4` and an odd state `o > e`. Put `p=p(e+1)` and `q=p(o)`, both odd primes. Eliminating `o` from the exact branch equations gives

```text
e = 2[pq+q+2] / [6p-pq-2q-4].
```

Positivity forces `q < 6`, hence `q` is 3 or 5. The `q=3` case reduces to `e = 2 + 30/(3p-10)` and leaves only an algebraic candidate whose claimed `p` is not the actual least prime divisor. The `q=5` case reduces to `e = 10 + 154/(p-14)` and yields no prime `p`. Therefore no period-two cycle exists.

## A growth family that blocks easy descent arguments

For every integer `k >= 1`, the seed `n0 = 2+6^k` satisfies

```text
T^j(2+6^k) = 2 + 7^j 6^(k-j),    0 <= j <= k.
```

Thus its first `k` moves strictly increase and end at `2+7^k`. Consequently there is no universal constant `C` with every orbit bounded by `C` times its starting value, and no fixed number of moves that guarantees descent below the start for all sufficiently large seeds.

This construction does **not** produce an infinite increasing orbit: every `k` uses a different finite seed.

For the strongest current computer-assisted result and the complete finite census, see the included reports under `reports/`.
