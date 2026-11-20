'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs');
const {math:m,labNames,renderLab}=require('../docs/mpc-workbench/labs.js');
const map=JSON.parse(fs.readFileSync('docs/mpc-workbench/source-map.json','utf8'));
const wanted=['HW6 1(a.i)','HW6 1(a.ii)','HW6 1(b)','HW6 1(c)','HW6 2(a)','HW6 2(b)','HW6 2(c)','HW6 2(d)','HW6 2(e)','HW6 3(a)','HW6 3(b)','HW6 3(c)','HW6 4(a)','HW6 4(b)','HW6 4(c)','HW6 4(d)'];
assert.equal(map.length,48);assert.equal(new Set(map.map(c=>c.id)).size,48);
assert.deepEqual(map.filter(c=>c.kind==='homework').map(c=>c.exercise).sort(),wanted.sort());
for(let i=0;i<map.length;i++){assert(map[i].requires.every(id=>map.slice(0,i).some(c=>c.id===id)),map[i].id+' has an unintroduced prerequisite');assert(map[i].source);assert(map[i].check_type);}
for(const [path,count] of [['docs/mpc-workbench/index.html',48],['docs/hw6/index.html',16]]){
 const html=fs.readFileSync(path,'utf8');assert.equal((html.match(/<article class="lesson"/g)||[]).length,count);assert.equal((html.match(/<section class="checkpoint"/g)||[]).length,count);assert.equal((html.match(/<details class="solution">/g)||[]).length,count);
 assert(!/data-mjx-error|<merror|fill="red"|\{\{lab:|src="https?:/.test(html));
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,new Set(ids).size,'duplicate IDs in '+path);
 for(const link of html.matchAll(/href="#([^"]+)"/g))assert(ids.includes(link[1]),'broken hash '+link[1]);
 for(const t of html.matchAll(/<script type="application\/json" class="check-data">(.*?)<\/script>/gs)){const q=JSON.parse(t[1]);assert(['choice','number','written'].includes(q.type));}
 assert(!/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(html));
}
for(let x=0;x<17;x++)for(let y=0;y<17;y++){
 const b=m.beaver(x,y);assert.equal(m.sum(b.xs),x);assert.equal(m.sum(b.ys),y);assert.equal(b.result,m.mod(x*y));assert.equal(m.sum(b.ds),b.d);assert.equal(m.sum(b.es),b.e);
 const s=m.square(x,y);assert.equal(s.result,m.mod(x*x));assert.equal(m.sum(s.as),y);assert.equal(m.sum(s.a2s),m.mod(y*y));
 const f=m.polynomial(x,y);assert.equal(f.result,m.mod(2+3*x+x*x+2*x*x*x));
 const a=m.mac(x,y);assert.equal(a.residual,m.mod(x*(7-y)));assert.equal(m.mac(x,y,true).residual,0);
}
for(let delta=1;delta<17;delta++)assert.equal(Array.from({length:17},(_,guess)=>m.mac(delta,guess).residual).filter(r=>r===0).length,1);
const indices=[1,2,3,4,5];let subsets=0;
for(let a=0;a<3;a++)for(let b=a+1;b<4;b++)for(let c=b+1;c<5;c++){const I=[indices[a],indices[b],indices[c]],w=m.lagrange(I),values=I.map(i=>m.poly(6,4,2,i));assert.equal(m.sum(w.map((v,i)=>v*values[i])),6);subsets++;}assert.equal(subsets,10);
for(let alpha=0;alpha<17;alpha++){const c=m.compatible(alpha);assert.equal(c.points[1][1],12);assert.equal(c.points[2][1],5);assert.equal(c.points[0][1],alpha);assert.equal(c.points[3][1]===2,alpha===6);}
for(const name of labNames){const html=renderLab(name);assert(!/undefined|NaN/.test(html),name);assert(html.includes('class="lab-view"'));}
console.log('PASS MPC content: 48 source-mapped cards, all 16 HW6 subquestions, closed solutions, prerequisites, static math and no runtime CDN.');
console.log('PASS MPC arithmetic: exhaustive F17 input pairs for Beaver/squares/polynomials/MAC, all Shamir triples and candidate secrets.');
