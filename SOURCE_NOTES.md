# PETS source notes and corrections

Chapter 3 is based on **lecture9-10-11-12_snarks.pdf** (12 pages). Its exercises and the standalone HW3 deck use **hw3_sol.pdf**, Exercise Sheet 3 version 1.1 (5 pages). Document instructions such as “write at most one sentence” describe the assignment's submission format; they do not override the requested step-by-step teaching format.

The site numbers its chapters 1: Commitment, 2: Zero Knowledge, 3: SNARKs, 4: PIR. Existing Commitment and Zero Knowledge URLs and lesson IDs remain valid. The labels do not renumber the original course lectures.

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

## Chapter 4: PIR and the HW4 midterm bridge

Sources are **lecture13-14_pir.pdf** (8 pages, lecture header FS2026) and **hw4_sol.pdf** (5 pages, Exercise Sheet 4 version 1, header FS2025). The differing course-year headers are retained as source facts; they are not used to infer an exam syllabus beyond the supplied material.

Chapter 4 contains **28 teaching cards and 17 assigned subquestions**: all 15 HW4 questions, plus HW3 1(a) and 1(c). The first part develops PIR; the second is explicitly labelled as a midterm bridge back to polynomial proofs and commitments, since ten HW4 questions concern those earlier topics. HW4 is a separate 15-card deck in assignment order. Both decks use the same HW4 source, and the two HW3 reviews reuse the existing canonical question and solution. `scripts/pir-audit.json` records card order, prerequisites and source pages.

| Source | Teaching path and exercise placement |
| --- | --- |
| PIR pp. 1–3 | Goal, indexed retrieval, correctness/privacy distinction, cost model |
| PIR pp. 3–5 | Bit arithmetic, secret shares, flat and matrix protocols, correctness, privacy, communication balance → HW4 1(c) |
| PIR pp. 5–6 | Randomized encryption, LHE operations, encrypted matrix selector → HW4 1(b) |
| PIR pp. 6–7 | Recursive selection, ciphertext encodings, expansion, limits of direct two-server reuse |
| HW4 pp. 4–5 | Binary addresses and Boolean gates → 4(a); FHE lookup → 4(b); gate noise and powers → 4(c) |
| PIR pp. 7–8 | Server work, batching, offline/online preprocessing and scope of cited results |
| HW3 1(c); HW4 pp. 1–3 | Field/root-bound review → HW3 1(c); coefficient shifts → HW4 2(a); coefficient split → 2(b); product coefficient → 2(c) |
| HW3 1(a); HW4 p. 1 | Proof guarantees and oracle models → HW3 1(a), HW4 1(a); succinct verifier cost → HW4 1(d) |
| HW4 pp. 3–4 | Groups and encoded setup powers → 3(a–b); quotient/remainder → 3(c); product-check interface → 3(d–e) |

### Clarifications needed for a sound beginner derivation

1. **Malicious servers versus correctness.** Non-collusion protects query privacy in the displayed two-server protocol; it does not stop a malicious server from returning a wrong answer. Correctness uses honest answering. Ordinary PIR also does not guarantee database privacy from the client, anonymity, or concealment of timing.
2. **Reconstruction keeps client state.** The matrix client retains its row index; the encrypted client retains its secret key. The terse algorithm signatures should not imply that this information is unnecessary.
3. **Dimensions and cost units.** For an R×C matrix, two-server communication is exactly 2C+2R bits for the basic scheme. Nonsquare databases can be padded. Single-server communication counts ciphertexts first, then multiplies by their lengths; O(λ√n) uses the lecture's ciphertext-size simplification. Setup/evaluation material must be accounted for separately when reused.
4. **Homomorphism is a decryption relation.** The lecture's Enc(m₁)+Enc(m₂)=Enc(m₁+m₂) shorthand does not promise byte-for-byte equality to a fresh randomized encryption. Distinguish encrypted addition, multiplication by a known scalar, and multiplication of hidden plaintexts.
5. **Recursive PIR.** Intermediate ciphertext encodings become plaintext data for the outer selection, possibly in suitable blocks. This does not grant LHE arbitrary multiplication of hidden plaintexts. Counting O(n^(1/3)) objects alone omits their lengths; the cited polylogarithmic construction needs a suitable low-expansion scheme and recursive encoding. The expansion chart is an illustrative size model, not an implementation benchmark.
6. **Two-server recursion.** The naive recursion loses the replicated-database precondition because the intermediate answers are different shares. This is not a general impossibility result for all recursive or more efficient multi-server PIR.
7. **Online-work intuition.** The raw-database scan argument does not rule out preprocessing models. Batching and preprocessing results cited in the notes are separate constructions with their own assumptions; they are not performance guarantees for the simple examples on these cards.
8. **HW4 1(d).** P = NP supplies a polynomial-time decider and hence an empty proof, but does not by itself supply the lecture's nearly linear-plus-polylogarithmic verification bound. The supplied solution's “unlikely” is not an unconditional impossibility theorem. The deck states the intended negative inference and distinguishes a definition requiring only short communication.
9. **HW4 2(a–c).** Fix polynomials before the relevant random challenge, and enforce all degree bounds. At coefficient endpoints, an empty side is the zero polynomial. In 2(c), use z consistently for the claimed inner product; the sheet switches to “a” once. The 4d/|F| union bound is conservative, and probabilities are capped at 1.
10. **HW4 3(b).** For d≥1, an unbounded attacker can recover α and produce f′=f+t(X−α). For d=0, constants have an injective encoding. Computational binding needs the appropriate PCS hardness assumptions: the existence of collisions, unknown α, or a bare assertion of small collision-finding probability is not a security proof. No hiding claim is implied.
11. **HW4 3(d).** The stated VerifProd interface restricts exponents to nonzero field values, but legitimate openings can have zero exponents. Handle identity-element cases before calling the nonzero interface. The setup α precedes the adversary's choices and is exposed through encoded powers; a fresh-challenge root-bound proof cannot simply be applied to it. Negligible evaluation-binding error needs the intended PCS theorem and assumptions.
12. **HW4 3(e).** c/g^y′ is a group element g^x, not the exponent x. Apply the assumed exponent-division algorithm to that element without taking a discrete logarithm. Division requires z≠α. A forged group element need not represent a genuine quotient polynomial to satisfy the verifier under this extra capability.
13. **HW4 4(a–b).** Use m for the equality-string length and n for database size. Encode record i by i−1 in ℓ=ceil(log₂ n) bits, avoiding the off-by-one problem when n is a power of two. The secret-key construction supplies encrypted constants; compactness and correct evaluation for the circuit are required. One response ciphertext does not mean one server operation.
14. **HW4 4(c).** The exact stated-circuit noise is 2n·8^ceil(log₂ n); it is 2n⁴ when n is a power of two. The result uses the full equality circuit with encrypted constants and the sheet's stipulated gate rules. Other optimizations or schemes need a separate calculation; no decryption threshold is specified.
