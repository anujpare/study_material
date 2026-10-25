const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const base = process.env.PETS_TEST_URL || 'http://127.0.0.1:8765';
const standard = 18.32 + 4 / 3, box = standard - 8 / 3;

async function checkText(page, label) {
  const failures = await page.evaluate(({standard, box}) => {
    const bad = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode, el = node.parentElement;
      if (!node.textContent.trim() || el.closest('script,style,mjx-container')) continue;
      if (!el.getClientRects().length || el.closest('[hidden]') || getComputedStyle(el).visibility === 'hidden') continue;
      // Closed details can still report descendant rectangles in some engines.
      const closed = el.closest('details:not([open])');
      if (closed && !closed.querySelector(':scope > summary').contains(el)) continue;
      const font = parseFloat(getComputedStyle(el).fontSize);
      const boxed = el.closest('.chapter-menu,.deck-jump,.nav,.count,.learning,.beginner-context,.guide,.reasoning-link,blockquote,table,.math,details.solution>summary,.card,.foot');
      const expected = boxed ? box : standard;
      let actual = font;
      if (el.matches('svg.lab-diagram text')) {
        const matrix = el.getScreenCTM();
        actual *= Math.hypot(matrix.a, matrix.b);
      }
      if (Math.abs(actual - expected) > 0.02) bad.push({text: node.textContent.slice(0, 70), actual, expected});
    }
    return bad;
  }, {standard, box});
  assert.deepEqual(failures, [], label);
}

(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox']});
  try {
    const page = await browser.newPage();
    for (const width of [320, 390, 768]) {
      await page.setViewportSize({width, height: 844});
      await page.goto(base);
      await checkText(page, `overview at ${width}px`);
      for (const deck of ['commitment', 'zero-knowledge', 'hw1', 'hw2', 'snarks', 'hw3', 'pir', 'hw4']) {
        await page.goto(`${base}/${deck}/`);
        const count = await page.locator('.slide').count();
        for (let n = 1; n <= count; n++) {
          await page.evaluate(async n => {
            const slider = document.getElementById('pet-card-slider');
            slider.value = n;
            slider.dispatchEvent(new Event('input', {bubbles: true}));
            document.querySelectorAll('.pet-active details').forEach(el => el.open = true);
            await new Promise(requestAnimationFrame);
            await new Promise(requestAnimationFrame);
          }, n);
          await checkText(page, `${deck} card ${n} at ${width}px`);
        }
        await page.locator('.chapter-menu summary').click();
        await checkText(page, `${deck} menu at ${width}px`);
      }
      console.log(`PASS two text sizes: overview, all 352 cards, expanded solutions, menus and diagram labels at ${width}px`);
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
