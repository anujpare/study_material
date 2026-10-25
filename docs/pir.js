/* PETS: deterministic teaching examples, not cryptographic implementations. */
(() => {
 'use strict';
 const mod=(x,p)=>((x%p)+p)%p;
 const power=(x,n,p)=>{let r=1;for(let i=0;i<n;i++)r=r*x%p;return r;};
 const bits=(v,n)=>Array.from({length:n},(_,i)=>(v>>(n-i-1))&1);
 const bitstring=a=>a.join('');
 const xor=(a,b)=>a.map((v,i)=>v^b[i]);
 const dot=(a,b)=>a.reduce((v,x,i)=>v^(x&b[i]),0);
 const X=[[1,0,1,1],[0,1,0,1],[1,1,0,0],[0,0,1,0]];
 const database=[1,0,1,1,0,0,1,0];
 function controls(panel){const el=document.createElement('div');el.className='pir-controls';panel.querySelector('figcaption').after(el);return el;}
 function select(box,label,choices,initial){const l=document.createElement('label'),s=document.createElement('select');l.append(document.createTextNode(label));for(const [v,t] of choices)s.add(new Option(t,String(v)));s.value=String(initial);l.append(s);box.append(l);return s;}
 function range(box,label,min,max,value){const l=document.createElement('label'),t=document.createElement('span'),s=document.createElement('input');s.type='range';s.min=min;s.max=max;s.value=value;s.setAttribute('aria-label',label);const update=()=>t.textContent=`${label}: ${s.value}`;s.addEventListener('input',update);update();l.append(t,s);box.append(l);return s;}
 function checkbox(box,label,value){const l=document.createElement('label'),s=document.createElement('input');s.type='checkbox';s.checked=value;l.append(s,document.createTextNode(label));box.append(l);return s;}
 function output(panel){const out=document.createElement('output');out.setAttribute('aria-live','polite');out.setAttribute('aria-atomic','true');panel.append(out);return out;}
 function tiles(el,entries,cls='pir-strip'){el.className=cls;el.replaceChildren(...entries.map(e=>{const s=document.createElement('span');s.textContent=e.text;if(e.hit)s.classList.add('is-hit');if(e.fail)s.classList.add('is-fail');return s;}));}
 function flow(el,values){tiles(el,values.map(text=>({text})),'pir-flow');}
 function stepper(panel,labels,draw){
  const nav=document.createElement('div');nav.className='pir-stepper';
  const back=document.createElement('button'),next=document.createElement('button');back.type=next.type='button';back.textContent='Previous step';next.textContent='Next step';
  const state=document.createElement('div');state.className='pir-step-state';state.setAttribute('role','status');
  nav.append(back,next);
  const anchor=panel.querySelector('[data-matrix-stage],[data-recursion-stage],[data-noise-stages]');
  if(anchor)anchor.before(nav,state);else panel.querySelector('figcaption').after(nav,state);
  let step=0;
  const update=()=>{back.disabled=step===0;next.disabled=step===labels.length-1;state.textContent=`Step ${step+1} of ${labels.length}: ${labels[step]}`;draw(step);};
  back.addEventListener('click',()=>{step--;update();});next.addEventListener('click',()=>{step++;update();});
  return {update,reset:()=>{step=0;update();}};
 }
 function table(host,headers,rows){
  const t=document.createElement('table'),head=document.createElement('thead'),hr=document.createElement('tr');
  for(const text of headers){const th=document.createElement('th');th.scope='col';th.textContent=text;hr.append(th);}head.append(hr);t.append(head);
  const body=document.createElement('tbody');for(const row of rows){const tr=document.createElement('tr');row.forEach((v,i)=>{const td=document.createElement(i===0?'th':'td');if(i===0)td.scope='row';td.textContent=typeof v==='object'?v.text:String(v);if(v?.hit)td.classList.add('is-hit');if(v?.fail)td.classList.add('is-fail');tr.append(td);});body.append(tr);}t.append(body);host.replaceChildren(t);return t;
 }
 function bar(host,label,value,max,cls=''){
  const row=document.createElement('div'),cap=document.createElement('div');cap.className='pir-bar-label';
  const name=document.createElement('span'),number=document.createElement('span');name.textContent=label;number.textContent=value.toLocaleString();cap.append(name,number);
  const track=document.createElement('div'),fill=document.createElement('div');track.className='pir-bar-track';fill.className='pir-bar '+cls;fill.style.width=100*value/max+'%';track.setAttribute('aria-hidden','true');track.append(fill);row.append(cap,track);host.append(row);
 }
 const setups={
  shares(panel){
   const box=controls(panel),target=select(box,'Requested position',[[1,'1'],[2,'2'],[3,'3'],[4,'4']],3),mask=range(box,'Mask choice',0,15,10),view=select(box,'Whose view?',[[0,'Server 0 only'],[1,'Server 1 only'],[2,'Both servers collude']],0),out=output(panel);
   panel.querySelector('p').textContent='The learner controls the client’s mask and target. A real server sees only its own query. The mask control enumerates all 16 possibilities; below the sample, compare the view over all 16 equally likely masks.';
   const draw=()=>{
    const e=[0,0,0,0];e[+target.value-1]=1;const q0=bits(+mask.value,4),q1=xor(q0,e),who=+view.value;
    flow(panel.querySelector('[data-shares-sample]'),who===0?[`Server 0 sees q₀ = ${bitstring(q0)}`]:who===1?[`Server 1 sees q₁ = ${bitstring(q1)}`]:[`q₀ = ${bitstring(q0)}`,`q₁ = ${bitstring(q1)}`,`Combined XOR = ${bitstring(e)}`]);
    const counts=new Map();for(let r=0;r<16;r++){const a=bits(r,4),b=xor(a,e),v=bitstring(who===0?a:who===1?b:xor(a,b));counts.set(v,(counts.get(v)||0)+1);}
    tiles(panel.querySelector('[data-share-distribution]'),[...counts].sort().map(([v,count])=>({text:`${v}: ${count}/16`,hit:who===2})),'pir-distribution');
    out.textContent=who===2?'Combining the queries reveals the one-hot selector. Non-collusion is necessary.':'Every four-bit query has probability 1/16, for every target. Changing the target preserves this whole distribution.';
    panel.dataset.q0=bitstring(q0);panel.dataset.q1=bitstring(q1);
   };[target,view].forEach(x=>x.addEventListener('change',draw));mask.addEventListener('input',draw);draw();
  },
  matrix(panel){
   const box=controls(panel),opts=[1,2,3,4].map(i=>[i,String(i)]),row=select(box,'Client’s target row',opts,2),col=select(box,'Client’s target column',opts,2),mask=range(box,'Mask choice',0,15,10),out=output(panel);
   panel.querySelector('p').textContent='This is the client’s walkthrough. Both servers hold the table, but each receives only its own query share. Advance through their computations.';
   const draw=stage=>{
    const r=+row.value-1,c=+col.value-1,q0=bits(+mask.value,4),e=[0,0,0,0];e[c]=1;const q1=xor(q0,e),a0=X.map(v=>dot(v,q0)),a1=X.map(v=>dot(v,q1)),column=xor(a0,a1);
    const t=table(panel.querySelector('[data-matrix-table]'),['Row','C1','C2','C3','C4'],X.map((values,i)=>[String(i+1),...values]));t.className='pir-matrix';
    [...t.querySelectorAll('tbody tr')].forEach((tr,i)=>{tr.children[c+1].classList.add(i===r?'is-target':'is-query');});
    const lines=[`Client prepares q₀ = ${bitstring(q0)} and q₁ = ${bitstring(q1)}.`, `Server 0 uses q₀ = ${bitstring(q0)} to compute a₀ = ${bitstring(a0)}. Each result bit is one row’s XOR of selected entries.`, `Server 1 uses q₁ = ${bitstring(q1)} to compute a₁ = ${bitstring(a1)}.`, `Client XORs a₀ = ${bitstring(a0)} with a₁ = ${bitstring(a1)} to get column ${c+1}: ${bitstring(column)}.`, `Select entry ${r+1} of column ${bitstring(column)}: X${r+1},${c+1} = ${column[r]}.`];
    flow(panel.querySelector('[data-matrix-stage]'),[lines[stage]]);out.textContent=stage===4?'Only the final row selection happens locally; the row number was never sent.':'The highlighted cell is the client’s target, shown here to explain the computation.';
    panel.dataset.a0=bitstring(a0);panel.dataset.a1=bitstring(a1);panel.dataset.result=column[r];
   };
   const steps=stepper(panel,['Prepare shares','First answer','Second answer','Reconstruct the column','Read the target bit'],draw);
   row.addEventListener('change',steps.reset);col.addEventListener('change',steps.reset);mask.addEventListener('input',steps.reset);steps.update();
  },
  balance(panel){
   const c=select(controls(panel),'Columns for a 64-bit database',[1,2,4,8,16,32,64].map(v=>[v,String(v)]),8),out=output(panel);
   panel.querySelector('p').textContent='Each bar shows total communication in bits on a linear scale. The green bar marks the minimum; the selected layout is labelled. Whole-database download uses 64 bits.';
   const draw=()=>{const plot=panel.querySelector('[data-balance-plot]');plot.className='pir-plot';plot.replaceChildren();for(const cols of [1,2,4,8,16,32,64])bar(plot,`${64/cols} rows × ${cols} cols${cols===+c.value?' ←':''}`,2*cols+128/cols,130,cols===8?'best':'');const cols=+c.value,rows=64/cols;out.textContent=`Upload: ${2*cols} bits. Download: ${2*rows} bits. Total: ${2*cols+2*rows} bits.`;panel.dataset.total=2*cols+2*rows;};c.addEventListener('change',draw);draw();
  },
  recursion(panel){
   const box=controls(panel),opts=[1,2,3,4].map(i=>[i,String(i)]),a=select(box,'Local row a',opts,2),b=select(box,'Column b',opts,3),c=select(box,'Column c',opts,4),out=output(panel);
   panel.querySelector('p').textContent='For 64 records, follow coordinates (a,b,c) through two encrypted selections. Tile labels identify source records for teaching; the real encrypted query does not expose these coordinates.';
   const draw=stage=>{const av=+a.value,bv=+b.value,cv=+c.value,id=((av-1)*4+bv-1)*4+cv,host=panel.querySelector('[data-recursion-stage]');
    if(stage===0)tiles(host,Array.from({length:16},(_,r)=>({text:`Row ${r+1}: records ${4*r+1}–${4*r+4}`,hit:r===(av-1)*4+bv-1})),'pir-recursion-grid');
    if(stage===1)tiles(host,Array.from({length:16},(_,r)=>({text:`Inner record ${4*r+cv}`,hit:r===(av-1)*4+bv-1})),'pir-recursion-grid');
    if(stage===2)tiles(host,[1,2,3,4].map(i=>({text:`Outer record ${((i-1)*4+bv-1)*4+cv}`,hit:i===av})),'pir-recursion-grid records');
    if(stage===3)flow(host,[`Choose outer record ${id} locally.`,`Decrypt the outer encoding → inner ciphertext for record ${id}.`,`Decrypt the inner ciphertext → database bit X${id}.`]);
    out.textContent=[`Start with 16 rows and 4 columns. The target lies in row ${(av-1)*4+bv}, column ${cv}.`,`Selecting column ${cv} leaves 16 inner ciphertexts, now laid out with row a and column b.`,`Selecting column ${bv} of the encrypted table leaves 4 outer-encrypted records.`,`The query contains two length-4 selector vectors; the reply has four nested records. Their bit lengths still need to be counted.`][stage];panel.dataset.record=id;panel.dataset.stage=stage;
   };
   const steps=stepper(panel,['Original table','First private selection','Second private selection','Local choice and decryption'],draw);[a,b,c].forEach(x=>x.addEventListener('change',steps.reset));steps.update();
  },
  expansion(panel){
   const depth=range(controls(panel),'Encryption layers',0,6,4),out=output(panel);
   panel.querySelector('p').textContent='Both models start at 128 bits. Blue doubles the length at each layer; green adds 128 bits per layer. Bars share a linear scale measured in bits.';
   const draw=()=>{const d=+depth.value,plot=panel.querySelector('[data-expansion-plot]');plot.className='pir-plot';plot.replaceChildren();const doubled=128*2**d,added=128*(d+1);bar(plot,'Doubling expansion',doubled,8192);bar(plot,'Additive overhead',added,8192,'additive');out.textContent=`After ${d} layers: ${doubled.toLocaleString()} bits versus ${added.toLocaleString()} bits. Counting both as “one ciphertext” would hide this difference.`;panel.dataset.sizes=[doubled,added].join(',');};depth.addEventListener('input',draw);draw();
  },
  work(panel){
   const n=select(controls(panel),'Database bits',[16,64,256,1024].map(v=>[v,String(v)]),256),out=output(panel);
   panel.querySelector('p').textContent='Keep bits, ciphertext counts and computation counts in separate columns of reasoning. These values describe the constructions, not measured running times.';
   const draw=()=>{const count=+n.value,l=Math.log2(count);table(panel.querySelector('[data-work-table]'),['Quantity','Matrix PIR','FHE PIR'],[['Upload',`${2*Math.sqrt(count)} bits`,`${l+2} ciphertexts`],['Download',`${2*Math.sqrt(count)} bits`,'1 ciphertext'],['Server processing',`${count} table entries per server`,`${count} equality tests of ${l} bits`]]);out.textContent=`Increasing n makes both protocols process more records, even though communication grows much more slowly.`;panel.dataset.work=count*l;};n.addEventListener('change',draw);draw();
  },
  'coefficient-shift'(panel){
   const shift=range(controls(panel),'Shift i',0,4,2),out=output(panel);panel.querySelector('p').textContent='Keep g(X) = 3 + 5X. Move its coefficient list upward by multiplying by Xⁱ; the positions below i must stay zero.';
   const draw=()=>{const i=+shift.value,coeff=Array(i).fill(0).concat([3,5]);tiles(panel.querySelector('[data-shift-strip]'),coeff.map((v,k)=>({text:`X^${k}: ${v}`,hit:v!==0})));out.textContent=`f(X) = 3X^${i} + 5X^${i+1}. Its degree is ${i+1}, and all ${i} positions below ${i} have coefficient zero.`;panel.dataset.coefficients=coeff.join(',');};shift.addEventListener('input',draw);draw();
  },
  'coefficient-split'(panel){
   const index=range(controls(panel),'Coefficient position i',0,3,2),out=output(panel),coef=[4,2,7,3];panel.querySelector('p').textContent='The polynomial is f(X) = 4 + 2X + 7X² + 3X³. Choose the position to reserve for β. The other coefficients must stay strictly below or above it.';
   const draw=()=>{const i=+index.value;tiles(panel.querySelector('[data-coefficient-strip]'),coef.map((v,k)=>({text:`${v} · X^${k}: ${k<i?'lower':k===i?'β':'upper'}`,hit:k===i})));out.textContent=`β = ${coef[i]}. ${i===0?'The lower part is zero.':`The lower part has degree at most ${i-1}.`} ${i===3?'The upper part is zero.':`Factor X^${i+1} from the upper part; the remaining polynomial has degree at most ${2-i}.`}`;};index.addEventListener('input',draw);draw();
  },
  'product-coefficient'(panel){
   const k=range(controls(panel),'Product coefficient position',0,4,2),out=output(panel),a=[1,2,3],b=[4,5,6];panel.querySelector('p').textContent='Rows use coefficients 1, 2, 3 of f; columns use 4, 5, 6 of g. Highlight the products whose exponents add to the selected position. Arithmetic is in F₁₀₁.';
   const draw=()=>{const degree=+k.value,entries=[];let total=0;for(let i=0;i<3;i++)for(let j=0;j<3;j++){const hit=i+j===degree,v=a[i]*b[j];if(hit)total+=v;entries.push({text:`${a[i]}×${b[j]} = ${v}, X^${i+j}`,hit});}tiles(panel.querySelector('[data-product-grid]'),entries,'pir-product-grid');out.textContent=`Coefficient of X^${degree}: ${total} modulo 101.${degree===2?' These are exactly the reversed-inner-product terms.':''}`;panel.dataset.coefficient=total;};k.addEventListener('input',draw);draw();
  },
  'powers-setup'(panel){
   const box=controls(panel),opts=Array.from({length:11},(_,i)=>[i,String(i)]),coeff=[4,2,1].map((v,i)=>select(box,`Coefficient f${i}`,opts,v));
   panel.querySelector('p').textContent='Use the order-11 subgroup generated by 2 modulo 23. The public encoded powers are 2, 8, 6. Change the known polynomial coefficients, raise each public element to its coefficient, and multiply.';
   const result=panel.querySelector('[data-powers-output]');result.setAttribute('role','status');
   const draw=()=>{const values=coeff.map(x=>+x.value),terms=values.map((v,i)=>power([2,8,6][i],v,23)),commitment=terms.reduce((a,b)=>a*b%23,1),exponent=mod(values[0]+3*values[1]+9*values[2],11);result.textContent=`Powered elements: ${terms.join(', ')}. Their product modulo 23 is c = ${commitment}. For this revealed setup α = 3, f(α) = ${exponent} modulo 11, and 2^${exponent} mod 23 = ${power(2,exponent,23)}.`;panel.dataset.commitment=commitment;};coeff.forEach(s=>s.addEventListener('change',draw));draw();
  },
  'opening-check'(panel){
   const box=controls(panel),point=range(box,'Opening point z',0,10,1),tamper=checkbox(box,'Change the claimed value by 1; keep the honest proof',false);
   panel.querySelector('p').textContent='For this arithmetic example, g = 2 modulo 23, group order is 11, α = 3 and f(X) = X² + 2X + 4. Commitment c stays 3. Follow the honest quotient proof at each point, then alter its claimed value.';
   const out=panel.querySelector('[data-opening-output]');out.setAttribute('role','status');
   const draw=()=>{const z=+point.value,y=mod(z*z+2*z+4,11),claimed=mod(y+(tamper.checked?1:0),11),qa=mod(5+z,11),b=mod(3-z,11),c=mod(8-claimed,11),A=power(2,qa,23),B=power(2,b,23),C=power(2,c,23),ok=mod(qa*b,11)===c;out.textContent=`True f(${z}) = ${y}; claimed y = ${claimed}. Public inputs (A, B, C) = (${A}, ${B}, ${C}). The teaching exponents obey ${qa} × ${b} ≡ ${mod(qa*b,11)} modulo 11, compared with ${c}. ${ok?'Accept.':'Reject.'}${A===1||B===1?' An identity group element requires the zero-exponent case.':''}`;panel.dataset.accept=String(ok);};point.addEventListener('input',draw);tamper.addEventListener('change',draw);draw();
  },
  'equality-circuit'(panel){
   const box=controls(panel),a=select(box,'Three-bit string a',Array.from({length:8},(_,i)=>[i,bitstring(bits(i,3))]),5),b=select(box,'Three-bit string b',Array.from({length:8},(_,i)=>[i,bitstring(bits(i,3))]),7),out=output(panel);
   panel.querySelector('p').textContent='At each position, OR the “both 1” and “both 0” cases. Then AND the position results to test the complete strings.';
   const draw=()=>{const av=bits(+a.value,3),bv=bits(+b.value,3),eq=av.map((v,i)=>(v&bv[i])|((1-v)&(1-bv[i])));table(panel.querySelector('[data-equality-circuit]'),['Position','Both 1','Both 0','Equal'],av.map((v,i)=>[i+1,v&bv[i],(1-v)&(1-bv[i]),{text:String(eq[i]),hit:!!eq[i],fail:!eq[i]}]));const result=eq.reduce((x,y)=>x&y,1);out.textContent=`AND of ${eq.join(', ')} = ${result}. The strings ${result?'agree at every position.':'differ, so the final equality test fails.'}`;panel.dataset.result=result;};[a,b].forEach(x=>x.addEventListener('change',draw));draw();
  },
  'fhe-lookup'(panel){
   const target=select(controls(panel),'Requested record',database.map((_,i)=>[i+1,`Record ${i+1}: address ${bitstring(bits(i,3))}`]),3),out=output(panel);
   panel.querySelector('p').textContent='Each equality circuit produces a selector. AND it with that record’s data bit; OR the last column to recover the requested bit.';
   const draw=()=>{const i=+target.value-1;table(panel.querySelector('[data-fhe-table]'),['Address','Data','Equal','Masked'],database.map((v,j)=>[bitstring(bits(j,3)),v,{text:String(i===j?1:0),hit:i===j},{text:String(i===j?v:0),hit:i===j}]));out.textContent=`Address ${bitstring(bits(i,3))} selects record ${i+1}. OR of the masked results is ${database[i]}.`;panel.dataset.result=database[i];};target.addEventListener('change',draw);draw();
  },
  noise(panel){
   const n=range(controls(panel),'Database records n',2,32,8),out=output(panel);panel.querySelector('p').textContent='Apply only the noise rules given in HW4. Advance through the actual equality, masking and final OR gates; the noise is not the plaintext bit.';
   const draw=stage=>{const count=+n.value,l=Math.ceil(Math.log2(count)),values=[8,8**l,2*8**l,2*count*8**l],lines=[`One equality position: 2×2 + 2×2 = ${values[0]}.`,`AND ${l} equality positions: 8^${l} = ${values[1].toLocaleString()}.`,`AND with one encrypted data bit: 2 × ${values[1].toLocaleString()} = ${values[2].toLocaleString()}.`,`OR ${count} masked records: ${count} × ${values[2].toLocaleString()} = ${values[3].toLocaleString()}.`];flow(panel.querySelector('[data-noise-stages]'),lines.slice(0,stage+1));out.textContent=`The address needs ${l} bits.${stage===3?(Number.isInteger(Math.log2(count))?` Since n is a power of two, the result equals 2n⁴.`:` Here n is not a power of two; use 2n·8^ceil(log₂ n), not 2n⁴.`):' Predict the next magnitude before advancing.'}`;panel.dataset.noise=values[3];};const steps=stepper(panel,['One equality position','All address positions','Mask a database bit','OR all records'],draw);n.addEventListener('input',steps.reset);steps.update();
  }
 };
 document.querySelectorAll('[data-pir-lab]').forEach(panel=>setups[panel.dataset.pirLab]?.(panel));
})();
