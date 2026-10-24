# study_material

Interactive PETS study decks.

## Published structure

- `docs/index.html` — landing page with chapter selection
- `docs/commitment/index.html` — Chapter 2 deck
- `docs/zero-knowledge/index.html` — Chapter 3 deck
- `docs/hw1/index.html` — standalone HW1 exercises and prerequisites
- `docs/hw2/index.html` — standalone HW2 exercises and prerequisites

## Notes

- The site uses plain static HTML and works with GitHub Pages.
- The original single PETS deck has been split into two chapter-specific decks.
- Homework was placed with the deck where it fits best topically.

## Reader and browser checks

Both decks load `docs/reader.js`. The reader derives slider bounds from the
chapter's cards, synchronizes the URL and counter, and preserves the SVG math.
Previous/next links also work when JavaScript is unavailable.

To run the browser regression checks (Node.js and Python 3 required):

```sh
npm install --no-save playwright
npx playwright install chromium
python3 -m http.server 8765 --directory docs
# In another terminal:
node tests/reader.cjs
```

Set `CHROMIUM_PATH` to use an existing Chromium executable, or `PETS_TEST_URL`
to check a server at a different URL. The checks cover both complete decks,
320/390/768px layouts, slider dragging and keyboard input, history, deep links,
solutions, mathematical glyphs, chapter links, and navigation without JavaScript.

## Interactive learning

The three-line chapter picker includes links to both decks and shortcuts to the
selected interactive cards. It works without JavaScript; Escape and outside clicks
also dismiss it when JavaScript is enabled. Reading type is 1 pt larger.

`docs/learning.js` and `docs/learning.css` add seven experiments alongside the
original explanations, without changing card numbering or mathematical markup:

| Chapter | Card | Experiment |
| --- | --- | --- |
| Commitment | 3 | Distinct guesses and uniform-secret probability |
| Commitment | 20 | Hiding versus binding with a one-time pad |
| Commitment | 34 | Modular clock with signed steps |
| Commitment | 49 | Pedersen commitment distributions over all randomizers |
| Zero Knowledge | 21 | Graph proof challenge disclosures |
| Zero Knowledge | 38 | Soundness amplification with fresh challenges |
| Zero Knowledge | 43 | Schnorr transcript verification, tampering, and extraction |

The group examples use tiny parameters explicitly labeled as teaching examples.
Random challenge trials illustrate the theoretical bound; they do not estimate it.
All original explanations remain readable without JavaScript.

With the local server running, run `node tests/learning.cjs` as well as
`node tests/reader.cjs`. The learning checks cover expected numerical results,
menu keyboard/touch behavior, +1 pt text sizing, disclosure rules, and mobile
portrait/landscape layouts. Both scripts support `CHROMIUM_PATH` and `PETS_TEST_URL`.

## Dedicated homework decks and math repairs

- `docs/hw1/index.html`: 22 cards, including all 15 HW1 exercises.
- `docs/hw2/index.html`: 20 cards, including all 13 HW2 exercises.

Each exercise has its original statement and worked solution, local prerequisite
notes, a reasoning route, and an interactive checkpoint with explanatory feedback.
Additional experiments illustrate XOR openings, the zero-message hiding test,
known-log Pedersen openings, DDH shifts and joint distributions, vector commitment
sizes, Merkle paths, parallel simulation, reverse Schnorr simulation, and circuit
wire consistency. The chapter decks keep their integrated homework.

`python3 scripts/build-homework.py` regenerates the homework HTML from the corrected
chapter cards and the exercise notes in that script, then updates all four menus.
Update chapter content and the notes there before regenerating the homework decks.
`docs/homework.js` contains the homework experiment logic.

The formula repairs restore the concatenation operator in the oracle-guessing card,
five missing sampling domains, and protocol instructions accidentally rendered as
math. Repaired equations are self-contained SVGs; no network math renderer is needed.
The oracle-guessing explanation now distinguishes conditional from overall success
probability, the statistical-binding counterexample uses two distinct hash bases,
and the single-query PRF reduction states its exact distribution match.

Run `node tests/homework.cjs` to check all 28 homework checkpoints, numerical
experiments, responsive layouts, and every mathematical SVG across all 189 cards
with solutions expanded. The scripts test Chromium; Safari/iOS device testing is
not included.
