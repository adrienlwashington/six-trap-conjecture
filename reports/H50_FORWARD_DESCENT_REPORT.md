# Six Trap — Collatz Descent Attack 01
## A prime-aware extension of the finite-density descent method

**Date:** September 24, 2026, America/New_York  
**Project:** Adrien's Six-Trap Conjecture research  
**Provenance:** Adrien requested the attack. These derivations, programs, and internal checks were produced with ChatGPT assistance. No external researcher was contacted, and no claim of independent human review or publication-level novelty is made.

## 1. Outcome

This attack did **not** prove or disprove the Six-Trap Conjecture. It did not prove density-one descent, a Korec-type power reduction, or a Tao-type almost-bounded-orbit result. It was not another billion-start census.

It produced an internally checked, computer-assisted partial result. Define

\[
H_K=\{n\ge2:\exists j\in\{1,\ldots,K\},\ T^j(n)<n\}.
\]

The main result is

\[
\boxed{\underline d(H_{50})\ge Q_{50}>0.86957394.}
\]

Here lower natural density is

\[
\underline d(H)=\liminf_{X\to\infty}\frac{\#(H\cap[2,X])}{X}.
\]

The computed rational Q_50 is approximately **86.9573941371%**. This is a bound about infinite families of starting integers, not a percentage measured in a finite sample. It does not assert that exactly this percentage descends, nor that the complement fails to descend. It is not a proof of capture by the six registered cycles.

The saved research log already reported **85.2476077926% within 50 moves**. The pre-run conversational description that only the odd 50% had been proved was incomplete and should not be retained as the research baseline. The present comparison uses the same 50-move window, improving that recorded bound by about **1.7098 percentage points**.

The proof combines the earlier finite-parity density lemma with newly generated arithmetic-family certificates and a prime-aware treatment of an unresolved even branch. The latter is described in Section 5. “New” here means developed and used in this run; mathematical originality relative to all prior literature or all possible unpublished arguments has not been established.

## 2. Frozen definition and affine descent criterion

For n >= 2, let p(n) be its least prime divisor and

\[
D(n)=n/p(n),\qquad T(n)=n+D(n)-D(n+1).
\]

For an odd prime p, the actual branches are

\[
E_p(x)=\frac{(3p-2)x-2}{2p},\quad x\text{ even},\quad p=p(x+1),
\]

\[
O_p(x)=\frac{(p+2)x-p}{2p},\quad x\text{ odd},\quad p=p(x).
\]

Both are of the form ax-b with a>0 and b>0. For a valid positive-length branch path,

\[
T^k(n)=A_k n-B_k,\qquad A_k>0,\quad B_k>0.
\]

Therefore **A_k <= 1 is sufficient for strict descent**. It is not necessary: the negative affine offset can also cause descent when A_k>1. Our certificates deliberately use the sufficient condition, avoiding numerical judgments about enormous individual inputs.

Odd inputs decrease immediately, with slope at most 5/6. Even inputs greater than 2 increase, with slope less than 3/2. These identities and the affine-composition criterion were already in the project's earlier work.

## 3. Why the direct Terras-style parity shortcut does not close the proof

The standard accelerated Collatz branches have slopes 1/2 and 3/2. Their balanced multiplicative product is 3/4. In Six Trap, the unconditional upper slopes are 5/6 and 3/2; their product is 5/4, which is greater than 1.

Thus a balanced count of odd and even steps is not enough to force contraction using these bounds. This calculation is about the **bounds**, not a positive-growth theorem for actual Six Trap orbits.

The known E–O refinement improves the estimate but still does not produce a negative-drift conclusion. If e is even, m=T(e) is odd, p=p(e+1), and q=p(m), put e+1=pa. Then

\[
m=\frac{(3p-2)a-3}{2}.
\]

If q=3, reduction modulo 3 forces p=3. The slope product is then 35/36. If q=5, the product is less than 21/20. If q>=7, it is less than 27/28. Consequently every actual E–O block has slope product less than 21/20.

A valid conservative parity-word bound consequently charges:

- 3/2 for an even step;
- 7/10 for an odd step immediately following an even step already charged 3/2;
- 5/6 for any other odd step.

The 7/10 factor is a **two-step accounting device**, not an unconditional pointwise bound on that odd step. It must not be attached to an even step whose contribution was previously handled differently without checking the resulting product.

Under balanced finite-word counting, the corresponding long-word mean log bound is

\[
\tfrac12\log(3/2)+\tfrac14\log(7/10)+\tfrac14\log(5/6)
=\tfrac14\log(21/16)>0.
\]

This identifies the gap in the straightforward parity-bound argument. It neither disproves convergence nor proves that no stronger adaptation of Collatz methods can work.

## 4. Arithmetic families and finite-parity density: the proof foundation

### 4.1 Representation and exact density

A finite family is represented as

\[
n=Mt+r,\qquad x=ut+v,
\]

with M,u>0 and restrictions t mod q not in F_q at finitely many odd primes q. Each forbidden set is proper. Its natural density among starting integers is

\[
w=\frac1M\prod_q\frac{q-|F_q|}{q}.
\]

Finitely many small parameter values outside the positive domain can be discarded without changing density. The formula follows by the Chinese remainder theorem. It is not a stochastic assumption about an individual orbit.

After a complete actual branch, u is odd. Initially u=1. Selecting a parity replaces t by 2s+b. Selecting an odd least prime either adds an odd-modulus substitution or is already forced by the coefficient and constant. The branch then divides the coefficient by 2p and multiplies it by an odd numerator, leaving an odd integer.

### 4.2 Parity halves every complete family

When u is odd, specifying x's parity specifies one residue of t modulo 2. The substitution t=2s+b permutes every forbidden set at an odd prime without changing its size. Its density is exactly half the parent density.

### 4.3 Unbounded prime cases require tail control

Within a fixed parity family, the relevant odd integer is a linear expression cs+d. Away from the finitely many primes dividing c or already appearing in restrictions, excluding a new prime removes one residue class. The density of the subset whose least prime exceeds Y is bounded by a constant times a product of (1-1/q) over nonexceptional primes q<=Y. This product tends to zero. If a prime divisor of c also divides d, the least prime is already bounded instead.

For any fixed number of steps, finitely many actual-prime branches can therefore capture all but an arbitrarily small density. This justifies sums over the remaining countably many cases. It is not an interchange of an infinite time limit with a density limit.

### 4.4 Consequence

Every specified length-L parity word at a complete family has relative natural density exactly 2^(-L). The statement is also valid conditional on each actual finite branch family. This is the previously recorded finite-parity theorem, rederived here as the foundation of the continuation calculation.

It does **not** say that every individual infinite trajectory is balanced or random. It also supplies no quantitative uniformity when L grows with the starting-value cutoff X; this distinction matters for stronger goals.

## 5. Prime-aware continuation through an unresolved even branch

This is the additional arithmetic information used in the improved bound.

### 5.1 Setting

Take a parity-fixed family whose current state is the even integer e=ut+v. Here u and v are even. Suppose all possible prime divisors of e+1 up to 97 have been excluded, but its actual least prime p>97 has not been resolved. Let

\[
a_q=q-|F_q|\quad (q\le97\text{ odd prime}).
\]

The branch slope is less than 3/2. Resolve each actual p temporarily for the proof. Conditioning on p preserves the cardinalities of the allowed residue sets at all q<=97: the parameter substitutions have multipliers coprime to these q, and any additional exclusions between 97 and p occur at different primes.

Let m=E_p(e). Its parity splits each actual-p family into equal densities. The calculation below concerns the subfamily where m is odd.

### 5.2 The prime 3 is impossible at m

Writing e+1=pa gives

\[
2m=(3p-2)a-3.
\]

Because 3 does not divide e+1 and p>97, 3 does not divide a. Reducing the displayed identity modulo 3 shows 3 does not divide m.

### 5.3 Bounds on divisibility by q>=5

Fix q in {5,7,...,97}. If q does not divide the pre-branch coefficient u, there are two possibilities after applying E_p:

1. The coefficient of the new parameter at m is nonzero modulo q. Then divisibility of m by q selects at most one of its a_q allowed residues. The conditional relative density is either 0 or 1/a_q.
2. The coefficient becomes zero modulo q. Since p and 2 are invertible modulo q, this requires 3p-2=0 modulo q. The identity for m then gives m=-3/2 modulo q, which is nonzero for q>=5. The divisibility density is 0.

If q divides u, a safe upper bound is 1: this case can carry a forced residue and is not assumed uniform.

Thus valid upper probabilities are

\[
\beta_q=\begin{cases}1/a_q,&q\nmid u,\\1,&q\mid u.\end{cases}
\]

Selecting m's odd parity is another substitution with multiplier 2 and preserves all allowed-set cardinalities. For fixed actual p, divisibility events at distinct q concern separate CRT coordinates, so their finite joint densities factor. The actual probabilities need not equal beta_q; each is only bounded above by it.

### 5.4 Conservative least-prime mixture

Order q=5,7,...,97 and put

\[
S_q=\prod_{5\le r<q}(1-\beta_r).
\]

Use mass S_q beta_q for a pessimistic least-prime value q, with remaining mass product(1-beta_q) assigned to the threshold 101. This model makes small least primes at least as likely as in each actual-p family. Consequently it gives a conservative lower bound on any payoff that improves as the least prime increases.

For the next odd branch, the slope upper bound is 1/2+1/q, decreasing with q. The subsequent parity-certificate success probability is nonincreasing in its input slope bound. The mixture therefore gives a valid **lower** bound on eventual certificate success. This is finite CRT stochastic domination, not an assertion that actual orbit factors are independently sampled over time.

For the following even branch, the calculation simply charges another factor 3/2. In symbols, if A bounds the coefficient before the unresolved even step:

- half the family receives the bound (9/4)A after two moves, with the last even step eligible for a later E–O discount;
- half receives the conservative mixture of bounds (3/2)(1/2+1/q)A after two moves, with no pending E–O discount.

The bounds hold within every actual p>97 family. Section 4.3 permits their aggregation over all such p without a missing tail. Future parity counting is applied conditional on actual completed branches, then aggregated; no unjustified independence from prior prime choices is required.

## 6. Executed certificate search and continuation

The search used exact integer coefficients and Fraction-valued densities. Its retained completed settings were:

- actual branch primes through 97;
- 10,000 expanded complete families, prioritized by density;
- a configured depth cap of 24, with all actual direct descent certificates obtained within at most 9 moves;
- all prime, node-budget, and depth frontiers explicitly retained rather than declared successful.

The search produced 56,178 direct certificates, of combined density 0.7580285297234837... . It retained 10,791 prime-tail families and 228,427 node-frontier families. Together the certificates and frontier form 295,396 disjoint arithmetic families with total density exactly 1.

This raw direct-certificate percentage is only one component, not the final theorem. Applying the prime-aware continuation to the frontier adds immediate two-step certificates and prepares further continuation families.

For the main result, each positive coefficient bound greater than 1 is rounded **upward**, using exact fractions, to a power of 101/100. This weakens rather than strengthens the contraction claim. Families are grouped by that grid value and whether the last even factor remains eligible for pairing. There are 415 nonzero groups.

A dynamic program counts all length-39 future parity words. It absorbs a word at its first certified cumulative coefficient <=1. Each word has relative weight 2^(-39), justified by Section 4. The longest prefix used before these 39 moves is 11, so the total window is at most **50** moves. Early absorption remains a success regardless of the later bits.

The program represents a live word by counts (e,c,b), where e is the number of E steps, c the number of discounted O steps, and b records whether the most recent step was E. At depth t the coefficient multiplier is

\[
(3/2)^e(7/10)^c(5/6)^{t-e-c}.
\]

All threshold comparisons are integer cross-products. Counts are arbitrary-precision integers. Floating-point values are used only for search priority and decimal reporting, not certificate acceptance, density addition, or coefficient rounding.

## 7. Results and control

| Calculation | Guaranteed move window | Lower-density bound |
|---|---:|---:|
| Earlier saved Attack 05 result | 50 | 85.2476077926...% |
| This run's control, without prime-aware even-tail mixture | 50 | 85.4296971383...% |
| This run's main prime-aware result | 50 | 86.9573941371...% |
| Separate longer continuation, grid 51/50 | 71 | 87.0979321943...% |

The control uses the same newly generated direct cover and a 101/100 grid. It has a maximum prefix length of 10 and 40 additional parity moves. The main calculation has a maximum prefix of 11 and 39 additional moves. Both therefore use the same 50-move ceiling. The difference is not merely a different time window.

The longer run is retained as a secondary calculation. The full independent Fraction-state dynamic-program check described below was applied to the **main 50-move result**, not separately to every secondary horizon.

### Exact main rational

The exact bound Q_50 is

```
1465497517150036500881632322460683852989669687076834714478473874462285105941798237166631226960041972312602350786713236795739/1685305236769110904458560286557724281112736457290136277951208019840411778367507660296252856676868304273502102196584448000000
```

The displayed decimals are rounded presentations. The stated strict bound Q_50 > 0.86957394 is below the exact rational and does not depend on rounding direction.

## 8. Checks completed

### 8.1 Independent arithmetic-family checker

`verify_cover.py` does not import the search implementation. It replays each stored branch symbolically, verifies the least-prime exclusions, recomputes density directly from M and the forbidden residue sets, checks terminal coefficient inequalities, and checks prefix disjointness of the family descriptions.

It passed:

- all 295,396 arithmetic families;
- all 56,178 direct certificates;
- 1,591,065 symbolic branch transitions;
- 7,755,274 least-prime exclusion checks;
- exact total partition mass 1.

### 8.2 Independent grouping checker

`verify_grouping.py` independently rebuilt all 239,218 frontier contributions using cumulative CRT survival products and a different exact-corrected grid-rounding routine. It reproduced all 415 grouped masses, the immediate-certificate contribution, and the maximum prefix length 11 exactly.

### 8.3 Independent continuation checker

`verify_continuation.py` uses Fraction-valued cumulative products as state keys instead of the first dynamic program's exponent counts. It reproduced all **415 exact length-39 success fractions** and the final rational Q_50.

It also completed 15 direct short-word enumeration checks at lengths 6, 10, and 12, and 16,800 modular divisibility checks on 700 selected even-tail families with actual even-branch prime 101. These modular checks corroborate the lemma; its all-prime justification is the hand argument in Section 5, not the finite sample.

These are independent **implementations within the same AI-assisted session**, not independent external authors or reviewers. The argument has not been formalized in a proof assistant. Exact arithmetic and multiple checks reduce implementation risk but do not make mathematical review unnecessary.

## 9. Korec and Tao applicability audit

Terras–Everett-style descent asks whether almost every starting integer eventually falls below itself. The present result advances a finite-time lower-density bound; it does not establish density one.

Korec's Collatz result gives a power-scale reduction for almost all starts, while Tao's result gives eventual descent below any prescribed function tending to infinity, in logarithmic density. Neither conclusion has been established here for Six Trap. In particular, neither follows from repeating the current 86.96% statement: the images of surviving starts need not have the same distribution as fresh starts.

The published generalization of Tao consulted here concerns a specific fixed-residue affine family. Six Trap is not directly an instance of that family. This is an applicability distinction, not a theorem that their techniques can never be adapted.

### No fixed finite residue-affine representation of Six Trap

Here is a direct proof of the relevant structural obstruction. Suppose a fixed modulus M made T affine on each residue class. Choose two distinct odd primes p_1,p_2 not dividing M. For either chosen p, the CRT provides infinitely many odd n satisfying

\[
n\equiv1\pmod{2M},\quad n\equiv0\pmod p,
\]

and n not divisible by any smaller prime. To obtain such a progression, impose n=1 modulo every smaller odd prime not already handled by 2M. All these conditions are compatible.

These n have least prime p, so

\[
T(n)=(1/2+1/p)n-1/2.
\]

An affine formula on the residue class 1 modulo M would therefore have to possess slope 1/2+1/p_1 and also slope 1/2+1/p_2, since it agrees at infinitely many inputs of each kind. This is impossible. Thus **no fixed finite modulus supplies an exact residue-affine table for T**.

This proof rules out a direct identification, not a clever acceleration, embedding, or new generalization of the methods.

## 10. What remains unproved, and the next precise target

No seventh cycle or unbounded orbit was constructed. No proof was obtained that all starting integers reach the registered six cycles. No cryptographic, computational-speedup, physical, or other practical application is claimed by this run.

Even a density-one descent theorem would not by itself identify all cycles or exclude exceptional starting integers. A start can fall below its own initial value and later enter a cycle not yet known. The remaining 13.04% in the main bound is **uncertified mass in this proof**, not a measured escaping population.

A sufficient next target for this line is to control the coefficient-survivor sets

\[
S_K=\{n\ge2:A_j(n)>1\text{ for all }1\le j\le K\},
\]

where A_j(n) is the product of the actual branch slopes along n's first j moves. Proving

\[
\lim_{K\to\infty}\overline d(S_K)=0
\]

would imply density-one descent, because coefficient crossing is sufficient for actual descent. The current certificates do not establish this limit. Prime-dependent behavior among surviving families, rather than unconditioned one-step averages, is the key missing control.

This target is sufficient, not equivalent to every possible proof of descent: some actual descents occur before coefficient crossing because of the negative offsets. Stronger methods are not ruled out by this particular formulation.

**Final status:** genuine partial progress in the descent-certificate approach, with a concrete, internally checked 50-move lower-density improvement. No complete Six-Trap resolution and no automatic transfer of the strongest Collatz theorems.

## 11. Sources and provenance

The following primary mathematical sources were consulted for the external comparison and scope of the imported methods, not as proofs of the new Six Trap bound:

1. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562, version 6, July 6, 2026. Introduction and main theorem; it also identifies the historical Terras, Everett, and Korec results.
2. Felipe Gonçalves, Rachel Greenfeld, and Jose Madrid, *Generalized Collatz Maps with Almost Bounded Orbits*, arXiv:2111.06170, version 2. Fixed-residue map definitions and applicability conditions.

The project baseline came from `Six-Trap_Conjecture_Log_through_Attack_10.md`, especially the preserved Attack 05 section on finite parity balance and the 85.2476% result, and the Attack 04 notes distinguishing interval averages from orbit averages. The billion-start report was not needed as a premise for the theorem and its census was not rerun here.

No claim is made that every relevant theorem in the Collatz literature was exhausted. “Attack 01” in this filename labels this Collatz-descent experiment; it does not renumber the original research log's Attacks 01–10.
