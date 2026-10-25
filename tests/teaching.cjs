const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base=process.env.PETS_TEST_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});
 try{
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const width of [320,390,768]){
   await page.setViewportSize({width,height:844});
   for(const deck of ['commitment','zero-knowledge','snarks','pir','hw1','hw2','hw3','hw4']){
    await page.goto(`${base}/${deck}/`);
    assert.equal(await page.locator('.concept-switch,.beginner-context').count(),0);
    const aliases=await page.locator('.card-alias').evaluateAll(es=>es.map(e=>[e.id,e.closest('.slide').id]));
    for(const [alias,target]of aliases){
     await page.evaluate(a=>{history.replaceState(null,'','#'+a);dispatchEvent(new HashChangeEvent('hashchange'));},alias);
     assert.equal(await page.locator('.slide:visible').getAttribute('id'),target);
    }
    const figures=await page.locator('[data-protocol]').evaluateAll(es=>es.map(e=>({key:e.dataset.protocol,card:e.closest('.slide').id,steps:e.querySelectorAll('.protocol-step').length})));
    for(const {key,card,steps}of figures){
     await page.evaluate(id=>{location.hash=id;},card);await page.waitForFunction(id=>document.querySelector('.pet-active').id===id,card);
     const solution=page.locator('.pet-active details.solution');if(await solution.count())await solution.evaluate(e=>e.open=true);
     const f=page.locator(`[data-protocol="${key}"]`);assert(await f.isVisible());
     const bad=await f.evaluate(el=>[el,...el.querySelectorAll('.protocol-parties,.protocol-action,.protocol-message,button')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.className));
     assert.deepEqual(bad,[],`${deck} ${key} at ${width}px`);
     assert.equal(await f.locator('.protocol-step:visible').count(),steps);
     await f.locator('[data-next]').click();assert.equal(await f.locator('[aria-current=step]').count(),1);
     for(let i=1;i<steps;i++)await f.locator('[data-next]').click();
     assert(await f.locator('[data-next]').isDisabled());assert.equal(await f.locator('.protocol-step:visible').count(),steps);
     await f.locator('[data-reset]').click();assert.equal(await f.locator('[aria-current=step]').count(),0);
    }
   }
   console.log(`PASS ${width}px: all bookmark redirects, visible teaching prose and static/interactive protocol geometry`);
  }
  const fallback=await browser.newPage({javaScriptEnabled:false,viewport:{width:320,height:844}});
  for(const [deck,alias,target]of [['commitment','start-notation','lesson-1'],['commitment','start-powers','lesson-10'],['commitment','lesson-21','lesson-22'],['zero-knowledge','lesson-27','lesson-29'],['hw1','lesson-2','lesson-3'],['hw2','start-notation','lesson-2'],['pir','bit-selection','query-shares']]){
   await fallback.goto(`${base}/${deck}/#${alias}`);assert.equal(await fallback.locator('.slide:visible').count(),1);assert.equal(await fallback.locator('.slide:visible').getAttribute('id'),target);
  }
  await fallback.goto(`${base}/zero-knowledge/#lesson-21`);assert(await fallback.locator('[data-protocol=hamiltonian]').isVisible());assert.equal(await fallback.locator('.protocol-controls').count(),0);
  await page.goto(`${base}/hw2/#lesson-14`);assert.equal(await page.locator('.pet-active details.solution').getAttribute('open'),null);assert.equal(await page.locator('.pet-active [data-protocol]:visible').count(),0);
  assert.deepEqual(errors,[]);console.log('PASS no-JS legacy links and protocol diagram; homework answers stay closed');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
