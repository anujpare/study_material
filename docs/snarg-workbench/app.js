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

function wireDiagram(rows,input){
 const copies=[
  ["Input x₁",input[0],"Gate 0 left",rows[0][0]],
  ["Gate 0 out",rows[0][2],"Gate 2 left",rows[2][0]],
  ["Gate 1 out",rows[1][2],"Gate 2 right",rows[2][1]],
  ["Gate 2 out",rows[2][2],"Final gate left",rows[3][0]]
 ];
 let out='<div class="plot"><svg class="math-visual" viewBox="0 0 330 226" role="img" aria-label="Exact wire-copy equalities. Green connections reuse identical field values; red connections disagree.">';
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
     '<p class="viz-insight">'+(fake?'The dishonest difference polynomial is \\(h(X)=X-3\\), so only challenge r = 3 gives false acceptance.':'The honest identity holds at every challenge, establishing perfect completeness.')+'</p>');
  }
  if(type==="interp"){
    const y0=val(lab,"a",1),y1=val(lab,"b",3),y2=val(lab,"c",2);
    const q=mod((y2-2*y1+y0)*9,17),a=mod(y1-y0,17);
    const ys=Array.from({length:17},(_,i)=>mod(y0+a*i+q*i*(i-1),17));
    txt(lab,'The unique degree-at-most-two interpolant is \\(f(X)='+y0+'+'+a+'X+'+q+'X(X-1)\\pmod{17}\\).'+
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
    txt(lab,wireDiagram(rows,traceInputs)+'<p class="note">Original trace input cells: \\(x_1='+traceInputs[0]+',\\;x_2='+traceInputs[1]+',\\;w_1='+traceInputs[2]+'\\). Public statement: \\(x_1=2,\\;x_2=4\\).</p>'+tbl+'<div class="two">'+[status("Public inputs",pubok),status("Gate equations",gateok.every(Boolean)),status("Wire copies",wireok),status("Final output = 0",outputok)].map(s=>'<div>'+s+'</div>').join("")+'</div><p class="note">'+explain+'</p>');
  }

  if(type==="growth"){
    const k=val(lab,"k",10),M=2**k;
    txt(lab,'<div class="two"><div class="stage"><strong>Witness length</strong><p>'+M.toLocaleString('en-US')+' values</p></div><div class="stage"><strong>Binary logarithm</strong><p>'+k+'</p></div></div><p class="viz-insight">\\(M=2^{'+k+'}\\), therefore \\(\\log_2 M='+k+'\\). This comparison concerns asymptotic growth. No exact SNARG proof length is inferred from it.</p>');
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
  if(type==="opening"){
    const stage=val(lab,"stage",1),r=val(lab,"r",3),y=mod(r*r+1,17);
    const info=[
      ['Commit','Prover fixes the entire polynomial f(X)=X²+1 under the published degree bound and sends c.'],
      ['Challenge','Verifier selects evaluation point r = '+r+' after the commitment is fixed.'],
      ['Open and verify','Prover supplies y = f('+r+') = '+y+' and proof π. Verify(pp,c,r,y,π) checks whether this opening is authenticated.']
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
 return '<label>'+math+'<input type="range" data-key="'+name+'" min="'+min+'" max="'+max+'" step="1" value="'+def+'"></label>';
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
  "succinctness":extraBox("Witness length versus logarithmic growth","Choose a witness length M = 2ᵏ. The displayed k is log₂ M, not a claim that a real SNARG proof has exactly k bits.",range("k","Exponent k",3,20,10),"growth"),
  "pcp-box":extraBox("Read-only oracle: what does a position query reveal?","The eight bits are fixed before you choose the index. This demonstrates the oracle interface, not the PCP theorem or its soundness.",range("i","Query position i",1,8,4),"bitbox"),
  "equality-proof":extraBox("Why the prover must commit before the challenge","Give the cheating prover r first. It can then choose the nonzero degree-one polynomial gᵣ(X) = X − r, which always agrees with f(X) = 0 at the known challenge.",range("r","Challenge r",0,16,4),"adaptive"),
  "schwartz-zippel":extraBox("Two-variable root count: h(X,Y) = XY","All 49 pairs in 𝔽₇² are equally likely. Highlighted cells satisfy h = 0. This enumerates an example; the preceding induction proves the general lemma.",range("r1","First coordinate r₁",0,6,2)+range("r2","Second coordinate r₂",0,6,3),"szplot"),
  "midterm-polynomial":extraBox("Test the exact midterm acceptance polynomial","Choose a valid basis vector or an invalid vector. Green squares are precisely the random challenges that satisfy the verifier's equality, for N = 2 and p = 7.",choice("case",[["valid","Valid x = (1,0)"],["two","Invalid x = (1,1)"],["single","Invalid x = (2,0)"]])+range("r1","First challenge r₁",0,6,2)+range("r2","Second challenge r₂",0,6,3),"onehot"),
  "vanishing-polynomial":extraBox("Vanishing means every designated point is a root","For Ω = {1,2}, inspect ZΩ(r)=(r−1)(r−2). The product vanishes precisely at the two required points.",range("r","Evaluation point r",0,16,1),"vanish"),
  "polynomial-commitments":extraBox("Why a commitment and an opening have different jobs","Select a stage. This is a protocol-flow visualization; it does not simulate a cryptographic commitment algorithm.",range("stage","Protocol stage",1,3,1)+range("r","Evaluation point r",0,16,3),"opening"),
  "roots-unity-cost":extraBox("Twelve factors versus four multiplications","For ω = 6 in 𝔽₉₇, the entire 12-point vanishing product must equal r¹²−1. Both sides update as you change r.",range("r","Field element r",0,96,8),"unitycost"),
  "circuits-meaning":extraBox("What the witness must make zero","In 𝔽₉₇, the statement requires C(x,w) = (2·4)(4+w) − 56 = 0. Change the private witness and inspect the exact residual.",range("w","Candidate witness w",0,8,3),"circuit"),
  "plonk-output-input":extraBox("Public-input mismatch is a nonzero polynomial value","The public input is x₁ = 2. Change what the committed trace claims at its designated input location and inspect g(ω⁻¹) = ftrace(ω⁻¹) − fin(ω⁻¹).",range("x","Claimed trace input",0,8,2),"public"),
  "plonk-gates":extraBox("The selector determines which gate equation is checked","The gate triple (L,R,O) = (4,3,7) is an addition gate. Change only the selector to see why the gate equation passes or fails.",choice("s",[["1","Addition selector s = 1"],["0","Multiplication selector s = 0"]]),"selector"),
  "plonk-final":extraBox("Which component certifies each PLONK requirement?","Inspect the exact implication at each verification stage. The claimed global circuit proof succeeds only after all four conditions hold.",range("stage","Verification check",1,4,1),"plonkstages")
 };
 const html=extras[id];if(!html)return;
 const anchor=main.querySelector(".proof")||main.querySelector(".diagram")||main.querySelector(".panel")||main.querySelector(".three")||main.querySelector("h2")||main.querySelector(".aim");
 if(anchor)anchor.insertAdjacentHTML("afterend",html);
 else main.insertAdjacentHTML("beforeend",html);
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
  });
  byId("deck-slider").addEventListener("change",e=>{
   const v=Math.max(1,Math.min(cards.length,Number(e.target.value)));
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