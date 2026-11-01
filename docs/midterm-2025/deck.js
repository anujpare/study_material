/* PETS 2025: one original question per card, using the existing homework reader. */
(() => {
'use strict';
const root=document.getElementById('lessons'),qs=window.PETS_MIDTERM_QUESTIONS||[],defs=window.PETS_MIDTERM_DEFINITIONS||[];
const solutions=window.PETS_MIDTERM_SOLUTIONS||{},foundations=window.MIDTERM_FOUNDATIONS||{},labs=window.PETS_MIDTERM_LABS||{};
if(!root||qs.length!==17){if(root)root.textContent='The original exam questions did not load.';return;}
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
const prevIcon='<svg aria-hidden="true" viewBox="0 0 24 24"><path d="m14.5 6.5-5.5 5.5 5.5 5.5"/></svg>';
const nextIcon='<svg aria-hidden="true" viewBox="0 0 24 24"><path d="m9.5 6.5 5.5 5.5-5.5 5.5"/></svg>';
const cards=[];for(const q of qs){for(const d of defs.filter(d=>d.before===q.id))cards.push({id:d.id,title:d.title,page:d.page,type:'definition',def:d});cards.push({id:'exam-'+q.id,title:'Midterm Q'+q.group+'('+q.id.slice(1).replace(/([bcd])([12])$/,'$1.$2')+') · '+q.title,page:q.page,type:'question',q});}
function questionHTML(q){
 const prereq=foundations[q.id]||[],steps=solutions[q.id]||[];
 const choices=q.group===1?'<div class="exam-choice" role="group" aria-label="Choose true or false"><button type="button" data-answer="true">TRUE</button><button type="button" data-answer="false">FALSE</button><output aria-live="polite">Choose an answer before opening the solution.</output></div>':'';
 const prep=prereq.length?'<details class="midterm-prep" open><summary>Learn the prerequisites · '+prereq.length+' focused steps</summary><div class="mini-lesson"><span class="mini-count">Step <span data-mini-index>1</span> / '+prereq.length+'</span><h3 data-mini-title></h3><div data-mini-body></div><div class="mini-buttons"><button type="button" data-mini-prev>← Previous</button><button type="button" data-mini-next>Next idea →</button></div></div></details>':'';
 const worked='<details class="solution midterm-solution"><summary>Reveal step-by-step solution</summary><div class="solution-content"><ol class="midterm-worked">'+steps.map((s,i)=>'<li data-step="'+i+'" '+(i?'hidden':'')+'><strong>'+s[0]+'</strong><div>'+s[1]+'</div></li>').join('')+'</ol><div class="mini-buttons"><button type="button" data-reveal-next>Reveal next step →</button><button type="button" data-show-all>Show all steps</button></div><p class="mini-count"><span data-solution-count>1</span> / '+steps.length+' steps</p></div></details>';
 const givenMap={'2a':'psi-def','2b':'psi-def','2c1':'hash-def','2c2':'hash-def','2d1':'oprf-def','2d2':'oprf-def','2e':'oprf-def','3a':'voting-def','3b1':'dpf-def','3b2':'dpf-def','3c1':'iop-def','3c2':'iop-def'};
 const givenId=givenMap[q.id];
 const givenDef=defs.find(d=>d.id===givenId);
 const context=givenDef?'<details class="midterm-given" '+(['2c1','2c2','3b1','3b2'].includes(q.id)?'open':'')+'><summary>Given in the original exam: '+esc(givenDef.title)+'</summary><div class="given-content">'+givenDef.content+'</div></details>':'';
 const previousProtocol=q.id==='2d2'?'<p class="source-note"><b>Protocol from (d.1):</b> Bob chooses a key k, sends Y_B={F(k,b):b∈B}, Alice uses the OPRF on every a∈A, and returns the members of A whose keyed outputs occur in Y_B.</p>':'';
 const note=q.id==='3c2'?'<p class="source-note">The question refers to “part (a)” as printed, although the voting construction is in (b.1). The separately posted correction fixes the solution’s query count to k, rather than three.</p>':'';
 return '<p class="source-label">Original 2025 exam · Page '+q.page+' · '+q.marks+' '+(q.marks===1?'mark':'marks')+'</p><div class="problem-statement exact-question">'+q.question+'</div>'+note+context+previousProtocol+choices+prep+(labs[q.id]||'')+worked;
}
function definitionHTML(d){return '<p class="source-label">Printed in the 2025 exam · Page '+d.page+'</p><div class="problem-statement">'+d.content+'</div><p class="source-note">This is a provided exam definition or instruction, not a separate question. Continue to the next card for the original question.</p>';}
const slide=(card,i)=>{
 const before=cards[i-1],after=cards[i+1];
 const back=before?'<a class="navbtn" href="#'+before.id+'" aria-label="Previous card">'+prevIcon+'</a>':'';
 const next=after?'<a class="navbtn" href="#'+after.id+'" aria-label="Next card">'+nextIcon+'</a>':'';
 const body=card.type==='definition'?definitionHTML(card.def):questionHTML(card.q);
 return '<section class="slide '+(card.type==='definition'?'midterm-definition':'homework midterm-question')+'" id="'+card.id+'" data-source="Midterm 2025 page '+card.page+'"><header class="head"><div class="section">'+esc(card.title)+'</div></header><article class="reading">'+body+'</article><nav aria-label="Card navigation" class="nav">'+back+next+'</nav></section>';
};
const footer=root.querySelector('.deck-jump');if(!footer)throw Error('Shared PETS card slider missing');
footer.insertAdjacentHTML('beforebegin',cards.map(slide).join(''));
for(const section of root.querySelectorAll('.midterm-question')){
 const id=section.id.replace('exam-',''),prep=foundations[id]||[],mini=section.querySelector('.mini-lesson');
 if(prep.length&&mini){
  let i=0;
  const draw=()=>{mini.querySelector('[data-mini-index]').textContent=i+1;mini.querySelector('[data-mini-title]').textContent=prep[i][0];mini.querySelector('[data-mini-body]').innerHTML=prep[i][1];mini.querySelector('[data-mini-prev]').disabled=i===0;mini.querySelector('[data-mini-next]').disabled=i===prep.length-1;};
  mini.querySelector('[data-mini-prev]').onclick=()=>{i=Math.max(0,i-1);draw();};
  mini.querySelector('[data-mini-next]').onclick=()=>{i=Math.min(prep.length-1,i+1);draw();};
  draw();
 }
 const box=section.querySelector('.midterm-solution');
 if(box){
  const steps=[...box.querySelectorAll('[data-step]')];let visible=1;
  const reveal=(all)=>{visible=all?steps.length:Math.min(visible+1,steps.length);steps.forEach((el,i)=>el.hidden=i>=visible);box.querySelector('[data-solution-count]').textContent=visible;box.querySelector('[data-reveal-next]').disabled=visible===steps.length;};
  box.querySelector('[data-reveal-next]').onclick=()=>reveal(false);
  box.querySelector('[data-show-all]').onclick=()=>reveal(true);
 }
 section.querySelectorAll('[data-answer]').forEach(button=>button.onclick=()=>{
  section.querySelectorAll('[data-answer]').forEach(el=>el.setAttribute('aria-pressed',String(el===button)));
  section.querySelector('.exam-choice output').textContent='Your answer is selected. Open the worked solution to check it.';
 });
}
window.PETS_MIDTERM_CARD_COUNT=cards.length;
})();