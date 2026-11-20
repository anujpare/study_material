'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const base=process.env.PETS_TEST_URL||'http://127.0.0.1:8765';
const out=process.env.PETS_SCREENSHOTS||'/workspace/scratch/10d15d5fecea/tmp/mpc/screens';
const map=JSON.parse(fs.readFileSync('docs/mpc-workbench/source-map.json','utf8'));
(async()=>{
 fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});
 try{
  const ctx=await browser.newContext({viewport:{width:375,height:812},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  const page=await ctx.newPage(),errors=[],failed=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>failed.push(r.url()));
  await page.goto(base+'/mpc-workbench/',{waitUntil:'networkidle'});
  async function card(id){await page.evaluate(id=>{location.hash=id},id);await page.waitForFunction(id=>document.querySelector('article[data-active=true]')?.id===id,id);}
  async function set(lab,key,value){await lab.locator(`[data-key="${key}"]`).evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event('input',{bubbles:true}));},value);}
  for(let i=0;i<map.length;i++){
   const c=map[i];await card(c.id);const active=page.locator(`article#${c.id}`);assert.equal(await page.locator('article.lesson:visible').count(),1);assert.equal(await active.locator('details.solution').getAttribute('open'),null);
   // Test the whole expanded solution and every rendered diagram, not only the first viewport.
   await active.locator('details.solution').evaluate(el=>el.open=true);
   const problems=await active.evaluate(el=>{const vw=innerWidth;return [...el.querySelectorAll('p,h1,h2,h3,li,table,.lab,.protocol,.checkpoint,textarea,button')].filter(e=>{if(!e.getClientRects().length)return false;const r=e.getBoundingClientRect();if(e.closest('.math,.table-scroll'))return false;return r.right>vw+3||r.left< -3;}).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,70),r:e.getBoundingClientRect().right}));});
   assert.deepEqual(problems,[],c.id+' spills outside phone');
   const pageWidth=await page.evaluate(()=>document.documentElement.scrollWidth);assert(pageWidth<=375+2,c.id+' page overflow');
   assert.equal(await active.locator('[data-mjx-error],merror').count(),0);
   // The allowed typography is the shared standard text and exactly two points smaller.
   const sizes=await active.evaluate(el=>{const allowed=[parseFloat(getComputedStyle(document.body).fontSize),parseFloat(getComputedStyle(document.body).fontSize)-8/3];return [...el.querySelectorAll('p,h1,h2,h3,button,summary,td,th,label,span')].filter(e=>e.getClientRects().length&&!e.closest('mjx-container')).filter(e=>!allowed.some(n=>Math.abs(parseFloat(getComputedStyle(e).fontSize)-n)<.04)).map(e=>({tag:e.tagName,cls:e.className,size:getComputedStyle(e).fontSize}));});assert.deepEqual(sizes,[],c.id+' inconsistent font sizes');
   await active.locator('details.solution').evaluate(el=>el.open=false);
   await page.screenshot({path:path.join(out,String(i+1).padStart(2,'0')+'-'+c.id+'.png')});
  }
  // Every experiment responds; a hidden secret must preserve the coalition view.
  const seen=new Set();
  for(const c of map){
   for(const name of c.labs){
    if(seen.has(name))continue;
    seen.add(name);await card(c.id);
    const active=page.locator(`article#${c.id}`);
    await active.locator('details.solution').evaluate(el=>el.open=true);
    const lab=active.locator(`[data-lab="${name}"]`).first(),view=lab.locator('.lab-view'),before=await view.innerHTML();
    const input=lab.locator('input[type=range]').first(),select=lab.locator('select').first(),step=lab.locator('[data-step="1"]'),button=lab.locator('[data-set][aria-pressed="false"]').first();
    if(await input.count()){
     await input.evaluate(el=>{el.value=String(Number(el.value)<Number(el.max)?Number(el.value)+1:Number(el.value)-1);el.dispatchEvent(new Event('input',{bubbles:true}));});
    }else if(await select.count()){
     await select.evaluate(el=>{el.selectedIndex=(el.selectedIndex+1)%el.options.length;el.dispatchEvent(new Event('change',{bubbles:true}));});
    }else if(await step.count())await step.click();
    else await button.click();
    if(name==='shares'){
     assert.equal(await view.innerHTML(),before,'Hidden-secret changes must preserve the observed two shares');
     assert.equal(await lab.locator('[data-output=secret]').textContent(),'5');
     await lab.locator('[data-set=reveal][data-value="1"]').click();
     assert.match(await view.textContent(),/6 \+ 8 \+ 8 ≡ 5/);
    }
    assert.notEqual(await view.innerHTML(),before,name+' control has no consequence');
   }
  }
  assert.equal(seen.size,21,'Every experiment type is exercised');
  // Exact user journeys and attack outcomes.
  await card('beaver-opening');let lab=page.locator('article[data-active=true] [data-lab=beaver]');assert.equal(await lab.locator('.broadcast-row').count(),3);await set(lab,'x',10);await set(lab,'y',4);assert.match(await lab.locator('.lab-view').textContent(),/6 = 10×4/);
  await card('public-constants');lab=page.locator('article[data-active=true] [data-lab=constants]');await lab.locator('[data-set=rule][data-value=all]').click();assert(await lab.locator('.readout.bad').isVisible());await lab.locator('select').selectOption('multiply');assert.equal(await lab.locator('[data-set=rule]:visible').count(),0);
  await card('mac-security');lab=page.locator('article[data-active=true] [data-lab=mac]');await set(lab,'delta',1);await set(lab,'guess',0);assert.match(await lab.locator('.readout').textContent(),/rejected/);await set(lab,'guess',7);assert.match(await lab.locator('.readout').textContent(),/accepted/);await set(lab,'guess',0);await lab.locator('[data-set=rushing][data-value="1"]').click();assert.match(await lab.locator('.readout').textContent(),/accepted/);
  await card('shamir-generation');lab=page.locator('article[data-active=true] [data-lab=shamir]');await set(lab,'alpha',7);await lab.locator('[data-set=third][data-value="1"]').click();assert(await lab.locator('.readout.bad').isVisible());await set(lab,'alpha',6);assert(await lab.locator('.readout.good').isVisible());
  await card('mpc-goal');await page.locator('article[data-active=true] input[type=number]').fill('12');await page.locator('article[data-active=true] form button').click();assert(await page.locator('article[data-active=true] .answer-feedback.bad').isVisible());await page.locator('article[data-active=true] input[type=number]').fill('13');await page.locator('article[data-active=true] form button').click();assert(await page.locator('article[data-active=true] .answer-feedback.good').isVisible());
  await card('simulation-test');await page.locator('article[data-active=true] textarea').fill('Choose inputs 2 and 7; the equality bit remains 0.');await page.reload({waitUntil:'networkidle'});assert.match(await page.locator('article[data-active=true] textarea').inputValue(),/2 and 7/);await page.locator('article[data-active=true] details.solution').evaluate(e=>e.open=true);await page.locator('article[data-active=true] [data-self=ready]').click();assert.match(await page.locator('article[data-active=true] .answer-feedback').textContent(),/tick/);for(const box of await page.locator('article[data-active=true] .rubric input').all())await box.check();await page.locator('article[data-active=true] [data-self=ready]').click();assert.match(await page.locator('article[data-active=true] .check-state').textContent(),/Self-checked/);
  // Popup, homework route, slider, deep links, history and narrow/wide layout.
  await page.locator('#menu-toggle').click();assert(await page.locator('#chapter-panel').isVisible());await page.locator('#mode').selectOption('homework');assert.equal(await page.locator('article[data-active=true]').getAttribute('id'),'hw6-1ai');assert.equal(await page.locator('#deck-slider').getAttribute('max'),'16');await page.locator('#next').click();await page.waitForFunction(()=>location.hash==='#hw6-1aii');await page.goBack();await page.waitForFunction(()=>location.hash==='#hw6-1ai');
  await page.locator('#deck-slider').evaluate(el=>{el.value='16';el.dispatchEvent(new Event('input',{bubbles:true}));});await page.waitForFunction(()=>location.hash==='#hw6-4d');
  for(const width of [320,390,768]){await page.setViewportSize({width,height:812});await card('beaver-opening');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.screenshot({path:path.join(out,`beaver-${width}.png`)});}
  // A long rubric equation must scroll within the text column beside its checkbox.
  await page.setViewportSize({width:320,height:812});await card('hw6-3a');
  await page.locator('article[data-active=true] details.solution').evaluate(e=>e.open=true);
  const rubricOverflow=await page.locator('article[data-active=true] .rubric label').evaluateAll(labels=>labels.some(label=>label.querySelector('span').getBoundingClientRect().right>label.getBoundingClientRect().right+1));
  assert.equal(rubricOverflow,false,'Rubric text must stay inside its checkbox row');
  await page.setViewportSize({width:375,height:812});await page.goto(base+'/hw6/#hw6-2e',{waitUntil:'networkidle'});assert.equal(await page.locator('article.lesson').count(),16);assert.equal(await page.locator('article[data-active=true]').getAttribute('id'),'hw6-2e');assert.equal(await page.locator('#deck-slider').getAttribute('max'),'16');
  const fallback=await browser.newContext({javaScriptEnabled:false,viewport:{width:375,height:812}});const nojs=await fallback.newPage();await nojs.goto(base+'/mpc-workbench/#beaver-identity');assert.equal(await nojs.locator('article.lesson:visible').count(),48);assert(await nojs.locator('#beaver-identity [role=math]').count()>0);assert.equal(await nojs.locator('#beaver-identity details.solution').getAttribute('open'),null);assert(await nojs.locator('#beaver-identity .static-nav a').first().isVisible());
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
  console.log(`PASS MPC browser: all48 cards and expanded solutions at375px; ${seen.size} lab types; attack/reconstruction outcomes; answer feedback, drafts and self-checks; homework route, history, slider;320/390/768px; no-JS content. Screenshots: ${out}`);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
