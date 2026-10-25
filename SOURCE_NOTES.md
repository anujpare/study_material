# PETS source notes and corrections

Chapter 3 is based on **lecture9-10-11-12_snarks.pdf** (12 pages). Its exercises and the standalone HW3 deck use **hw3_sol.pdf**, Exercise Sheet 3 version 1.1 (5 pages). Document instructions such as “write at most one sentence” describe the assignment's submission format; they do not override the requested step-by-step teaching format.

The site numbers its chapters 1: Commitment, 2: Zero Knowledge, 3: SNARKs. Existing Commitment and Zero Knowledge URLs and lesson IDs remain valid. The labels do not renumber the original course lectures.

## Coverage and placement

The new chapter contains 36 teaching cards and all 12 HW3 subquestions: 48 cards total. HW3 contains the same 12 questions and solutions, ordered by assignment number. Both views are generated from one exercise source. `scripts/snarks-audit.json` maps every chapter card to source pages and prerequisite IDs.

| Lecture pages | Chapter material |
| --- | --- |
| 1 | Succinctness, input-reading cost, SNARG versus SNARK |
| 2–3 | PCP/IOP interfaces, commitments, PCP argument and communication |
| 4 | Polynomial encoding and the Fibonacci example |
| 5 | Root bound, random equality testing, Schwartz–Zippel |
| 6 | Vanishing polynomials, quotient tests, seven-query recurrence check |
| 7–8 | Polynomial commitments, compilation, arithmetic circuit relations |
| 9 | Execution trace, interpolation domain and four obligations |
| 10 | Public inputs, gate selectors and efficient vanishing evaluation |
| 11–12 | Wire consistency, setup/preprocessing and the construction's scope |

| HW3 | Placed after |
| --- | --- |
| 1(a) | Soundness and knowledge error are distinguished |
| 1(b) | Plain, CRS and random-oracle models are introduced |
| 2(a), 2(b), 1(d) | Schnorr, Fiat–Shamir and privacy strengths |
| 2(d) | Transferable proofs versus simulated recordings |
| 2(c), 3(a) | Counting possible challenges and attempts |
| 3(b) | Parallel repetition and special soundness |
| 4(a) | PCP authentication, logical checks and communication count |
| 4(b) | Deriving PCP randomness with Fiat–Shamir |
| 1(c) | Finite-field arithmetic and the proof of the root bound |

Linear-query IOPs on lecture page 3 are also introduced in the two-routes card: a weighted inner product connects vector queries to polynomial evaluation from coefficients. The route diagram then follows bit-query PCPs and polynomial-evaluation IOPs as the two constructions developed in detail.

## Mathematical and model clarifications

1. **Fibonacci indexing (lecture pp. 4, 6).** The printed value 354224848179261915075 is F₁₀₀ for F₀ = 0, F₁ = 1. Starting 1,1 instead gives 573147844013817084101 at index 100. The deck consistently uses 0,1. Field identities do not establish unrestricted integer claims; the worked recurrence uses a prime greater than its largest value.
2. **Root bound (lecture p. 5; HW3 1(c)).** The relevant theorem is the degree bound on roots of a nonzero polynomial over a field. It is not the usual fundamental theorem of algebra. Z₆ is not a field; 2X² + 4X has roots 0,1,3,4 there.
3. **Plain versus standard model (HW3 1(b)).** No random oracle does not imply no setup. Plain-model NIZKs for all NP languages would imply NP ⊆ BPP under the usual efficient-simulation guarantees. CRS-based NIZKs in the standard model are possible under suitable assumptions. The assignment's “likely false” answer uses the plain-model interpretation.
4. **Schnorr guessing (HW3 2(c)).** The Q/q explanation is for the stated strategy with u,z fixed before a fresh challenge query and h ≠ 1. Count a final unqueried candidate as an additional test if allowed. This informal argument is not a full extraction theorem against arbitrary provers.
5. **Small challenges (HW3 3(a)).** Error 1/2 is interpreted as attainable cheating success, as in the supplied solution. An upper bound alone would not establish an attack.
6. **Parallel soundness (HW3 3(b)).** Do not justify malicious-prover soundness by saying honest copies use independent randomness. For fixed first messages on a false statement, special soundness permits at most one accepting challenge per binary coordinate; count accepting vectors. Independent honest simulations establish HVZK separately.
7. **PCP verification (HW3 4(a)).** The supplied solution omits the PCP local predicate from its final verification step. Checking Merkle openings alone accepts arbitrary honestly committed strings. The deck explicitly requires both authenticated bits and accepted PCP predicates. Add the computational binding failure term to the soundness error.
8. **Communication versus time (HW3 4).** The supplied PCP theorem gives an efficient verifier and constant query count. The O(λ² log n) communication calculation does not alone prove the lecture's stronger input-linear-plus-polylogarithmic verification time.
9. **Roots of unity and degree (lecture p. 9).** Require a primitive root of order N, not merely ωᴺ = 1. N distinct slots determine a unique interpolant of degree less than N. N denotes domain size, separately from later degree bounds on constraint products.
10. **Circuit example (lecture pp. 8–9).** The three-gate example outputs 56, whereas normalized circuit satisfaction is C(x,w) = 0. The deck labels it a computation fragment with public target 56 and explains the final subtraction needed to normalize the relation.
11. **All wire aliases (lecture pp. 9–11).** The private-input slot and its gate occurrence also require a copy constraint. The displayed permutation includes every trace position, with the final-output position fixed.
12. **Fast evaluation (lecture pp. 6, 10–11).** ZΩ = Xᴺ − 1 applies to the full domain of N roots. Arbitrary input/gate subsets require their own formulas or authenticated preprocessing. Precomputing coefficients alone does not make evaluating a large polynomial sublinear.
13. **Compiler scope (lecture pp. 7–11).** Evaluation binding alone is not a full bounded-degree oracle-emulation theorem. The selected PCS and compiler must justify degree-consistent evaluations. Three messages alone do not establish Sigma properties. The notes outline, rather than derive, the full PLONK permutation protocol, zero-knowledge blinding and knowledge extraction; the deck states this scope explicitly.

## Earlier-deck second pass

The original 189-card audit and all existing IDs are retained. Chapter 1/2 and HW1/2 retain their card counts. This pass makes targeted improvements using the teaching guide rather than claiming a fresh derivation of every source theorem:

- Replace envelope, puzzle and city/road framing in prerequisite material with commitments, encryption randomness, proposed keys and graph structure.
- Make the ciphertext-versus-plaintext distinction with two randomized encryptions of the same message in the HW1 solution.
- Prevent “inverse polynomial” from accidentally triggering a modular-inverse glossary before modular arithmetic has been taught.
- Remove first-use glossary entries where the card's main explanation already supplies the full definition, rather than saying it twice.
- Make the simulator/hidden-bit practice question hold the public statement fixed with two valid witnesses and a balanced chosen bit. Its 1/2 baseline otherwise need not follow merely from simulation.
- Explain parallel HVZK using exact distributions only for perfect HVZK; computational HVZK uses a sequence of indistinguishable replacements.
- Remove overlapping parallel-simulation explanations and explain sequential soundness through conditional bounds.
- Distinguish plain-model limitations from CRS-based standard-model NIZKs before Chapter 3 uses that distinction.

The executable audit verifies stable links, prerequisite order and source coverage. Browser checks verify navigation, displayed math, interactions and the two font sizes. These checks complement mathematical review; they cannot prove that an explanation is sufficient for every learner.
