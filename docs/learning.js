(() => {
  'use strict';
  const root = document.getElementById('lessons');
  if (!root) return;
  const menu = root.querySelector('.chapter-menu');
  const trigger = menu.querySelector('summary');
  let chapterJump = false;
  menu.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    if (link.hash === location.hash) { menu.open = false; trigger.focus(); }
    else chapterJump = true;
  });
  document.addEventListener('click', event => {
    if (menu.open && !menu.contains(event.target)) menu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) { menu.open = false; trigger.focus(); }
  });
  menu.addEventListener('focusout', () => {
    requestAnimationFrame(() => { if (!menu.contains(document.activeElement)) menu.open = false; });
  });
  window.addEventListener('hashchange', () => {
    if (menu.open || chapterJump) {
      menu.open = false; chapterJump = false;
      requestAnimationFrame(() => trigger.focus());
    }
  });

  const mod = (a, q) => ((a % q) + q) % q;
  const power = (g, x, p = 23) => {
    let result = 1;
    for (let i = 0; i < x; i++) result = result * g % p;
    return result;
  };
  const inverse = (a, q) => {
    for (let n = 1; n < q; n++) if (mod(a * n, q) === 1) return n;
    throw new Error('No modular inverse');
  };
  function lab(card, key, title, intro, content, setup) {
    const homeworkMap = {hw1: {29:32}, hw2: {21:39, 38:38, 43:43}};
    const mapped = homeworkMap[root.dataset.chapter]?.[card];
    const reader = root.dataset.chapter.startsWith('hw')
      ? (mapped ? root.querySelector(`[data-source-card="${mapped}"] .reading`) : null)
      : root.querySelector(`#lesson-${card} .reading`);
    if (!reader) return;
    const panel = document.createElement('aside');
    panel.className = 'learning';
    panel.dataset.lab = key;
    panel.setAttribute('aria-labelledby', `${key}-title`);
    panel.innerHTML = `<h3 id="${key}-title">${title}</h3><p>${intro}</p>${content}`;
    const solution=reader.querySelector('.solution-content');
    if(solution)solution.append(panel);else reader.append(panel);
    setup(panel);
  }
  const result = '<output class="lab-result" aria-live="polite" aria-atomic="true"></output>';
  function range(key, label, min, max, value) {
    return `<label for="${key}">${label}<span data-value="${key}">${value}</span></label><input id="${key}" type="range" min="${min}" max="${max}" step="1" value="${value}">`;
  }
  function value(panel, id) {
    const n = Number(panel.querySelector(`#${id}`).value);
    panel.querySelector(`[data-value="${id}"]`).textContent = n;
    return n;
  }
  function diagram(label, body) {
    return `<svg class="lab-diagram" viewBox="0 0 280 230" role="img" aria-label="${label}">${body}</svg>`;
  }
  const point = (i, n, radius = 85) => [140 + radius * Math.sin(i * 2 * Math.PI / n), 115 - radius * Math.cos(i * 2 * Math.PI / n)];
  const line = (a, b, cls = 'edge') => `<line class="${cls}" x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}"/>`;

  if (['commitment','hw1'].includes(root.dataset.chapter)) {
    lab(29, 'guessing', 'How likely is a guess to work?', 'Each square represents one possible secret, and each secret is equally likely. Move the guesses control to check more squares. Each guess checks a different possibility.',
      range('secret-bits', 'Number of bits in the secret', 1, 6, 4) + range('guess-count', 'Number of guesses', 1, 16, 3) +
      '<div class="lab-grid" aria-hidden="true"></div><div class="lab-metric" aria-hidden="true"></div>' + result, panel => {
        const draw = () => {
          const n = value(panel, 'secret-bits'), total = 2 ** n;
          const guesses = panel.querySelector('#guess-count');
          guesses.max = total;
          const q = value(panel, 'guess-count');
          panel.querySelector('.lab-grid').innerHTML = Array.from({length: total}, (_, i) => `<span class="lab-cell ${i < q ? 'is-hit' : ''}"></span>`).join('');
          panel.querySelector('.lab-metric').textContent = `${(100 * q / total).toFixed(2)}%`;
          panel.querySelector('output').textContent = `You have checked ${q} of the ${total} possible secrets. Your chance of finding the secret is therefore ${q}/${total}, or ${(100 * q / total).toFixed(2)}%.`;
        };
        panel.addEventListener('input', draw); draw();
      });
    lab(20, 'hiding-binding', 'Hidden is not the same as fixed', 'The sender has already sent c = 1. Try opening it as a different move. The first rule adds a randomizer and keeps the remainder after dividing by 3; this is what “mod 3” means. The second rule simply sends the move itself.',
      '<label for="commit-mode">Rule for computing c</label><select id="commit-mode"><option value="pad">Add a randomizer: c = m + r mod 3</option><option value="plain">Send the message: c = m</option></select><div class="lab-actions"><button data-move="0" aria-pressed="false">Rock · 0</button><button data-move="1" aria-pressed="true">Paper · 1</button><button data-move="2" aria-pressed="false">Scissors · 2</button></div><div class="lab-equation"></div>' + result +
      '', panel => {
        let message = 1;
        function draw() {
          const pad = panel.querySelector('select').value === 'pad';
          const randomizer = mod(1 - message, 3), accepted = pad || message === 1;
          panel.querySelectorAll('[data-move]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.move) === message)));
          panel.querySelector('.lab-equation').textContent = pad ? `${message} + ${randomizer} ≡ 1 (mod 3) ✓` : `${message} ${accepted ? '=' : '≠'} 1 ${accepted ? '✓' : '✕'}`;
          const out = panel.querySelector('output'); out.dataset.error = !accepted;
          out.textContent = pad ? `Accepted: choosing r = ${randomizer} makes your new move produce the value 1 that was already sent. Try another move: you can still find a value of r that works. This lets the sender change the message, so the rule is not binding.` : `${accepted ? 'Accepted.' : 'Rejected.'} With c = m, only Paper matches the value 1 that was sent. This fixes the move, but the receiver can read it immediately, so the rule is not hiding.`;
        }
        panel.addEventListener('click', event => { const button = event.target.closest('[data-move]'); if (button) { message = Number(button.dataset.move); draw(); } });
        panel.addEventListener('change', draw); draw();
      });
    lab(34, 'modular', 'Walk around a modular clock', 'Choose where to start and how many steps to move. Positive steps go clockwise; negative steps go backwards. After a full lap, you return to the same number.',
      range('modulus', 'Modulus q', 3, 11, 5) + range('start-residue', 'Start a', 0, 4, 4) + range('mod-step', 'Add b', -12, 12, 3) + '<div class="clock-diagram"></div><div class="lab-equation"></div>' + result, panel => {
        const draw = () => {
          const q = value(panel, 'modulus'); panel.querySelector('#start-residue').max = q - 1;
          const a = value(panel, 'start-residue'), b = value(panel, 'mod-step'), end = mod(a + b, q);
          let marks = '<circle cx="140" cy="115" r="85" fill="none" stroke="#cdd8c3" stroke-width="2"/>';
          // Trace at most one lap; the text explains any additional full laps.
          for (let j = 0; j < Math.min(Math.abs(b), q); j++) marks += line(point(mod(a + Math.sign(b) * j, q), q), point(mod(a + Math.sign(b) * (j + 1), q), q), 'cycle');
          for (let i = 0; i < q; i++) { const [x,y] = point(i,q); marks += `<circle class="node ${i === end ? 'selected' : ''}" cx="${x}" cy="${y}" r="15"/><text class="${i === end ? 'selected-label' : ''}" x="${x}" y="${y}">${i}</text>`; }
          marks += `<text x="140" y="104">start ${a}</text><text x="140" y="127">${b >= 0 ? '+' : '−'} ${Math.abs(b)} steps</text>`;
          panel.querySelector('.clock-diagram').innerHTML = diagram(`Start ${a}, add ${b}, finish at ${end} modulo ${q}`, marks);
          panel.querySelector('.lab-equation').textContent = `${a} + (${b}) = ${a + b} ≡ ${end} (mod ${q})`;
          panel.querySelector('output').textContent = `${a + b} = ${Math.floor((a + b) / q)} × ${q} + ${end}. The highlighted residue is always between 0 and ${q - 1}, even when the sum is negative.`;
        }; panel.addEventListener('input', draw); draw();
      });
    lab(49, 'pedersen', 'Why the commitment hides the message', 'This small example uses g = 2 and h = 8, with multiplication modulo 23. There are eleven possible randomizers, from 0 to 10. Change the message and see whether the possible commitment values change.',
      range('pedersen-m', 'Message m', 0, 10, 2) + range('pedersen-r', 'Randomizer r', 0, 10, 3) + '<div class="lab-equation"></div><div class="distribution" aria-label="Commitment probabilities"></div>' + result +
      '<p class="lab-note">These small numbers let us list every outcome. Real commitments use much larger groups.</p>', panel => {
        function draw() {
          const m = value(panel, 'pedersen-m'), r = value(panel, 'pedersen-r');
          const outcomes = Array.from({length: 11}, (_, k) => power(2, m) * power(8, k) % 23);
          const c = outcomes[r];
          panel.querySelector('.lab-equation').innerHTML = `c = 2<sup>${m}</sup> · 8<sup>${r}</sup> mod 23 = <b>${c}</b>`;
          panel.querySelector('.distribution').innerHTML = [...outcomes].sort((a,b) => a-b).map(n => `<span class="${n === c ? 'is-hit' : ''}"><b>${n}</b><small>1 / 11</small></span>`).join('');
          panel.querySelector('output').textContent = `For message ${m}, each of the eleven commitment values is produced by exactly one randomizer. If we choose the randomizer with equal probability each time, every value has probability 1/11. Changing the message leaves these probabilities unchanged, so the commitment does not reveal which message was chosen.`;
        } panel.addEventListener('input', draw); draw();
      });
  } else if (['zero-knowledge','hw2'].includes(root.dataset.chapter)) {
    lab(21, 'graph-proof', 'What does each challenge reveal?', 'The prover has hidden a renamed graph in commitments. In the protocol, the verifier randomly chooses one of two checks. Here you can choose a check yourself to see what it reveals.',
      '<div class="graph-diagram"></div><div class="lab-actions"><button data-challenge="0">0 · Check renaming</button><button data-challenge="1">1 · Check cycle</button></div><button data-new-round>New round</button>' + result, panel => {
        let challenge = null, round = 0;
        function draw() {
          const permutation = [2,4,1,0,3].map(n => (n + round) % 5);
          const cycle = [[0,1],[1,2],[2,3],[3,4],[4,0]], graph = [...cycle,[0,2],[1,3]];
          const edges = challenge === 1 ? cycle : graph;
          let drawing = '';
          if (challenge === null) {
            for (let a = 0; a < 5; a++) for (let b = a+1; b < 5; b++) drawing += line(point(a,5),point(b,5));
          } else {
            for (const [a,b] of edges) drawing += line(point(permutation[a],5),point(permutation[b],5),challenge === 1 ? 'cycle' : 'edge');
          }
          for (let i=0; i<5; i++) { const [x,y] = point(i,5); drawing += `<circle class="node" cx="${x}" cy="${y}" r="18"/><text x="${x}" y="${y}">${String.fromCharCode(65+i)}</text>`; }
          panel.querySelector('.graph-diagram').innerHTML = diagram(challenge === null ? 'Five vertices; all ten adjacency entries are still committed and hidden' : challenge === 1 ? 'A revealed cycle visits all five renamed vertices exactly once' : 'The full renamed graph, including extra edges',drawing);
          panel.querySelectorAll('[data-challenge]').forEach(button => {button.disabled = challenge !== null; button.setAttribute('aria-pressed', String(Number(button.dataset.challenge) === challenge));});
          panel.querySelector('output').textContent = challenge === null ? 'All adjacency entries are sealed. Gray lines represent possible edges, not disclosed edges. The graph is fixed before the challenge arrives.' : challenge === 0 ? `Reveal the graph and renaming: ${permutation.map((n,i) => `${i+1}→${String.fromCharCode(65+n)}`).join(', ')}. Check all edges against the public graph. No witness cycle is singled out.` : 'Reveal only a cycle: every vertex has two cycle neighbors and all five are visited once. Keep the other entries and the original-to-new vertex mapping hidden. Revealing both answers for this same commitment would expose the original cycle.';
        }
        panel.addEventListener('click', event => { const button = event.target.closest('button'); if (!button) return; if (button.hasAttribute('data-new-round')) {round = (round+1)%5; challenge = null;} else if (button.hasAttribute('data-challenge') && challenge === null) challenge = Number(button.dataset.challenge); draw(); }); draw();
      });
    lab(38, 'soundness', 'Why repeating the check catches cheating', 'Imagine a cheater who can answer challenge 0 but cannot answer challenge 1. Each round uses a fresh, fair challenge bit. The verifier accepts only if the cheater passes every round.',
      range('proof-rounds', 'Fresh challenge rounds k', 1, 12, 4) + '<div class="lab-metric"></div><div class="lab-bar" aria-hidden="true"><span></span></div><div class="lab-equation"></div><div class="lab-actions"><button data-add-round>Add one round</button><button data-random-challenge>Try random challenges</button></div>' + result +
      '', panel => {
        function draw() {
          const k = value(panel, 'proof-rounds'), total = 2 ** k;
          panel.querySelector('.lab-metric').textContent = `${(100 / total).toFixed(k > 9 ? 4 : 2)}%`;
          panel.querySelector('.lab-bar span').style.width = `${100/total}%`;
          panel.querySelector('.lab-equation').innerHTML = `(1/2)<sup>${k}</sup> = 1 / ${total}`;
          panel.querySelector('[data-add-round]').disabled = k === 12;
          panel.querySelector('output').textContent = `With ${k} rounds there are ${total} equally likely sequences of challenges. Only the sequence containing all zeros lets this cheater pass. That gives a success probability of 1/${total}.`;
        }
        panel.addEventListener('input', draw);
        panel.querySelector('[data-add-round]').addEventListener('click', () => {panel.querySelector('input').stepUp();draw();});
        panel.querySelector('[data-random-challenge]').addEventListener('click', () => {
          const k = Number(panel.querySelector('input').value), bits = Array.from(crypto.getRandomValues(new Uint8Array(k)), n => n % 2);
          const accepted = bits.every(n => n === 0);
          panel.querySelector('output').textContent = `Challenges: ${bits.join(' ')}. ${accepted ? 'Every challenge was 0, so the cheater passed this time.' : 'A challenge was 1, so the cheater could not answer it and the verifier rejected.'}`;
        }); draw();
      });
    lab(43, 'schnorr', 'Follow the three messages of a Schnorr proof', 'We use the small group from the earlier example: g = 2, with multiplication modulo 23 and exponents modulo 11. The prover knows x = 4, so the public value is y = 2⁴ = 16. For this run the prover chooses r = 3 and sends a = 2³ = 8. Now choose the verifier’s challenge and follow the reply.',
      '<div class="lab-steps"><span>1 · Commit</span><span>2 · Challenge</span><span>3 · Respond</span></div><div class="lab-transcript"></div>' + range('schnorr-e', 'Verifier challenge e', 0, 10, 2) + '<div class="lab-actions"><button data-next-step>Send challenge</button><button data-reset-proof>Restart</button></div><div class="tamper-controls" hidden>' + range('schnorr-offset', 'Tamper: add to response', 0, 10, 0) + '<button data-extract>Show why reusing r reveals x</button></div>' + result + '<div class="extraction"></div>', panel => {
        let stage = 0, e = 2;
        function draw() {
          const z = mod(3 + e * 4, 11), offset = value(panel, 'schnorr-offset'), sent = mod(z + offset, 11);
          panel.querySelectorAll('.lab-steps span').forEach((span,i) => span.classList.toggle('is-done', i <= stage));
          panel.querySelector('.lab-transcript').innerHTML = '<div class="lab-message"><small>Prover → Verifier</small>a = gʳ = 8</div>' + (stage >= 1 ? `<div class="lab-message"><small>Verifier → Prover</small>e = ${e}</div>` : '') + (stage === 2 ? `<div class="lab-message"><small>Prover → Verifier</small>z = r + ex mod 11 = ${sent}</div>` : '');
          panel.querySelector('#schnorr-e').disabled = stage > 0;
          panel.querySelector('[data-next-step]').disabled = stage === 2;
          panel.querySelector('[data-next-step]').textContent = stage === 0 ? 'Send challenge' : stage === 1 ? 'Send response' : 'Transcript complete';
          panel.querySelector('.tamper-controls').hidden = stage !== 2;
          panel.querySelector('.extraction').innerHTML = '';
          const left = power(2, sent), right = 8 * power(16, e) % 23;
          const out = panel.querySelector('output');out.dataset.error = stage === 2 && left !== right;
          out.textContent = stage === 0 ? 'The first message a is fixed before the challenge. Choose e, then send it. In a real run the verifier samples it uniformly.' : stage === 1 ? `Challenge e = ${e} is locked. The prover combines its fresh r with e times its secret x.` : `Verify gᶻ = a · yᵉ mod 23: ${left} ${left === right ? '=' : '≠'} ${right}. ${left === right ? 'Accept: the response satisfies the public equation.' : 'Reject: the changed response no longer satisfies the equation.'}`;
          panel.querySelector('[data-extract]').disabled = offset !== 0;
        }
        panel.querySelector('#schnorr-e').addEventListener('input', () => {e = value(panel, 'schnorr-e');draw();});
        panel.querySelector('#schnorr-offset').addEventListener('input', draw);
        panel.querySelector('[data-next-step]').addEventListener('click', () => {stage = Math.min(2,stage+1);draw();});
        panel.querySelector('[data-reset-proof]').addEventListener('click', () => {stage=0;panel.querySelector('#schnorr-offset').value=0;draw();});
        panel.querySelector('[data-extract]').addEventListener('click', () => {
          const e2 = mod(e + 1, 11), z = mod(3 + e*4,11), z2 = mod(3 + e2*4,11), delta = mod(e-e2,11), inv = inverse(delta,11), x = mod((z-z2)*inv,11);
          panel.querySelector('.extraction').innerHTML = `<p>Suppose the prover uses the same r again but answers a different challenge. These two accepted conversations then have the same first message a:</p><div class="lab-equation">(a, e, z) = (8, ${e}, ${z})<br>(a, e′, z′) = (8, ${e2}, ${z2})</div><p>Each response follows z = r + ex. Subtract the two responses: the repeated r cancels, leaving z − z′ = (e − e′)x modulo 11.</p><p>To recover x, undo multiplication by e − e′. Its remainder is ${delta}, whose inverse is ${inv}, because ${delta} × ${inv} has remainder 1 modulo 11.</p><div class="lab-equation">x = (${z} − ${z2}) · ${inv}<br>mod 11 = <b>${x}</b></div><p>We recovered the secret from the two conversations. This is why the prover must choose a fresh r for each proof.</p>`;
        }); draw();
      });
  }
})();
