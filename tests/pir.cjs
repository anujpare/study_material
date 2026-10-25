const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base=process.env.PETS_TEST_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});
 try{
  const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  async function visit(id,key,deck='pir'){
   await page.goto(`${base}/${deck}/#${id}`);await page.waitForFunction(id=>document.querySelector('.pet-active')?.id===id,id);
   await page.locator('.pet-active details.solution').evaluateAll(els=>els.forEach(e=>e.open=true));
   return page.locator(`.pet-active [data-pir-lab="${key}"]`);
  }
  let lab=await visit('query-shares','shares');
  for(const target of ['1','2','3','4'])for(const view of ['0','1','2']){
   await lab.locator('select').nth(0).selectOption(target);await lab.locator('select').nth(1).selectOption(view);
   assert.equal(await lab.locator('.pir-distribution>span').count(),view==='2'?1:16);
   if(view!=='2')assert((await lab.locator('.pir-distribution>span').allTextContents()).every(t=>t.endsWith(': 1/16')));
   const a=await lab.getAttribute('data-q0'),b=await lab.getAttribute('data-q1');
   assert.deepEqual([...a].map((x,i)=>+x^+b[i]),[1,2,3,4].map(i=>Number(i===+target)));
  }
  lab=await visit('matrix-layout','matrix');
  const X=[[1,0,1,1],[0,1,0,1],[1,1,0,0],[0,0,1,0]];
  for(let r=1;r<=4;r++)for(let c=1;c<=4;c++)for(const mask of [0,5,10,15]){
   await lab.locator('select').nth(0).selectOption(String(r));await lab.locator('select').nth(1).selectOption(String(c));await lab.locator('input').fill(String(mask));
   assert.equal(+(await lab.getAttribute('data-result')),X[r-1][c-1]);
   const a=await lab.getAttribute('data-a0'),b=await lab.getAttribute('data-a1');assert.deepEqual([...a].map((v,i)=>+v^+b[i]),X.map(row=>row[c-1]));
  }
  for(let step=0;step<4;step++)await lab.getByRole('button',{name:'Next step'}).click();
  assert(await lab.getByRole('button',{name:'Next step'}).isDisabled());
  lab=await visit('communication-balance','balance');
  for(const c of [1,8,64]){await lab.locator('select').selectOption(String(c));assert.equal(+(await lab.getAttribute('data-total')),2*c+128/c);}
  lab=await visit('recursive-selection','recursion');
  for(const abc of [[1,1,1],[2,3,4],[4,4,4]]){
   for(let i=0;i<3;i++)await lab.locator('select').nth(i).selectOption(String(abc[i]));
   assert.equal(+(await lab.getAttribute('data-record')),((abc[0]-1)*4+abc[1]-1)*4+abc[2]);
   for(let i=0;i<3;i++)await lab.getByRole('button',{name:'Next step'}).click();
   assert.match(await lab.locator('[data-recursion-stage]').textContent(),/Decrypt the outer encoding.*Decrypt the inner ciphertext/);
  }
  lab=await visit('recursive-size','expansion');await lab.locator('input').fill('6');assert.equal(await lab.getAttribute('data-sizes'),'8192,896');
  lab=await visit('server-work','work');await lab.locator('select').selectOption('1024');assert.equal(await lab.getAttribute('data-work'),'10240');
  lab=await visit('hw4-2a','coefficient-shift','hw4');
  for(const i of [0,2,4]){await lab.locator('input').fill(String(i));assert.deepEqual((await lab.getAttribute('data-coefficients')).split(',').map(Number),Array(i).fill(0).concat([3,5]));}
  lab=await visit('hw4-2b','coefficient-split','hw4');await lab.locator('input').fill('0');assert.match(await lab.locator('output').textContent(),/lower part is zero/);await lab.locator('input').fill('3');assert.match(await lab.locator('output').textContent(),/upper part is zero/);
  lab=await visit('hw4-2c','product-coefficient','hw4');
  for(const [i,v] of [4,13,28,27,18].entries()){await lab.locator('input').fill(String(i));assert.equal(+(await lab.getAttribute('data-coefficient')),v);}
  lab=await visit('hw4-3a','powers-setup','hw4');
  for(const coeff of [[0,0,0],[4,2,1],[10,10,10]]){
   for(let i=0;i<3;i++)await lab.locator('select').nth(i).selectOption(String(coeff[i]));
   let expected=1;for(let i=0;i<(coeff[0]+3*coeff[1]+9*coeff[2])%11;i++)expected=expected*2%23;
   assert.equal(+(await lab.getAttribute('data-commitment')),expected);
  }
  lab=await visit('hw4-3d','opening-check','hw4');
  for(let z=0;z<11;z++)for(const tamper of [false,true]){
   await lab.locator('input[type=range]').fill(String(z));await lab.locator('input[type=checkbox]').setChecked(tamper);
   assert.equal(await lab.getAttribute('data-accept'),String(!tamper));
  }
  lab=await visit('hw4-4a','equality-circuit','hw4');
  for(let a=0;a<8;a++)for(let b=0;b<8;b++){await lab.locator('select').nth(0).selectOption(String(a));await lab.locator('select').nth(1).selectOption(String(b));assert.equal(+(await lab.getAttribute('data-result')),Number(a===b));}
  lab=await visit('hw4-4b','fhe-lookup','hw4');
  for(const [i,v]of [1,0,1,1,0,0,1,0].entries()){await lab.locator('select').selectOption(String(i+1));assert.equal(+(await lab.getAttribute('data-result')),v);}
  lab=await visit('hw4-4c','noise','hw4');
  for(const n of [2,3,5,8,16,31,32]){await lab.locator('input').fill(String(n));assert.equal(+(await lab.getAttribute('data-noise')),2*n*8**Math.ceil(Math.log2(n)));}
  for(let s=0;s<3;s++)await lab.getByRole('button',{name:'Next step'}).click();assert.match(await lab.locator('output').textContent(),/result equals 2n⁴/);
  for(const width of [320,390,768])for(const deck of ['pir','hw4']){
   await page.setViewportSize({width,height:640});await page.goto(`${base}/${deck}/`);
   const ids=await page.locator('.slide').evaluateAll(els=>els.map(e=>e.id));
   for(const id of ids){
    await page.evaluate(id=>{location.hash=id;},id);await page.waitForFunction(id=>document.querySelector('.pet-active').id===id,id);
    await page.locator('.pet-active details').evaluateAll(els=>els.forEach(e=>e.open=true));
    const bad=await page.locator('.pet-active').evaluate(slide=>{
     const errors=[];for(const e of slide.querySelectorAll('.reading,.learning,table,select,.pir-product-grid'))if(e.scrollWidth>e.clientWidth+2)errors.push(e.tagName+'.'+e.className);
     for(const e of slide.querySelectorAll('mjx-container>svg')){const r=e.getBoundingClientRect();if(r.width<=0||r.height<=0)errors.push('invisible math');}
     return errors;
    });assert.deepEqual(bad,[],`${deck} ${id} ${width}px`);
   }
  }
  // Also exercise the reused HW3 root visualization in its new chapter context.
  await page.goto(`${base}/pir/#hw3-1c`);await page.locator('.pet-active details').evaluateAll(els=>els.forEach(e=>e.open=true));
  const roots=page.locator('.pet-active [data-snark-lab=roots]');assert.equal(await roots.locator('.is-hit').count(),4);await roots.locator('select').selectOption('7');assert.equal(await roots.locator('.is-hit').count(),2);
  const fallback=await browser.newPage({javaScriptEnabled:false,viewport:{width:320,height:640}});
  await fallback.goto(`${base}/pir/#matrix-layout`);assert.equal(await fallback.locator('.slide:visible table tbody tr').count(),4);
  await fallback.goto(`${base}/hw4/#hw4-4b`);await fallback.locator('.slide:visible summary').click();assert.equal(await fallback.locator('.slide:visible table tbody tr').count(),8);
  assert.deepEqual(errors,[]);
  console.log('PASS PIR/HW4: query distributions, matrix reconstruction, costs, recursion, polynomial coefficients, opening zero cases, all equality pairs, FHE lookup/noise, mobile layouts and no-JS diagrams');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
