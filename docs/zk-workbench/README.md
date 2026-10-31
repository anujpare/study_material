# Zero Knowledge Learning Lab — Canonical Editable Tutorial

**Permanent URL:** https://anujpare.github.io/study_material/zk-workbench/
**GitHub repo:** anujpare/study_material
**Landing page:** docs/index.html
**Content coverage:** 35 integrated navigable lessons. Full PETS Zero Knowledge Lecture 5–8, all HW2 subquestions, all HW3 subquestions (including optional next-chapter overlap), plus relevant HW1 commitment and Merkle prerequisites.

See [HOMEWORK_COVERAGE.md](HOMEWORK_COVERAGE.md) for a subpart-by-subpart audit, exclusions and source provenance.

## Architecture (do not regenerate the website)

- index.html: stable single-page viewer, lesson selector and next/previous arrow navigation.
- app.js: **authoritative lesson manifest** with stable fragment IDs, each mapped explicitly to one file. Also contains interactive teaching demonstrations and navigation state.
- style.css: readable 20–23px lesson prose, ≥18px supporting labels, semantic role colors (teal prover, blue verifier, purple simulator, amber cautions, red failure). Mobile diagrams may horizontally scroll to preserve readable labels.
- card-01.html…card-21.html: the original 21 source lessons, now improved.
- lecture-power.html, lecture-applications.html: material missing from the first version of the lecture syllabus.
- hw1-security.html, hw1-pedersen.html, hw1-vector.html: relevant HW1 commitment problems, including a fully interactive Pedersen counterexample and Merkle authentication path.
- hw3-fs-schnorr.html, hw3-fs-attacks.html, hw3-amplify.html: all directly applicable HW3 Fiat–Shamir, Schnorr, proof-transference and soundness amplification exercises.
- hw3-pcp.html, hw3-roots.html: explicitly optional next-chapter SNARK exercises, included for complete HW3 coverage without interrupting the core ZK argument.
- HOMEWORK_COVERAGE.md: audit and stable reference map.

### Mathematical content requirements

1. Teach from the learner's first principles. Introduce each difficult question and its purpose before definitions. Explain notation at first use, define the proof objective, and show every intermediate inferential step rather than relying on an unstated implication.
2. Be concise through **precision**, not omission. Once an idea is properly explained, do not needlessly repeat it in later cards. Bridge new cards by showing exactly which unresolved question they answer.
3. Every figure or interaction must demonstrate one named mathematical claim. Distinguish an example from a general proof; an example may test a proof's predictions but never replace its derivation.
4. Math is LaTeX through MathJax: scalar variables non-bold, vector/matrix bold, source notation maintained. Keep all labels readable on mobile, allowing horizontal scrolling rather than shrinking complicated diagrams.
5. Present each homework statement before its full worked solution. Do not claim a derivation is complete when the assumptions in the course notes do not suffice. Call out such assumptions, especially the HW2 circuit simulator and gate error.
6. Avoid untested extrapolations: naive parallel simulator inefficiency is not a universal lower bound; the Fiat–Shamir restricted Q/q bound is not a full ROM security theorem; concrete SHA-3 is not the random oracle.

### Persistence and revision contract

**The deployed GitHub URL is the tutorial. Chat is only the editing interface.** When the learner asks to correct a card:

1. Read the present card and its neighbors from GitHub, plus its relevant lecture/homework source. Use the manifest in app.js to resolve visible card position or URL fragment to the actual filename; **visual positions no longer equal numeric file suffixes** because exercises were inserted.
2. Patch only that existing file; update app.js/style.css only if required for the requested interactive or layout change. Never create a disconnected replacement site, new chat-only lesson, or additional unrelated pages.
3. Preserve stable fragment IDs, selector, arrows, and the user's existing landing page. Verify math delimiters, diagrams, interactions, and mobile readability.
4. Read back changes from GitHub and confirm no unrelated cards changed. Report the same permanent URL. Do not claim GitHub Pages is deployed/rendered unless independently verified.

### Sources

- PETS FS2026 Lecture 5–8, user-provided PDF.
- Homework 1 FS2026 v1.2 PDF, directly inspected.
- Homework 2 FS2025 v1 PDF, directly inspected.
- Homework 3 subparts from the already-published HW3 GitHub deck. Original HW3 PDF was not available in the accessible file library for independent verbatim checking.
- The original pre-existing commitment/ZK/SNARKs/PIR decks and separate homework decks remain untouched.

### Audit status (2026-10-28)

GitHub connector writes and readbacks succeeded. All 31 manifest lesson files were inspected for source presence, balanced article/details/paragraph tags, balanced inline/display LaTeX delimiters, and duplicate element IDs; no problems were detected. JavaScript syntax parsed successfully. Mocked interaction tests verified the witness checker, Hamiltonicity opening matrix and four soundness challenge cases, fixed first-message behavior, sequential scheduling, simulator mismatch, Schnorr verification/simulation/extraction, Pedersen double openings, Merkle authentication paths, IP/PSPACE counter, and Fiat–Shamir probability calculations. These are source/logic tests, not an actual screen rendering. Independently verified live browser rendering of the latest GitHub Pages deployment remains outstanding; do not claim visual QA is complete.


### Rebuild in progress (2026-10-31)
The guided reading order begins with the lecture's statements, witnesses and interactive proofs, before Hamiltonicity. The navigation counts, participant diagrams and repetition schedule are corrected. Homework and stable lesson IDs are retained. This entry records changes actually committed; full browser and pedagogy verification remain separate.
