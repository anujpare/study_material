# PETS

Learn the concepts in order, then work through the exercises with explanations and interactive examples.

## Open the website

- [All PETS decks](https://anujpare.github.io/study_material/)
- [Commitment — Chapter 2](https://anujpare.github.io/study_material/commitment/)
- [Zero Knowledge — Chapter 3](https://anujpare.github.io/study_material/zero-knowledge/)
- [HW1 — exercises and worked solutions](https://anujpare.github.io/study_material/hw1/)
- [HW2 — exercises and worked solutions](https://anujpare.github.io/study_material/hw2/)

Start at the first card of a deck. The three-line menu also has **Start from the basics** and shortcuts to visual lessons. Homework remains integrated in the chapters as well as available separately.

## Beginner learning order

Every deck introduces notation, powers, bits and probability before using them. Further prerequisites appear where needed: running time, commitments and extra randomizers, random oracles, modular arithmetic, groups, graphs, DDH, two-input linear maps, and circuits.

All 189 original cards have been reviewed for prerequisite terminology. New terms are explained at their first use in each deck, without adding repeated summaries and glossaries to every card. All 28 homework solutions have been rewritten as reasoned steps, with concrete examples where helpful. The informal circuit-simulation argument explicitly identifies the extra assumption it needs.

| Deck | Total cards | Included exercises |
| --- | ---: | ---: |
| Commitment | 95 | Integrated chapter practice and HW1 |
| Zero Knowledge | 73 | Integrated chapter practice and HW2 |
| HW1 | 33 | 15 homework exercises |
| HW2 | 31 | 13 homework exercises |

The totals include 43 new prerequisite cards across the four decks. Existing `#lesson-N` links still identify their original cards. The slider shows position in the learning sequence, which can differ from that stable lesson ID. The original SVG math, card controls and interactive experiments remain available; examples with tiny cryptographic parameters are explicitly for learning.

## Explore difficult ideas

Selected cards offer **Explore visually** and **Read explanation** views of the same lesson. This keeps the deck lengths unchanged and avoids stacking another explanation onto the page. Without JavaScript, the original written lesson appears normally.

- Plot polynomial and exponential growth, then compare negligible functions against increasingly strict thresholds.
- Choose an observer’s test and see its distinguishing advantage as selected tickets in two distributions.
- Count query pairs to understand the birthday bound; follow a double opening through the steps of a security reduction.
- Inspect a simulator’s successful and discarded attempts. In HW2, switch between a real Schnorr proof and its simulator while keeping the recorded conversation unchanged.
- In HW1, tap DDH output pairs to inspect their inputs, and rebuild a Merkle root one sibling hash at a time.

The chapter popup includes shortcuts to these visual lessons. All labels, controls and diagrams follow the same two text sizes as the rest of PETS.

## Maintain the material

- `docs/commitment/index.html` and `docs/zero-knowledge/index.html` hold the chapter material.
- `scripts/beginner_content.py` holds the prerequisite lessons, editorial learning aims and definitions.
- `scripts/beginner_solutions.py` holds the beginner worked solutions.
- `scripts/build-homework.py` supplies homework selection, exercise guides and checkpoints.
- `docs/learning.js`, `docs/homework.js` and `docs/concepts.js` supply the interactive examples and alternate visual views.
- `docs/typography.css` defines the two text sizes: the original enlarged card-body size, and exactly 2 pt smaller for boxes and diagrams. Headings use weight, not a larger size.

After editing the chapter material or editorial sources, run:

```sh
python3 scripts/revise-beginner.py
```

This applies the explanations, regenerates both homework decks, inserts prerequisites, rebuilds previous/next links, and refreshes menus and counts. `scripts/beginner-audit.json` records coverage for each original card. Run the complete pipeline rather than the core homework generator alone.

## Browser checks

The site is static HTML/CSS/JavaScript, served from `docs/` by GitHub Pages. It does not need a network math renderer.

```sh
npm install --no-save playwright
npx playwright install chromium
python3 -m http.server 8765 --directory docs
# In another terminal:
python3 tests/beginner_content.py
node tests/reader.cjs
node tests/learning.cjs
node tests/homework.cjs
node tests/typography.cjs
node tests/concepts.cjs
```

Set `CHROMIUM_PATH` to use an installed Chromium executable, or `PETS_TEST_URL` to use a different server. Checks cover prerequisite ordering, all cards and expanded formulas, stable deep links, mouse/touch/keyboard navigation, popup behavior, homework feedback, numerical experiments, mobile layouts and navigation without JavaScript. Browser coverage is Chromium; physical Safari/iOS device testing is not included.
