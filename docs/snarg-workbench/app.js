(() => {
"use strict";
const chapterFiles=["part-1.html","part-2.html","part-3.html","part-4.html","part-5.html"];
const chapters=["I · Why SNARGs exist","II · Polynomial reasoning","III · Commitments & Fiat–Shamir","IV · PLONK from circuits","V · Examination workshop"];
const byId=id=>document.getElementById(id);
const main=byId("lesson"), select=byId("lesson-select"), chapter=byId("chapter-select");
const prev=byId("previous"), next=byId("next");
let cards=[],current=0,req=0,mathReady=false,readingMode="guided";
/* Main teaching route. Every other card is still available at its lesson link. */
const coreIds=new Set([
 "the-question","succinctness","pcp-box","merkle","hw1-vectors","hw3-pcp-argument","iop-types",
 "field-foundation","interpolation","equality-proof","schwartz-zippel","midterm-polynomial","vanishing-polynomial",
 "zerotest-proof","fibonacci-protocol","polynomial-commitments",
 "fiat-shamir","hw3-fs-pcp","circuits-meaning","trace-encoding","roots-unity-cost","plonk-output-input",
 "plonk-gates","plonk-wiring","plonk-final"
]);
const exerciseSources={
 "hw1-vectors":"merkle",
 "midterm-polynomial":"schwartz-zippel",
 "schnorr-recall":"fiat-shamir",
 "repetition-hw2":"fiat-shamir",
 "hw3-schnorr-fs":"fiat-shamir",
 "hw3-schnorr-attacks":"fiat-shamir",
 "hw3-conceptual":"fiat-shamir",
 "hw3-amplification":"fiat-shamir",
 "hw3-fs-pcp":"fiat-shamir",
 "hw2-circuit-sat":"circuits-meaning",
 "midterm-interpolation":"polynomial-commitments",
 "exam-fake-trace":"plonk-wiring",
 "exam-security-proof":"zerotest-proof",
 "coverage":"plonk-final"
};
function routeCards(){return readingMode==="all"?cards:cards.filter(c=>coreIds.has(c.id));}
function neighbor(delta){
 const list=routeCards(),currentId=cards[current]?.id;
 const index=list.findIndex(c=>c.id===currentId);
 if(index>=0)return list[index+delta]||null;
 if(delta>0)return list.find(c=>cards.findIndex(x=>x.id===c.id)>current)||null;
 return [...list].reverse().find(c=>cards.findIndex(x=>x.id===c.id)<current)||null;
}
function jumpRelative(delta){const target=neighbor(delta);if(target)location.hash=target.id;}
function syncRouteFooter(){
 const c=cards[current];if(!c)return;
 const list=routeCards(),ix=list.findIndex(x=>x.id===c.id);
 const previousCard=neighbor(-1),nextCard=neighbor(1);
 prev.disabled=!previousCard;next.disabled=!nextCard;
 const slider=byId("deck-slider");
 let thumb=ix>=0?ix+1:Math.max(1,list.filter(x=>cards.indexOf(x)<current).length);
 slider.min="1";slider.max=String(list.length);slider.value=String(thumb);
 slider.setAttribute("aria-valuetext",ix>=0
   ?"Lesson "+(ix+1)+" of "+list.length+": "+c.title
   :"Practice card: "+c.title+". Select a numbered lesson to return to the guided path.");
 const label=ix>=0?(ix+1)+" / "+list.length:"Practice";
 byId("counter").textContent=label;
 byId("position").textContent=label;
}
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

function wireDiagram(rows,input){
 const copies=[
  ["Input x₁",input[0],"Gate 0 left",rows[0][0]],
  ["Input x₂",input[1],"Gate 0 right",rows[0][1]],
  ["Input x₂",input[1],"Gate 1 left",rows[1][0]],
  ["Input w₁",input[2],"Gate 1 right",rows[1][1]],
  ["Gate 0 out",rows[0][2],"Gate 2 left",rows[2][0]],
  ["Gate 1 out",rows[1][2],"Gate 2 right",rows[2][1]]
 ];
 let out='<div class="plot"><svg class="math-visual" viewBox="0 0 330 340" role="img" aria-label="Exact wire-copy equalities. Green connections reuse identical field values; red connections disagree.">';
 copies.forEach((c,i)=>{
  const y=8+i*55,ok=c[1]===c[3],color=ok?"#4b9070":"#b24b4f";
  out+='<rect x="3" y="'+y+'" width="127" height="42" rx="7" fill="#f5f7f5" stroke="#cbd8cd"/>';
  out+='<rect x="202" y="'+y+'" width="125" height="42" rx="7" fill="'+(ok?"#edf6ef":"#fff0ef")+'" stroke="'+color+'"/>';
  out+='<path d="M131 '+(y+20)+' H200" stroke="'+color+'" stroke-width="3" fill="none"/>';
  out+='<path d="M193 '+(y+14)+' L201 '+(y+20)+' L193 '+(y+26)+'" stroke="'+color+'" stroke-width="2" fill="none"/>';
  out+='<text x="10" y="'+(y+16)+'" font-size="11" fill="#485a4d">'+c[0]+'</text>';
  out+='<text x="10" y="'+(y+32)+'" font-size="15" font-weight="700" fill="#263e31">'+c[1]+'</text>';
  out+='<text x="210" y="'+(y+16)+'" font-size="11" fill="#485a4d">'+c[2]+'</text>';
  out+='<text x="210" y="'+(y+32)+'" font-size="15" font-weight="700" fill="'+color+'">'+c[3]+(ok?" ✓":" ✕")+'</text>';
 });
 return out+'</svg><div class="visual-note">Every arrow represents an equality required by the circuit wiring. A red arrow alone invalidates the proposed trace.</div></div>';
}

function syncRangeValues(lab){
  lab.querySelectorAll('input[type="range"]').forEach(input=>{
    const label=input.closest('label');
    if(!label)return;
    label.classList.add("range-label");
    const key=input.dataset.key || input.id || "range";
    let output=label.querySelector('output[data-live-for="'+key+'"]');
    if(!output){
      output=document.createElement('output');
      output.className="range-value";
      output.dataset.liveFor=key;
      input.before(output);
    }
    output.value=input.value;
    output.textContent=input.value;
    input.setAttribute("aria-valuetext",key+" = "+input.value);
  });
}
function initLab(lab){
 const type=lab.dataset.lab;
 const update=()=>{
  syncRangeValues(lab);
  if(type==="ring"){
    const r=val(lab,"r",3),y=mod(2*r*r+4*r,6);
    txt(lab,'\\(f('+r+')='+y+'\\pmod 6\\). '+(y===0?'This is a root.':'This is not a root.')+' The four roots are 0, 1, 3, and 4.'+grid([0,1,2,3,4,5],x=>mod(2*x*x+4*x,6)===0,r));
  }
  if(type==="naive"){
    const n=val(lab,"n",100),detection=3/n,miss=1-detection;
    const percent=(100*miss).toFixed(2);
    const diagram='<div class="address-summary"><div><span class="small-label">Checked transitions</span><strong>3 of '+n+'</strong></div>'+
      '<div><span class="small-label">Probability of missing the error</span><strong>'+percent+'%</strong></div></div>'+
      '<div style="height:14px;border-radius:8px;background:#e4e9e4;overflow:hidden;margin:12px 0">'+
      '<div style="height:100%;width:'+(100*miss)+'%;background:#ba715b"></div></div>';
    txt(lab,diagram+'<p>\\(\\Pr[\\text{miss the single bad transition}]=1-\\frac{3}{'+n+'}='+miss.toFixed(6)+'\\).</p>'+
      '<p class="viz-insight">This calculation applies only to sampling three distinct positions uniformly from the ordinary trace. It does not describe the PCP verifier, whose query rule and encoded proof are different.</p>');
  }
  if(type==="pcp"){
    const t=val(lab,"t",4),err=1/Math.pow(2,t);
    txt(lab,'<b>'+t+' independent PCP tests</b> involve up to '+(3*t)+' queried proof-bit positions in the three-query version. For a fixed false-proof string, \\(\\Pr[\\mathrm{all\\ pass}]\\le 2^{-'+t+'}='+err.toFixed(6)+'\\).<p class="note">This is a bound, not a simulation of a PCP encoding. Independence holds because fresh verifier randomness is used for each test against the same fixed proof.</p>');
  }
  if(type==="eq"){
    const r=val(lab,"r",1),f=mod(r*r+1,17),g=mod(f+(r-1)*(r-4),17),pass=f===g;
    const h=Array.from({length:17},(_,i)=>mod((i-1)*(i-4),17));
    txt(lab,'\\(f('+r+')='+f+'\\), \\(g('+r+')='+g+'\\) in \\(\\mathbb F_{17}\\). <b>'+(pass?'False acceptance':'Rejection')+'</b>.'+
      grid(Array.from({length:17},(_,i)=>i),x=>x===1||x===4,r)+
      svgTrend(h,16,16,r)+
      '<p class="visual-note">The bars show the disagreement \\(h(r)=g(r)-f(r)\\) in the finite field. A zero-height bar at r = 1 or 4 means the false equality passes at that challenge.</p>'+
      '<p class="viz-insight">The difference has exactly two roots, so false acceptance occurs on exactly 2 of 17 equally likely challenges.</p>');
  }
  if(type==="zero"){
    const r=val(lab,"r",3),fake=lab.querySelector('[data-key="fake"]')?.checked??true;
    const z=mod((r-1)*(r-2),17),q=mod(r+3,17),rhs=mod(z*q,17);
    const lhs=mod(rhs+(fake?r-3:0),17);
    const domain=Array.from({length:17},(_,i)=>i);
    txt(lab,'\\(f('+r+')='+lhs+'\\), \\(Z_\\Omega('+r+')q('+r+')='+rhs+'\\). <b>'+(lhs===rhs?'Accept':'Reject')+'</b>.'+
     grid(domain,x=>!fake||x===3,r)+
     (fake?'<div class="two"><div class="stage"><strong>Required point 1</strong><p>f(1) = 15, Z(1) = 0</p></div><div class="stage"><strong>Required point 2</strong><p>f(2) = 16, Z(2) = 0</p></div></div><p class="visual-note">At both required points the right side Z(i)q(i) equals zero for every q, while f(i) is nonzero. This proves the example is false; Theorem 2 establishes the general equivalence.</p>':'')+
     '<p class="viz-insight">'+(fake?'The dishonest difference polynomial is \\(h(X)=X-3\\), so only challenge r = 3 gives false acceptance.':'The honest identity holds at every challenge, establishing perfect completeness.')+'</p>');
  }
  if(type==="interp"){
    const y0=val(lab,"a",0),y1=val(lab,"b",1),y2=val(lab,"c",1);
    const q=mod((y2-2*y1+y0)*9,17),a=mod(y1-y0,17);
    const ys=Array.from({length:17},(_,i)=>mod(y0+a*i+q*i*(i-1),17));
    const termA=a===0?'':a===1?'+X':'+'+a+'X';
    const termQ=q===0?'':q===1?'+X(X-1)':'+'+q+'X(X-1)';
    const formula=y0+termA+termQ;
    txt(lab,'The degree-at-most-two interpolant is \\(f(X)\\equiv '+formula+'\\pmod{17}\\).'+
      svgTrend(ys,16,16,[0,1,2])+
      '<p class="visual-note">Highlighted bars are the three imposed values f(0), f(1), f(2); the other field evaluations follow from the same polynomial. Values are discrete residues, not a smooth real-number curve.</p>'+
      '<p class="viz-insight">The polynomial matches \\(f(0)='+y0+'\\), \\(f(1)='+y1+'\\), \\(f(2)='+y2+'\\). Two degree-at-most-two polynomials agreeing at these three distinct points must be identical.</p>');
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
    txt(lab,'To open proof entry <b>\\(\\pi_{'+selected+'}\\)</b>, send its value and '+sib.length+' sibling hashes (amber). The verifier hashes upward along the blue branch and compares the resulting root with commitment \\(c\\). Only '+sib.length+' hashes are needed because each sibling authenticates an entire subtree.');
  }
  if(type==="trace"){
    const mode=lab.querySelector('[data-key="mode"]')?.value??"honest";
    const rows=[[2,4,8,0],[4,3,7,1],[8,7,56,0]];
    const traceInputs=[2,4,3],publicX=[2,4];
    const target=56;
    let explain="Every gate equation, wire equality, public input and output condition holds.";
    if(mode==="public"){
      traceInputs[0]=5;traceInputs[2]=57;
      rows[0]=[5,4,20,0];rows[1]=[4,57,61,1];rows[2]=[20,61,56,0];
      explain="Only the public-input check fails: the trace uses x₁ = 5 instead of the stated x₁ = 2. All gates and wires agree, and 20 × 61 ≡ 56 (mod 97). This is why the verifier must bind the trace to the public statement.";
    }
    if(mode==="gate"){
      rows[0][2]=9;rows[2][0]=9;
      explain="Only the gate-arithmetic family fails: gate 0 falsely claims 2 × 4 = 9, and gate 2 falsely claims 9 × 7 = 56. Every copied wire agrees, the public inputs match, and the final output is 56.";
    }
    if(mode==="wire"){
      rows[2]=[9,17,56,0];
      explain="All three gate equations pass: 9 × 17 = 153 ≡ 56 (mod 97). The public inputs and final output also pass. But gate 0 produced 8, not 9, and gate 1 produced 7, not 17. Only the wiring check catches this false trace.";
    }
    if(mode==="output"){
      traceInputs[2]=4;rows[1]=[4,4,8,1];rows[2]=[8,8,64,0];
      explain="Only the output check fails: the witness w₁ = 4 makes the circuit compute 64 instead of the public target 56. All gate equations and wire equalities hold, and the public inputs remain 2 and 4.";
    }
    const gateok=rows.every(r=>mod(r[3]===1?r[0]+r[1]-r[2]:r[0]*r[1]-r[2],97)===0);
    const pubok=traceInputs[0]===publicX[0]&&traceInputs[1]===publicX[1];
    const wireok=traceInputs[0]===rows[0][0]&&traceInputs[1]===rows[0][1]&&
      traceInputs[1]===rows[1][0]&&traceInputs[2]===rows[1][1]&&
      rows[0][2]===rows[2][0]&&rows[1][2]===rows[2][1];
    const outputok=rows[2][2]===target;
    const tbl='<div class="table-scroll"><table><thead><tr><th>Gate</th><th>Left</th><th>Right</th><th>Out</th><th>Type</th><th>Residual</th></tr></thead><tbody>'+
      rows.map((r,i)=>'<tr><td>'+i+'</td><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+r[2]+'</td><td>'+(r[3]?"+":"×")+'</td><td>'+
      mod(r[3]?r[0]+r[1]-r[2]:r[0]*r[1]-r[2],97)+'</td></tr>').join("")+'</tbody></table></div>';
    const status=(name,ok)=>'<span style="color:'+(ok?"#146655":"#ac3136")+';font-weight:750">'+(ok?"✓ ":"✕ ")+name+'</span>';
    txt(lab,wireDiagram(rows,traceInputs)+
      '<p class="note">Trace inputs: \\(x_1='+traceInputs[0]+',\\;x_2='+traceInputs[1]+',\\;w_1='+traceInputs[2]+'\\). Public statement: \\(x_1=2,\\;x_2=4,\\;\\mathrm{target}='+target+'\\). All arithmetic is modulo 97.</p>'+
      tbl+'<div class="two">'+[
        status("Public inputs",pubok),status("Gate equations",gateok),
        status("Wire copies",wireok),status("Output = "+target,outputok)
      ].map(v=>'<div>'+v+'</div>').join("")+'</div><p class="viz-insight">'+explain+'</p>');
  }

  if(type==="growth"){
    const k=val(lab,"k",3),count=2**k;
    const last=count-1,allOnes="1".repeat(k),allZeros="0".repeat(k);
    let addresses="";
    if(k<=4){
      addresses='<div class="address-grid" aria-label="All '+count+' binary addresses">'+
        Array.from({length:count},(_,i)=>'<span class="address-cell '+(i===last?"last":"")+'"><small>'+i+'</small><b>'+i.toString(2).padStart(k,"0")+'</b></span>').join("")+'</div>';
    }else{
      addresses='<div class="address-ends" aria-label="First and last binary addresses">'+
      '<span>First position <b>0</b><code>'+allZeros+'</code></span>'+
      '<span class="dots" aria-hidden="true">···</span>'+
      '<span>Last position <b>'+last.toLocaleString("en-US")+'</b><code>'+allOnes+'</code></span></div>';
    }
    txt(lab,
      '<div class="address-summary"><div><span class="small-label">Encoded proof length M</span><strong>'+
         count.toLocaleString("en-US")+' <small>bits</small></strong></div>'+
      '<div><span class="small-label">Digits to address one bit</span><strong>'+
         k+' <small>bits</small></strong></div></div>'+
      '<div class="address-rule">\\(M=2^{'+k+'}='+count.toLocaleString("en-US").replace(/,/g,"\\,")+
         '\\quad\\Longrightarrow\\quad\\log_2 M='+k+'\\)</div>'+
      addresses+
      '<p class="viz-insight">These '+k+' address digits can select <em>one</em> position among '+
      count.toLocaleString("en-US")+' bits. They do not contain those bits or prove that the computation was correct. The PCP theorem explains why those positions matter; this figure measures only the cost of specifying them.</p>');
  }
  if(type==="bitbox"){
    const i=val(lab,"i",4),bits=[1,0,1,1,0,0,1,0];
    const cells='<div class="lab-grid">'+bits.map((b,j)=>'<span class="'+(i===j+1?"root current":"")+'">'+(i===j+1?b:"?")+'</span>').join("")+'</div>';
    txt(lab,cells+'<p class="viz-insight">Only \\(\\pi_{'+i+'}='+bits[i-1]+'\\) is revealed. The other seven bits remain concealed. The full vector was fixed before the query.</p>');
  }
  if(type==="adaptive"){
    const r=val(lab,"r",4);
    txt(lab,'<div class="two"><div class="stage"><strong>At r = '+r+'</strong><p>\\(f(r)=0\\), \\(g_r(r)=0\\)</p></div><div class="stage"><strong>At r + 1</strong><p>\\(f(r+1)=0\\), \\(g_r(r+1)=1\\)</p></div></div><p class="viz-insight">After learning r, a cheating prover sets \\(g_r(X)=X-'+r+'\\), a nonzero polynomial. The test accepts at r with certainty even though the polynomials differ. The root theorem does not justify a probability bound when the polynomial depends on the random challenge.</p>');
  }
  if(type==="szplot"){
    const r1=val(lab,"r1",2),r2=val(lab,"r2",3),h=mod(r1*r2,7);
    txt(lab,svgMatrix(7,(x,y)=>x*y%7===0,[r1,r2])+
      '<div class="two"><div class="stage"><strong>Selected point</strong><p>\\(h('+r1+','+r2+')='+h+'\\)</p></div><div class="stage"><strong>Exact chance</strong><p>13 of 49 field pairs</p></div></div>'+
      '<p class="viz-insight">The only zeros occur when r₁ = 0 or r₂ = 0. The row and column contain 7 + 7 − 1 = 13 points (subtracting the shared origin). Thus \\(13/49\\le 2/7\\), matching the Schwartz–Zippel upper bound for degree 2.</p>');
  }
  if(type==="onehot"){
    const selected=lab.querySelector('[data-key="case"]')?.value||"valid";
    const x=selected==="valid"?[1,0]:selected==="two"?[1,1]:[2,0];
    const r1=val(lab,"r1",2),r2=val(lab,"r2",3);
    const poly=(a,b)=>mod((x[0]*a+x[1]*b)**2-x[0]*a*a-x[1]*b*b,7);
    let roots=0;for(let a=0;a<7;a++)for(let b=0;b<7;b++)if(poly(a,b)===0)roots++;
    const value=poly(r1,r2);
    txt(lab,svgMatrix(7,(a,b)=>poly(a,b)===0,[r1,r2])+
      '<div class="two"><div class="stage"><strong>Selected challenge</strong><p>\\(h('+r1+','+r2+')='+value+'\\)</p></div><div class="stage"><strong>Accepting choices</strong><p>'+roots+' / 49</p></div></div>'+
      '<p class="viz-insight">'+(selected==="valid"?
        'Every challenge is accepted, as required by perfect completeness.':
        'This invalid vector is accepted on exactly '+roots+' out of 49 challenges, below the upper bound 2/7. The proof derives the bound for every invalid vector, not just this small example.')+'</p>');
  }
  if(type==="vanish"){
    const r=val(lab,"r",1),a=mod(r-1,17),b=mod(r-2,17),z=mod(a*b,17);
    txt(lab,'<div class="two"><div class="stage"><strong>Two factors</strong><p>\\((r-1)='+a+',\\;(r-2)='+b+'\\)</p></div><div class="stage"><strong>Their product</strong><p>\\(Z_\\Omega(r)='+z+'\\)</p></div></div>'+
      grid(Array.from({length:17},(_,i)=>i),n=>n===1||n===2,r)+
      '<p class="viz-insight">The product is zero at r = 1 or r = 2 because a factor is zero. At all other field points both factors are nonzero, so their product cannot be zero in a field.</p>');
  }
  if(type==="story-protocol"){
    const mode=lab.querySelector('[data-key="protocol"]')?.value??"interactive";
    const stage=val(lab,"stage",1);
    const steps=mode==="interactive"?[
      ["Prover fixes polynomials","The prover commits to f_fib and q and sends c_f and c_q. The verifier has not chosen r yet."],
      ["Verifier chooses r","After receiving the commitments, the verifier samples a uniform field element r and sends it to the prover."],
      ["Prover opens and verifier checks","The prover opens the required evaluations at 0, 1, 100, r, r+1, r+2 and q(r). The verifier authenticates them and checks the endpoint and ZeroTest equations."]
    ]:[
      ["Prover fixes polynomials","The prover commits to f_fib and q and fixes c_f and c_q. These commitments become part of the public proof."],
      ["Both parties derive r","They calculate r from the public statement, the fixed commitments, and the public parameters using the random-oracle hash. No verifier message is sent."],
      ["Prover publishes one proof","The prover publishes commitments, evaluation values and opening proofs. Any verifier recomputes r and checks the same equations."]
    ];
    const row=steps.map((x,i)=>'<div class="stage" style="opacity:'+(i===stage-1?'1':'.52')+';border-color:'+(i===stage-1?'#346b67':'#ccd6d1')+'"><strong>'+(i+1)+'. '+x[0]+'</strong><p>'+x[1]+'</p></div>').join("");
    txt(lab,'<div class="flow" style="flex-wrap:wrap;gap:10px">'+row+'</div>'+
      '<p class="viz-insight">'+steps[stage-1][1]+'</p>');
  }
  if(type==="opening"){
    const stage=val(lab,"stage",1),r=val(lab,"r",3),y=mod(r*r+1,17);
    const info=[
      ['Commit','Prover fixes the entire polynomial f(X)=X²+1 under the published degree bound and sends c.'],
      ['Challenge','Verifier selects evaluation point z = '+r+' after the commitment is fixed.'],
      ['Open and verify','Prover supplies y = f('+r+') = '+y+' and proof π. Verify(pp,c,z,y,π) checks whether this opening is authenticated.']
    ];
    txt(lab,'<div class="flow">'+info.map((a,i)=>'<div class="stage" style="border-color:'+(i+1===stage?'#4b7963':'#d5ddd6')+';background:'+(i+1===stage?'#e4f1e9':'#f3f4f1')+'"><strong>'+(i+1)+'. '+a[0]+'</strong><p>'+a[1]+'</p></div>').join('<span class="arrow">→</span>')+'</div>'+
      '<p class="viz-insight">The binding requirement makes the opening consistent with the previous commitment. Neither a real commitment c nor a real opening π is computed in this conceptual diagram.</p>');
  }
  if(type==="unitycost"){
    const r=val(lab,"r",8);
    const omega=Array.from({length:12},(_,i)=>gcdPow(6,i,97));
    const prod=omega.reduce((v,a)=>mod(v*(r-a),97),1);
    const power=mod(gcdPow(r,12,97)-1,97);
    txt(lab,'<div class="two"><div class="stage"><strong>12-factor product</strong><p>\\(\\prod_{j=0}^{11}(r-6^j)='+prod+'\\)</p></div><div class="stage"><strong>Compact formula</strong><p>\\(r^{12}-1='+power+'\\)</p></div></div>'+
      '<p class="viz-insight">They are equal for r = '+r+' because both evaluate the same polynomial over 𝔽₉₇. Computing r¹² uses r², r⁴, r⁸ and r⁸·r⁴: four multiplications, versus evaluating and multiplying twelve factors.</p>');
  }
  if(type==="circuit"){
    const w=val(lab,"w",3),a=8,b=4+w,out=a*b,res=mod(out-56,97);
    txt(lab,'<div class="three"><div class="stage"><strong>Gate 0 · ×</strong><p>2 × 4 = 8</p></div><div class="stage"><strong>Gate 1 · +</strong><p>4 + '+w+' = '+b+'</p></div><div class="stage"><strong>Gate 2 · ×</strong><p>8 × '+b+' = '+out+'</p></div></div>'+
      '<p>\\(C(\\mathbf{x},'+w+')=8('+b+')-56\\equiv '+res+'\\pmod{97}\\).</p>'+
      '<p class="viz-insight">'+(res===0?'The witness satisfies the public target, so this instance of the zero-output condition holds.':'This witness does not satisfy the public target: the output-check constraint is nonzero.')+'</p>');
  }
  if(type==="public"){
    const x=val(lab,"x",2),g=mod(x-2,97);
    txt(lab,'<div class="two"><div class="stage"><strong>Committed trace</strong><p>\\(f_{\\rm trace}(\\omega^{-1})='+x+'\\)</p></div><div class="stage"><strong>Public polynomial</strong><p>\\(f_{\\rm in}(\\omega^{-1})=2\\)</p></div></div>'+
      '<p>\\(g(\\omega^{-1})='+x+'-2\\equiv '+g+'\\pmod{97}\\).</p>'+
      '<p class="viz-insight">'+(g===0?'The required public input agrees exactly.':'The public input differs. The ZeroTest over the public-input positions must reject except with its bounded soundness error.')+'</p>');
  }
  if(type==="selector"){
    const s=Number(lab.querySelector('[data-key="s"]')?.value??1);
    const add=4+3,mul=4*3,v=s*add+(1-s)*mul,err=mod(v-7,97);
    txt(lab,'<div class="three"><div class="stage"><strong>Inputs</strong><p>L = 4, R = 3</p></div><div class="stage"><strong>Selected operation</strong><p>'+(s===1?'4 + 3 = 7':'4 × 3 = 12')+'</p></div><div class="stage"><strong>Claimed output</strong><p>O = 7</p></div></div>'+
      '<p>\\('+s+'(4+3)+(1-'+s+')(4\\cdot3)-7\\equiv '+err+'\\pmod{97}\\).</p>'+
      '<p class="viz-insight">'+(err===0?'The equation vanishes because the selector matches the gate type.':'The polynomial residual is nonzero: the same triple fails if the gate is multiplication instead of addition.')+' The real selector is fixed by the public circuit, not chosen by the prover.</p>');
  }
  if(type==="plonkstages"){
    const stage=val(lab,"stage",1);
    const tests=[
      ["Final output","The last output position contains 0, as required by the public statement."],
      ["Public input","The trace matches every public input at its designated position."],
      ["Gate operations","The gate constraint polynomial vanishes at every gate-start position."],
      ["Wiring copies","Every occurrence of the same logical wire has an identical field value."]
    ];
    txt(lab,tests.map((a,i)=>'<div class="stage" style="margin-bottom:6px;border-left:3px solid '+(i+1===stage?'#2d6b54':'#cad8cd')+';background:'+(i+1===stage?'#e8f2eb':'#f3f4f1')+'"><strong>'+(i+1)+'. '+a[0]+'</strong>'+(i+1===stage?'<p>'+a[1]+'</p>':'')+'</div>').join('')+
      '<p class="viz-insight">Passing all four constraint families implies an honest satisfying circuit trace. Authenticated randomized polynomial checks are needed to establish these conditions without checking the entire trace.</p>');
  }
 };
 lab.querySelectorAll("input,select").forEach(el=>el.addEventListener("input",update));
 update();
}


/* Each supplementary visualization is attached to the exact mathematical claim
   it tests; none of these small-field experiments replaces the general proof. */
function extraBox(title,why,fields,type){
 return '<div class="lab" data-lab="'+type+'"><div class="lab-top"><strong>'+title+'</strong><p>'+why+'</p></div><div class="lab-content">'+fields+'<div class="lab-output" aria-live="polite"></div></div></div>';
}
function range(name,math,min,max,def){
 return '<label class="range-label"><span class="range-name">'+math+'</span><output class="range-value" data-live-for="'+name+'">'+def+'</output><input type="range" data-key="'+name+'" min="'+min+'" max="'+max+'" step="1" value="'+def+'" aria-label="'+math.replace(/<[^>]*>/g,"")+'"></label>';
}
function choice(name,options){
 return '<label>Choose a case<select data-key="'+name+'">'+options.map(([v,t])=>'<option value="'+v+'">'+t+'</option>').join("")+'</select></label>';
}
function vizMath(x){return '\\('+x+'\\)'}
function svgTrend(values,maxX,maxY,highlight){
 const w=330,h=135,left=28,top=9,bottom=114;
 let s='<div class="plot"><svg class="math-visual" viewBox="0 0 330 135" role="img" aria-label="Discrete values plotted at each integer input">';
 s+='<path d="M28 9 V114 H320" stroke="#a9b7af" stroke-width="1" fill="none"/>';
 values.forEach((v,i)=>{
  const x=left+(i+.5)*(290/values.length);
  const y=bottom-v/maxY*99;
  const chosen=Array.isArray(highlight)?highlight.includes(i):i===highlight;
  const color=chosen?"#2b6f58":"#b3c9bb";
  s+='<rect x="'+(x-290/values.length*.34)+'" y="'+y+'" width="'+Math.max(2,290/values.length*.68)+'" height="'+Math.max(1,bottom-y)+'" rx="1" fill="'+color+'"/>';
  if(chosen)s+='<text x="'+x+'" y="'+(y-4)+'" text-anchor="middle" font-size="10" font-weight="700" fill="#254d3d">'+v+'</text>';
 });
 s+='<text x="6" y="14" font-size="11" fill="#66766b">'+maxY+'</text><text x="10" y="115" font-size="11" fill="#66766b">0</text>';
 s+='<text x="29" y="129" font-size="11" fill="#66766b">0</text>';
 s+='<text x="300" y="129" font-size="11" fill="#66766b">'+maxX+'</text></svg></div>';
 return s;
}
function svgMatrix(size,test,selected){
 let s='<div class="plot"><svg viewBox="0 0 306 306" class="math-visual" role="img" aria-label="All equally likely pairs of challenges. Dark cells are the pairs accepted by the verifier.">';
 const step=35,pad=31;
 for(let j=0;j<size;j++)for(let i=0;i<size;i++){
  const x=pad+i*step,y=pad+j*step;
  const root=test(i,j);
  const focus=selected[0]===i&&selected[1]===j;
  s+='<rect x="'+x+'" y="'+y+'" width="31" height="31" rx="3" fill="'+(root?"#a9d5bc":"#e9e9e6")+'" stroke="'+(focus?"#1f5f49":"#d6d9d4")+'" stroke-width="'+(focus?3:1)+'"/>';
  if(focus)s+='<circle cx="'+(x+15.5)+'" cy="'+(y+15.5)+'" r="5" fill="#245b46"/>';
 }
 for(let i=0;i<size;i++){
  s+='<text x="'+(pad+i*step+15)+'" y="22" text-anchor="middle" font-size="12" fill="#66756a">'+i+'</text>';
  s+='<text x="20" y="'+(pad+i*step+20)+'" text-anchor="middle" font-size="12" fill="#66756a">'+i+'</text>';
 }
 s+='<text x="140" y="301" font-size="11" text-anchor="middle" fill="#65766b">r₁ →</text>';
 s+='<text transform="translate(9,161) rotate(-90)" font-size="11" text-anchor="middle" fill="#65766b">r₂ →</text>';
 return s+'</svg></div>';
}
function initLessonExtras(id){
 const extras={
  "pcp-box":extraBox("Ask the box for one bit","All eight bits are fixed first. Choose which one to reveal.",range("i","Query position i",1,8,4),"bitbox"),
  "equality-proof":extraBox("What if the cheater learns the question first?","Choose r first. The cheater can then invent gᵣ(X) = X − r, which agrees with f(X) = 0 exactly at r.",range("r","Challenge r",0,16,4),"adaptive"),
  "schwartz-zippel":extraBox("Which pairs make XY = 0?","There are 49 possible pairs in 𝔽₇². Green cells are the ones where XY = 0.",range("r1","First coordinate r₁",0,6,2)+range("r2","Second coordinate r₂",0,6,3),"szplot"),
  "midterm-polynomial":extraBox("Which random checks accept the vote?","Choose a two-entry vote. Green squares show which random challenges make the verifier accept.",choice("case",[["valid","Valid x = (1,0)"],["two","Invalid x = (1,1)"],["single","Invalid x = (2,0)"]])+range("r1","First challenge r₁",0,6,2)+range("r2","Second challenge r₂",0,6,3),"onehot"),
  "vanishing-polynomial":extraBox("Where does the product become zero?","For Ω = {1,2}, try different r in ZΩ(r) = (r−1)(r−2).",range("r","Evaluation point r",0,16,1),"vanish"),
  "roots-unity-cost":extraBox("A big product becomes one power","Try different r in 𝔽₉₇. Both formulas must give the same value.",range("r","Field element r",0,96,8),"unitycost"),
  "circuits-meaning":extraBox("Change the secret input","The public target is 56. Change w and see whether the circuit's final check equals zero.",range("w","Candidate witness w",0,8,3),"circuit"),
  "plonk-output-input":extraBox("What if the prover changes our public input?","The real input is x₁ = 2. Change the value written into the trace and watch the difference.",range("x","Claimed trace input",0,8,2),"public"),
  "plonk-gates":extraBox("Switch the gate from addition to multiplication","The inputs are 4 and 3; the claimed output is 7. Change only the selector.",choice("s",[["1","Addition selector s = 1"],["0","Multiplication selector s = 0"]]),"selector")
 };
 const html=extras[id];if(!html)return;
 // Put the experiment beside the equation or question it tests, never
 // before the student knows the variables being manipulated.
 const placement={
  "equality-proof":['.lab[data-lab="eq"]',"afterend"],
  "midterm-polynomial":[".exercise details.worked","beforebegin"],
  "roots-unity-cost":[".warning","beforebegin"],
  "circuits-meaning":[".bridge","beforebegin"],
  "plonk-gates":["h2","beforebegin"]
 }[id];
 if(placement){
  const target=main.querySelector(placement[0]);
  if(target){target.insertAdjacentHTML(placement[1],html);return;}
 }
 const anchor=main.querySelector(".proof")||main.querySelector(".diagram")||main.querySelector(".panel")||main.querySelector(".three")||main.querySelector("h2")||main.querySelector(".aim");
 if(anchor)anchor.insertAdjacentHTML("afterend",html);
 else main.insertAdjacentHTML("beforeend",html);
}

function getHash(){try{return decodeURIComponent(location.hash.slice(1))}catch(e){return ""}}
function setMenuOpen(open){
 const drawer=byId("chapter-menu"),button=byId("menu-toggle"),panel=byId("chapter-panel");
 if(!drawer||!button||!panel)return;
 drawer.dataset.open=open?"true":"false";
 button.setAttribute("aria-expanded",open?"true":"false");
 panel.hidden=!open;
}
function closeMenu(){setMenuOpen(false)}
function navigate(){
 const id=getHash();const found=cards.findIndex(c=>c.id===id);
 current=found>=0?found:0;
 const c=cards[current];
 if(window.MathJax?.typesetClear){try{MathJax.typesetClear([main]);}catch(e){}}
 main.innerHTML=c.html;
 main.dataset.lessonId=c.id;
 main.scrollTop=0;
 byId("header-title").textContent=c.title;
 chapter.value=String(c.chapter);
 select.innerHTML=cards.filter(x=>x.chapter===c.chapter).map(x=>'<option value="'+escape(x.id)+'">'+escape(x.title)+'</option>').join("");
 select.value=c.id;
 syncRouteFooter();
 if(!coreIds.has(c.id)){
   const originId=exerciseSources[c.id];
   if(originId){
     const origin=cards.find(x=>x.id===originId);
     const nextMain=neighbor(1);
     if(origin)main.insertAdjacentHTML("afterbegin",
       '<div class="practice-back"><a href="#'+origin.id+'">← Back to '+escape(origin.title)+'</a><span>Optional worked exercise</span></div>');
     if(nextMain)main.insertAdjacentHTML("beforeend",
       '<div class="practice-forward"><a href="#'+nextMain.id+'">Continue the explanation: '+escape(nextMain.title)+' →</a></div>');
   }
 }
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
  const missingCore=[...coreIds].filter(id=>!cards.some(c=>c.id===id));
  if(missingCore.length)throw Error("Missing required syllabus lessons: "+missingCore.join(", "));
  chapter.innerHTML=chapters.map((c,i)=>'<option value="'+i+'">'+escape(c)+'</option>').join("");
  byId("menu-toggle").addEventListener("click",()=>setMenuOpen(byId("chapter-menu").dataset.open!=="true"));
  chapter.addEventListener("change",()=>{
   const x=cards.find(c=>c.chapter===Number(chapter.value));
   if(x)location.hash=x.id;
  });
  select.addEventListener("change",()=>{location.hash=select.value;});
  const modeSelect=byId("reading-mode");
  modeSelect.addEventListener("change",()=>{
    readingMode=modeSelect.value==="all"?"all":"guided";
    syncRouteFooter();
    closeMenu();
  });
  prev.addEventListener("click",()=>jumpRelative(-1));
  next.addEventListener("click",()=>jumpRelative(1));
  byId("deck-slider").addEventListener("input",e=>{
    const v=Number(e.target.value),length=routeCards().length;
    byId("position").textContent=Math.max(1,Math.min(length,v))+" / "+length;
  });
  byId("deck-slider").addEventListener("change",e=>{
    const target=routeCards()[Math.max(0,Number(e.target.value)-1)];
    if(target&&target.id!==getHash())location.hash=target.id;
    else syncRouteFooter();
  });
  document.addEventListener("keydown",e=>{
   if(e.key==="Escape"){closeMenu();return}
   if(e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;
   if(["INPUT","TEXTAREA","SELECT","BUTTON","SUMMARY"].includes(document.activeElement?.tagName)||document.activeElement?.isContentEditable)return;
   if(e.key==="ArrowRight"&&neighbor(1)){e.preventDefault();jumpRelative(1);}
   if(e.key==="ArrowLeft"&&neighbor(-1)){e.preventDefault();jumpRelative(-1);}
  });
  document.addEventListener("pointerdown",e=>{
   const drawer=byId("chapter-menu");
   if(drawer?.dataset.open==="true"&&!drawer.contains(e.target))closeMenu();
  });
  window.addEventListener("hashchange",navigate);
  if(!getHash())history.replaceState(null,"","#"+cards[0].id);
  navigate();
 }catch(e){main.innerHTML='<h1>Unable to load the learning lab</h1><p>'+escape(e.message)+'</p><p><a href="../">Return to PETS</a></p>';console.error(e);}
}
start();
})();