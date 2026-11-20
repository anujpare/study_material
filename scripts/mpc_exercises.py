"""MPC homework and malicious-security teaching, authored from HW6 FS2025 v1.

CARDS is consumed by build-mpc.py. All homework answers live in check.solution.
"""

CARDS = [
    {
        'id': 'hw6-1b', 'title': 'Can equality disclose an extra input?',
        'section': 'I · What MPC protects', 'kind': 'homework', 'exercise': 'HW6 1(b)',
        'source': 'HW6, p. 1, Problem 1(b)', 'source_ref': 'hw6',
        'requires': ['simulation-test'],
        'body': r'''<p>The ideal execution gives each party its own input and the prescribed output. To disprove a claim about <em>every</em> function, one function is enough. A constant function is useful because its output gives no information about the other input.</p><p>Interpret “reveals the other input” as an additional, reliable disclosure, so the recipient learns that the disclosed value really is the other input. Simply writing down your own input is not such a disclosure.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 1(b).</strong> True or false? For every function \(f:\mathcal X\times\mathcal X\to\{0,1\}\), there is a secure two-party protocol that reveals each party's input to the other whenever the inputs are equal. Give one sentence of justification, supported by a concrete function.</p>''',
            'hint': r'''<p>Let \(f\) always output zero. Keep Alice's input fixed and compare two possible inputs for Bob.</p>''',
            'solution': r'''<p><strong>False under the intended disclosure interpretation.</strong> Take \(\mathcal X=\{0,1\}\) and \(f(x_A,x_B)=0\). Fix Alice's input at zero. Whether Bob's input is zero or one, Alice's ideal information is exactly \((x_A,y)=(0,0)\).</p><p>A reliable additional disclosure that Bob's input equals Alice's would distinguish these two cases. A simulator receiving only \((0,0)\) cannot produce different reliable disclosures for the two cases, because its input has not changed. Hence this disclosure cannot be guaranteed for every functionality.</p><p><strong>Exam-length answer:</strong> False: for a constant function, reliably revealing equality would distinguish two input pairs with the same own input and function output, which violates simulation privacy.</p><aside class="note"><p>The wording is ambiguous if “reveals” means only “outputs a guess that happens to be right.” Alice can always output her own value, which is right when the inputs coincide; that does not establish that Bob has that value. Also, equality is not universally forbidden: a functionality that outputs equality is allowed to disclose it.</p></aside>''',
            'rubric': ['Choose a constant functionality.', 'Hold the recipient’s own input and output fixed.', 'Explain why a reliable extra disclosure distinguishes the two possible other inputs.']
        }
    },
    {
        'id': 'hw6-1ai', 'title': 'Does sharing rely on a hard problem?',
        'section': 'II · Computing on shares', 'kind': 'homework', 'exercise': 'HW6 1(a.i)',
        'source': 'HW6, p. 1, Problem 1(a.i)', 'source_ref': 'hw6',
        'requires': ['additive-privacy'],
        'body': r'''<p>A computational security argument says that an attack requires too much computation. A perfect-privacy argument says that the observed values have exactly the same distribution for every possible secret. No amount of computation separates identical distributions.</p><p>The question \(\mathrm P=\mathrm{NP}\) asks whether every decision problem with efficiently checkable yes-certificates can also be solved efficiently. Here “efficiently” means using a number of steps bounded by a fixed power of the input length. You only need to decide whether the sharing argument assumes that some computation is hard.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 1(a.i).</strong> True or false? In a world where \(\mathrm P=\mathrm{NP}\), additive secret-sharing schemes exist. Justify your answer in one sentence.</p>''',
            'hint': r'''<p>With two shares, write \(s_1=r\) and \(s_2=\alpha-r\), where \(r\) is uniform in \(\mathbb F_p\). Does either single-share distribution depend on \(\alpha\)?</p>''',
            'solution': r'''<p><strong>True.</strong> In an \(n\)-party additive sharing of \(\alpha\), every possible fixed list of \(n-1\) observed shares occurs with probability \(p^{-(n-1)}\). There are \(p\) choices for each of those shares, hence \(p^{n-1}\) equally likely lists. This probability is the same for every \(\alpha\): the remaining share is whatever makes the total equal to \(\alpha\).</p><p>The privacy proof therefore compares identical distributions. It does not ask the observer to fail at a hard computational problem.</p><p><strong>Exam-length answer:</strong> True: additive sharing has information-theoretic privacy, so its existence does not depend on whether \(\mathrm P=\mathrm{NP}\).</p>''',
            'rubric': ['Answer true.', 'Identify perfect or information-theoretic privacy.', 'Explain that no computational hardness assumption is used.']
        }
    },
    {
        'id': 'hw6-1aii', 'title': 'A two-party sum can reveal the other input',
        'section': 'II · Computing on shares', 'kind': 'homework', 'exercise': 'HW6 1(a.ii)',
        'source': 'HW6, p. 1, Problem 1(a.ii)', 'source_ref': 'hw6',
        'requires': ['local-addition', 'simulation-definition'],
        'body': r'''<p>A protocol may disclose information already determined by a party's permitted input and output. Here both parties receive the sum. Work over \(\mathbb F_p\), so subtraction is performed modulo the prime \(p\).</p><p>Alice knows \(x_A\) and receives \(y=x_A+x_B\). Ask what she can calculate from those two values before deciding whether seeing \(x_B\) would violate privacy.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 1(a.ii).</strong> True or false? In a world where \(\mathrm P=\mathrm{NP}\), two parties can securely compute \(f(x_A,x_B)=x_A+x_B\) with semi-honest security. Give a protocol and explain briefly how its received messages can be simulated.</p>''',
            'hint': r'''<p>How much does \(y-x_A\) tell Alice? Consider the simplest possible exchange.</p>''',
            'solution': r'''<p><strong>True.</strong> The additive-sharing protocol works without public-key cryptography because addition uses only local additions of shares. There is also a particularly short protocol for this two-party functionality: Alice sends \(x_A\) to Bob, Bob sends \(x_B\) to Alice, and both add them.</p><p>This exchange is private <em>relative to the stated output</em>. Given Alice's permitted information \((x_A,y)\), the simulator computes \(x_B=y-x_A\) and supplies exactly the message Alice would receive. For Bob, it computes \(x_A=y-x_B\). Neither simulated transcript requires any information beyond that party's input and output.</p><p>This example does not say that raw inputs are usually safe to exchange. For three parties receiving only a total, one input and the total do not normally determine the other two inputs separately.</p><p><strong>Exam-length answer:</strong> True: two-party addition needs no computational assumption, and each other input is already determined by the recipient's own input and the sum.</p>''',
            'rubric': ['Answer true and supply a correct protocol.', r'For a corrupted Alice, simulate Bob’s message using \(y-x_A\).', 'Explain that the disclosure is already implied by the specified output.']
        }
    },
    {
        'id': 'hw6-3a', 'title': 'Use an ordinary triple to square a secret',
        'section': 'III · Multiplication and preprocessing', 'kind': 'homework', 'exercise': 'HW6 3(a)',
        'source': 'HW6, p. 3, Problem 3(a)', 'source_ref': 'hw6',
        'requires': ['beaver-combine', 'mask-privacy', 'mpc-cost'],
        'body': r'''<p>All arithmetic is in \(\mathbb F_p\). The parties hold additive shares \([x]=(x_1,\ldots,x_n)\). A trusted dealer gives them shares of independent uniform masks \(a,b\) and their product \(c=ab\). Each triple is used once.</p><p>The notation \([k]\) for a public constant means a valid sharing, for example \((k,0,\ldots,0)\); it does not mean that everyone adds \(k\) to their share.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 3(a).</strong> Show how the parties can compute shares of \(x^2\) using a dealer who supplies ordinary Beaver multiplication triples. Specify what is opened and what each party computes.</p>''',
            'hint': r'''<p>Apply the multiplication protocol with both secret inputs equal to \(x\), while keeping the two masks independent.</p>''',
            'solution': r'''<p>Let the dealer supply \([a],[b],[c]\), with \(c=ab\). Party \(P_i\) sends the two masked shares \(\delta_i=x_i-a_i\) and \(\varepsilon_i=x_i-b_i\). Everyone sums these messages to obtain the public values</p><div class="math">\[\delta=x-a,\qquad \varepsilon=x-b.\]</div><p>The masks \(a,b\) are independent and uniform, so this pair of opened values is uniform for every fixed \(x\). Opening it does not reveal \(x\).</p><p>Since \(x=\delta+a=\varepsilon+b\), multiplication gives</p><div class="math">\[x^2=\delta\varepsilon+\varepsilon a+\delta b+c.\]</div><p>Each party sets \(z_i=\varepsilon a_i+\delta b_i+c_i\); one designated party also adds \(\delta\varepsilon\). Summing the \(z_i\) gives the displayed identity, so \((z_1,\ldots,z_n)\) is a sharing of \(x^2\).</p><p>There are two opened field values. Through a broadcast primitive this means two field elements from each party. Both can be sent in the same communication round.</p>''',
            'rubric': [r'Open both \(x-a\) and \(x-b\) using independent masks.', r'Derive \([x^2]=[c]+\varepsilon[a]+\delta[b]+[\delta\varepsilon]\).', 'Add the public term only once and explain why opening is private.']
        }
    },
    {
        'id': 'hw6-3b', 'title': 'A correlated square saves one opening',
        'section': 'III · Multiplication and preprocessing', 'kind': 'homework', 'exercise': 'HW6 3(b)',
        'source': 'HW6, pp. 3–4, Problem 3(b)', 'source_ref': 'hw6',
        'requires': ['hw6-3a'],
        'body': r'''<p>The dealer now gives shares of \(a\) and \(a^2\), where \(a\) is uniformly random in \(\mathbb F_p\). The square is correlated with the mask on purpose. The dealer shares these values privately; parties do not receive \(a\) or \(a^2\) in the clear.</p><p>As in an ordinary Beaver multiplication, one fresh preprocessing item may be consumed for this computation. The task is to use its special structure to reduce online communication.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 3(b).</strong> Given \([x],[a],[a^2]\), show how to securely compute \([x^2]\). Compare the communication between parties with the ordinary-triple method, excluding the dealer's communication.</p>''',
            'hint': r'''<p>Open \(\delta=x-a\), then expand \(x^2=(\delta+a)^2\). Which remaining multiplications have a public factor?</p>''',
            'solution': r'''<p>Party \(P_i\) sends \(\delta_i=x_i-a_i\). Their sum opens \(\delta=x-a\). Since \(a\) is uniform and fresh, \(\delta\) is uniform for each fixed secret \(x\).</p><p>Expand the square without discarding either cross term:</p><div class="math">\[x^2=(\delta+a)^2=\delta^2+2\delta a+a^2.\]</div><p>Both \(\delta\) and \(\delta^2\) are now public. If \(q_i\) denotes party \(i\)'s share of \(a^2\), it computes \(z_i=2\delta a_i+q_i\). One designated party adds the public constant \(\delta^2\). These shares sum to \(x^2\).</p><p>The sheet's equivalent formula is</p><div class="math">\[[x^2]=\delta([x]+[a])+[a^2],\]</div><p>because \(\delta(x+a)=(x-a)(x+a)=x^2-a^2\). Both methods use only local multiplication by public values after the single opening.</p>{{lab:square}}<p>Each party now broadcasts one field element instead of two: the opened-value payload is halved. If broadcasts are implemented by sending separately to the other \(n-1\) parties, the count falls from \(2n(n-1)\) to \(n(n-1)\) field elements. Both versions can use one opening round, so this is not a claim that the number of rounds halves.</p>''',
            'rubric': [r'Open only \(\delta=x-a\) with a fresh uniform mask.', r'Use \([a^2]+2\delta[a]+[\delta^2]\), or the equivalent sheet formula.', 'Distinguish halved field-element payload from unchanged opening-round count.']
        }
    },
    {
        'id': 'hw6-3c', 'title': 'Evaluate a polynomial after one opening',
        'section': 'III · Multiplication and preprocessing', 'kind': 'homework', 'exercise': 'HW6 3(c)',
        'source': 'HW6, p. 4, Problem 3(c)', 'source_ref': 'hw6',
        'requires': ['hw6-3b', 'public-constants'],
        'body': r'''<p>The public polynomial is \(f(X)=\beta_0+\beta_1X+\cdots+\beta_dX^d\), with coefficients \(\beta_k\in\mathbb F_p\). Uppercase \(X\) is a placeholder; lowercase \(x\) is the secret input. The parties want shares of \(f(x)\), not a public reconstruction of every power of \(x\).</p><p>The binomial rule says \((u+v)^k=\sum_{j=0}^{k}\binom{k}{j}u^jv^{k-j}\). The number \(\binom{k}{j}\) counts which \(j\) of the \(k\) factors contribute \(u\); for example, \((u+v)^3=u^3+3u^2v+3uv^2+v^3\). These integer coefficients are reduced modulo \(p\) when used in the field.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 3(c).</strong> Show how to compute \([f(x)]\) when a trusted dealer sends each party only \(d\) field values. Specify the dealer's values, the single masked value to open, and the local formula.</p>''',
            'hint': r'''<p>Let the dealer supply shares of \(a,a^2,\ldots,a^d\) for one random \(a\). Expand powers of \(x=(x-a)+a\).</p>''',
            'solution': r'''<p>The dealer samples one uniform \(a\in\mathbb F_p\) and additively shares each of \(a,a^2,\ldots,a^d\). Each party receives one share of each power, hence exactly \(d\) field values. The power sharings are independently randomized subject to their required sums.</p><p>For \(d\geq1\), the parties open \(\delta=x-a\) once. For each \(k=1,\ldots,d\), the binomial rule gives</p><div class="math">\[[x^k]=\sum_{j=0}^{k}\binom{k}{j}\delta^j[a^{k-j}].\]</div><p>Here every coefficient \(\binom{k}{j}\delta^j\) is public. Every positive power sharing needed on the right came from the dealer. The term with \(j=k\) uses \(a^0=1\), so take \([1]=(1,0,\ldots,0)\); do not add that constant at every party.</p><p>Then compute the desired sharing using public coefficients:</p><div class="math">\[[f(x)]=\sum_{k=0}^{d}\beta_k[x^k],\qquad [x^0]=[1].\]</div><p>For a concrete cubic, \(x^3=\delta^3+3\delta^2a+3\delta a^2+a^3\). Once \(\delta\) is public, this expression contains no multiplication of two still-secret values.</p>{{lab:polynomial}}<p>The only online opening is protected by the fresh uniform mask \(a\). All later operations are local and reveal no additional transcript. This is one shared input evaluated with one set of correlated powers; reusing the same mask for an unrelated second input would reveal their difference. If \(d=0\), the answer is the public constant \(\beta_0\), so no dealer values or opening are needed.</p>''',
            'rubric': [r'Dealer supplies one share of each power \(a^1,\ldots,a^d\).', r'Open \(\delta=x-a\) once and give the binomial expansion with public coefficients.', r'Handle \([1]\) and \(\beta_0\) as public constants added only once.', 'Explain fresh-mask privacy and distinguish local work from communication.']
        }
    },
    {
        'id': 'malicious-guarantees', 'title': 'What changes when a party cheats?',
        'section': 'IV · Malicious parties and authentication', 'kind': 'lesson',
        'source': 'Lecture 17–19, pp. 8–9; HW6, pp. 1–2', 'source_ref': 'lecture',
        'requires': ['mpc-cost'],
        'body': r'''<p>Semi-honest parties follow each message rule. A malicious party may replace a share, send an invalid message, or stop. The ideal-world comparison now needs to say which failures a real protocol may have and what an honest party is allowed to accept.</p><table><caption>The lecture distinguishes four guarantees.</caption><thead><tr><th scope="col">Guarantee</th><th scope="col">What it requires</th></tr></thead><tbody><tr><th scope="row">Privacy</th><td>The adversary learns only its own inputs and what its prescribed outputs imply.</td></tr><tr><th scope="row">Correctness</th><td>An accepted honest output equals the function on the parties' effective inputs.</td></tr><tr><th scope="row">Input independence</th><td>A corrupted party cannot choose its effective input using secret information about honest inputs.</td></tr><tr><th scope="row">Fairness</th><td>If the adversary obtains the output, the honest parties obtain it too.</td></tr></tbody></table><p>“Effective input” matters: cryptography cannot force a hospital to report a truthful database. It can require a party to use a single chosen input consistently. Privacy also cannot remove information already present in the prescribed output.</p><p>The lecture permits malicious security with abort even when as many as \(n-1\) parties are corrupted, under suitable cryptographic assumptions. An honest party may reject a detected deviation instead of accepting a wrong answer. General fairness is a stronger requirement: for arbitrary functionalities the lecture requires an honest majority. Some particular functions admit easier solutions, so this is not a claim that every two-party function makes fairness impossible.</p><p>One simple attack exposes the missing check in the semi-honest protocol. When output shares are added, a forged share changes the total. Authenticating the <em>sender</em> of a message does not prove that the <em>share value</em> is correct.</p>{{lab:rushing}}''',
        'check': {
            'type': 'choice',
            'prompt': r'''<p><strong>Practice.</strong> A corrupted party learns the correct output, then refuses to release its final share. Honest parties detect the missing message and abort without accepting a wrong value. Which guarantee does this execution directly violate?</p>''',
            'choices': ['Correctness of an accepted output', 'Fairness', 'Privacy, necessarily'], 'answer': 1,
            'feedback': [r'<p>No wrong honest output was accepted. Correctness with abort permits rejection; the missing guarantee concerns who obtains the result.</p>',r'<p>Correct. The adversary obtained the output while honest parties did not. That is precisely the fairness condition.</p>',r'<p>This does not by itself show extra information leakage. It directly shows unequal delivery of the permitted output.</p>'],
            'hint': r'<p>Compare the output received by the adversary with the output received by the honest parties.</p>',
            'solution': r'<p>Fairness fails because the adversary has the output while honest parties do not. Correctness with abort may still hold: honest parties accepted no incorrect result.</p>'
        }
    },
    {
        'id': 'hw6-2a', 'title': 'Force a chosen reconstructed output',
        'section': 'IV · Malicious parties and authentication', 'kind': 'homework', 'exercise': 'HW6 2(a)',
        'source': 'HW6, pp. 1–2, Problem 2(a)', 'source_ref': 'hw6',
        'requires': ['malicious-guarantees'],
        'body': r'''<p>HW6 Problem 2 assumes authenticated broadcast: all recipients receive the same message and know its sender. Parties do not abort by omitting messages, and Beaver triples are already available. These assumptions do not require a sender to announce its output share before seeing anyone else's.</p><p>Let \(s_i\) be party \(P_i\)'s final output share. Honest reconstruction adds all announced shares in \(\mathbb F_p\). The honest circuit output is a bit, but the shares themselves are field elements.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 2(a).</strong> A circuit \(C:\{0,1\}^n\to\{0,1\}\) is evaluated by the lecture's semi-honest MPC protocol. Show how one malicious party can make all honest parties reconstruct any chosen bit \(\widehat b\).</p>''',
            'hint': r'''<p>If the honest shares have already summed to \(S\), which field element makes the total equal to \(\widehat b\)?</p>''',
            'solution': r'''<p>Suppose \(P_m\) is malicious. It waits until all other parties broadcast their output shares, then calculates \(S=\sum_{i\ne m}s_i\). Instead of its genuine share, it broadcasts</p><div class="math">\[\widehat s_m=\widehat b-S.\]</div><p>Every honest party sees the same authenticated broadcasts and reconstructs \(S+\widehat s_m=\widehat b\). The attack sends a message, so it does not violate the no-omission assumption. It also needs no knowledge of the private inputs.</p><p>For example, in \(\mathbb F_{17}\), if the honest shares sum to \(12\) and the attacker wants \(\widehat b=1\), it sends \(1-12\equiv6\pmod{17}\). The reconstructed value is \(12+6\equiv1\).</p><p>This is a <em>rushing</em> attack: the attacker chooses its own message after reading the others in the same intended stage. Broadcast identifies who sent the forged share but supplies no proof that its value is valid.</p>''',
            'rubric': ['Wait for all honest output shares and sum them.', r'Send \(\widehat s_m=\widehat b-\sum_{i\ne m}s_i\).', 'Show that reconstruction equals the chosen bit and that broadcast does not prevent the attack.']
        }
    },
    {
        'id': 'commitments-channel', 'title': 'Fix a message before learning others',
        'section': 'IV · Malicious parties and authentication', 'kind': 'lesson',
        'source': 'HW6, p. 2, Problem 2(b); lecture commitment prerequisite', 'source_ref': 'hw6',
        'requires': ['hw6-2a'],
        'body': r'''<p>A commitment has two stages. To commit to a message \(m\), a party chooses fresh secret randomness \(r\) and publishes \(c=\operatorname{Com}(m;r)\). Later it opens by revealing \((m,r)\); everyone checks that the same commitment is obtained. The message and the randomizer remain private until opening.</p><p><strong>Hiding</strong> means that the commitment does not reveal the message. <strong>Binding</strong> means that the sender cannot find valid openings of one commitment to two different messages. The two guarantees have different jobs: hiding conceals the value while the other senders act, and binding prevents a sender from changing its chosen value afterward.</p><p>The homework's fair communication channel provides \(\operatorname{Push}(m_i)\) and \(\operatorname{Pull}\). Here \(m_i\) is party \(i\)'s message. Push fixes it without revealing it. Pull releases a message only after every party has pushed. The value \(\bot\) means that nothing is released yet.</p><p>The intended commit-then-open construction uses a commitment in the first stage and an opening in the second. Everyone waits for all first-stage commitments before opening. This blocks the earlier attack of reading clear output shares and then choosing a different committed share.</p>{{lab:fair-channel}}<p>A message can be fixed and still be wrong. Moreover, a party may refuse to open or send an invalid opening. Commitments therefore do not by themselves guarantee correct computation or eventual delivery. The homework's no-omission assumption removes one source of interruption, while failed verification still leads to abort.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'''<p><strong>Practice.</strong> A commitment hides its message perfectly, but its sender can open it to any message after seeing the other openings. Which missing property permits the rushing attack again?</p>''',
            'choices': ['Binding', 'Hiding', 'Reliable broadcast'], 'answer': 0,
            'feedback': [r'<p>Correct. Without binding, the first-stage commitment does not fix the attacker’s eventual message.</p>',r'<p>Hiding is already assumed. It protects the message before opening, but does not stop its sender changing it.</p>',r'<p>All recipients can reliably receive the same forged opening. Agreement about the received message does not make it binding.</p>'],
            'hint': r'<p>Which property restricts the sender rather than protecting against the observer?</p>',
            'solution': r'<p>Binding is missing. Hiding prevents premature reading; binding prevents a sender from replacing its committed message after reading other messages.</p>'
        }
    },
    {
        'id': 'hw6-2b', 'title': 'Implement Push and Pull',
        'section': 'IV · Malicious parties and authentication', 'kind': 'homework', 'exercise': 'HW6 2(b)',
        'source': 'HW6, p. 2, Problem 2(b)', 'source_ref': 'hw6',
        'requires': ['commitments-channel'],
        'body': r'''<p>Use authenticated broadcast. The homework's channel fixes one message from every party before revealing any of them. In its notation, \(\operatorname{Push}(m_i)\) stores party \(i\)'s message, and \(\operatorname{Pull}\) releases it only when every party has pushed. Until then it returns \(\bot\), meaning no message.</p><p>Recall that a commitment conceals its message until opening, while its binding property prevents two different valid openings. State explicitly when verification takes place and what happens if it fails.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 2(b).</strong> Implement the Push/Pull interface using tools from class and argue why parties cannot wait to see the clear messages before choosing their own.</p>''',
            'hint': r'''<p>Push should broadcast something hiding and binding. Pull should wait for every Push before accepting openings.</p>''',
            'solution': r'''<ol><li><p><strong>Push.</strong> Party \(P_i\) samples fresh \(r_i\), computes \(c_i=\operatorname{Com}(m_i;r_i)\), and broadcasts \(c_i\) with its authenticated identity and session label. It retains \(m_i,r_i\).</p></li><li><p><strong>Wait.</strong> No party reveals an opening until a valid first-stage commitment has been received from every party. Earlier Pull attempts release nothing.</p></li><li><p><strong>Pull.</strong> The sender broadcasts \((m_i,r_i)\). Recipients check that it opens the previously stored \(c_i\) for the same sender and session. They accept \(m_i\) only if this check passes; an invalid opening causes abort.</p></li></ol><p>Hiding prevents learning honest messages from their commitments. Binding prevents a sender from replacing its fixed committed message after honest openings become visible. Authenticated broadcast gives all honest parties the same commitments and openings, so they apply the same verification rule.</p><p><strong>Scope of this construction.</strong> This is the sheet's intended argument against choosing a new message <em>after seeing cleartext</em>. Ordinary hiding and binding alone do not prove the stronger claim that every committed message is independent of other hidden messages: for example, an unprotected commitment could be copied and later opened by copying the original opening. An implementation of that stronger ideal interface must also prevent such copying or related-message attacks, using suitably non-malleable, sender/session-bound commitments or an ideal commitment functionality. “Non-malleable” here means that seeing a commitment does not enable creating a commitment to a related unknown message.</p><p>Finally, commit-then-open does not force a malicious sender to provide a valid opening. The protocol may abort; it does not establish general MPC output fairness.</p>''',
            'rubric': ['Broadcast a hiding, binding commitment during Push.', 'Open only after all commitments are fixed, and verify sender/session and opening.', 'Use hiding and binding for their distinct purposes.', 'State abort behavior and do not claim that commitments alone guarantee correct output or delivery.']
        }
    },
    {
        'id': 'hw6-2c', 'title': 'Cheat even when all shares are fixed',
        'section': 'IV · Malicious parties and authentication', 'kind': 'homework', 'exercise': 'HW6 2(c)',
        'source': 'HW6, p. 2, Problem 2(c)', 'source_ref': 'hw6',
        'requires': ['hw6-2b'],
        'body': r'''<p>Now assume the fair channel works exactly as specified: every sender's message is fixed before the others are revealed. This removes the ability to select a target output after inspecting the honest output shares.</p><p>It does not check that a party's fixed message equals its genuine share. Let the genuine final shares be \(s_1,\ldots,s_n\), with correct output \(b=\sum_i s_i\).</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 2(c).</strong> Show that a malicious party can still make every honest party reconstruct an incorrect output even when all communication uses the fair channel. Your attack must choose its message before seeing other output shares.</p>''',
            'hint': r'''<p>Add a fixed nonzero offset \(\Delta\) to your genuine output share. What happens to their total?</p>''',
            'solution': r'''<p>A malicious party \(P_m\) chooses any fixed nonzero \(\Delta\in\mathbb F_p\) and pushes \(\widehat s_m=s_m+\Delta\) instead of \(s_m\). It does this before seeing any other output share, so the fair channel's timing rule is satisfied.</p><p>The reconstructed value is</p><div class="math">\[\widehat b=\sum_{i\ne m}s_i+(s_m+\Delta)=b+\Delta\ne b.\]</div><p>The inequality holds because \(\Delta\) is a nonzero field element. The attacker does not have to know \(b\) in advance.</p><p>For a Boolean circuit represented over \(\mathbb F_2\), choose \(\Delta=1\). Then adding one flips the bit: \(0+1=1\) and \(1+1=0\). Thus the reconstructed output is a different bit. Over a larger field, the same attack guarantees a wrong field result, which may also fail a required bit-validity check.</p><p>The difference from part (a) is the goal: rushing lets the attacker force a chosen target; a fixed nonzero offset already suffices to violate correctness.</p>''',
            'rubric': ['Choose a fixed nonzero offset before other output shares are revealed.', r'Show reconstruction changes from \(b\) to \(b+\Delta\).', r'For a wrong bit specifically, explain the \(\mathbb F_2\) bit flip.']
        }
    },
    {
        'id': 'authenticated-shares', 'title': 'Attach a secret check to each shared value',
        'section': 'IV · Malicious parties and authentication', 'kind': 'lesson',
        'source': 'Lecture 17–19, p. 9; HW6, pp. 2–3, Problem 2(d–e)', 'source_ref': 'hw6',
        'requires': ['hw6-2c', 'beaver-combine'],
        'body': r'''<p>To detect a forged share, the homework associates every secret value \(x\) with a tag \(t=ax\). Here \(a\) is one global secret authentication key in \(\mathbb F_p\). It is unrelated to the fresh per-gate Beaver mask that was also called \(a\) earlier. The global key, the data and the tag are all shared.</p><div class="math">\[a=\sum_i a_i,\qquad x=\sum_i x_i,\qquad t=\sum_i t_i=ax.\]</div><p>Party \(P_i\) holds \(a_i,x_i,t_i\). No party is given the full key \(a\). Crucially, the condition is on the <em>totals</em>: in general \(t_i\ne a_i x_i\), because a product of sums contains cross terms between different parties.</p><p>Suppose an attacker changes the reconstructed value from \(x\) to \(x+\Delta\). The correct tag would have to change from \(ax\) to \(a(x+\Delta)=ax+a\Delta\). If \(\Delta\ne0\), supplying exactly this correction depends on the unknown global key. This is the reason the tag can detect tampering.</p><p>The intended setup uses a uniform key and correctly randomized tag sharings. We assume those authenticated shares were produced correctly; arbitrary pairs of shares do not become authenticated merely by being labelled that way. A full malicious MPC system must also verify preprocessing and preserve the relation when it computes on shares.</p><p>Addition and multiplication require new tags for the new values. Their formulas follow from the desired invariant “tag equals global key times value,” rather than from multiplying each party's local pieces.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'''<p><strong>Practice.</strong> In \(\mathbb F_{17}\), a shared value has total \(x=5\) and global key \(a=7\), so its tag totals \(t=1\). An attacker increases the opened value by \(\Delta=2\). By how much must the total tag change to remain valid?</p>''',
            'choices': [r'\(2\)',r'\(14\)',r'\(10\)'], 'answer': 1,
            'feedback': [r'<p>The value changes by 2, but its tag must change by the key times that offset.</p>',r'<p>Correct. The needed change is \(a\Delta=7\cdot2=14\pmod{17}\). The new tag is \(1+14=15\), equal to \(7\cdot7\pmod{17}\).</p>',r'<p>This is \(x\Delta\). Authentication uses the secret key \(a\), not the original data value \(x\).</p>'],
            'hint': r'<p>Subtract the old correct tag \(ax\) from the new correct tag \(a(x+\Delta)\).</p>',
            'solution': r'<p>The required change is \(a(x+\Delta)-ax=a\Delta=14\pmod{17}\). This numerical illustration exposes the key for teaching; real parties have only their individual key shares.</p>'
        }
    },
    {
        'id': 'hw6-2d', 'title': 'Carry the tag through arithmetic',
        'section': 'IV · Malicious parties and authentication', 'kind': 'homework', 'exercise': 'HW6 2(d)',
        'source': 'HW6, pp. 2–3, Problem 2(d)', 'source_ref': 'hw6',
        'requires': ['authenticated-shares'],
        'body': r'''<p>The parties hold \([x],[y]\), their tags \([t],[u]\), and the global key shares \([a]\). Their totals satisfy \(t=ax\) and \(u=ay\). Brackets denote additive sharings; they do not allow arbitrary componentwise multiplication.</p><p>A tag for a newly computed value \(v\) must total \(av\). Use local additions for sums and the previously learned multiplication subprotocol for products of two shared values.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 2(d).</strong> Show how the parties can compute tag shares for \([x+y]\) and \([xy]\). State which tag computation is local and which requires interaction.</p>''',
            'hint': r'''<p>Expand \(a(x+y)\). For the product, associate \(a(xy)\) as \((ax)y\), and recall which existing tag equals \(ax\).</p>''',
            'solution': r'''<p>For addition, distribute the key:</p><div class="math">\[a(x+y)=ax+ay=t+u.\]</div><p>Party \(P_i\) therefore adds its tag shares, producing \(t_i+u_i\). Their sum is the correct tag for the sum, and no messages are needed.</p><p>For multiplication, use the already authenticated factor \(t=ax\):</p><div class="math">\[a(xy)=(ax)y=ty.\]</div><p>Run a secure multiplication of the shared values \([t]\) and \([y]\), using a fresh Beaver triple. Its output shares form the tag for \([xy]\). Equivalently, multiply \([x]\) by \([u]\), since \(xu=x(ay)=axy\).</p><p>One should not set the new local tag to \(t_i y_i\): summing such terms misses products \(t_i y_j\) with \(i\ne j\). The shared product subprotocol supplies those cross terms without revealing the factors.</p><aside class="note"><p>This derives the tag-update invariant requested in the exercise. Calling a semi-honest multiplication does not automatically make the complete protocol maliciously secure. A full construction must authenticate/check intermediate openings, ensure correct preprocessing and account for invalid inputs. The sheet's rule identifies the required algebra, not a complete SPDZ security proof.</p></aside>''',
            'rubric': [r'Use \([t]+[u]\) as the tag for the sum.', r'Use a fresh secure multiplication for \([t][y]\), or \([x][u]\), as the tag for the product.', 'Explain why componentwise tag multiplication is invalid and identify the interaction cost.']
        }
    },
    {
        'id': 'mac-security', 'title': 'Check a tag without opening the key',
        'section': 'IV · Malicious parties and authentication', 'kind': 'lesson',
        'source': 'HW6, p. 3, Problem 2(e), with explicit sharing and scheduling assumptions', 'source_ref': 'hw6',
        'requires': ['hw6-2d'],
        'body': r'''<p>After a shared value is opened, everyone knows the claimed value \(\widehat x\). The key \(a\) and the tag \(t\) must stay secret. Opening both \(t\) and a nonzero correct value \(x\) would reveal \(a=t/x\), since every nonzero field element has an inverse.</p><p>Instead, check the difference between the expected tag and the stored tag:</p><div class="math">\[z=\widehat x a-t.\]</div><p>The multiplier \(\widehat x\) is public, so parties can form a sharing of \(z\) using only local operations. If \(\widehat x=x\) and the tag is valid, its total is zero. Its individual shares usually are not zero.</p><p>Opening a zero total protects the key only under the correct sharing distribution. Suppose the tag shares were chosen uniformly among all tuples summing to \(ax\), independently of the key-share tuple apart from that total. For a correct opening, the transformation \(z_i=xa_i-t_i\) maps these tag-share tuples one-to-one onto all tuples whose sum is zero. Every such tuple is equally likely for every key. Thus the full check transcript has the same distribution whichever global key is used; the claim is stronger than merely saying “the answer is zero.”</p><p>Scheduling also matters. Each party must fix its check share before seeing the other check shares. Otherwise the last sender can announce the negative of their sum and make the test pass without knowing any key. The fair channel from the homework supplies this fixed-before-reveal ordering.</p>{{lab:mac}}<p>If a nonzero offset \(\Delta\) is introduced and the attacker fixes a guessed correction beforehand, passing requires guessing \(\Delta a\). With a uniform hidden key and one attempt, that happens with probability \(1/p\). A successful lucky guess does not logically prove knowledge of the key.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'''<p><strong>Practice.</strong> In \(\mathbb F_{17}\), the first two parties have already revealed check shares \(10\) and \(1\). If the last sender can rush, what check share makes the total zero? Give its representative from 0 to 16.</p>''',
            'answer': 6,
            'feedback': [r'<p>The attacker chooses \(-10-1=-11\equiv6\pmod{17}\). This forces a zero total without knowing the key, which is why messages must be fixed first.</p>'],
            'hint': r'<p>Choose \(z_3\) so that \(10+1+z_3\) is a multiple of 17.</p>',
            'solution': r'<p>Choose \(z_3=6\), because \(10+1+6=17\equiv0\). This is a scheduling attack; a larger field alone would not stop it.</p>'
        }
    },
    {
        'id': 'hw6-2e', 'title': 'Prove the authentication check works',
        'section': 'IV · Malicious parties and authentication', 'kind': 'homework', 'exercise': 'HW6 2(e)',
        'source': 'HW6, p. 3, Problem 2(e)', 'source_ref': 'hw6',
        'requires': ['mac-security'],
        'body': r'''<p>Party \(P_i\) holds key share \(a_i\), value share \(x_i\) and tag share \(t_i\), with totals \(a,x,t=ax\). Use correctly randomized sharings and a uniform global key. The value shares have just been opened as a public claimed value \(\widehat x\).</p><p>Assume the fair channel from part (b): check messages are fixed before other check messages are revealed. Count one logical field-element message per party through this channel. Implementing that logical channel with commitments requires additional physical commitment/opening messages.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p><strong>HW6 2(e).</strong> Give a one-message-per-party check for the opened value's tag. Prove that an honest check reveals no additional information about the global key. If one party changes its value share by a nonzero \(\Delta\), show what correction is needed to pass and quantify the chance of a blind guess.</p>''',
            'hint': r'''<p>Let each party contribute a share of \(\widehat x a-t\). For privacy, compare the distribution of the whole vector of contributions, not just its sum.</p>''',
            'solution': r'''<p>Each party locally computes its check share</p><div class="math">\[z_i=\widehat x a_i-t_i.\]</div><p>It fixes and sends this single field element through the fair channel. Everyone accepts exactly when the received shares sum to zero. Under honest behavior, \(\widehat x=x\), and therefore</p><div class="math">\[\sum_i z_i=x\sum_i a_i-\sum_i t_i=xa-t=0.\]</div><p><strong>Key privacy.</strong> Fix any key-share tuple \((a_1,\ldots,a_n)\) and the correct public value \(x\). For any proposed check tuple \((z_1,\ldots,z_n)\) with total zero, exactly one tag-share tuple generates it: set \(t_i=xa_i-z_i\). Those tag shares total \(ax\), as required.</p><p>There are \(p^{n-1}\) tag-share tuples with that total, all equally likely under the stated sharing assumption. Hence every zero-sum check tuple has probability \(p^{-(n-1)}\), independent of the global key. A party's own check share is already determined by its existing \(a_i,t_i\); conditioned on that information, the other check shares are uniform subject to their required sum. Thus receiving them adds no key information.</p><p><strong>Tampering.</strong> If one data share changes by \(\Delta\ne0\), then \(\widehat x=x+\Delta\). Honest-form check shares now total</p><div class="math">\[\sum_i z_i=(x+\Delta)a-t=\Delta a.\]</div><p>If the attacker subtracts a correction \(\gamma\) from its announced check share, the test passes exactly when \(\gamma=\Delta a\). Since nonzero \(\Delta\) has a multiplicative inverse, knowing the required correction would determine \(a=\gamma/\Delta\). Without that information, and with messages fixed before honest checks are visible, a blind guess succeeds with probability \(1/p\) for a uniform hidden key.</p><p>The source's phrase “must know the key” should be read as requiring the correct key-dependent correction, not excluding a lucky guess. This check is one part of malicious MPC: the authentication invariant and the fair scheduling assumption are essential.</p>''',
            'rubric': [r'Send \(z_i=\widehat x a_i-t_i\) and accept exactly when the total is zero.', 'Prove privacy from uniform zero-sum check tuples, not from the total alone.', r'Derive the required correction \(\gamma=\Delta a\) for a nonzero offset.', r'State the fixed-before-reveal condition and the \(1/p\) blind-guess probability.']
        }
    }
]

