# PETS

Connected explanations, worked exercises and visual experiments for first-time learners of privacy-enhancing technologies.

## Open the website

- [All PETS decks](https://anujpare.github.io/study_material/)
- [Chapter 1 — Commitment](https://anujpare.github.io/study_material/commitment/)
- [Chapter 2 — Zero Knowledge](https://anujpare.github.io/study_material/zero-knowledge/)
- [Chapter 3 — SNARKs](https://anujpare.github.io/study_material/snarks/)
- [Chapter 4 — PIR and midterm review](https://anujpare.github.io/study_material/pir/)
- [HW1 — exercises and solutions](https://anujpare.github.io/study_material/hw1/)
- [HW2 — exercises and solutions](https://anujpare.github.io/study_material/hw2/)
- [HW3 — exercises and solutions](https://anujpare.github.io/study_material/hw3/)
- [HW4 — exercises and solutions](https://anujpare.github.io/study_material/hw4/)

Links show the version deployed from `main`; additions on a pull request become live after merge and the GitHub Pages deployment.

Start at the beginning of a chapter. The three-line popup switches decks and offers visual shortcuts. The slider follows the learning order; existing `#lesson-N` links still identify their original cards.

| Deck | Cards | Practice |
| --- | ---: | --- |
| Commitment | 95 | Integrated chapter practice and HW1 |
| Zero Knowledge | 73 | Integrated chapter practice and HW2 |
| SNARKs | 48 | 36 teaching cards and all 12 HW3 subquestions |
| PIR | 45 | 28 teaching cards, all 15 HW4 questions and 2 HW3 review questions |
| HW1 | 33 | 15 homework exercises with prerequisites |
| HW2 | 31 | 13 homework exercises with prerequisites |
| HW3 | 12 | All 12 subquestions, with self-contained worked solutions |
| HW4 | 15 | All 15 subquestions, with self-contained worked solutions |

Chapter 3 introduces notation and algebra where needed: Fiat–Shamir and challenge counting, PCPs and authenticated queries, finite fields, interpolation, quotient tests, polynomial commitments, and the PLONK circuit outline. Its homework appears immediately after the relevant preparation. HW3 uses the same exercise source in assignment order and links back to that preparation.

Chapter 4 first develops PIR through bit arithmetic, secret sharing, matrix queries, homomorphic encryption, recursion and FHE. A clearly signposted midterm review then builds the polynomial algebra needed by the rest of HW4. HW3 questions 1(a) and 1(c) are reused with their original labels. HW4 follows assignment order and shares its worked solutions with Chapter 4.

## Learn visually

- Explore growth rates, distinguishing advantage, collision pairs, modular arithmetic and security reductions in Chapter 1.
- Inspect graph challenges, simulator retries and real versus simulated Schnorr transcripts in Chapter 2 and HW2.
- In Chapter 3, change the field to inspect roots, reconstruct an interpolating polynomial, test candidate roots of unity, and trace copies of a circuit wire.
- Change a circuit trace to isolate an incorrect public input, gate operation, wire copy or output. Switch a gate selector and inspect the equation's residual.
- In Chapter 4, inspect each server’s query distribution, reconstruct a matrix column, compare upload/download costs, and follow encrypted records through recursive selection.
- In HW4, inspect coefficient shifts, product-polynomial diagonals, encoded setup powers, Boolean equality gates and the noise at each FHE stage.
- In HW3, check Schnorr responses and count challenge vectors. Solutions start closed so you can attempt the question first.

Static diagrams and pre-rendered mathematical notation remain available without JavaScript. Interactive controls enhance those examples. The interface uses only the standard text size and a box/diagram size exactly 2 pt smaller.

## Teaching and source review

[TEACHING_GUIDE.md](TEACHING_GUIDE.md) is the editable authoring framework. Its five categories cover prerequisites, explanatory coherence, visual representations, practice with feedback, and review. It records learner preferences, research references and a process for incorporating future corrections.

[SOURCE_NOTES.md](SOURCE_NOTES.md) records source coverage, corrections to the supplied lecture/homework, and the second pass on the earlier decks. In particular, it explains the Fibonacci indexing correction, the missing PCP predicate check, and the distinction between plain-model and CRS-based NIZKs.

## Maintain and build

- `scripts/pir_content.py` supplies Chapter 4; `scripts/hw4_content.py` supplies shared HW4 questions and solutions.
- `scripts/snarks_content.py` supplies Chapter 3; `scripts/hw3_content.py` supplies the shared HW3 questions and solutions.
- `scripts/beginner_content.py`, `scripts/beginner_solutions.py` and `scripts/earlier_review.py` supply prerequisite lessons and editorial revisions for the earlier decks.
- The original chapter HTML remains the source for existing lessons. Generated homework preserves its source-card links.
- `scripts/deck_catalog.py` defines public names and menu links.
- `docs/learning.js`, `docs/homework.js`, `docs/concepts.js`, `docs/snarks.js` and `docs/pir.js` implement the interactive examples.
- `docs/typography.css` defines the two text sizes.
- `scripts/beginner-audit.json`, `scripts/snarks-audit.json` and `scripts/pir-audit.json` record coverage and prerequisite order.

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
