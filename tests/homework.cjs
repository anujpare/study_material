const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('playwright');
const base=process.env.PETS_TEST_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});
 try{
  const page=await browser.newPage({viewport:{width:320,height:844},hasTouch:true});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const [deck,count,exercises] of [['hw1',15,15],['hw2',13,13]]){
   await page.goto(`${base}/${deck}/`);
   assert.equal(await page.locator('.slide').count(),count);
   assert.equal(await page.locator('.homework-prep').count(),0);
   assert.equal(await page.locator('.homework-check').count(),0);
   assert.equal(await page.locator('.chapter-panel a[aria-current=page]').count(),1);
   assert.equal(await page.locator('details.solution').count(),exercises);
   console.log(`PASS ${deck}: ${count} cards, ${exercises} self-contained worked solutions`);
  }
  const visit=async(deck,source,key)=>{
   await page.goto(`${base}/${deck}/`);
   const id=await page.locator(`[data-source-card="${source}"]`).getAttribute('id');
   await page.evaluate(id=>{location.hash=id;},id);
   await page.locator('.pet-active details.solution').evaluateAll(es=>es.forEach(e=>e.open=true));
   return page.locator(`[data-lab="${key}"]`);
  };
  let lab=await visit('hw1',26,'xor-openings');
  await lab.locator('[data-control=c]').fill('9');await lab.locator('[data-control=m]').fill('12');
  assert.match(await lab.locator('.lab-equation').textContent(),/r′ = 5/);
  lab=await visit('hw1',53,'identity-leak');
  assert.equal(await lab.locator('.distribution small').first().textContent(),'5 / 5');
  await lab.locator('input').fill('1');assert((await lab.locator('.distribution small').allTextContents()).every(t=>t==='1 / 5'));
  lab=await visit('hw1',54,'trapdoor-opening');
  for(const m of [0,7,10]){await lab.locator('input').fill(String(m));assert.match(await lab.locator('.lab-equation').textContent(),/mod 23 = 1$/);}
  lab=await visit('hw1',73,'ddh-shift');await lab.locator('input').fill('4');
  assert.match(await lab.locator('.lab-equation').textContent(),/≡ 0 = 0·2/);
  lab=await visit('hw1',77,'ddh-plane');
  assert.equal(await lab.locator('.seen').count(),25);await lab.locator('input').fill('2');assert.equal(await lab.locator('.seen').count(),5);
  lab=await visit('hw1',84,'merkle-path');
  for(const i of [1,4,8]){await lab.locator('input').fill(String(i));assert.equal(await lab.locator('.tree-sibling').count(),3);assert.equal(await lab.locator('.tree-path').count(),3);}
  lab=await visit('hw2',45,'reverse-simulator');
  for(const c of [0,2,10])for(const z of [0,7,10]){await lab.locator('[data-control=c]').fill(String(c));await lab.locator('[data-control=z]').fill(String(z));const text=await lab.locator('output').textContent();const m=/gets (\d+) on the left of its equation and (\d+) on the right/.exec(text);assert(m);assert.equal(m[1],m[2]);}
  lab=await visit('hw2',41,'composition');await lab.locator('input').fill('12');assert.match(await lab.locator('.lab-transcript').textContent(),/4096 expected/);
  for(const source of [57,58,61]){
   lab=await visit('hw2',source,`circuit-${source}`);await lab.locator('[data-control=b]').fill('1');await lab.locator('[data-control=tamper]').fill('1');assert.match(await lab.locator('output').textContent(),/XOR statement is false/);
  }
  // Inspect every equation, including expanded solutions, in all eight decks.
  for(const [deck,count]of [['commitment',58],['zero-knowledge',46],['hw1',15],['hw2',13],['snarks',48],['hw3',12],['pir',44],['hw4',15]]){
   const source=fs.readFileSync(`docs/${deck}/index.html`,'utf8');
   assert(!/fill="red"|data-mjx-error|data-mml-node="merror"|\\parallelr/.test(source));
   await page.goto(`${base}/${deck}/`);
   assert.equal(await page.locator('svg use[href^="#pet-math-glyph-"]').count(),0);
   for(let n=1;n<=count;n++){
    await page.locator('#pet-card-slider').fill(String(n));
    const readView=page.locator('.pet-active [data-view="reading"]');
    if(await readView.count())await readView.click();
    const problems=await page.locator('.pet-active').evaluate(slide=>{
     slide.querySelectorAll('details').forEach(d=>{d.open=true;});
     return [...slide.querySelectorAll('mjx-container>svg')].flatMap((svg,i)=>{
      const r=svg.getBoundingClientRect(),b=svg.getBBox(),v=svg.viewBox.baseVal;
      const glyphs=[...svg.querySelectorAll('[data-c]')].map(e=>String.fromCodePoint(parseInt(e.getAttribute('data-c'),16))).join('').normalize('NFKD');
      return r.width<=0||r.height<=0||v.width<=0||v.height<=0||b.width<=0||/←\s*$|andstore|proversends|andsends/.test(glyphs)?[{i,glyphs,width:r.width,height:r.height}]:[];
     });
    });
    assert.deepEqual(problems,[],`${deck} card ${n}: malformed or invisible formula`);
   }
   console.log(`PASS rendering: all ${count} cards and expanded solutions in ${deck}`);
  }
  // Check all homework visual panels fit at mobile and tablet sizes.
  for(const width of [320,390,768])for(const deck of ['hw1','hw2']){
   await page.setViewportSize({width,height:640});await page.goto(`${base}/${deck}/`);
   const ids=await page.locator('.slide:has(.learning)').evaluateAll(els=>els.map(e=>e.id));
   for(const id of ids){await page.evaluate(id=>{location.hash=id;},id);await page.waitForFunction(id=>document.querySelector('.pet-active').id===id,id);
    await page.locator('.pet-active details.solution').evaluateAll(es=>es.forEach(e=>e.open=true));
    const bad=await page.locator('.pet-active .learning').evaluateAll(els=>els.filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.dataset.lab||'checkpoint'));
    assert.deepEqual(bad,[],`${deck} ${id} width ${width}`);
   }
  }
  assert.deepEqual(errors,[]);console.log('PASS homework experiments, equation rendering and mobile layout');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
