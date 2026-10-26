// Alternate visual explanations for existing cards. The static lesson remains
// readable without JavaScript; switching views never changes the card sequence.
document.addEventListener('DOMContentLoaded', () => {
  'use strict';
  const root = document.getElementById('lessons');
  if (!root) return;
  const deck = root.dataset.chapter;
  const out = '<output class="lab-result" aria-live="polite" aria-atomic="true"></output>';
  const range = (id, label, min, max, value) => `<label for="${id}">${label}<span data-value="${id}">${value}</span></label><input id="${id}" type="range" min="${min}" max="${max}" value="${value}">`;
  const value = (panel, id) => {
    const n = Number(panel.querySelector(`#${id}`).value);
    panel.querySelector(`[data-value="${id}"]`).textContent = n;
    return n;
  };
  const number = n => n.toLocaleString('en-US');
  function panel(key, title, intro, content, setup) {
    const el = document.createElement('aside');
    el.className = 'learning concept'; el.dataset.lab = key;
    el.id = `${key}-visual`; el.setAttribute('aria-labelledby', `${key}-title`);
    el.innerHTML = `<h3 id="${key}-title">${title}</h3><p>${intro}</p>${content}`;
    setup(el);
    return el;
  }
  function lesson(chapter, id, ...args) {
    if (deck !== chapter) return;
    const reader = root.querySelector(`#lesson-${id} .reading`);
    if (!reader) return;
    const visual = panel(...args);
    // The text is the primary explanation. The experiment follows it visibly.
    reader.append(visual);

  }

  lesson('commitment', 10, 'growth', 'What changes when the input grows?',
    'Compare n² steps with 2ⁿ steps. Move n to the right and watch how quickly the two costs separate. Both curves use the same scale; this illustrates the attacker runtime model.',
    range('growth-n', 'Input size n', 1, 12, 4) + '<div class="growth-plot"></div><div class="plot-key"><span class="key-square">n² steps</span><span class="key-exp">2ⁿ steps</span></div>' + out, p => {
      const draw = () => {
        const n = value(p, 'growth-n'), max = Math.max(n * n, 2 ** n), left = 58, right = 278, top = 30, bottom = 190;
        const x = i => left + (i - 1) / Math.max(1, n - 1) * (right - left);
        const y = cost => bottom - cost / max * (bottom - top);
        const curve = f => Array.from({length: n}, (_, i) => `${x(i + 1)},${y(f(i + 1))}`).join(' ');
        p.querySelector('.growth-plot').innerHTML = `<svg class="lab-diagram growth-chart" viewBox="0 0 320 245" role="img" aria-label="At input size ${n}, n squared takes ${n*n} steps and 2 to the n takes ${2**n} steps. Vertical axis: steps, from 0 to ${max}; horizontal axis: input size, from 1 to ${n}."><path class="plot-axis" d="M${left} ${top}V${bottom}H${right}"/><path class="plot-grid" d="M${left} ${top}H${right}"/><text x="28" y="${top}">${max}</text><text x="28" y="${bottom}">0</text><text x="${left}" y="211">1</text>${n > 1 ? `<text x="${right}" y="211">${n}</text>` : ''}<text x="165" y="236">Input size n</text><text x="160" y="10">Number of steps</text><polyline class="plot-square" points="${curve(i=>i*i)}"/><polyline class="plot-exp" points="${curve(i=>2**i)}"/><circle class="dot-square" cx="${x(n)}" cy="${y(n*n)}" r="5"/><circle class="dot-exp" cx="${x(n)}" cy="${y(2**n)}" r="4"/></svg>`;
        const relation = 2 ** n === n * n ? 'The costs are equal here. Try a larger n.' : 2 ** n > n * n ? `The exponential cost is ${(2**n/(n*n)).toFixed(1)} times the square cost. Each extra bit doubles the exponential cost.` : 'The exponential cost is smaller here. A comparison at one small input does not tell us which grows faster.';
        p.querySelector('output').textContent = `At n = ${n}, n² is ${number(n*n)} steps and 2ⁿ is ${number(2**n)} steps. ${relation}`;
      };
      p.addEventListener('input', draw); draw();
    });

  lesson('commitment', 13, 'negligible', 'Small enough for every threshold?',
    'Negligible means eventually smaller than 1/λᵈ for every fixed positive d. Choose a function and make the threshold stricter by increasing d. Tap a value of λ to inspect the comparison.',
    '<label for="negligible-function">Function to test</label><select id="negligible-function"><option value="exponential">1 / (2 to the power λ)</option><option value="polynomial">1 / λ⁵</option></select>' + range('negligible-d', 'Threshold exponent d', 1, 8, 4) + '<div class="threshold-samples" role="group" aria-label="Compare at a security size"></div>' + out, p => {
      let selected = 16;
      const draw = () => {
        const d = value(p, 'negligible-d'), exponential = p.querySelector('select').value === 'exponential';
        const denominator = n => exponential ? 2n ** BigInt(n) : BigInt(n) ** 5n;
        const limit = n => BigInt(n) ** BigInt(d);
        p.querySelector('.threshold-samples').innerHTML = [4,8,16,32,64,128].map(n => `<button type="button" data-size="${n}" aria-pressed="${n===selected}" class="${denominator(n)>limit(n)?'below-threshold':'above-threshold'}">λ = ${n}<span>${denominator(n)>limit(n)?'Below':'Not below'}</span></button>`).join('');
        const a = denominator(selected), b = limit(selected), sign = a > b ? '>' : a === b ? '=' : '<';
        const power = exponential ? `2<sup>${selected}</sup>` : `${selected}<sup>5</sup>`;
        const conclusion = exponential
          ? 'For any fixed d, doubling repeatedly eventually outgrows the fixed power λᵈ. The finite samples help you see this; the explanation above gives the general argument.'
          : d < 5 ? 'This function beats the chosen threshold, but negligible requires every fixed d. Try d = 6.' : 'This function never gets below this threshold for λ > 1. One such fixed d is enough to show it is not negligible.';
        p.querySelector('output').innerHTML = `At λ = ${selected}, the denominators satisfy ${power} ${sign} ${selected}<sup>${d}</sup>. ${a>b?'The function is below the threshold.':a===b?'The function equals the threshold, so the strict inequality does not hold.':'The function is above the threshold.'}<span class="concept-takeaway">${conclusion}</span>`;
      };
      p.addEventListener('input', draw); p.addEventListener('change', draw);
      p.addEventListener('click', e => {const b=e.target.closest('[data-size]');if(b){selected=Number(b.dataset.size);draw();p.querySelector(`[data-size="${selected}"]`).focus({preventScroll:true});}});
      draw();
    });

  lesson('commitment', 22, 'distinguishing', 'Build a test that tells two worlds apart',
    'Each world has eight equally likely tickets, labeled 0, 1, 2 or 3. Your test answers 1 when the drawn label is one you select. Compare how often it answers 1 in each world.',
    '<label for="world-pair">Worlds to compare</label><select id="world-pair"><option value="different">Different ticket counts</option><option value="same">Identical ticket counts</option></select><div class="world-tickets"></div><fieldset class="outcome-choices"><legend>Answer 1 for these labels</legend>'+[0,1,2,3].map(n=>`<label><input type="checkbox" value="${n}" ${n===0?'checked':''}>${n}</label>`).join('')+'</fieldset>'+out, p => {
      const draw = () => {
        const worlds = p.querySelector('select').value === 'same' ? [[2,2,2,2],[2,2,2,2]] : [[4,2,1,1],[1,1,2,4]];
        const chosen = [...p.querySelectorAll('input:checked')].map(el=>Number(el.value));
        const hits = worlds.map(counts=>chosen.reduce((sum,n)=>sum+counts[n],0));
        p.querySelector('.world-tickets').innerHTML = worlds.map((counts,i)=>`<div class="world-row"><strong>World ${i}</strong><div class="tickets" aria-label="${counts.map((v,k)=>`${v} tickets labeled ${k}`).join(', ')}">${counts.flatMap((count,n)=>Array.from({length:count},()=>`<span class="ticket ${chosen.includes(n)?'ticket-chosen':''}">${n}</span>`)).join('')}</div><span>${hits[i]} of 8 selected</span></div>`).join('');
        const gap = Math.abs(hits[0]-hits[1]);
        p.querySelector('output').textContent = `Your test answers 1 with probability ${hits[0]}/8 in World 0 and ${hits[1]}/8 in World 1. Its advantage is the difference: ${gap}/8 = ${gap/8}. ${gap?'The same test behaves differently in the two worlds, giving an observer a clue about which world supplied the ticket.':'This test gives no clue: it answers 1 equally often in both worlds.'}`;
      };
      p.addEventListener('change', draw); draw();
    });

  const collision = ['collision-pairs', 'Why collisions depend on pairs',
    'A collision needs two different inputs with the same output. The square at row i, column j compares query i with query j. We count each pair once and leave out comparisons of a query with itself. Increase Q to see how many pairs appear.',
    range('collision-q', 'Number of different queries Q', 2, 8, 4) + range('collision-bits', 'Bits in each oracle output', 3, 10, 8) + '<div class="pair-grid" role="img"></div>' + out, p => {
      const draw = () => {
        const q=value(p,'collision-q'), bits=value(p,'collision-bits'), pairs=q*(q-1)/2, outputs=2**bits;
        const grid=p.querySelector('.pair-grid'); grid.style.setProperty('--pair-columns',q+1);
        grid.setAttribute('aria-label',`${q} queries make ${pairs} distinct pairs. Each highlighted square is one pair.`);
        grid.innerHTML='<span></span>'+Array.from({length:q},(_,j)=>`<b>${j+1}</b>`).join('')+Array.from({length:q},(_,i)=>`<b>${i+1}</b>`+Array.from({length:q},(_,j)=>`<span class="${j>i?'query-pair':''}">${j>i?'•':'–'}</span>`).join('')).join('');
        p.querySelector('output').innerHTML = `There are ${pairs} pairs: Q(Q−1)/2 = ${q}×${q-1}/2. Each pair matches with probability 1/${outputs}. Adding these chances gives an <strong>upper bound</strong> of ${pairs}/${outputs}${pairs>=outputs?' (use 1, since a probability cannot exceed 1). This bound is too large to tell us how likely a collision really is; it does not mean a collision is certain.':`, or ${(100*pairs/outputs).toFixed(2)}%, for any collision. Every new query is compared with all the earlier queries, which is why the number of pairs grows faster than Q.`}`;
      };
      p.addEventListener('input',draw);draw();
    }];
  lesson('commitment',31,...collision);
  if(deck==='hw1') {
    const old=root.querySelector('[data-lab="guessing"]');
    if(old)old.replaceWith(panel(...collision));
  }

  lesson('commitment',51,'binding-reduction','Turn a double opening into the hidden exponent',
    'A reduction turns one successful attack into a solution to another problem. Here a solver receives g = 2 and h = 8 modulo 23. Its job is to find x in h = gˣ. Follow how a hypothetical binding attacker helps it.',
    '<ol class="proof-flow"><li data-stage="0">Receive g and h</li><li data-stage="1">Ask the attacker</li><li data-stage="2">Cancel equal commitments</li><li data-stage="3">Recover x</li></ol><div class="proof-scene"></div><div class="lab-actions"><button type="button" data-back>Previous step</button><button type="button" data-next>Next step</button></div>'+out, p => {
      let step=0;
      const scenes=[
        ['<div class="flow-box">Public input<br>g = 2, h = 8</div><div class="flow-arrow" aria-hidden="true">↓</div><div class="flow-box">Solver<br>x = ?</div>','The group has order 11, so exponents are calculated modulo 11. The solver knows the public values, but has not been given x.'],
        ['<div class="flow-box">Hypothetical attacker</div><div class="flow-arrow" aria-hidden="true">↓</div><div class="flow-box">Opening A: m = 2, r = 3<br>Opening B: m′ = 7, r′ = 5</div><div class="lab-equation">2² · 8³ mod 23 = 1<br>2⁷ · 8⁵ mod 23 = 1</div>','Suppose the attacker returns these different messages with the same commitment. The solver checks both openings. We are assuming a successful attacker here so we can see what its success would imply.'],
        ['<div class="flow-box">Same commitment</div><div class="flow-arrow" aria-hidden="true">↓</div><div class="lab-equation">g<sup>m</sup>h<sup>r</sup> = g<sup>m′</sup>h<sup>r′</sup><br>m + xr ≡ m′ + xr′<br>m − m′ ≡ x(r′ − r)<br>2 − 7 ≡ x(5 − 3) mod 11</div>','Replace h with gˣ. Equality of the group elements gives equality of their exponents modulo 11. Moving the message terms to one side and the x terms to the other isolates the unknown.'],
        ['<div class="lab-equation">−5 ≡ 2x mod 11<br>2⁻¹ ≡ 6 mod 11<br>x ≡ −5 · 6 ≡ <b>3</b> mod 11</div><div class="flow-box">Check: 2³ mod 23 = 8 = h</div>','Multiplying by 6 undoes multiplication by 2, because 2×6 leaves remainder 1 modulo 11. The solver has recovered x using the attacker’s two openings. Thus an efficient binding attacker would give an efficient discrete-log solver.']
      ];
      const draw=()=>{
        p.querySelectorAll('[data-stage]').forEach((li,i)=>{li.classList.toggle('current-step',i===step);if(i===step)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current');});
        p.querySelector('.proof-scene').innerHTML=scenes[step][0];p.querySelector('output').textContent=scenes[step][1];
        p.querySelector('[data-back]').disabled=step===0;p.querySelector('[data-next]').disabled=step===3;
      };
      p.querySelector('[data-back]').addEventListener('click',()=>{step=Math.max(0,step-1);draw();});
      p.querySelector('[data-next]').addEventListener('click',()=>{step=Math.min(3,step+1);draw();});draw();
    });

  lesson('zero-knowledge',24,'simulator-retry','Why the simulator sometimes starts again',
    'The simulator does not know a secret cycle. It prepares for one check before learning the verifier’s challenge. Focus here on an honest verifier with a fair challenge bit. In the simulation, each attempt uses a fresh random guess; here you choose the cases to inspect.',
    '<label for="prepared-check">Prepare to answer</label><select id="prepared-check"><option value="0">0 · Show a renamed copy of the public graph</option><option value="1">1 · Show a cycle in a prepared graph</option></select><div class="retry-flow"></div><div class="lab-actions"><button type="button" data-challenge="0">Ask challenge 0</button><button type="button" data-challenge="1">Ask challenge 1</button></div><button type="button" data-retry>Start another attempt</button>'+out, p => {
      let challenge=null;
      const draw=()=>{
        const guess=Number(p.querySelector('select').value), matched=challenge===guess;
        p.querySelector('.retry-flow').innerHTML=`<div class="flow-box">Prepared for check ${guess}</div><div class="flow-arrow" aria-hidden="true">↓</div><div class="flow-box">${challenge===null?'Challenge has not arrived':`Verifier asks ${challenge}`}</div>${challenge===null?'':`<div class="flow-arrow" aria-hidden="true">↓</div><div class="flow-box ${matched?'flow-accept':'flow-retry'}">${matched?'Keep this completed view':'Discard this attempt and restore the verifier’s saved state'}</div>`}`;
        p.querySelector('select').disabled=challenge!==null;p.querySelectorAll('[data-challenge]').forEach(b=>b.disabled=challenge!==null);p.querySelector('[data-retry]').disabled=challenge===null;
        p.querySelector('output').textContent=challenge===null
          ? guess===0?'Renaming the public graph needs no secret cycle. This preparation can answer check 0. Try either verifier challenge to see what happens.':'The simulator can build a graph containing a cycle it chose itself. This preparation can answer check 1, but it need not be a renamed copy of the public graph.'
          : matched?'The prepared answer matches the requested check, so the simulator can finish this view. A fair challenge matches one of two possible guesses, giving success probability 1/2 per attempt and two attempts on average.':'The simulator cannot answer this check with its prepared information. It discards the attempt and retries from the saved state. The kept output contains only the successful attempt; rewinding is a tool used in the simulation proof.';
      };
      p.querySelector('select').addEventListener('change',draw);
      p.querySelectorAll('[data-challenge]').forEach(b=>b.addEventListener('click',()=>{challenge=Number(b.dataset.challenge);draw();}));
      p.querySelector('[data-retry]').addEventListener('click',()=>{challenge=null;draw();});draw();
    });
});
