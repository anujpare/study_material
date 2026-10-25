/* Progressive teaching interactions: each figure is also meaningful without JS. */
(() => {
  'use strict';
  const mod = (x, p) => ((x % p) + p) % p;
  const power = (x, n, p) => {
    let result = 1;
    for (let i = 0; i < n; i++) result = result * x % p;
    return result;
  };
  function controls(panel) {
    const box = document.createElement('div');
    box.className = 'snark-controls';
    panel.querySelector('figcaption').after(box);
    return box;
  }
  function select(box, label, choices, initial) {
    const wrap = document.createElement('label');
    wrap.append(document.createTextNode(label));
    const input = document.createElement('select');
    for (const [value, text] of choices) input.add(new Option(text, value));
    input.value = String(initial);
    wrap.append(input); box.append(wrap);
    return input;
  }
  function range(box, label, min, max, initial) {
    const wrap = document.createElement('label');
    const caption = document.createElement('span');
    const input = document.createElement('input');
    input.type = 'range'; input.min = min; input.max = max; input.value = initial;
    input.setAttribute('aria-label', label);
    const update = () => caption.textContent = `${label}: ${input.value}`;
    input.addEventListener('input', update); update();
    wrap.append(caption, input); box.append(wrap);
    return input;
  }
  function checkbox(box, label, checked) {
    const wrap = document.createElement('label'), input = document.createElement('input');
    input.type = 'checkbox'; input.checked = checked;
    wrap.append(input, document.createTextNode(label)); box.append(wrap);
    return input;
  }
  function output(panel) {
    const out = document.createElement('output');
    out.setAttribute('aria-live', 'polite'); out.setAttribute('aria-atomic', 'true');
    panel.append(out); return out;
  }
  function tiles(el, entries) {
    el.replaceChildren(...entries.map(({text, hit=false, fail=false}) => {
      const span = document.createElement('span'); span.textContent = text;
      if (hit) span.classList.add('is-hit'); if (fail) span.classList.add('is-fail');
      return span;
    }));
  }
  const setups = {
    roots(panel) {
      const box = controls(panel), field = select(box, 'Arithmetic domain', [[6,'Modulo 6: not a field'],[7,'Modulo 7: a field']], 6);
      panel.querySelector('p').textContent = 'Evaluate f(X) = 2X² + 4X at every allowed input. A check mark identifies a root.';
      const out = output(panel);
      const draw = () => {
        const p = +field.value, entries = Array.from({length:p}, (_,x) => ({x, y:mod(2*x*x+4*x,p)}));
        tiles(panel.querySelector('[data-roots]'), entries.map(({x,y})=>({text:`${x} → ${y}${y===0?' ✓':''}`,hit:y===0})));
        const roots = entries.filter(e=>e.y===0).map(e=>e.x);
        out.textContent = `Roots: ${roots.join(', ')}. ${p===6?'Four roots exceed the degree 2 because cancellation fails in this domain.':'Two roots respect the degree-2 bound over this field.'}`;
      };
      field.addEventListener('change',draw); draw();
    },
    schnorr(panel) {
      const z = range(controls(panel), 'Response z', 0, 10, 10);
      const result = panel.querySelector('[data-schnorr-result]');
      result.setAttribute('role','status');
      const draw = () => {
        const left=power(2,+z.value,23),right=16*power(8,2,23)%23;
        result.textContent=`gᶻ = ${left}; u · hᶜ = ${right} (modulo 23). ${left===right?'Accept: both sides agree.':'Reject: changing z broke the verification equation.'}`;
      };
      z.addEventListener('input',draw); draw();
    },
    'challenge-space'(panel) {
      const bits = range(controls(panel),'Challenge bits',1,6,3), out=output(panel);
      panel.querySelector('p').textContent='Each tile is one possible challenge vector. The marked vector is the most a false statement can answer for fixed first messages.';
      const draw=()=>{
        const n=+bits.value,total=2**n;
        tiles(panel.querySelector('[data-vectors]'),Array.from({length:total},(_,i)=>({text:i.toString(2).padStart(n,'0')+(i===0?' ✓':''),hit:i===0})));
        out.textContent=`At most 1 acceptable vector out of ${total}: the interactive error bound is 1/${total}. Each extra challenge bit doubles the denominator.`;
      };
      bits.addEventListener('input',draw);draw();
    },
    'pcp-checks'(panel) {
      const box=controls(panel), paths=checkbox(box,'All requested bits have valid authentication paths',true), predicate=checkbox(box,'All PCP logical tests accept the committed bits',false);
      const result=panel.querySelector('[data-pcp-result]');result.setAttribute('role','status');
      const draw=()=>{
        result.textContent=paths.checked&&predicate.checked?'Accept: the answers are authenticated and all logical tests pass.':!paths.checked?'Reject: the answers are not authenticated under the committed root.': 'Reject: valid authentication paths cannot rescue a failed PCP test.';
      };
      paths.addEventListener('change',draw);predicate.addEventListener('change',draw);draw();
    },
    equality(panel) {
      const field=select(controls(panel),'Field size',[[7,'F₇'],[11,'F₁₁'],[17,'F₁₇']],7),out=output(panel);
      panel.querySelector('p').textContent='For h(X) = (X − 1)(X − 3), each row is one input x. The dot shows h(x), from zero at the left to p − 1 at the right. Inputs with h(x) = 0 fool the equality test.';
      const plot=panel.querySelector('[data-equality-plot]');plot.className='snark-scatter';
      const draw=()=>{
        const p=+field.value;
        plot.replaceChildren(...Array.from({length:p},(_,x)=>{
          const y=mod((x-1)*(x-3),p), row=document.createElement('div');row.className='snark-scatter-row';row.setAttribute('aria-label',`Input ${x}, value ${y}${y===0?', root':''}`);
          const label=document.createElement('span');label.textContent=`${x}${y===0?' ✓':''}`;
          const track=document.createElement('span');track.className='snark-track';track.setAttribute('aria-hidden','true');
          const dot=document.createElement('span');dot.className='snark-dot'+(y===0?' is-hit':'');dot.style.left=`${100*y/(p-1)}%`;track.append(dot);
          const value=document.createElement('span');value.textContent=y;row.append(label,track,value);return row;
        }));
        out.textContent=`Exactly 2 roots among ${p} inputs: this false identity passes a uniform test with probability 2/${p}. The dots are finite-field values, not samples of a continuous real curve.`;
      };
      field.addEventListener('change',draw);draw();
    },
    interpolation(panel) {
      const box=controls(panel), choices=Array.from({length:7},(_,i)=>[i,String(i)]), values=[3,1,2].map((v,i)=>select(box,`Value f(${i})`,choices,v)), out=output(panel);
      panel.querySelector('p').textContent='Keep the addresses 0, 1, 2 in F₇. Change their stored values and watch the unique degree-at-most-2 interpolant change.';
      const draw=()=>{
        const [v0,v1,v2]=values.map(x=>+x.value), a=mod(4*(v2-2*v1+v0),7),b=mod(v1-v0-a,7),c=v0;
        tiles(panel.querySelector('[data-interpolation-table]'),[0,1,2].map(x=>({text:`f(${x}) = ${mod(a*x*x+b*x+c,7)} ✓`,hit:true})));
        out.textContent=`f(X) = ${a}X² + ${b}X + ${c} over F₇. Substitution recovers every chosen table value.`;
        panel.dataset.coefficients=[a,b,c].join(',');
      };
      values.forEach(x=>x.addEventListener('change',draw));draw();
    },
    unity(panel) {
      const candidate=select(controls(panel),'Candidate ω',[[6,'6: order 12'],[1,'1: repeats immediately'],[96,'96: order 2']],6);
      const result=panel.querySelector('[data-unity-result]');result.setAttribute('role','status');
      const draw=()=>{
        const w=+candidate.value, values=Array.from({length:12},(_,i)=>power(w,i,97)),seen=new Set();
        tiles(panel.querySelector('[data-unity-grid]'),values.map((v,i)=>{const duplicate=seen.has(v);seen.add(v);return {text:`ω^${i} = ${v}${duplicate?' repeat':''}`,fail:duplicate};}));
        result.textContent=`ω¹² = ${power(w,12,97)}, but there are ${seen.size} distinct addresses. ${seen.size===12?'These twelve points support the trace interpolation.':'This candidate cannot address twelve different trace slots.'}`;
      };
      candidate.addEventListener('change',draw);draw();
    },
    trace(panel) {
      const wires={'x1':[11,0],'x2':[10,1,3],'w1':[9,4],'gate0':[2,6],'gate1':[5,7],'output':[8]};
      const choice=select(controls(panel),'Highlight one wire', [['x1','Public input x₁'],['x2','Public input x₂'],['w1','Private input w₁'],['gate0','Gate 0 output'],['gate1','Gate 1 output'],['output','Final output']], 'x2'),out=output(panel);
      const values=[2,4,8,4,3,7,8,7,56,3,4,2];
      const draw=()=>{
        const selected=wires[choice.value];
        tiles(panel.querySelector('[data-trace-grid]'),values.map((v,i)=>({text:`${i}: ${v}${selected.includes(i)?' ✓':''}`,hit:selected.includes(i)})));
        out.textContent=`Slots ${selected.join(', ')} carry this wire. Their stored values must agree, even though their addresses are different.`;
      };
      choice.addEventListener('change',draw);draw();
    },
    obligations(panel) {
      const examples={
        valid:{inputs:[2,4,3],gates:[[2,4,8],[4,3,7],[8,7,56]]},
        public:{inputs:[3,4,33],gates:[[3,4,12],[4,33,37],[12,37,56]]},
        gate:{inputs:[2,4,13],gates:[[2,4,9],[4,13,17],[9,17,56]]},
        wire:{inputs:[2,4,2],gates:[[2,4,8],[5,2,7],[8,7,56]]},
        output:{inputs:[2,4,4],gates:[[2,4,8],[4,4,8],[8,8,64]]}
      };
      const choice=select(controls(panel),'Candidate trace', [['valid','Valid computation'],['public','Wrong public input'],['gate','Wrong gate calculation'],['wire','Broken wire copy'],['output','Wrong final output']], 'valid'),out=output(panel);
      panel.querySelector('p').textContent='The verifier expects public inputs 2, 4 and output 56. Choose a candidate trace, then inspect the four checks. Arithmetic is modulo 97.';
      const draw=()=>{
        const {inputs,gates}=examples[choice.value], [a,b,c]=gates;
        const checks=[inputs[0]===2&&inputs[1]===4,c[2]===56,mod(a[0]*a[1],97)===a[2]&&mod(b[0]+b[1],97)===b[2]&&mod(c[0]*c[1],97)===c[2],inputs[0]===a[0]&&inputs[1]===a[1]&&inputs[1]===b[0]&&inputs[2]===b[1]&&a[2]===c[0]&&b[2]===c[1]];
        const trace=panel.querySelector('[data-obligation-trace]');
        trace.replaceChildren();const p=document.createElement('p');p.textContent=`Stored inputs: x₁ = ${inputs[0]}, x₂ = ${inputs[1]}, w₁ = ${inputs[2]}.`;trace.append(p);
        const table=document.createElement('table');table.innerHTML='<thead><tr><th>Gate</th><th>Left</th><th>Right</th><th>Output</th></tr></thead><tbody>'+gates.map((g,i)=>`<tr><th>${i}: ${i===1?'+':'×'}</th>${g.map(v=>`<td>${v}</td>`).join('')}</tr>`).join('')+'</tbody>';trace.append(table);
        const names=['Public inputs','Output','Gates','Wire copies'];
        tiles(panel.querySelector('[data-obligation-result]'),checks.map((ok,i)=>({text:`${names[i]}: ${ok?'pass ✓':'fail ✗'}`,hit:ok,fail:!ok})));
        const explanation={valid:'Every required relation holds.',public:'The table uses x₁ = 3, while the public statement requires x₁ = 2.',gate:'Gate 0 claims 2 × 4 = 9, but the product is 8.',wire:'Gate 1 uses 5 for x₂, while the input slot and gate 0 use 4.',output:'The computation is internally consistent, but produces 64 instead of the claimed 56.'};
        out.textContent=explanation[choice.value];panel.dataset.checks=checks.map(Number).join(',');
      };
      choice.addEventListener('change',draw);draw();
    },
    selector(panel) {
      const box=controls(panel),gate=select(box,'Gate operation',[[1,'Addition: selector 1'],[0,'Multiplication: selector 0']],1),claimed=range(box,'Claimed output',0,15,7);
      panel.querySelector('p').textContent='Keep inputs L = 4 and R = 3. Choose the operation and claimed output. A zero residual means this gate equation holds.';
      const result=panel.querySelector('[data-selector-result]');result.setAttribute('role','status');
      const draw=()=>{
        const s=+gate.value,o=+claimed.value,residual=mod(s*7+(1-s)*12-o,97);
        result.textContent=`${s===1?'4 + 3':'4 × 3'} − ${o} = ${residual} in F₉₇. ${residual===0?'This gate passes.':'This gate fails.'}`;panel.dataset.residual=residual;
      };
      gate.addEventListener('change',draw);claimed.addEventListener('input',draw);draw();
    }
  };
  document.querySelectorAll('[data-snark-lab]').forEach(panel=>setups[panel.dataset.snarkLab]?.(panel));
})();
