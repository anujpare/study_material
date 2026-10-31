const assert=require("node:assert/strict");
const {chromium}=require("playwright");
const base=process.env.PETS_TEST_URL||"http://127.0.0.1:8765";
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:["--no-sandbox"]});
 try{
  const page=await browser.newPage({viewport:{width:390,height:844}});
  const errors=[];
  page.on("pageerror",e=>errors.push(e.message));
  async function lesson(id){
   await page.goto(base+"/zk-workbench/#"+id,{waitUntil:"domcontentloaded"});
   await page.locator("article.lesson").waitFor({timeout:15000});
  }
  await lesson("np");
  assert.match(await page.locator("article h1").textContent(),/prove a statement/i);
  await page.locator("#next").click();
  await page.waitForFunction(()=>location.hash==="#interaction");
  await lesson("permutation");
  const first=await page.locator("#perm-result").textContent();
  await page.locator('[data-demo="perm-select"][data-value="two"]').click();
  assert.notEqual(await page.locator("#perm-result").textContent(),first);
  assert(await page.locator("#perm-table table").isVisible());
  await lesson("repetition");
  const sequential=await page.locator("#schedule-messages .zk-exchange-row").count();
  await page.locator('[data-demo="schedule"][data-value="parallel"]').click();
  const parallel=await page.locator("#schedule-messages .zk-exchange-row").count();
  assert.equal(sequential,9);
  assert.equal(parallel,3);
  await lesson("schnorr");
  const firstZ=await page.locator("#schnorr-msg-z-p").textContent();
  await page.locator("#schnorr-c").evaluate(el=>{el.value="5";el.dispatchEvent(new Event("input",{bubbles:true}));});
  assert.notEqual(await page.locator("#schnorr-msg-z-p").textContent(),firstZ);
  await lesson("fiat-shamir");
  assert.equal(await page.locator("#fs-flow .zk-exchange-row").count(),3);
  await page.locator('[data-demo="fs"][data-value="noninteractive"]').click();
  assert.equal(await page.locator("#fs-flow .zk-exchange-row").count(),1);
  for(const width of [375,768]){
    await page.setViewportSize({width,height:820});
    await lesson("interaction");
    const dims=await page.evaluate(()=>({width:innerWidth,content:document.documentElement.scrollWidth}));
    assert(dims.content<=dims.width+4,"Page overflows at "+width+"px");
  }
  assert.deepEqual(errors,[]);
  console.log("PASS ZK lab: guided navigation, permutations, message flows and mobile viewport");
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
