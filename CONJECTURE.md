# The Six-Trap Conjecture

**Created and directed by Adrien Washington · 2026**  
AI-assisted mathematical exploration, computation, code development, derivations, and adversarial testing.

For an integer `n >= 2`, let `D(n)` be its largest positive divisor strictly smaller than `n`. Equivalently,

```text
D(n) = n / p(n),
```

where `p(n)` is the least prime divisor of `n`.

Define

```text
T(n) = n + D(n) - D(n+1),    n >= 2.
```

Both divisor functions are evaluated at the original `n` before the move. Repeatedly replace the current value with `T(current value)`.

## Exact conjecture

Every integer `n >= 2` has some iterate in the set

```text
{2, 3286, 4210, 5182, 54214, 127330}.
```

These six integers are minimum representatives of six explicitly recorded periodic cycles. They are not extra branches, exceptions, or six states of one cycle.

Equivalently, the conjecture asserts both:

- every orbit eventually becomes periodic; and
- the six registered cycles exhaust all possible periodic attractors.

## Status

**Unresolved.** The preserved project contains no complete proof, no seventh verified cycle, and no proved unbounded orbit. The canonical finite census ends at 1,000,000,000; the conjecture quantifies over every integer `n >= 2`.

See [SIX_CYCLES.md](SIX_CYCLES.md), [KNOWN_RESULTS.md](KNOWN_RESULTS.md), and [CHALLENGE.md](CHALLENGE.md).
