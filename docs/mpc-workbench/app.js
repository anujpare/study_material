(() => {
'use strict';
const $=s=>document.querySelector(s), all=s=>[...document.querySelectorAll(s)];
const cards=all('article.lesson');
const KEY='pets-mpc-progress-v1';
let state={mode:'guided',last:cards[0]?.id,checks:{},drafts:{}};
try{const saved=JSON.parse(localStorage.getItem(KEY)||'null');if(saved&&typeof saved==='object')state={...state,...saved,checks:saved.checks||{},drafts:saved.drafts||{}};}catch{}
if(![...document.querySelector('#mode').options].some(o=>o.value===state.mode))state.mode='guided';
let current, empty=false;
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(state));}catch{}};
const route=()=>state.mode==='homework'?cards.filter(c=>c.dataset.kind==='homework').sort((a,b)=>Number(a.dataset.homeworkOrder)-Number(b.dataset.homeworkOrder)):state.mode==='review'?cards.filter(c=>state.checks[c.id]?.status==='practice'):cards;
const status=id=>state.checks[id]?.status;
function updateStatus(card){
 const s=status(card.id), label=card.querySelector('.check-state');
 if(label)label.textContent=s==='ready'?'Self-checked · revisit whenever you like.':s==='correct'?'Correct · your reasoning check is saved on this device.':s==='practice'?'Marked for another attempt.':'';
}
function updateNav(){
 const list=route(),i=list.indexOf(current);empty=list.length===0;
 $('#counter').textContent=empty?'0 / 0':i>=0?`${i+1} / ${list.length}`:'Linked lesson';
 $('#position').textContent=$('#counter').textContent;
 $('#deck-slider').max=String(Math.max(1,list.length));$('#deck-slider').value=String(Math.max(1,i+1));$('#deck-slider').disabled=empty;
 $('#deck-slider').setAttribute('aria-valuetext',empty?'No cards need another attempt':`${i+1} of ${list.length}: ${current?.dataset.title||''}`);
 $('#previous').disabled=empty||i<=0;$('#next').disabled=empty||i===list.length-1;
 const learned=cards.filter(c=>['correct','ready'].includes(status(c.id))).length;
 $('#route-status').textContent=state.mode==='homework'?'HW6 · assignment practice':state.mode==='review'?'Questions to revisit':`${learned} / ${cards.length} checked`;
 $('#mode').value=state.mode;$('#lesson-select').value=current?.id||'';
 $('#saved-progress').textContent=`${learned} checks completed · ${cards.filter(c=>status(c.id)==='practice').length} marked to revisit. Answers stay in this browser.`;
}
function closeMenu(){ $('#chapter-panel').hidden=true;$('#menu-toggle').setAttribute('aria-expanded','false'); }
function show(id,{focus=false}={}){
 const found=cards.find(c=>c.id===id);current=found||route()[0]||cards[0];
 for(const c of cards){const active=c===current&&!empty;c.dataset.active=String(active);c.hidden=!active;}
 $('#empty-state').hidden=!empty;
 if(current&&!empty){state.last=current.id;document.title=`PETS · MPC · ${current.dataset.title}`;window.MPCLabs?.init(current);updateStatus(current);}
 updateNav();
 if(empty){for(const c of cards)c.hidden=true;$('#empty-state').hidden=false;}
 $('#lesson').scrollTop=0;closeMenu();save();if(focus)$('#lesson').focus({preventScroll:true});
}
function go(id){if(location.hash.slice(1)===id)show(id,{focus:true});else location.hash=id;}
function setMode(mode){state.mode=mode;empty=route().length===0;const list=route();save();if(list.length){if(!list.includes(current))go(list[0].id);else show(current.id);}else show(current?.id);}
$('#menu-toggle').addEventListener('click',()=>{const open=$('#chapter-panel').hidden;$('#chapter-panel').hidden=!open;$('#menu-toggle').setAttribute('aria-expanded',String(open));});
document.addEventListener('click',e=>{if(!e.target.closest('#chapter-panel')&&!e.target.closest('#menu-toggle'))closeMenu();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();$('#menu-toggle').focus();}if(e.target.matches('input,textarea,select')||e.target.isContentEditable)return;if(e.altKey||e.ctrlKey||e.metaKey)return;if(e.key==='ArrowRight')$('#next').click();if(e.key==='ArrowLeft')$('#previous').click();});
$('#mode').addEventListener('change',e=>setMode(e.target.value));
$('#lesson-select').addEventListener('change',e=>{const target=cards.find(c=>c.id===e.target.value);if(!route().includes(target)){state.mode='guided';empty=false;}go(e.target.value);});
$('#deck-slider').addEventListener('input',e=>{const c=route()[Number(e.target.value)-1];if(c)go(c.id);});
$('#previous').addEventListener('click',()=>{const list=route(),i=list.indexOf(current);if(i>0)go(list[i-1].id);});
$('#next').addEventListener('click',()=>{const list=route(),i=list.indexOf(current);if(i+1<list.length)go(list[i+1].id);});
$('#return-guided').addEventListener('click',()=>setMode('guided'));
window.addEventListener('hashchange',()=>{empty=route().length===0;const id=decodeURIComponent(location.hash.slice(1));if(!route().some(c=>c.id===id)&&cards.some(c=>c.id===id)){state.mode='guided';empty=false;}show(id,{focus:true});});
function record(card,good,manual=false){state.checks[card.id]={status:good?(manual?'ready':'correct'):'practice',at:Date.now()};save();updateStatus(card);updateNav();}
for(const card of cards){
 const check=card.querySelector('.checkpoint');if(!check)continue;
 const feedback=check.querySelector('.answer-feedback'),data=JSON.parse(check.querySelector('script.check-data').textContent);
 const showFeedback=(html,good)=>{feedback.hidden=false;feedback.innerHTML=html;feedback.classList.toggle('good',good);feedback.classList.toggle('bad',!good);};
 check.querySelectorAll('[data-choice]').forEach(btn=>btn.addEventListener('click',()=>{const chosen=Number(btn.dataset.choice),good=chosen===data.answer;check.querySelectorAll('[data-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));showFeedback(data.feedback?.[chosen]||'<p>Compare your reasoning with the worked solution.</p>',good);record(card,good);}));
 const form=check.querySelector('form.number-answer');if(form)form.addEventListener('submit',e=>{e.preventDefault();const input=form.querySelector('input'),v=input.value.trim();if(v===''||!Number.isFinite(Number(v))){input.focus();return;}const good=Math.abs(Number(v)-data.answer)<1e-9;showFeedback(good?(data.correctFeedback||'<p>Correct. Open the worked solution to compare the calculation.</p>'):(data.wrongFeedback||'<p>That value does not satisfy the required relation. Try the hint, then check the algebra in the solution.</p>'),good);record(card,good);});
 const draft=check.querySelector('textarea');if(draft){draft.value=state.drafts[card.id]||'';draft.addEventListener('input',()=>{state.drafts[card.id]=draft.value;save();});}
 check.querySelectorAll('[data-self]').forEach(b=>b.addEventListener('click',()=>{const good=b.dataset.self==='ready';if(good){const boxes=[...check.querySelectorAll('.rubric input')];if(boxes.some(x=>!x.checked)){showFeedback('<p>Compare each point in the marking guide with your answer, then tick the points you can justify.</p>',false);return;}}record(card,good,true);showFeedback(good?'<p>Your answer is marked self-checked. This records your own review of the proof; it is not automatic grading.</p>':'<p>This question is saved in “Try again”. You can return to the explanation now and attempt it later.</p>',good);}));
 updateStatus(card);
}
const explicit=decodeURIComponent(location.hash.slice(1));if(explicit&&!route().some(c=>c.id===explicit)&&cards.some(c=>c.id===explicit))state.mode='guided';
document.documentElement.classList.add('reader-ready');empty=route().length===0;show(explicit||state.last||cards[0]?.id);
})();
