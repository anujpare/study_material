# ZK Learning Lab — Homework Coverage Audit

Canonical tutorial: https://anujpare.github.io/study_material/zk-workbench/

This is the permanent one-tutorial coverage map, prepared 2026-10-28. **The 31 navigable lessons cover every subpart of Homework 2 and Homework 3**, including explicitly marked next-chapter HW3 exercises. From Homework 1, all commitment problems needed for the ZK and adjacent Merkle/PCP constructions are included; unrelated FHE and PRF-reduction tasks remain in the separate original HW1 deck rather than interrupting the ZK teaching sequence.

## Homework 1 — FS2026 v1.2

| Part | Subject | Tutorial coverage |
|---|---|---|
| 1(a) | ROM hash commitment | [Commitment security](https://anujpare.github.io/study_material/zk-workbench/#hw1-security) |
| 1(b) | P=NP and PRFs | Not required for ZK; PRF hardness; original HW1 deck |
| 1(c) | FHE evaluation | Not required for ZK; homomorphic encryption; original HW1 deck |
| 1(d) | ROM versus SHA-3 | [Commitment security](https://anujpare.github.io/study_material/zk-workbench/#hw1-security) |
| 2(a) | Hash-power commitment: hiding and binding | [Commitment security](https://anujpare.github.io/study_material/zk-workbench/#hw1-security) |
| 2(b) | XOR commitment: perfect hiding, no binding | [Commitment security](https://anujpare.github.io/study_material/zk-workbench/#hw1-security) |
| 2(c) | Pedersen with known discrete-log relation | [Pedersen lab](https://anujpare.github.io/study_material/zk-workbench/#hw1-pedersen) |
| 2(d) | ElGamal-style pair with known relation | [Pedersen lab](https://anujpare.github.io/study_material/zk-workbench/#hw1-pedersen) |
| 3(a–d) | DDH/PRF reduction | Not required for ZK lecture: independent PRF reduction topic; original HW1 deck |
| 4(a) | Large vector commitment; empty proof | [Vector commitments](https://anujpare.github.io/study_material/zk-workbench/#hw1-vector) |
| 4(b) | One hash; full-vector opening | [Vector commitments](https://anujpare.github.io/study_material/zk-workbench/#hw1-vector) |
| 4(c) | Merkle root and log-size opening | [Merkle path diagram](https://anujpare.github.io/study_material/zk-workbench/#hw1-vector) |

## Homework 2 — FS2025 v1

| Part | Subject | Tutorial coverage |
|---|---|---|
| 1(a) | P=NP gives empty ZK | [ZK definition](https://anujpare.github.io/study_material/zk-workbench/#zk) |
| 1(b)(i) | Malicious verifier may reject | [Completeness/soundness](https://anujpare.github.io/study_material/zk-workbench/#guarantees) |
| 1(b)(ii) | Malicious prover may reveal witness | [Completeness/soundness](https://anujpare.github.io/study_material/zk-workbench/#guarantees) |
| 1(c) | Empty NIZK for P languages | [ZK definition](https://anujpare.github.io/study_material/zk-workbench/#zk) |
| 2(a) | Sequential simulator | [Composition worked proof](https://anujpare.github.io/study_material/zk-workbench/#homework2) |
| 2(b) | Parallel malicious-verifier challenge | [Composition worked proof](https://anujpare.github.io/study_material/zk-workbench/#homework2) |
| 2(c) | Parallel honest-verifier ZK | [Composition worked proof](https://anujpare.github.io/study_material/zk-workbench/#homework2) |
| 3(a) | Schnorr completeness | [Schnorr](https://anujpare.github.io/study_material/zk-workbench/#schnorr) |
| 3(b) | Schnorr HVZK | [Schnorr simulator](https://anujpare.github.io/study_material/zk-workbench/#schnorr-zk) |
| 3(c) | Schnorr extractor | [Schnorr extractor](https://anujpare.github.io/study_material/zk-workbench/#schnorr-ext) |
| 4(a) | Circuit Sigma protocol | [Circuit construction](https://anujpare.github.io/study_material/zk-workbench/#circuits) |
| 4(b) | Circuit soundness | [Circuit proof](https://anujpare.github.io/study_material/zk-workbench/#circuits) |
| 4(c) | Circuit simulation and its missing assumption | [Circuit analysis](https://anujpare.github.io/study_material/zk-workbench/#circuits) |

## Homework 3 — existing published HW3 deck

| Part | Subject | Tutorial coverage |
|---|---|---|
| 1(a) | Knowledge error implies soundness | [PoK](https://anujpare.github.io/study_material/zk-workbench/#knowledge) |
| 1(b) | Plain model/CRS qualification | [NIZK](https://anujpare.github.io/study_material/zk-workbench/#fiat-shamir) |
| 1(c) | Polynomial root bound modulo 6 | [Optional SNARK prerequisite](https://anujpare.github.io/study_material/zk-workbench/#hw3-roots) |
| 1(d) | FS does not upgrade to statistical ZK | [NIZK](https://anujpare.github.io/study_material/zk-workbench/#fiat-shamir) |
| 2(a) | Noninteractive Schnorr proof | [FS–Schnorr](https://anujpare.github.io/study_material/zk-workbench/#hw3-fs-schnorr) |
| 2(b) | Public Schnorr verifier | [FS–Schnorr](https://anujpare.github.io/study_material/zk-workbench/#hw3-fs-schnorr) |
| 2(c) | Q/q restricted guessing bound | [Guessing lab](https://anujpare.github.io/study_material/zk-workbench/#hw3-fs-attacks) |
| 2(d) | Transferable NIZKs vs simulator-generated transcripts | [Proof transfer](https://anujpare.github.io/study_material/zk-workbench/#hw3-fs-attacks) |
| 3(a) | One-bit FS non-negligible soundness | [Amplification](https://anujpare.github.io/study_material/zk-workbench/#hw3-amplify) |
| 3(b) | Parallel amplification then FS | [Amplification](https://anujpare.github.io/study_material/zk-workbench/#hw3-amplify) |
| 4(a) | PCP + Merkle → succinct interactive argument | [Optional PCP bridge](https://anujpare.github.io/study_material/zk-workbench/#hw3-pcp) |
| 4(b) | FS removes PCP challenge | [Optional PCP bridge](https://anujpare.github.io/study_material/zk-workbench/#hw3-pcp) |

## Lecture 5–8 coverage

| Pages | Concepts | Anchors |
|---|---|---|
| 1–2 | Witnesses and NP, interactive proofs, IP=PSPACE, completeness/soundness | [Witnesses](https://anujpare.github.io/study_material/zk-workbench/#witness); [NP](https://anujpare.github.io/study_material/zk-workbench/#np); [IP/PSPACE](https://anujpare.github.io/study_material/zk-workbench/#lecture-power); [Interaction](https://anujpare.github.io/study_material/zk-workbench/#interaction); [Security](https://anujpare.github.io/study_material/zk-workbench/#guarantees) |
| 3–5 | Applications, verifier views, ZK and simulation | [Applications](https://anujpare.github.io/study_material/zk-workbench/#lecture-applications); [ZK definition](https://anujpare.github.io/study_material/zk-workbench/#zk) |
| 5–7 | Commitments, Hamiltonicity, soundness, simulator, repetition | [Commitments](https://anujpare.github.io/study_material/zk-workbench/#commitments); [Hamiltonicity](https://anujpare.github.io/study_material/zk-workbench/#permutation); [Protocol](https://anujpare.github.io/study_material/zk-workbench/#ham-protocol); [Proof](https://anujpare.github.io/study_material/zk-workbench/#ham-proof); [Simulator](https://anujpare.github.io/study_material/zk-workbench/#simulation); [Simulation analysis](https://anujpare.github.io/study_material/zk-workbench/#zk-proof); [Composition](https://anujpare.github.io/study_material/zk-workbench/#repetition); [Cost](https://anujpare.github.io/study_material/zk-workbench/#cost) |
| 7–8 | Proof of knowledge, extractor, rewinding | [Knowledge](https://anujpare.github.io/study_material/zk-workbench/#knowledge) |
| 8–9 | Sigma protocols, special soundness, HVZK, Schnorr | [Sigma](https://anujpare.github.io/study_material/zk-workbench/#sigma); [Schnorr](https://anujpare.github.io/study_material/zk-workbench/#schnorr); [HVZK](https://anujpare.github.io/study_material/zk-workbench/#schnorr-zk); [Extraction](https://anujpare.github.io/study_material/zk-workbench/#schnorr-ext) |
| 10–11 | NIZK, plain-model limits, Fiat–Shamir and ROM | [Fiat–Shamir](https://anujpare.github.io/study_material/zk-workbench/#fiat-shamir); [HW3 FS](https://anujpare.github.io/study_material/zk-workbench/#hw3-fs-schnorr); [Attack bounds](https://anujpare.github.io/study_material/zk-workbench/#hw3-fs-attacks); [Amplification](https://anujpare.github.io/study_material/zk-workbench/#hw3-amplify) |

## Important mathematical distinctions checked

- A hash commitment proven binding in the random-oracle model is not automatically perfectly binding against an unbounded prover.
- Hamiltonicity perfect completeness, soundness and zero knowledge are three separate proof obligations. The simulation analysis distinguishes honest and malicious verifier challenges.
- The exponential cost of the naive parallel guess-and-rewind simulator is not an impossibility theorem for all possible simulators.
- HW2 4(b) requires negligible underlying gate soundness (or proper amplification) for negligible combined soundness.
- HW2 4(c) uses a simulator on potentially false gate commitment statements, which plain Sigma HVZK does not guarantee. The extra property needed for the informal homework construction is spelled out.
- The Q/q Fiat–Shamir attack bound is for the prescribed restricted strategy, with a nonidentity public h and distinct oracle queries.
- Optional HW3 PCP/root-bound cards are explicitly marked as SNARK-chapter overlap, not prerequisites for core Lecture 5–8.

## Source provenance and maintenance

Homework 1 FS2026 v1.2 and Homework 2 FS2025 v1 were reviewed directly from the PDFs. Homework 3 was mapped against the existing published GitHub HW3 deck, which contains all 12 subpart cards. **The original HW3 PDF was not found in the accessible file library**, so the HW3 phrasing is not independently verified against an original PDF.

Individual lesson file names and display card numbers differ because additional lessons were inserted without renaming existing files. Always resolve a visible card using the stable ID/file mapping in app.js before applying an edit. Preserve the canonical URL and unrelated chapter decks.
