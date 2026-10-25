const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const base = process.env.PETS_TEST_URL || 'http://127.0.0.1:8765';

(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox']});
  try {
    const page = await browser.newPage({viewport: {width: 320, height: 844}, hasTouch: true});
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    const visit = async (deck, card, key) => {
      await page.goto(`${base}/${deck}/#lesson-${card}`);
      const lab = page.locator(`[data-lab="${key}"]`);
      await lab.waitFor({state: 'visible'});
      return lab;
    };
    let lab = await visit('commitment',2,'growth');
    assert.match(await lab.locator('output').textContent(), /costs are equal/);
    const cardPosition = await page.locator('#pet-card-slider').inputValue();
    await lab.locator('input').focus(); await page.keyboard.press('End');
    assert.match(await lab.locator('output').textContent(), /144 steps.*4,096 steps/);
    assert.equal(await page.locator('#pet-card-slider').inputValue(),cardPosition);
    assert.match(await lab.locator('svg').getAttribute('aria-label'),/from 0 to 4096/);
    await page.locator('.pet-active [data-view=reading]').click();
    assert.equal(await lab.isVisible(),false);
    assert(await page.locator('.pet-active .concept-reading mjx-container').first().isVisible());
    await page.locator('.pet-active [data-view=visual]').click();
    assert.equal(await lab.locator('input').inputValue(),'12');
    assert.equal(new URL(page.url()).hash,'#lesson-2');

    lab = await visit('commitment',13,'negligible');
    assert.match(await lab.locator('output').textContent(),/Equal denominators/); // 2^16 = 16^4
    await lab.locator('select').selectOption('polynomial');
    assert.equal(await lab.locator('.below-threshold').count(),6);
    await lab.locator('input').fill('6');
    assert.equal(await lab.locator('.below-threshold').count(),0);
    assert.match(await lab.locator('output').textContent(),/not negligible/);
    await lab.locator('select').selectOption('exponential');
    await lab.locator('input').fill('8');
    await lab.locator('[data-size="128"]').click();
    assert.match(await lab.locator('output').textContent(),/larger denominator gives the smaller fraction/);
    assert(await lab.locator('[data-size="128"]').evaluate(el=>el===document.activeElement));
    assert.equal(await lab.locator('[data-size="16"]').textContent(),'λ = 16Not below');

    lab = await visit('commitment',22,'distinguishing');
    const gaps=[0,3,1,4,1,2,0,3,3,0,2,1,4,1,3,0];
    for(const scenario of ['different','same']){
      await lab.locator('select').selectOption(scenario);
      for(let mask=0;mask<16;mask++){
        await lab.evaluate((el,mask)=>{
          el.querySelectorAll('input').forEach((input,i)=>input.checked=!!(mask&(1<<i)));
          el.querySelector('input').dispatchEvent(new Event('change',{bubbles:true}));
        },mask);
        const gap=scenario==='same'?0:gaps[mask];
        assert.match(await lab.locator('output').textContent(),new RegExp(`difference: ${gap}/8 = ${gap/8}\\.`));
      }
    }
    await lab.locator('input').first().focus();await page.keyboard.press('Space');
    assert.equal(await lab.locator('input').first().isChecked(),false);

    for(const [deck,card] of [['commitment',31],['hw1',1]]){
      lab=await visit(deck,card,'collision-pairs');
      for(const [q,pairs] of [[2,1],[4,6],[8,28]]){
        await lab.locator('#collision-q').fill(String(q));
        assert.equal(await lab.locator('.query-pair').count(),pairs);
        assert.match(await lab.locator('output').textContent(),new RegExp(`There are ${pairs} pairs`));
      }
      await lab.locator('#collision-bits').fill('3');
      assert.match(await lab.locator('output').textContent(),/does not mean a collision is certain/);
    }

    lab=await visit('commitment',51,'binding-reduction');
    assert(await lab.locator('[data-back]').isDisabled());
    for(let n=1;n<=3;n++){
      await lab.locator('[data-next]').click();
      assert.equal(await lab.locator('[aria-current=step]').getAttribute('data-stage'),String(n));
    }
    assert.equal(await lab.locator('.lab-equation b').textContent(),'3');
    assert.match(await lab.locator('.flow-box').textContent(),/2³ mod 23 = 8 = h/);
    assert(await lab.locator('[data-next]').isDisabled());
    await lab.locator('[data-back]').click();
    assert.match(await lab.locator('output').textContent(),/isolates the unknown/);

    lab=await visit('zero-knowledge',24,'simulator-retry');
    await lab.locator('[data-challenge="1"]').click();
    assert.match(await lab.locator('.retry-flow').textContent(),/Discard/);
    assert(await lab.locator('select').isDisabled());
    assert(await lab.locator('[data-challenge="0"]').isDisabled());
    await lab.locator('[data-retry]').click();
    await lab.locator('select').selectOption('1');
    await lab.locator('[data-challenge="1"]').click();
    assert.match(await lab.locator('.retry-flow').textContent(),/Keep/);
    assert.match(await lab.locator('output').textContent(),/two attempts on average/);

    lab=await visit('hw1',16,'ddh-plane');
    for(const gamma of [0,1,2,3,4]){
      await lab.locator('input').fill(String(gamma));
      assert.equal(await lab.locator('.seen').count(),gamma===2?5:25);
    }
    await lab.locator('input').fill('2');
    await lab.locator('[data-pair="0"]').click();
    assert.match(await lab.locator('.mapping-detail').textContent(),/5\/25/);
    await lab.locator('[data-pair="1"]').click();
    assert.match(await lab.locator('.mapping-detail').textContent(),/No input pair/);
    assert(await lab.locator('[data-pair="1"]').evaluate(el=>el===document.activeElement));

    lab=await visit('hw2',13,'reverse-simulator');
    for(const c of [0,2,10])for(const z of [0,7,10]){
      await lab.locator('[data-control=c]').fill(String(c));
      await lab.locator('[data-control=z]').fill(String(z));
      const transcript=await lab.locator('.lab-message').last().textContent();
      await lab.locator('[data-order=honest]').click();
      assert.equal(await lab.locator('.lab-message').last().textContent(),transcript);
      assert.match(await lab.locator('label[for="reverse-simulator-z"]').textContent(),/Randomizer r/);
      await lab.locator('[data-order=simulator]').click();
      assert.equal(await lab.locator('[data-control=z]').inputValue(),String(z));
      assert.equal(await lab.locator('.lab-message').last().textContent(),transcript);
    }

    lab=await visit('hw1',22,'merkle-path');
    const siblings=[/leaf 3 on its left/,/leaves 1–2 on its left/,/leaves 5–8 on its right/];
    for(let step=0;step<3;step++){
      await lab.locator('[data-tree-next]').click();
      assert.match(await lab.locator('output').textContent(),siblings[step]);
      assert.equal(await lab.locator('.tree-current').count(),1);
    }
    assert.match(await lab.locator('output').textContent(),/compare the computed root/i);
    await lab.locator('input').fill('8');
    assert(await lab.locator('[data-tree-back]').isDisabled());
    assert.match(await lab.locator('output').textContent(),/Start by hashing/);
    console.log('PASS visual reasoning: growth, negligible thresholds, all 16 distinguishing tests, collision bounds, reduction steps, retries, DDH mappings, Schnorr correspondence and Merkle path');

    const cases=[['commitment',2,'growth'],['commitment',13,'negligible'],['commitment',22,'distinguishing'],['commitment',31,'collision-pairs'],['commitment',51,'binding-reduction'],['zero-knowledge',24,'simulator-retry'],['hw1',1,'collision-pairs'],['hw1',16,'ddh-plane'],['hw1',22,'merkle-path'],['hw2',13,'reverse-simulator']];
    for(const width of [320,390,768]){
      await page.setViewportSize({width,height:640});
      for(const [deck,id,key] of cases){
        lab=await visit(deck,id,key);
        if(key==='growth')await lab.locator('input').fill('12');
        if(key==='collision-pairs')await lab.locator('#collision-q').fill('8');
        await page.evaluate(async()=>{await new Promise(requestAnimationFrame);await new Promise(requestAnimationFrame);});
        const bad=await lab.evaluate(el=>{
          const box=el.getBoundingClientRect();
          return [...el.querySelectorAll('button,input,select,svg,text')].flatMap(item=>{
            const r=item.getBoundingClientRect();
            return r.width&& (r.left<box.left-1||r.right>box.right+1)?[{tag:item.tagName,text:item.textContent.slice(0,40),left:r.left,right:r.right}]:[];
          });
        });
        assert.deepEqual(bad,[],`${key} at ${width}px`);
        assert(await lab.evaluate(el=>el.scrollWidth<=el.clientWidth+1),`${key} scroll overflow at ${width}px`);
      }
      console.log(`PASS visual lesson geometry and touch controls at ${width}px`);
    }
    const fallback=await browser.newPage({javaScriptEnabled:false,viewport:{width:320,height:640}});
    for(const [deck,id] of cases.filter(([d])=>d==='commitment'||d==='zero-knowledge')){
      await fallback.goto(`${base}/${deck}/#lesson-${id}`);
      assert(await fallback.locator('.slide:visible .reading>p').first().isVisible());
      assert.equal(await fallback.locator('.concept-switch').count(),0);
    }
    assert.deepEqual(errors,[]);
    console.log('PASS original written lessons without JavaScript; no browser exceptions');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
