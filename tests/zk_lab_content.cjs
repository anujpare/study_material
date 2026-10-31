// Structural regression tests for the independent PETS Zero Knowledge workbench.
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.join(__dirname,"..","docs","zk-workbench");
const read=(p)=>fs.readFileSync(path.join(root,p),"utf8");
const app=read("app.js");
new Function(app);
const cards=[...app.matchAll(/\["([^"]+)","([^"]+)","([^"]+\.html)"\]/g)].map(m=>({id:m[1],title:m[2],file:m[3]}));
assert.equal(cards.length,35);
assert.equal(new Set(cards.map(c=>c.id)).size,35);
assert.deepEqual(cards.slice(0,3).map(c=>c.id),["np","interaction","guarantees"]);
const core=app.match(/const coreIds=new Set\(\[([\s\S]*?)\]\)/);
assert(core,"Guided route missing");
const guided=[...core[1].matchAll(/"([^"]+)"/g)].map(m=>m[1]);
assert.equal(guided.length,32);
for(const id of guided)assert(cards.some(c=>c.id===id),"Missing guided ID "+id);
const index=read("index.html");
assert(index.includes("32 lessons")&&index.includes("35 lessons"));
for(const card of cards){
 const html=read(card.file);
 assert(html.startsWith('<article class="lesson">'),card.id+" missing root");
 assert(html.trim().endsWith("</article>"),card.id+" unclosed root");
 assert.equal((html.match(/<div\b/g)||[]).length,(html.match(/<\/div>/g)||[]).length,card.id+" unbalanced divs");
 assert.equal((html.match(/\\\(/g)||[]).length,(html.match(/\\\)/g)||[]).length,card.id+" unbalanced inline math");
 assert.equal((html.match(/\\\[/g)||[]).length,(html.match(/\\\]/g)||[]).length,card.id+" unbalanced display math");
 assert.equal((html.match(/<article\b/g)||[]).length,1,card.id+" multiple root articles");
 assert(html.includes('class="lead"'),card.id+" missing teaching context");
 assert(html.includes('class="source"'),card.id+" missing source reference");
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(new Set(ids).size,ids.length,card.id+" duplicate element id");
}
const np=read("card-02.html");
assert(np.includes("public <strong>input"),"The public input must be named before NP");
assert(np.indexOf("a <strong>witness")<np.toLowerCase().indexOf("definition of np"));
assert(np.includes("factor-p")&&np.includes("factor-q"),"Prime-factor witness control must remain in the opening lesson");
assert(read("card-01.html").includes("np-slider"),"Graph search control belongs in Hamiltonicity lesson");
assert(read("card-20.html").includes("gate-diagram-shared"),"Two gate circuit requires one shared committed wire");
const per=read("card-07.html");
assert(per.includes("perm-select")&&per.includes("perm-table"));
assert(app.includes('case"perm-select"'));
const worlds=read("card-05.html");
assert(worlds.includes("zk-worlds"));
assert(read("card-08.html").includes("zk-exchange"));
assert(read("card-12.html").includes('id="schedule-messages"'));
assert(app.includes("function scheduleUpdate()"));
const schnorr=read("card-17.html");
for(const id of ["schnorr-msg-u-p","schnorr-msg-c-v","schnorr-msg-z-v"])assert(schnorr.includes(id));
assert(read("card-21.html").includes('id="fs-flow"'));
for(const map of [{1:2,2:4,3:1,4:5,5:3},{1:5,2:3,3:2,4:1,5:4}]){
 assert.equal(new Set(Object.values(map)).size,5);
 assert(Object.keys(map).filter(k=>map[k]!==Number(k)).length>=4);
}
console.log("PASS ZK lab source order, 35 deep links, HTML/math structure and interactive prerequisites");
