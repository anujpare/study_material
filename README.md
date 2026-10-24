# study_material

Interactive PETS study decks.

## Published structure

- `docs/index.html` — landing page with chapter selection
- `docs/commitment/index.html` — Chapter 2 deck
- `docs/zero-knowledge/index.html` — Chapter 3 deck

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
