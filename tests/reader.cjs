// Run against: python3 -m http.server 8765 --directory docs
// Test dependency: npm install --no-save playwright
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const base = process.env.PETS_TEST_URL || 'http://127.0.0.1:8765';
(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || undefined,
    args: ['--no-sandbox'],
  });
  try {
    for (const width of [320, 390, 768]) {
      const page = await browser.newPage({ viewport: { width, height: 844 }, hasTouch: true });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(base);
      assert.equal(await page.locator('.card').count(), 2);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      for (const [chapter, count] of [['commitment', 85], ['zero-knowledge', 62]]) {
        await page.goto(`${base}/${chapter}/`);
        const slider = page.locator('#pet-card-slider');
        async function check(n) {
          assert.equal(await slider.inputValue(), String(n));
          assert.equal(await page.locator('#pet-card-position').textContent(), `${n} / ${count}`);
          assert.equal(await slider.getAttribute('aria-valuetext'), `Card ${n} of ${count}`);
          assert.equal(await page.locator('.slide:visible').count(), 1);
          assert.equal(await page.locator('.slide:visible').getAttribute('id'), `lesson-${n}`);
        }
        await check(1);
        assert.equal(await slider.getAttribute('max'), String(count));
        // Every card must be reachable, with one visible slide and valid glyphs.
        for (let n = 1; n <= count; n++) {
          await slider.fill(String(n));
          await check(n);
        }
        assert.equal(await page.locator('section.slide svg use[href^="#pet-math-glyph-"]').count(), 0);
        assert(await page.locator('section.slide svg path').count() > 0);
        await slider.focus();
        await page.keyboard.press('Home');
        await check(1);
        await page.keyboard.press('ArrowRight');
        await check(2);
        await page.locator('.slide:visible [aria-label="Next card"]').click();
        await check(3);
        await page.goBack();
        await check(2);
        await page.goForward();
        await check(3);
        await page.locator('.slide:visible [aria-label="Previous card"]').click();
        await check(2);
        // Native pointer dragging must retain focus and synchronize the active card.
        const box = await slider.boundingBox();
        await page.mouse.move(box.x + 10, box.y + box.height / 2);
        await page.mouse.down();
        await page.mouse.move(box.x + box.width - 10, box.y + box.height / 2, { steps: 12 });
        await page.mouse.up();
        const dragged = Number(await slider.inputValue());
        assert(dragged > count / 2);
        await check(dragged);
        // Exercise real touch events as well as mouse and keyboard input.
        const touch = await page.context().newCDPSession(page);
        await touch.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [{x: box.x + 10, y: box.y + box.height / 2}]});
        for (let step = 1; step <= 10; step++) {
          await touch.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: box.x + 10 + (box.width - 20) * step / 10, y: box.y + box.height / 2}]});
        }
        await touch.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
        assert(Number(await slider.inputValue()) > count / 2);
        await check(Number(await slider.inputValue()));
        await touch.detach();
        await page.goto(`${base}/${chapter}/#lesson-${count}`);
        await check(count);
        await page.reload();
        await check(count);
        for (const [hash, expected] of [['#lesson-999', count], ['#lesson-0', 1], ['#unknown', 1]]) {
          await page.evaluate(hash => { location.hash = hash; }, hash);
          await page.waitForFunction(n => document.querySelector('input').value === String(n), expected);
          await check(expected);
        }
        // Opening a solution and resizing keeps its content and math present.
        const detailCard = await page.locator('.slide:has(details)').first().getAttribute('id');
        await page.evaluate(id => { location.hash = id; }, detailCard);
        await page.locator('.slide:visible details summary').first().click();
        assert(await page.locator('.slide:visible details').first().getAttribute('open') !== null);
        await page.setViewportSize({width, height: 390});
        const geometry = await page.evaluate(() => {
          const home = document.querySelector('.deck-home').getBoundingClientRect();
          const head = document.querySelector('.pet-active .head').getBoundingClientRect();
          const slider = document.querySelector('input').getBoundingClientRect();
          const nav = document.querySelector('.pet-active .nav').getBoundingClientRect();
          return {homeBottom: home.bottom, headTop: head.top, sliderRight: slider.right, navLeft: nav.left, navBottom: nav.bottom, height: innerHeight};
        });
        assert(geometry.homeBottom <= geometry.headTop);
        assert(geometry.sliderRight <= geometry.navLeft);
        assert(geometry.navBottom <= geometry.height);
        await page.locator('.deck-home').click();
        await page.waitForURL(`${base}/`);
        await page.setViewportSize({width, height: 844});
        console.log(`PASS ${chapter}: ${count} cards, slider, history, math, solutions, mobile ${width}px`);
      }
      assert.deepEqual(errors, []);
      await page.close();
    }
    const fallback = await browser.newPage({javaScriptEnabled: false, viewport: {width: 320, height: 640}});
    for (const chapter of ['commitment', 'zero-knowledge']) {
      await fallback.goto(`${base}/${chapter}/`);
      assert.equal(await fallback.locator('.slide:visible').count(), 1);
      await fallback.locator('.slide:visible [aria-label="Next card"]').click();
      assert.equal(await fallback.locator('.slide:visible').getAttribute('id'), 'lesson-2');
      assert.equal(await fallback.locator('#pet-card-slider:visible').count(), 0);
    }
    console.log('PASS no-JavaScript card navigation');
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
