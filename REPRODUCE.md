# Reproduction guide

This repository provides two main reproduction lanes: the finite census and the computer-assisted 50-move forward-descent bound.

The canonical frozen Version 1.0 archive, including the full selected trajectory-verification corpus and SHA-256 manifest, is preserved at:

**https://doi.org/10.5281/zenodo.23357210**

## 1. Fresh finite-census rerun

Requirements: GCC or compatible Clang with C++17 support, plus Python 3. Exact ratio comparisons use the compiler's 128-bit integer extension.

```sh
g++ -O3 -std=c++17 -Wall -Wextra code/census/census.cpp -o /tmp/sixtrap_census
/tmp/sixtrap_census 10000000 /tmp/sixtrap_10m compact
```

For the exact source used in the retained billion run, compile `code/census/census_executed.cpp` instead. The preserved report states that the full billion-range run requires roughly 3 GB for the main arrays plus process overhead.

The reusable `census.cpp` contains a pre-publication boundary-handling hardening for small reruns whose dense cache boundary cuts through a discovered cycle. That hardening does not change the retained billion result.

A separately written verifier is included:

```sh
g++ -O3 -std=c++17 -Wall -Wextra code/census/verify.cpp -o /tmp/sixtrap_verify
```

See `reports/BILLION_CENSUS_REPORT.md` for the retained census methodology and scope.

## 2. Inspect the saved billion outputs

The essential saved outputs are in `data/census_billion/`.

For the larger selected independent trajectory-verification corpus and package-level checksum manifest, use the canonical Zenodo Version 1.0 archive.

## 3. Verify the H50 certificate corpus

Requirements: Python 3.10 or newer; standard library only.

The large compressed files `certificates.jsonl.gz` and `frontier.jsonl.gz` are intentionally kept in the canonical Zenodo Version 1.0 package rather than duplicated in this GitHub repository. Download the Zenodo archive and place those files under `data/h50_descent/cover_10000/`, alongside the included `summary.json`, then run:

```sh
python code/h50_descent/verify_cover.py \
  --folder data/h50_descent/cover_10000 \
  --out /tmp/sixtrap_cover_check.json

python code/h50_descent/verify_grouping.py \
  --folder data/h50_descent/cover_10000 \
  --groups data/h50_descent/continuation_50_steps/groups.json \
  --out /tmp/sixtrap_grouping_check.json

python code/h50_descent/verify_continuation.py \
  --folder data/h50_descent/cover_10000 \
  --result data/h50_descent/continuation_50_steps/continuation_result.json \
  --out /tmp/sixtrap_continuation_check.json
```

These are independent internal-implementation checks, not outside peer review or proof-assistant formalization.

## 4. Regenerate the H50 computation

```sh
python code/h50_descent/descent_attack.py \
  --prime-max 97 --max-nodes 10000 --max-depth 24 \
  --out /tmp/sixtrap_cover

python code/h50_descent/continue_cover.py \
  --folder /tmp/sixtrap_cover --out /tmp/sixtrap_main \
  --aware --grid 101/100 --horizon 39
```

Then run the verification scripts above against the regenerated output.

The target exact lower bound is recorded in `data/h50_descent/RESULT_STATUS.json`. Floating point is used for search ordering/display in the original computation; certificate acceptance and density arithmetic use exact integers or fractions as documented in the included report.
