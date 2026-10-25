const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base=process.env.PETS_TEST_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});
 try {
  const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const visit=async(id,key,deck='snarks')=>{
   await page.goto(`${base}/${deck}/#${id}`);
   await page.waitForFunction(id=>document.querySelector('.pet-active')?.id===id,id);
   await page.locator('.pet-active details.solution').evaluateAll(els=>els.forEach(e=>e.open=true));
   return page.locator(`.pet-active [data-snark-lab="${key}"]`);
  };
  let lab=await visit('hw-1c','roots','hw3');
  assert.equal(await lab.locator('.is-hit').count(),4);
  await lab.locator('select').selectOption('7');assert.equal(await lab.locator('.is-hit').count(),2);
  assert.match(await lab.locator('output').textContent(),/Roots: 0, 5/);
  lab=await visit('hw-2b','schnorr','hw3');
  for(let z=0;z<11;z++){
   await lab.locator('input').fill(String(z));const result=await lab.locator('[role=status]').textContent();
   assert(result.includes(z===10?'Accept:':'Reject:'));
  }
  lab=await visit('hw-3b','challenge-space','hw3');
  for(const n of [1,3,6]){
   await lab.locator('input').fill(String(n));assert.equal(await lab.locator('.snark-grid>span').count(),2**n);
   assert.equal(await lab.locator('.is-hit').count(),1);
  }
  lab=await visit('pcp-protocol','pcp-checks');
  for(const a of [false,true])for(const b of [false,true]){
   await lab.locator('input').nth(0).setChecked(a);await lab.locator('input').nth(1).setChecked(b);
   assert.match(await lab.locator('[role=status]').textContent(),a&&b?/^Accept:/:/^Reject:/);
  }
  lab=await visit('polynomial-equality','equality');
  for(const p of [7,11,17]){
   await lab.locator('select').selectOption(String(p));assert.equal(await lab.locator('.snark-scatter-row').count(),p);
   assert.equal(await lab.locator('.is-hit').count(),2);
   assert.match(await lab.locator('output').textContent(),new RegExp(`probability 2/${p}`));
  }
  lab=await visit('interpolation','interpolation');
  // Reconstruct several arbitrary tables, including constant and linear polynomials.
  for(const values of [[3,1,2],[0,0,0],[1,2,3],[6,0,4]]){
   for(let i=0;i<3;i++)await lab.locator('select').nth(i).selectOption(String(values[i]));
   const [a,b,c]=(await lab.getAttribute('data-coefficients')).split(',').map(Number);
   for(let x=0;x<3;x++)assert.equal((a*x*x+b*x+c)%7,values[x]);
  }
  lab=await visit('roots-of-unity','unity');
  for(const [w,unique]of [[6,12],[1,1],[96,2]]){
   await lab.locator('select').selectOption(String(w));
   assert.equal(await lab.locator('.is-fail').count(),12-unique);
   assert.match(await lab.locator('[role=status]').textContent(),new RegExp(`${unique} distinct`));
  }
  lab=await visit('trace-polynomial','trace');
  for(const [wire,slots]of [['x2',[1,3,10]],['w1',[4,9]],['gate0',[2,6]]]){
   await lab.locator('select').selectOption(wire);
   assert.deepEqual((await lab.locator('.is-hit').allTextContents()).map(t=>+t.split(':')[0]),slots);
  }
  lab=await visit('four-obligations','obligations');
  for(const [scenario,result]of [['valid','1,1,1,1'],['public','0,1,1,1'],['gate','1,1,0,1'],['wire','1,1,1,0'],['output','1,0,1,1']]){
   await lab.locator('select').selectOption(scenario);assert.equal(await lab.getAttribute('data-checks'),result);
  }
  lab=await visit('gate-selector','selector');
  for(const [s,value]of [[1,7],[0,12]]){
   await lab.locator('select').selectOption(String(s));await lab.locator('input').fill(String(value));
   assert.equal(await lab.getAttribute('data-residual'),'0');
   await lab.locator('input').fill('0');assert.equal(await lab.getAttribute('data-residual'),String(value));
  }
  // All new cards, expanded solutions and controls fit narrow screens. No hidden external math runtime.
  for(const width of [320,390,768])for(const deck of ['snarks','hw3']){
   await page.setViewportSize({width,height:640});await page.goto(`${base}/${deck}/`);
   const ids=await page.locator('.slide').evaluateAll(els=>els.map(e=>e.id));
   for(const id of ids){
    await page.evaluate(id=>{location.hash=id;},id);await page.waitForFunction(id=>document.querySelector('.pet-active').id===id,id);
    await page.locator('.pet-active details').evaluateAll(els=>els.forEach(e=>e.open=true));
    const failures=await page.locator('.pet-active').evaluate(slide=>{
     const bad=[];
     for(const e of slide.querySelectorAll('.reading,.learning,select,table'))if(e.scrollWidth>e.clientWidth+2)bad.push(`${e.tagName}.${e.className}`);
     for(const e of slide.querySelectorAll('mjx-container>svg')){const r=e.getBoundingClientRect();if(r.width<=0||r.height<=0)bad.push('invisible math');}
     return bad;
    });assert.deepEqual(failures,[],`${deck} ${id} at ${width}px`);
   }
  }
  assert.deepEqual(errors,[]);
  const fallback=await browser.newPage({javaScriptEnabled:false,viewport:{width:320,height:640}});
  for(const id of ['polynomial-equality','interpolation','roots-of-unity','trace-polynomial','four-obligations']){
   await fallback.goto(`${base}/snarks/#${id}`);
   assert.equal(await fallback.locator('.slide:visible').getAttribute('id'),id);
   assert(await fallback.locator('.slide:visible .learning').textContent());
  }
  await fallback.goto(`${base}/hw3/#hw-1c`);await fallback.locator('.slide:visible summary').click();
  assert.equal(await fallback.locator('.slide:visible .snark-grid>span').count(),6);
  console.log('PASS SNARKs/HW3 numerical experiments, independent circuit failures, all new mobile cards, math and no-JS figures');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
