# PETS

Connected explanations, worked exercises and visual experiments for undergraduates learning cryptography.

## Open the website

- [All PETS decks](https://anujpare.github.io/study_material/)
- [Chapter 1 — Commitment](https://anujpare.github.io/study_material/commitment/)
- [Chapter 2 — Zero Knowledge](https://anujpare.github.io/study_material/zero-knowledge/)
- [Zero Knowledge · Interactive Learning Lab](https://anujpare.github.io/study_material/zk-workbench/) — pedagogical lessons, message-flow diagrams and worked exercises
- [SNARGs → PLONK · rigorous learning lab](https://anujpare.github.io/study_material/snarg-workbench/) — 36 connected lessons, all HW3 and relevant HW1/HW2, interactive proofs and PLONK trace
- [Chapter 3 — SNARKs](https://anujpare.github.io/study_material/snarks/)
- [Chapter 4 — PIR and midterm review](https://anujpare.github.io/study_material/pir/)
- [Secure MPC · Interactive Learning Lab](https://anujpare.github.io/study_material/mpc-workbench/) — 48 cards, 21 experiments and a question on every card
- [HW6 — secure MPC exercises](https://anujpare.github.io/study_material/hw6/) — all 16 assigned subquestions in assignment order
- [HW1 — exercises and solutions](https://anujpare.github.io/study_material/hw1/)
- [HW2 — exercises and solutions](https://anujpare.github.io/study_material/hw2/)
- [HW3 — exercises and solutions](https://anujpare.github.io/study_material/hw3/)
- [HW4 — exercises and solutions](https://anujpare.github.io/study_material/hw4/)

Links show the version deployed from `main`; additions on a pull request become live after merge and the GitHub Pages deployment.

Start at the beginning of a chapter. The three-line popup switches decks and offers visual shortcuts. The slider follows the learning order; existing card bookmarks lead to the corresponding retained lesson.

| Deck | Cards | Practice |
| --- | ---: | --- |
| Commitment | 58 | Integrated chapter practice and HW1 |
| Zero Knowledge | 46 | Integrated chapter practice and HW2 |
| SNARKs | 48 | 36 teaching cards and all 12 HW3 subquestions |
| PIR | 44 | 27 teaching cards, all 15 HW4 questions and 2 HW3 review questions |
| HW1 | 15 | All exercises, with preparation explained in their worked solutions |
| HW2 | 13 | All exercises, with preparation explained in their worked solutions |
| HW3 | 12 | All 12 subquestions, with self-contained worked solutions |
| HW4 | 15 | All 15 subquestions, with self-contained worked solutions |

Chapter 3 introduces notation and algebra where needed: Fiat–Shamir and challenge counting, PCPs and authenticated queries, finite fields, interpolation, quotient tests, polynomial commitments, and the PLONK circuit outline. Its homework appears immediately after the relevant preparation. HW3 uses the same exercise source in assignment order and links back to that preparation.

Chapter 4 first develops PIR through private selectors, secret sharing, matrix queries, homomorphic encryption, recursion and FHE. A clearly signposted midterm review then builds the polynomial algebra needed by the rest of HW4. HW3 questions 1(a) and 1(c) are reused with their original labels. HW4 follows assignment order and shares its worked solutions with Chapter 4.

The learning path assumes ordinary undergraduate maths. Course-specific concepts—PPT, the security parameter, indistinguishability, prime-order groups, simulation and extraction—receive precise definitions and connected explanations. The eight decks contain 251 cards, down from 352 after removing elementary primers and merging repeated explanations. Old card bookmarks resolve to the corresponding retained lesson.

## Learn visually

- Follow the distinguishing game, commitment exchange, PRF oracle queries and security reductions in Chapter 1. Explore their probability bounds with numerical experiments.
- Inspect graph challenges, simulator retries and real versus simulated Schnorr transcripts in Chapter 2 and HW2.
- In Chapter 3, change the field to inspect roots, reconstruct an interpolating polynomial, test candidate roots of unity, and trace copies of a circuit wire.
- Change a circuit trace to isolate an incorrect public input, gate operation, wire copy or output. Switch a gate selector and inspect the equation's residual.
- In Chapter 4, inspect each server’s query distribution, reconstruct a matrix column, compare upload/download costs, and follow encrypted records through recursive selection.
- In HW4, inspect coefficient shifts, product-polynomial diagonals, encoded setup powers, Boolean equality gates and the noise at each FHE stage.
- In HW3, check Schnorr responses and count challenge vectors. Solutions start closed so you can attempt the question first.

Written explanations are always visible. Protocol diagrams identify both participants, their starting knowledge, each transmitted value and local checks; optional controls highlight steps while keeping the whole conversation visible. Homework diagrams and experiments sit inside the initially closed solutions. Static diagrams and pre-rendered mathematical notation remain available without JavaScript. Interactive controls enhance those examples. The interface uses only the standard text size and a box/diagram size exactly 2 pt smaller.

## Teaching and source review

[TEACHING_GUIDE.md](TEACHING_GUIDE.md) is the editable authoring framework. Its five categories cover prerequisites, explanatory coherence, visual representations, practice with feedback, and review. It records learner preferences, research references and a process for incorporating future corrections.

[SOURCE_NOTES.md](SOURCE_NOTES.md) records syllabus coverage and corrections to the supplied lecture/homework. [TEACHING_REVIEW.md](TEACHING_REVIEW.md) records the current review scope and the reason for the rebuild. In particular, it explains the Fibonacci indexing correction, the missing PCP predicate check, and the distinction between plain-model and CRS-based NIZKs.

## Maintain and build

- `scripts/pir_content.py` supplies Chapter 4; `scripts/hw4_content.py` supplies shared HW4 questions and solutions.
- `scripts/snarks_content.py` supplies Chapter 3; `scripts/hw3_content.py` supplies the shared HW3 questions and solutions.
- `scripts/undergraduate_content.py` supplies the Chapter 1/2 explanations, sequence and bookmark redirects; `scripts/beginner_solutions.py` supplies their worked solutions.
- `scripts/later_teaching.py` applies the undergraduate teaching pass to Chapters 3/4.
- `scripts/teaching_visuals.py` and `scripts/homework_visuals.py` define static protocol diagrams; `docs/teaching.js` adds step highlighting.
- The original chapter HTML remains the source for existing lessons. Generated homework preserves its source-card links.
- `scripts/deck_catalog.py` defines public names and menu links.
- `docs/learning.js`, `docs/homework.js`, `docs/concepts.js`, `docs/snarks.js` and `docs/pir.js` implement the interactive examples.
- `docs/typography.css` defines the two text sizes.
- `scripts/beginner-audit.json`, `scripts/snarks-audit.json` and `scripts/pir-audit.json` record coverage and prerequisite order; `scripts/teaching-audit.json` records the review disposition of every current card.

```sh
npm ci
npm run build
```

The build regenerates homework, prerequisite ordering, navigation and new-deck math. MathJax is a pinned **build-time** dependency; the static site has no runtime CDN or math-rendering dependency. Do not edit generated HW3/HW4 HTML directly.

## Verify locally

```sh
npx playwright install chromium
python3 -m http.server 8765 --directory docs
# In another terminal:
npm run test:content
npm run test:browser
```

Set `CHROMIUM_PATH` to an installed Chromium executable or `PETS_TEST_URL` to another local server. Checks cover all eight decks, stable links, sliders and history, popup menus, no-JavaScript navigation, expanded math, two text sizes, mobile layouts and numerical behavior of the visualizations. Browser automation uses Chromium; physical Safari/iOS device testing is not included.

## Secure MPC interactive learning lab

The [MPC lab](https://anujpare.github.io/study_material/mpc-workbench/) follows lectures 17–19 and the supplied handwritten notes. Its 48 cards develop the real/ideal definition, additive sharing, circuit evaluation, Beaver triples, malicious security, Shamir sharing and threshold BLS. All 16 HW6 subquestions appear after their prerequisites and also in a separate assignment-order HW6 deck, built from the same canonical sources.

Every card asks a bounded application question. Numerical and choice answers receive feedback; written answers stay editable, with an initially concealed worked solution and explicit self-check criteria. The menu offers the complete route, HW6 only, and questions marked for another attempt. Answers, drafts and progress stay in local storage on the current browser. No answers are transmitted to a server.

Twenty-one experiment types show consequences: inspect who holds each share, follow each Beaver broadcast, add a public constant incorrectly, reuse masks, rush an opening, forge a MAC, count communication, vary a Shamir secret while observations remain fixed, reconstruct from different subsets, and combine or reject symbolic signature shares. The experiments use toy values for instruction; they are not cryptographic implementations.

The supplied HS2025 endterm concerns differential privacy. Its subquestion structure informs practice design; the MPC practice is not mislabelled as an actual question from that paper. See [the source map and corrections](docs/mpc-workbench/sources.html).

Authoring sources are `scripts/mpc_core.py`, `scripts/mpc_exercises.py`, and `scripts/mpc_shamir.py`. `scripts/build-mpc.py` generates both readers, the source page and the coverage map. Mathematical notation is rendered during the build, so the new readers need no external math service and retain their full text and static examples without JavaScript. `docs/mpc-workbench/labs.js` supplies both static lab defaults and live behavior.

Run `npm run build` and `npm run test:content`. To check the new browser flows, serve `docs` at port 8765 and run `npm run test:mpc` (set `CHROMIUM_PATH` only when using a system browser). The MPC-specific GitHub Actions workflow checks all cards and expanded solutions, functional experiments, navigation, local progress, small-screen layouts and no-JavaScript content. It retains mobile screenshots as a run artifact. Chromium emulation does not replace testing on a physical iPhone or Safari.