SOURCE_ISSUES = [
    'HS2025 Endterm contains differential privacy only. It informs short subquestion scope, counterexample and derivation practice, but supplies no actual MPC exam questions.',
    'HW6 1(b): the supplied FALSE answer assumes a reliable additional disclosure/equality certification. Merely outputting one\'s own input, which happens to equal the other when equal, would not establish disclosure; equality may also be an allowed functionality output.',
    'HW6 2(b): commit-then-open with hiding/binding supplies the intended fixed-before-cleartext-opening argument and may abort. Generic hiding/binding alone does not establish non-malleability or fully independent committed inputs; copied commitments/openings illustrate the gap. Full ideal-channel realization needs suitable commitment functionality. This is separate from MPC output fairness.',
    'HW6 2(c): a fixed nonzero offset forces a wrong field result. For a wrong output bit specifically, use the Boolean circuit over F2 and offset one.',
    'HW6 2(d): computing a product tag via Beaver multiplication establishes its algebraic invariant; it is not a complete malicious-security proof. Preprocessing and intermediate openings must also be protected.',
    'HW6 2(e): individual opened check shares need not be zero; only their sum is zero. Key privacy requires correct randomized authenticated-share distributions, with an explicit zero-sum transcript argument.',
    'HW6 2(e): check messages must be fixed before others are revealed; otherwise a rushing sender cancels their sum without knowing the key. One logical field element over the fair channel is not one physical message when commit/open implements the channel.',
    'HW6 2(e): for a nonzero offset and uniform hidden key, the needed correction is Delta times the key; an attacker may guess successfully with probability 1/p, so success does not literally imply key knowledge.',
    'HW6 3(b): the two displayed square identities are equivalent. The online field-element payload halves from two openings to one, while both versions can use one opening round.',
    'HW6 3(c): powers a^0 and x^0 are public one and must be shared consistently, e.g. (1,0,...,0). The constant-polynomial case d=0 needs no preprocessing or opening. Never reuse the same mask for another private input.'
]
