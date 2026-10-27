(() => {
"use strict";
const chapterFiles=["part-1.html","part-2.html","part-3.html","part-4.html","part-5.html"];
const chapters=["I · Why SNARGs exist","II · Polynomial reasoning","III · Commitments & Fiat–Shamir","IV · PLONK from circuits","V · Examination workshop"];
const byId=id=>document.getElementById(id);
const main=byId("lesson"), select=byId("lesson-select"), chapter=byId("chapter-select");
const prev=byId("previous"), next=byId("next");
let cards=[],current=0,req=0,mathReady=false;
const mod=(x,p)=>((x%p)+p)%p;
const escape=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const gcdPow=(a,b,p)=>{let x=1;a=mod(a,p);while(b>0){if(b%2)x=x*a%p;a=a*a%p;b=Math.floor(b/2);}return x;};
window.addEventListener("mathjax-ready",()=>{mathReady=true;typeset(main);});
let mathQueue=Promise.resolve();
function typeset(node){if(!window.MathJax?.typesetPromise)return Promise.resolve();mathQueue=mathQueue.catch(()=>{}).then(()=>MathJax.typesetPromise([node])).catch(e=>console.warn("MathJax",e));return mathQueue;}
function htmlOut(el,html){if(window.MathJax?.typesetClear)try{MathJax.typesetClear([el])}catch(e){};el.innerHTML=html;typeset(el);}
function val(lab,key,def){let el=lab.querySelector('[data-key="'+key+'"]');return el?Number(el.value):def;}
function txt(lab,html){let out=lab.querySelector(".lab-output");if(out)htmlOut(out,html);}
function grid(vals,pred,current){return '<div class="lab-grid">'+vals.map(v=>'<span class="'+(pred(v)?"root ":"")+(v===current?"current":"")+'">'+v+'</span>').join("")+'</div>';}
function initLab(lab){
 const type=lab.dataset.lab;
 const update=()=>{
  if(type==="ring"){
    const r=val(lab,"r",3),y=mod(2*r*r+4*r,6);
    txt(lab,'\\(f('+r+')='+y+'\\pmod 6\\). '+(y===0?'This is a root.':'This is not a root.')+' The four roots are 0, 1, 3, and 4.'+grid([0,1,2,3,4,5],x=>mod(2*x*x+4*x,6)===0,r));
  }
  if(type==="pcp"){
    const t=val(lab,"t",4),err=1/Math.pow(2,t);
    txt(lab,'<b>'+t+' independent PCP tests</b> require '+(3*t)+' bit openings in the three-query version. For a fixed false-proof string, \\(\\Pr[\\mathrm{all\\ pass}]\\le 2^{-'+t+'}='+err.toFixed(6)+'\\).<p class="note">This is a bound, not a simulation of a PCP encoding. Independence holds because fresh verifier randomness is used for each test against the same fixed proof.</p>');
  }
  if(type==="eq"){
    const r=val(lab,"r",1),f=mod(r*r+1,17),g=mod(f+(r-1)*(r-4),17),pass=f===g;
    txt(lab,'\\(f('+r+')='+f+'\\), \\(g('+r+')='+g+'\\) in \\(\\mathbb F_{17}\\). <b>'+(pass?'False acceptance':'Rejection')+'</b>.'+grid(Array.from({length:17},(_,i)=>i),x=>x===1||x===4,r)+'<p class="note">Only points 1 and 4 make \\(f-g\\) vanish: exactly 2 false-accept challenges out of 17.</p>');
  }
  if(type==="zero"){
    const r=val(lab,"r",3),fake=lab.querySelector('[data-key="fake"]')?.checked??true;
    const z=mod((r-1)*(r-2),17),q=mod(r+3,17),rhs=mod(z*q,17);
    const lhs=mod(rhs+(fake?r-3:0),17);
    txt(lab,'\\(f('+r+')='+lhs+'\\), \\(Z_\\Omega('+r+')q('+r+')='+rhs+'\\). <b>'+(lhs===rhs?'Accept':'Reject')+'</b>.'+(fake?'<p class="note">The dishonest difference polynomial is \\(h(X)=X-3\\); only \\(r=3\\) fools this verifier.</p>':'<p class="note">The honest identity holds for every challenge.</p>'));
  }
  if(type==="interp"){
    const y0=val(lab,"a",1),y1=val(lab,"b",3),y2=val(lab,"c",2);
    const q=mod((y2-2*y1+y0)*9,17),a=mod(y1-y0,17);
    txt(lab,'The unique degree-at-most-two interpolant is \\(f(X)='+y0+'+'+a+'X+'+q+'X(X-1)\\pmod{17}\\).<br> Check: \\(f(0)='+y0+'\\), \\(f(1)='+y1+'\\), \\(f(2)='+y2+'\\).<p class="note">Here 9 is the multiplicative inverse of 2 modulo 17. Uniqueness follows because two distinct degree-2 polynomials cannot agree at three distinct points.</p>');
  }
  if(type==="fib"){
    let n=val(lab,"n",6),f=[0,1];for(let i=2;i<10;i++)f[i]=f[i-1]+f[i-2];
    const boxes=f.slice(0,9).map((v,i)=>'<span class="'+(n===i?"current root":"")+'">'+i+': '+v+'</span>').join("");
    txt(lab,'<div class="lab-grid">'+boxes+'</div><b>\\(F_{'+n+'}='+f[n]+'\\).</b> '+(n>=2?'The next entry is forced by \\(F_{'+(n-2)+'}+F_{'+(n-1)+'}='+f[n-2]+'+'+f[n-1]+'='+f[n]+'\\).':'This value is one of the two initial conditions.') );
  }
  if(type==="unity"){
    const j=val(lab,"j",3),v=gcdPow(6,j,97),vals=Array.from({length:12},(_,i)=>gcdPow(6,i,97));
    txt(lab,'\\(6^{'+j+'}\\equiv '+v+'\\pmod{97}\\).'+grid(vals,x=>false,v)+'<p class="note">All twelve listed elements are distinct, and \\(6^{12}\\equiv1\\), so 6 has multiplicative order 12.</p>');
  }
  if(type==="schnorr"){
    const r=val(lab,"r",4),c=val(lab,"c",2),u=gcdPow(2,r,23),z=mod(r+3*c,11),left=gcdPow(2,z,23),right=mod(u*gcdPow(8,c,23),23);
    txt(lab,'\\(u=2^{'+r+'}\\equiv '+u+'\\pmod{23}\\), \\(z='+r+'+3\\cdot'+c+'\\equiv '+z+'\\pmod{11}\\).<br> Verifier checks \\(2^{'+z+'}\\equiv '+left+'\\) and \\(u\\cdot8^{'+c+'}\\equiv '+right+'\\pmod{23}\\). <b>They agree.</b><p class="note">The challenge slider represents the verifier; Fiat–Shamir replaces this externally sent value with a hash-derived value. These tiny parameters are only for arithmetic.</p>');
  }
  if(type==="challenges"){
    const t=val(lab,"t",3),total=2**t;
    txt(lab,'A fixed cheating first-message vector can answer <b>at most one</b> of '+total+' challenge vectors. Hence \\(\\Pr[\\mathrm{accept}]\\le 1/'+total+'=2^{-'+t+'}\\).'+grid(Array.from({length:total},(_,i)=>i.toString(2).padStart(t,"0")),x=>x===("0".repeat(t)),null)+'<p class="note">Each string is one possible vector of verifier bits. This is a counting proof only after we establish why a false statement allows at most one answerable challenge per coordinate.</p>');
  }
  if(type==="merkle"){
    const selected=val(lab,"i",4);const path=[],sib=[];let k=selected+7;while(k>1){path.push(k);sib.push(k^1);k=Math.floor(k/2);}path.push(1);
    const level=(i)=>Math.floor(Math.log2(i)),xAt=(i)=>{let l=level(i),j=i-2**l;return (j+.5)*(520/2**l)},yAt=(i)=>28+level(i)*71;
    let svg='<svg viewBox="0 0 520 267" role="img" aria-label="Merkle tree. Blue nodes are the selected authentication branch, amber nodes are sibling hashes needed for the opening.">';
    for(let i=2;i<=15;i++){const p=Math.floor(i/2);svg+='<path d="M'+xAt(p)+' '+(yAt(p)+14)+' L'+xAt(i)+' '+(yAt(i)-14)+'" stroke="#aebfc9" stroke-width="2" fill="none"/>';}
    for(let i=1;i<=15;i++){const active=path.includes(i),proof=sib.includes(i),fill=active?"#1b7292":proof?"#d19a50":"#e5edf0";
      const label=i>=8?String(i-7):i===1?"c":"H";
      svg+='<circle cx="'+xAt(i)+'" cy="'+yAt(i)+'" r="18" fill="'+fill+'" stroke="'+(active?"#0f4c66":"#91a6b1")+'" stroke-width="'+(active?3:1)+'"/><text x="'+xAt(i)+'" y="'+(yAt(i)+5)+'" fill="'+(active||proof?"#fff":"#314d5b")+'" font-size="14" font-weight="700" text-anchor="middle">'+label+'</text>';
    }
    svg+='</svg>';lab.querySelector("#merkle-svg").innerHTML=svg;
    txt(lab,'To open message <b>\\(m_{'+selected+'}\\)</b>, send its value and '+sib.length+' sibling hashes (amber). The verifier hashes upward along the blue branch and compares the resulting root with commitment \\(c\\). Only '+sib.length+' hashes are needed because each sibling authenticates an entire subtree.');
  }
  if(type==="trace"){
    const mode=lab.querySelector('[data-key="mode"]')?.value??"honest";
    const rows=[[2,4,8,0],[4,3,7,1],[8,7,56,0],[56,41,0,1]];
    let traceInputs=[2,4,3],publicX=[2,4],explain="";
    if(mode==="public"){traceInputs[0]=5;explain="The trace records public input 5, although the actual public input is 2, and gate 0 uses 2. Therefore public-input agreement and the copy constraint both fail.";}
    if(mode==="gate"){rows[2][2]=55;explain="Gate 2 says 8 × 7 = 55, which is false. The last gate still contains 56, so wiring also fails.";}
    if(mode==="wire"){rows[2]=[9,7,63,0];explain="Every gate row is locally correct and the output is zero, but the output of gate 0 (8) does not equal gate 2's left input (9). The output of gate 2 (63) also disagrees with the last gate's left input (56).";}
    if(mode==="output"){rows[3][2]=1;explain="The final output is 1, not zero. The final gate also violates its addition relation, as it must when the earlier fixed values and public target remain unchanged.";}
    if(mode==="honest"){explain="All four conditions pass for the augmented assertion (2×4)(4+3)−56=0. The last addition gate uses 41 ≡ −56 in the field F₉₇.";}
    const gateok=rows.map(r=>mod(r[3]===1?r[0]+r[1]-r[2]:r[0]*r[1]-r[2],97)===0);
    const pubok=traceInputs[0]===publicX[0]&&traceInputs[1]===publicX[1];
    const wireok=traceInputs[0]===rows[0][0]&&traceInputs[1]===rows[0][1]&&traceInputs[1]===rows[1][0]&&traceInputs[2]===rows[1][1]&&rows[0][2]===rows[2][0]&&rows[1][2]===rows[2][1]&&rows[2][2]===rows[3][0];
    const outputok=rows[3][2]===0;
    const tbl='<div class="table-scroll"><table><thead><tr><th>Gate</th><th>Left</th><th>Right</th><th>Out</th><th>Type</th><th>Residual</th></tr></thead><tbody>'+rows.map((r,i)=>'<tr><td>'+i+'</td><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+r[2]+'</td><td>'+(r[3]?"+":"×")+'</td><td>'+mod(r[3]?r[0]+r[1]-r[2]:r[0]*r[1]-r[2],97)+'</td></tr>').join("")+'</tbody></table></div>';
    const status=(name,ok)=>'<span style="color:'+(ok?"#146655":"#ac3136")+';font-weight:750">'+(ok?"✓ ":"✕ ")+name+'</span>';
    txt(lab,'<p class="note">Original trace input cells: \\(x_1='+traceInputs[0]+',\\;x_2='+traceInputs[1]+',\\;w_1='+traceInputs[2]+'\\). Public statement: \\(x_1=2,\\;x_2=4\\).</p>'+tbl+'<div class="two">'+[status("Public inputs",pubok),status("Gate equations",gateok.every(Boolean)),status("Wire copies",wireok),status("Final output = 0",outputok)].map(s=>'<div>'+s+'</div>').join("")+'</div><p class="note">'+explain+'</p>');
  }
 };
 lab.querySelectorAll("input,select").forEach(el=>el.addEventListener("input",update));
 update();
}

function getHash(){try{return decodeURIComponent(location.hash.slice(1))}catch(e){return ""}}
function closeMenu(){const menu=byId("chapter-menu");if(menu)menu.open=false}
function navigate(){
 const id=getHash();const found=cards.findIndex(c=>c.id===id);
 current=found>=0?found:0;
 const c=cards[current];
 if(window.MathJax?.typesetClear){try{MathJax.typesetClear([main]);}catch(e){}}
 main.innerHTML=c.html;
 main.dataset.lessonId=c.id;
 main.scrollTop=0;
 byId("header-title").textContent=c.title;
 byId("counter").textContent=(current+1)+" / "+cards.length;
 byId("position").textContent=(current+1)+" / "+cards.length;
 const slider=byId("deck-slider");
 slider.max=String(cards.length);slider.value=String(current+1);
 slider.setAttribute("aria-valuetext","Lesson "+(current+1)+" of "+cards.length+": "+c.title);
 chapter.value=String(c.chapter);
 select.innerHTML=cards.filter(x=>x.chapter===c.chapter).map(x=>'<option value="'+escape(x.id)+'">'+escape(x.title)+'</option>').join("");
 select.value=c.id;
 prev.disabled=current===0;next.disabled=current===cards.length-1;
 initLessonExtras(c.id);
 main.querySelectorAll(".lab").forEach(initLab);
 typeset(main);
 closeMenu();
}
async function start(){
 try{
  const sources=await Promise.all(chapterFiles.map(async(path,i)=>{
   const res=await fetch("./"+path,{cache:"no-store"});
   if(!res.ok)throw Error(path+" returned "+res.status);
   const source=await res.text();
   const doc=new DOMParser().parseFromString(source,"text/html");
   return [...doc.querySelectorAll("article.lesson")].map(el=>({id:el.dataset.id,title:el.dataset.title,chapter:i,html:el.innerHTML}));
  }));
  cards=sources.flat();
  if(cards.length<20)throw Error("Course chapters incomplete: "+cards.length);
  chapter.innerHTML=chapters.map((c,i)=>'<option value="'+i+'">'+escape(c)+'</option>').join("");
  chapter.addEventListener("change",()=>{
   const x=cards.find(c=>c.chapter===Number(chapter.value));
   if(x)location.hash=x.id;
  });
  select.addEventListener("change",()=>{location.hash=select.value;});
  prev.addEventListener("click",()=>{if(current>0)location.hash=cards[current-1].id;});
  next.addEventListener("click",()=>{if(current<cards.length-1)location.hash=cards[current+1].id;});
  byId("deck-slider").addEventListener("input",e=>{
   const v=Math.max(1,Math.min(cards.length,Number(e.target.value)));
   byId("position").textContent=v+" / "+cards.length;
   if(cards[v-1]?.id!==getHash())location.hash=cards[v-1].id;
  });
  document.addEventListener("keydown",e=>{
   if(e.key==="Escape"){closeMenu();return}
   if(e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;
   if(["INPUT","TEXTAREA","SELECT","BUTTON","SUMMARY"].includes(document.activeElement?.tagName)||document.activeElement?.isContentEditable)return;
   if(e.key==="ArrowRight"&&current<cards.length-1){e.preventDefault();location.hash=cards[current+1].id;}
   if(e.key==="ArrowLeft"&&current>0){e.preventDefault();location.hash=cards[current-1].id;}
  });
  document.addEventListener("pointerdown",e=>{
   const menu=byId("chapter-menu");
   if(menu?.open&&!menu.contains(e.target))closeMenu();
  });
  window.addEventListener("hashchange",navigate);
  if(!getHash())history.replaceState(null,"","#"+cards[0].id);
  navigate();
 }catch(e){main.innerHTML='<h1>Unable to load the learning lab</h1><p>'+escape(e.message)+'</p><p><a href="../">Return to PETS</a></p>';console.error(e);}
}
start();
})();