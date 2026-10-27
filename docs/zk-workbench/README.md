# PETS — ZK Learning Lab

**Canonical URL:** https://anujpare.github.io/study_material/zk-workbench/
**Repository:** anujpare/study_material
**Landing page:** docs/index.html
**Publication:** GitHub Pages (same URL after every update).

This is the user's **single canonical persistent tutorial**, not a throwaway prototype. The tutorial contains **21 connected lessons**. It is independent of, and does not overwrite, the pre-existing Zero Knowledge chapter deck.

## Structure
- docs/zk-workbench/index.html — permanent page/viewer and fixed navigation.
- docs/zk-workbench/style.css — color semantics, mobile/desktop typography and layout. Main prose is 20–23px, never tiny.
- docs/zk-workbench/app.js — card manifest, arrows/selector, visual proof experiments, math engine.
- docs/zk-workbench/card-01.html through card-21.html — ONE source file per lesson, in fixed sequential order. Each article contains its own complete teaching prose, equations, and lab markup.
- MathJax renders LaTeX dynamically after the selected card loads. Check LaTeX rendering after each structural change.

## Learning order
1. Evidence and witnesses; 2. NP; 3. interactive proofs; 4. completeness/soundness; 5. ZK definition; 6. commitments; 7. permutation and graph; 8. challenges; 9. Hamiltonicity proofs; 10. simulator construction; 11. simulator correctness/efficiency; 12. sequential versus parallel message rules; 13. simulation cost; 14. Homework 2 Problem 2; 15. proof of knowledge; 16. Sigma protocols; 17. Schnorr/completeness; 18. Schnorr HVZK; 19. Schnorr extraction; 20. circuit satisfiability; 21. Fiat–Shamir NIZK.

## Source material
User-provided PETS lectures 5–8, pp. 1–11, and Homework 2 with solutions, Problems 1–4. The teaching follows these statements and notation, with added undergraduate-level prerequisites and all necessary inferential links. As a stylistic reference, Andrew Ng/Tengyu Ma's CS229 notes motivate concepts from a question, establish notation before using it, develop mathematical proofs in steps, and use figures to demonstrate a claim. The public tutorial uses only PETS branding.

## Immutable editing contract
1. Read the requested card **and its neighbors** from GitHub before editing. This URL and folder are authoritative. Edit these source files IN PLACE. No new standalone tutorial, alternative page, or chat-only replacement.
2. If the user asks to rewrite card N, update **card-NN.html only** unless a specific interaction requires updating app.js or CSS. Do not change neighboring cards, navigation, naming, or chapter index without explicit reason.
3. Set up the exact learning question before its theory. Define new symbols before introducing equations. For every proof, state what must be shown, justify each implication and finish the promised result. Do not offer related facts as if they proved the claim.
4. Enforce claim–evidence alignment. Each graph, slider or interactive panel must explain a precisely named conceptual/mathematical difficulty and dynamically demonstrate that claim. No decorative diagrams.
5. Maintain color distinctions: green/teal prover and valid evidence, blue verifier, purple simulator, amber cautions, red impossible/invalid. Labels must carry meaning beyond color. Never use tiny explanatory text.
6. Mathematics: use LaTeX through MathJax, consistent notation with the lecture, bold matrices/vectors; scalar variables not bold; no unexplained symbols. Verify rendering and mobile overflow.
7. State each homework question before the worked solution, and make each intermediate argument explicit. Distinguish an illustrative numerical example from a general proof. Flag missing assumptions rather than claiming a proof.
8. Test the changed file, relevant interactions and navigation; read back from the repository. Only report publication/rendering success after independently verifying it. A successful push is not proof that GitHub Pages deployment is live.
9. Preserve all unrelated original chapter decks and the original PETS landing page apart from the one Learning Lab entry.

## Test coverage
- Connector write/read and targeted in-place updates confirmed (2026-10-27).
- All 21 lesson files exist and HTML articles/details are structurally balanced.
- JS syntax parsed, and mocked browser tests verified graph witness checker; Hamiltonicity opening matrices; simulator mismatch; sequential schedule; Schnorr arithmetic, simulator and extraction.
- **Full live browser rendering has not been independently verified from this tool environment**. Check the deployed site on desktop and iPhone, MathJax loading and responsive layout before claiming final visual QA.
