# BREAK SIX TRAP.

**We tried to kill it. Repeatedly. It survived. Now it's your turn.**

## The Six-Trap Conjecture

Created and directed by **Adrien Washington**.  
**ORCID:** [0009-0005-5219-8404](https://orcid.org/0009-0005-5219-8404)

**Canonical frozen Version 1.0 record:** [Zenodo DOI 10.5281/zenodo.23357210](https://doi.org/10.5281/zenodo.23357210)

This GitHub repository is the **living technical home** for reproduction, challenge reports, corrections, and extensions. The Zenodo DOI above is the canonical immutable Version 1.0 research release.

Six observed traps. **999,999,999 consecutive starting values** were tested from 2 through 1,000,000,000. No seventh trap was found in that finite census. **No general proof.**

## The rule

For an integer `n >= 2`, let `D(n)` be the largest positive divisor strictly smaller than `n`. Equivalently, if `p(n)` is the least prime divisor of `n`, then `D(n) = n / p(n)`.

```text
T(n) = n + D(n) - D(n+1)
```

Both divisor functions are evaluated at the original `n` before the move.

**Conjecture:** every integer `n >= 2` eventually reaches one of the six recorded periodic cycles represented by

```text
2, 3286, 4210, 5182, 54214, 127330
```

## Your move

- Think there is a seventh trap? **Find it.**
- Think an orbit escapes? **Show it rigorously.**
- Think the computation is wrong? **Reproduce it and expose the flaw.**
- Think the six traps are complete? **Prove it.**
- Think there is prior art? **Bring the exact source.**

Use the repository's **Issues** tab to submit a concrete counterexample, candidate cycle, proof, reproducible computational error, prior-art source, or meaningful extension.

## Start here

- [Research note](RESEARCH_NOTE.md)
- [Canonical Version 1.0 record + PDF on Zenodo](https://doi.org/10.5281/zenodo.23357210)
- [Exact conjecture](CONJECTURE.md)
- [Complete six-cycle register](SIX_CYCLES.md)
- [Known results and scope](KNOWN_RESULTS.md)
- [Reproduction guide](REPRODUCE.md)
- [How to break Six-Trap](CHALLENGE.md)
- [How to submit a result](SUBMIT_A_RESULT.md)
- [Originality and limitations](ORIGINALITY_AND_LIMITATIONS.md)
- [AI-assisted provenance](AI_AND_PROVENANCE.md)
- [Contributing and challenge-response policy](CONTRIBUTING.md)
- [Code of conduct](CODE_OF_CONDUCT.md)

## What is established

This project separates four different kinds of statements:

1. **Conjecture:** the universal six-cycle capture statement remains unresolved.
2. **Written arguments:** elementary structural results whose proofs are given in the research note.
3. **Computer-assisted results:** notably the 50-move forward-descent lower-natural-density bound, with saved certificates and independent internal checkers.
4. **Finite exhaustive computation:** every start from 2 through 1,000,000,000 was classified in the retained census.

The billion census is finite evidence, **not proof** of the infinite conjecture. The 50-move density result is not a capture percentage and is not a probability that the conjecture is true.

## Reproducibility

The repo includes the principal source code, compact billion-census outputs, H50 result/continuation summaries, and verifier code. To keep GitHub lightweight, the large compressed H50 certificate/frontier corpus and the larger selected trajectory-verification corpus remain in the **canonical frozen Version 1.0 package** on Zenodo:

**https://doi.org/10.5281/zenodo.23357210**

## AI-assisted provenance

Six-Trap was created and directed by Adrien Washington. AI tools assisted with mathematical exploration, computation, code development, derivations, and adversarial testing. The project is public so its claims can be independently examined, reproduced, challenged, corrected, extended, proved, or disproved.

## Originality status

No exact predecessor for this recurrence was identified in the searches preserved during development. That is **not** a proof of historical originality. See [ORIGINALITY_AND_LIMITATIONS.md](ORIGINALITY_AND_LIMITATIONS.md).

## Citation

```text
Washington, Adrien. The Six-Trap Conjecture. Version 1.0, 2026.
https://doi.org/10.5281/zenodo.23357210
```

## Licenses

Original non-code materials are released under **CC BY 4.0**. Source code under `code/` is released under the **MIT License**. See the top-level [LICENSE.md](LICENSE.md) and full [LICENSES.md](LICENSES.md).
