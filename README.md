# PETS

Connected explanations, worked exercises and visual experiments for first-time learners of privacy-enhancing technologies.

## Open the website

- [All PETS decks](https://anujpare.github.io/study_material/)
- [Chapter 1 — Commitment](https://anujpare.github.io/study_material/commitment/)
- [Chapter 2 — Zero Knowledge](https://anujpare.github.io/study_material/zero-knowledge/)
- [Chapter 3 — SNARKs](https://anujpare.github.io/study_material/snarks/)
- [HW1 — exercises and solutions](https://anujpare.github.io/study_material/hw1/)
- [HW2 — exercises and solutions](https://anujpare.github.io/study_material/hw2/)
- [HW3 — exercises and solutions](https://anujpare.github.io/study_material/hw3/)

Links show the version deployed from `main`; additions on a pull request become live after merge and the GitHub Pages deployment.

Start at the beginning of a chapter. The three-line popup switches decks and offers visual shortcuts. The slider follows the learning order; existing `#lesson-N` links still identify their original cards.

| Deck | Cards | Practice |
| --- | ---: | --- |
| Commitment | 95 | Integrated chapter practice and HW1 |
| Zero Knowledge | 73 | Integrated chapter practice and HW2 |
| SNARKs | 48 | 36 teaching cards and all 12 HW3 subquestions |
| HW1 | 33 | 15 homework exercises with prerequisites |
| HW2 | 31 | 13 homework exercises with prerequisites |
| HW3 | 12 | All 12 subquestions, with self-contained worked solutions |

Chapter 3 introduces notation and algebra where needed: Fiat–Shamir and challenge counting, PCPs and authenticated queries, finite fields, interpolation, quotient tests, polynomial commitments, and the PLONK circuit outline. Its homework appears immediately after the relevant preparation. HW3 uses the same exercise source in assignment order and links back to that preparation.

## Learn visually

- Explore growth rates, distinguishing advantage, collision pairs, modular arithmetic and security reductions in Chapter 1.
- Inspect graph challenges, simulator retries and real versus simulated Schnorr transcripts in Chapter 2 and HW2.
- In Chapter 3, change the field to inspect roots, reconstruct an interpolating polynomial, test candidate roots of unity, and trace copies of a circuit wire.
- Change a circuit trace to isolate an incorrect public input, gate operation, wire copy or output. Switch a gate selector and inspect the equation's residual.
- In HW3, check Schnorr responses and count challenge vectors. Solutions start closed so you can attempt the question first.

Static diagrams and pre-rendered mathematical notation remain available without JavaScript. Interactive controls enhance those examples. The interface uses only the standard text size and a box/diagram size exactly 2 pt smaller.

## Teaching and source review

[TEACHING_GUIDE.md](TEACHING_GUIDE.md) is the editable authoring framework. Its five categories cover prerequisites, explanatory coherence, visual representations, practice with feedback, and review. It records learner preferences, research references and a process for incorporating future corrections.

[SOURCE_NOTES.md](SOURCE_NOTES.md) records source coverage, corrections to the supplied lecture/homework, and the second pass on the earlier decks. In particular, it explains the Fibonacci indexing correction, the missing PCP predicate check, and the distinction between plain-model and CRS-based NIZKs.

## Maintain and build

- `scripts/snarks_content.py` supplies Chapter 3; `scripts/hw3_content.py` supplies the shared HW3 questions and solutions.
- `scripts/beginner_content.py`, `scripts/beginner_solutions.py` and `scripts/earlier_review.py` supply prerequisite lessons and editorial revisions for the earlier decks.
- The original chapter HTML remains the source for existing lessons. Generated homework preserves its source-card links.
- `scripts/deck_catalog.py` defines public names and menu links.
- `docs/learning.js`, `docs/homework.js`, `docs/concepts.js` and `docs/snarks.js` implement the interactive examples.
- `docs/typography.css` defines the two text sizes.
- `scripts/beginner-audit.json` and `scripts/snarks-audit.json` record coverage and prerequisite order.

```sh
npm ci
npm run build
```

The build regenerates homework, prerequisite ordering, navigation and new-deck math. MathJax is a pinned **build-time** dependency; the static site has no runtime CDN or math-rendering dependency. Do not edit generated HW3 HTML directly.

## Verify locally

```sh
npx playwright install chromium
python3 -m http.server 8765 --directory docs
# In another terminal:
npm run test:content
npm run test:browser
```

Set `CHROMIUM_PATH` to an installed Chromium executable or `PETS_TEST_URL` to another local server. Checks cover all six decks, stable links, sliders and history, popup menus, no-JavaScript navigation, expanded math, two text sizes, mobile layouts and numerical behavior of the visualizations. Browser automation uses Chromium; physical Safari/iOS device testing is not included.
