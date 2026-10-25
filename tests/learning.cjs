const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const base = process.env.PETS_TEST_URL || 'http://127.0.0.1:8765';
(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox']});
  try {
    for (const width of [320, 390, 768]) {
      const page = await browser.newPage({viewport:{width,height:844},hasTouch:true});
      const errors=[]; page.on('pageerror',error=>errors.push(error.message));
      const visit = async (chapter,card,key) => {
        await page.goto(`${base}/${chapter}/#lesson-${card}`);
        const lab=page.locator(`[data-lab="${key}"]`);
        await lab.waitFor({state:'visible'});
        return lab;
      };
      let lab=await visit('commitment',3,'guessing');
      assert.equal(await page.locator('.learning[data-lab]').count(),9);
      const font=await page.locator('.pet-active .reading>p').first().evaluate(el=>parseFloat(getComputedStyle(el).fontSize));
      assert(Math.abs(font-(18.32+4/3))<0.01, `reading font is ${font}`);
      assert.equal(await page.locator('.deck-home').count(),0);
      const menu=page.locator('.chapter-menu');
      await menu.locator('summary').focus();await page.keyboard.press('Enter');
      assert(await menu.getAttribute('open')!==null);
      await page.keyboard.press('Tab');
      assert(await page.getByRole('link',{name:/Chapter 2/}).evaluate(el=>el===document.activeElement));
      await page.keyboard.press('Escape');
      assert.equal(await menu.getAttribute('open'),null);
      assert(await menu.locator('summary').evaluate(el=>el===document.activeElement));
      await menu.locator('summary').click();await page.locator('.pet-active .head').click({position:{x:10,y:10}});
      assert.equal(await menu.getAttribute('open'),null);
      await menu.locator('summary').click();await page.getByRole('link',{name:/Chapter 3/}).click();
      await page.waitForURL(`${base}/zero-knowledge/`);
      assert.equal(await page.locator('.learning[data-lab]').count(),4);
      await menu.locator('summary').click();
      await page.getByRole('link',{name:/Schnorr transcripts/}).click();
      await page.waitForURL(`${base}/zero-knowledge/#lesson-43`);
      await page.waitForFunction(()=>document.activeElement===document.querySelector('.chapter-menu summary'));
      assert.equal(await menu.getAttribute('open'),null);
      assert(await menu.locator('summary').evaluate(el=>el===document.activeElement));
      lab=await visit('commitment',3,'guessing');
      await lab.locator('#secret-bits').focus();await page.keyboard.press('ArrowRight');
      assert.equal(await lab.locator('#secret-bits').inputValue(),'5');
      await lab.locator('#secret-bits').evaluate(el=>el.scrollIntoView({block:'center'}));
      const box=await lab.locator('#secret-bits').boundingBox();
      assert(box.y >= 0 && box.y + box.height < 760, 'touch target must be clear of the footer');
      const touch=await page.context().newCDPSession(page);
      await touch.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:box.x+10,y:box.y+20}]});
      for(let step=1;step<=8;step++)await touch.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:box.x+10+(box.width-20)*step/8,y:box.y+20}]});
      await touch.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
      assert.equal(await lab.locator('#secret-bits').inputValue(),'6');
      await touch.detach();
      await lab.locator('#secret-bits').fill('6');await lab.locator('#guess-count').fill('4');
      assert.equal(await lab.locator('.lab-metric').textContent(),'6.25%');
      assert.equal(await lab.locator('.is-hit').count(),4);
      await lab.locator('#secret-bits').fill('5');
      assert.equal(await lab.locator('.lab-metric').textContent(),'12.50%');
      await lab.locator('#secret-bits').fill('1');
      assert.equal(await lab.locator('#guess-count').inputValue(),'2');
      assert.equal(await lab.locator('.lab-metric').textContent(),'100.00%');
      lab=await visit('commitment',20,'hiding-binding');
      for(let m=0;m<3;m++){
        await lab.locator(`[data-move="${m}"]`).click();
        assert.match(await lab.locator('output').textContent(),/Accepted/);
      }
      await lab.locator('select').selectOption('plain');
      assert.match(await lab.locator('output').textContent(),/Rejected/);
      await lab.locator('[data-move="1"]').click();
      assert.match(await lab.locator('output').textContent(),/Accepted/);
      lab=await visit('commitment',34,'modular');
      await lab.locator('#start-residue').fill('1');await lab.locator('#mod-step').fill('-3');
      assert.match(await lab.locator('output').textContent(),/-2 = -1 × 5 \+ 3/);
      assert.equal(await lab.locator('.selected-label').textContent(),'3');
      await lab.locator('#modulus').fill('7');await lab.locator('#mod-step').fill('12');
      assert.equal(await lab.locator('.selected-label').textContent(),'6');
      lab=await visit('commitment',49,'pedersen');
      const group=[1,2,3,4,6,8,9,12,13,16,18];
      for(const m of [0,2,10]){
        await lab.locator('#pedersen-m').fill(String(m));
        assert.deepEqual((await lab.locator('.distribution b').allTextContents()).map(Number),group);
        assert((await lab.locator('.distribution small').allTextContents()).every(x=>x==='1 / 11'));
      }
      await lab.locator('#pedersen-m').fill('2');await lab.locator('#pedersen-r').fill('3');
      assert.equal(await lab.locator('.distribution .is-hit b').textContent(),'1'); // 4 * 512 mod 23
      lab=await visit('zero-knowledge',21,'graph-proof');
      assert.equal(await lab.locator('line').count(),10);
      await lab.locator('[data-challenge="1"]').click();
      assert.equal(await lab.locator('line').count(),5);
      assert.equal(await lab.locator('[data-challenge="0"]').isDisabled(),true);
      assert(!/1→/.test(await lab.locator('output').textContent()));
      await lab.locator('[data-new-round]').click();
      await lab.locator('[data-challenge="0"]').click();
      assert.equal(await lab.locator('line').count(),7);
      assert.match(await lab.locator('output').textContent(),/1→D/);
      lab=await visit('zero-knowledge',38,'soundness');
      assert.equal(await lab.locator('.lab-metric').textContent(),'6.25%');
      await lab.locator('[data-add-round]').click();
      assert.equal(await lab.locator('.lab-metric').textContent(),'3.13%');
      await lab.locator('#proof-rounds').fill('12');
      assert.equal(await lab.locator('.lab-metric').textContent(),'0.0244%');
      assert(await lab.locator('[data-add-round]').isDisabled());
      await lab.locator('[data-random-challenge]').click();
      assert.match(await lab.locator('output').textContent(),/Challenges: [01 ]+\./);
      lab=await visit('zero-knowledge',43,'schnorr');
      for(const e of [0,2,10]){
        await lab.locator('[data-reset-proof]').click();
        await lab.locator('#schnorr-e').fill(String(e));
        await lab.locator('[data-next-step]').click();assert(await lab.locator('#schnorr-e').isDisabled());
        await lab.locator('[data-next-step]').click();
        assert.match(await lab.locator('output').textContent(),/Accept:/);
        await lab.locator('#schnorr-offset').fill('1');
        assert.match(await lab.locator('output').textContent(),/Reject:/);
        assert(await lab.locator('[data-extract]').isDisabled());
        await lab.locator('#schnorr-offset').fill('0');await lab.locator('[data-extract]').click();
        assert.equal(await lab.locator('.extraction b').textContent(),'4');
      }
      // Every experiment fits the reader in portrait and landscape, including its controls.
      for(const [chapter,ids] of [['commitment',[3,20,34,49]],['zero-knowledge',[21,38,43]]]){
        for(const height of [844,390]){
          await page.setViewportSize({width,height});
          for(const id of ids){
            await page.goto(`${base}/${chapter}/#lesson-${id}`);
            const bounds=await page.locator('.pet-active .learning').evaluate(el=>({client:el.clientWidth,scroll:el.scrollWidth,items:[...el.querySelectorAll('button,input,select,svg')].map(x=>({left:x.getBoundingClientRect().left,right:x.getBoundingClientRect().right}))}));
            assert(bounds.scroll<=bounds.client+1,`lab overflow ${chapter} ${id} ${width}`);
            assert(bounds.items.every(x=>x.left>=0 && x.right<=width),`control overflow ${chapter} ${id}`);
          }
        }
      }
      assert.deepEqual(errors,[]);
      console.log(`PASS learning: menu, +1pt type, all seven experiments and responsive layouts at ${width}px`);
      await page.close();
    }
    const fallback=await browser.newPage({javaScriptEnabled:false});
    await fallback.goto(`${base}/commitment/`);await fallback.locator('.chapter-menu summary').click();
    await fallback.getByRole('link',{name:/Chapter 3/}).click();await fallback.waitForURL(`${base}/zero-knowledge/`);
    assert.equal(await fallback.locator('.slide:visible').getAttribute('id'),'start-notation');
    console.log('PASS chapter popup and original content without JavaScript');
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
