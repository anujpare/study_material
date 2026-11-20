"""Source-authored lessons for the secure MPC interactive learning lab."""

CARDS = [
    {
        'id': 'mpc-goal',
        'title': 'Compute the agreed output without revealing extra information',
        'section': 'I · What MPC protects',
        'kind': 'lesson',
        'source': 'Lecture 17–19, pp. 1–3 and 9.',
        'source_ref': 'lecture',
        'requires': [],
        'body': r'''<p>Alice, Bob and Charlie each hold a private input. They agree on a function: a rule for combining those inputs into an output. A trusted third party could collect the inputs, evaluate the rule and return the result. <strong>Secure multi-party computation (MPC)</strong> aims to provide that service through a protocol among the parties.</p>
<p>Write \(P_1,\ldots,P_n\) for the \(n\) parties, \(x_i\) for party \(P_i\)'s input, and \(f\) for the publicly agreed function. In the lecture's main setting, everyone receives the same output:</p>
<div class="math">\[y=f(x_1,\ldots,x_n).\]</div>
<p>The security goal is to reveal no information beyond what a party can already infer from its own input and the output. It does <em>not</em> promise that the output reveals nothing. If Alice and Bob compute their sum, Alice can subtract her input from that sum and recover Bob's input. Even a trusted third party cannot prevent this inference while returning the exact sum.</p>
{{lab:ideal-world}}
<p>Our running circuit will compute \(f(x_A,x_B,x_C)=(x_A+x_B)x_C\). The subscripts identify the input owners. The protocol must evaluate its addition and multiplication without first publishing the intermediate sum. Later we will see exactly how each party holds only a share of each wire value.</p>
<p>Private machine learning, auctions and voting are examples of agreed computations. The allowed output must still be chosen carefully: cryptography protects the execution of that computation, including all intermediate data; it does not automatically make the chosen output harmless.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> Two parties securely compute their ordinary integer sum. Alice enters \(8\) and receives \(21\). What value can Alice infer for Bob’s input?</p>',
            'answer': 13,
            'hint': r'<p>The permitted output itself gives an equation containing just one unknown.</p>',
            'solution': r'<p>Alice solves \(8+x_B=21\), obtaining \(x_B=13\). This inference is permitted by the function: the trusted-party computation would reveal the same information. It is not, by itself, evidence that the MPC protocol leaked anything extra.</p>',
        },
    },
    {
        'id': 'mpc-models',
        'title': 'Decide what a corrupted party is allowed to do',
        'section': 'I · What MPC protects',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §1.1, p. 3.',
        'source_ref': 'lecture',
        'requires': ['mpc-goal'],
        'body': r'''<p>An adversary may control several parties, who then combine everything they know. This is <strong>collusion</strong>. A security claim must specify both how many parties can collude and whether they must send the messages prescribed by the protocol.</p>
<p>A <strong>semi-honest</strong> adversary follows the protocol, including its rules for choosing randomness and sending messages. It may nevertheless keep the complete record and perform additional calculations to infer secrets. “Follows the protocol” does not mean “forgets what it saw”.</p>
<p>A <strong>malicious</strong> adversary may depart from those rules: it can send a false share, choose malformed randomness, send different messages to different recipients, or stop sending messages. We first construct a semi-honest protocol. Later, HW6 will show why hiding shares alone does not stop a malicious party from changing the result.</p>
<table><caption>Two different questions about the same computation</caption><thead><tr><th scope="col">Model</th><th scope="col">What must the analysis handle?</th></tr></thead><tbody><tr><th scope="row">Semi-honest</th><td>The prescribed execution, plus every inference from the colluding parties’ combined information.</td></tr><tr><th scope="row">Malicious</th><td>Arbitrary deviations, including fabricated messages and attacks on correctness.</td></tr></tbody></table>
<p>The lecture often restricts attackers to <strong>probabilistic polynomial time (PPT)</strong>: randomized algorithms whose running time is bounded by a polynomial in the problem’s security parameter. A security parameter is a size setting used to make attacks increasingly difficult. Our additive-sharing privacy proof will be stronger: it will hold even for unlimited computation.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> Bob sends every prescribed message. Afterwards, he combines his random choices with Charlie’s received messages and runs a new calculation. Which model already requires protection against this attack?</p>',
            'choices': ['Semi-honest security against a coalition containing Bob and Charlie.', 'Only malicious security, because the extra calculation was not prescribed.', 'Neither model, because the protocol has already ended.'],
            'answer': 0,
            'feedback': [r'<p>Correct. Semi-honest parties may collude and perform additional local calculations. Their messages remain prescribed, so this attack is already inside the semi-honest model.</p>', r'<p>Extra local inference is allowed in the semi-honest model. A malicious deviation would change a required action, such as the message Bob sends.</p>', r'<p>Keeping and analysing the transcript after the execution is allowed. Privacy must protect against those later inferences too.</p>'],
            'hint': r'<p>Separate changing a transmitted message from analysing information already received.</p>',
            'solution': r'<p>This is a semi-honest attack by the coalition containing Bob and Charlie. The protocol must protect against their <em>joint</em> information, even when each individual view would appear harmless.</p>',
        },
    },
    {
        'id': 'simulation-definition',
        'title': 'Read the exact simulation requirement',
        'section': 'I · What MPC protects',
        'kind': 'lesson',
        'source': 'Lecture 17–19, Definition 1 and real/ideal diagram, p. 3.',
        'source_ref': 'lecture',
        'requires': ['mpc-models'],
        'body': r'''<p>A party’s <strong>view</strong> is everything available to it during an execution: its input, random choices, received messages, and resulting local computations and output. Denote party \(P_i\)'s view by \(\mathrm{View}_i\). A coalition gets all its members’ views together.</p>
<p>Let \(C\subseteq[n]\) be the indices of the corrupted parties, where \([n]=\{1,\ldots,n\}\). The lecture defines semi-honest security through an efficient randomized algorithm \(\mathrm{Sim}\), called a simulator. There must exist one such algorithm that works for <strong>every input assignment and every coalition \(C\subseteq[n]\)</strong>:</p>
<div class="math">\[\mathrm{Sim}\!\left(C,\{x_i:i\in C\},y\right)\approx\{\mathrm{View}_i:i\in C\},\qquad y=f(x_1,\ldots,x_n).\]</div>
<p>The simulator receives the coalition’s identities, its inputs and the agreed output. The function and protocol are public. It receives <strong>no honest party’s input</strong>. The left side is its invented record; the right side is the coalition’s record from a real execution. Both are random because the algorithms use randomness.</p>
<p>The symbol \(\approx\) means that these two distributions cannot be distinguished under the stated security notion. Perfect simulation means exactly equal probabilities for every possible record. Statistical simulation permits a negligible difference even for an unlimited observer; computational simulation only promises indistinguishability to efficient observers. A negligible difference becomes smaller than every inverse polynomial as the security parameter grows.</p>
<p>Why does this capture privacy? An invented record made from the permitted information alone cannot require an additional honest input. A real record indistinguishable from it cannot reveal a reliably detectable extra fact. The construction below protects against up to \(n-1\) corrupted parties. If everyone is corrupted, the simulator already knows every input. Correct evaluation of \(f\) is also required; privacy alone would not make a protocol returning the wrong answer useful.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> Four parties compute a common output \(y\). Parties \(P_2\) and \(P_4\) collude. Which input list is allowed for the simulator?</p>',
            'choices': [r'\(C=\{2,4\},x_2,x_4,y\).', r'\(C=\{2,4\},x_1,x_2,x_3,x_4\).', r'Only \(y\), because every input must stay secret.'],
            'answer': 0,
            'feedback': [r'<p>Correct. The coalition already knows its own inputs and is entitled to the common output. These are exactly the simulator’s private-data inputs.</p>', r'<p>This gives the simulator honest parties’ inputs, making the privacy test too weak. A simulator with every input could reproduce a protocol that reveals them all.</p>', r'<p>Corrupted parties know their own inputs. The simulator must reproduce a view consistent with those known values, so it is allowed to receive them.</p>'],
            'hint': r'<p>List what the coalition receives in the trusted-party execution.</p>',
            'solution': r'<p>The permitted data are \(C=\{2,4\}\), the inputs \(x_2,x_4\), and \(y\). The same simulator must work for all choices of the unknown honest inputs \(x_1,x_3\) that produce that output.</p>',
        },
    },
    {
        'id': 'simulation-test',
        'title': 'Break privacy with two indistinguishable ideal inputs',
        'section': 'I · What MPC protects',
        'kind': 'lesson',
        'source': 'Lecture 17–19, Definition 1, p. 3, and circuit example, p. 5; distinguishing example added for practice.',
        'source_ref': 'lecture',
        'requires': ['simulation-definition'],
        'body': r'''<p>The simulation definition gives a practical way to find a privacy failure. Choose two possible collections of honest inputs that give a fixed coalition the <strong>same own inputs and the same output</strong>. The simulator then receives exactly the same data in both cases. If a real message always distinguishes the cases, no simulator can reproduce both real views.</p>
<p>Consider the lecture’s function \(y=(x_A+x_B)x_C\). Suppose a proposed protocol first publishes the intermediate value \(u=x_A+x_B\), then publishes \(y\). Charlie is corrupted and enters \(x_C=0\). Consequently \(y=0\), whatever Alice and Bob entered.</p>
<table><caption>Charlie’s permitted information stays fixed</caption><thead><tr><th scope="col">Honest inputs</th><th scope="col">Output \(y\)</th><th scope="col">Extra message \(u\)</th></tr></thead><tbody><tr><td>\(x_A=4,x_B=5\)</td><td>\(0\)</td><td>\(9\)</td></tr><tr><td>\(x_A=1,x_B=2\)</td><td>\(0\)</td><td>\(3\)</td></tr></tbody></table>
<p>Charlie distinguishes the two cases simply by testing whether the message is \(9\). Yet the simulator is given the same coalition, input \(0\) and output \(0\) in both cases. Its distribution cannot be certain to output \(9\) in one case and certain to output \(3\) in the other.</p>
<p>This argument identifies the extra information precisely: the intermediate sum. It also explains why MPC keeps intermediate circuit wires secret-shared. Merely hiding the original inputs when they first arrive does not establish privacy for the later computation.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p><strong>Practice.</strong> Alice and Bob want only the bit \(y\) saying whether their integers are equal. A proposed protocol sends Bob’s input directly to Alice. Give two Bob inputs showing that privacy fails when Alice’s input is \(5\).</p>',
            'hint': r'<p>Choose two distinct values, both different from \(5\), so the permitted output stays the same.</p>',
            'solution': r'<p>Take Bob’s input to be \(2\) in one case and \(7\) in the other. Alice’s own input is \(5\) and the equality output is \(0\) in both cases. A simulator therefore receives identical permitted information. But the real message is deterministically \(2\) or \(7\), so Alice can distinguish the cases. The protocol reveals extra information beyond the equality bit.</p>',
            'rubric': [r'Choose two different Bob inputs, neither equal to \(5\).', 'State that Alice’s input and the equality output are identical in both cases.', 'Explain that the transmitted value distinguishes the cases, although the simulator’s inputs do not.'],
        },
    },
    {
        'id': 'additive-sharing',
        'title': 'Split a value into shares that add back to it',
        'section': 'II · Computing on shares',
        'kind': 'lesson',
        'source': 'Lecture 17–19, Definition 2, p. 4.',
        'source_ref': 'lecture',
        'requires': ['simulation-test'],
        'body': r'''<p>The computation will use the finite field \(\mathbb F_p\), where \(p\) is prime. Its values are \(0,\ldots,p-1\), with addition and multiplication reduced modulo \(p\). For example, in \(\mathbb F_{17}\), \(14+8=5\) because \(22\) leaves remainder \(5\) after division by \(17\). Negative values wrap around too: \(-10=7\).</p>
<p>To share a secret \(\alpha\in\mathbb F_p\) among \(n\) parties, independently choose \(n-1\) uniform field elements \(s_1,\ldots,s_{n-1}\). “Uniform” means each of the \(p\) values has probability \(1/p\). Choose the last share to make the total correct:</p>
<div class="math">\[s_n=\alpha-\sum_{i=1}^{n-1}s_i,\qquad \alpha=\sum_{i=1}^{n}s_i.\]</div>
<p>The sum symbol means add the indicated shares. Party \(P_i\) receives only \(s_i\). Following the lecture, write \([\alpha]\) for the whole distributed sharing; no individual party needs to possess every component.</p>
<p>For \(\alpha=4\) in \(\mathbb F_{17}\), choose \(s_A=6\) and \(s_B=8\). The remaining share is \(s_C=4-6-8=-10=7\). Reconstruction gives \(6+8+7=21=4\). The numerical size of a share says nothing about how much of the secret its holder owns.</p>
{{lab:shares}}
<p>Choose fresh random shares for each new sharing. If all shares are later revealed, their sum recovers the secret exactly. Before that, privacy is a statement about the entire collection visible to any colluding subset; we prove it next.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> In \(\mathbb F_{17}\), a dealer shares \(\alpha=12\). The first two shares are \(9\) and \(15\). What must the third share be? Enter its representative from \(0\) to \(16\).</p>',
            'answer': 5,
            'hint': r'<p>Subtract both chosen shares from the secret, then reduce modulo \(17\).</p>',
            'solution': r'<p>The third share is \(12-9-15=-12=5\pmod {17}\). Checking the construction, \(9+15+5=29=12\pmod {17}\).</p>',
        },
    },
    {
        'id': 'additive-privacy',
        'title': 'Prove privacy for the whole coalition view',
        'section': 'II · Computing on shares',
        'kind': 'lesson',
        'source': 'Lecture 17–19, Lemma 1, p. 4; expanded joint-distribution argument.',
        'source_ref': 'lecture',
        'requires': ['additive-sharing'],
        'body': r'''<p>Fix a secret \(\alpha\), and suppose a coalition sees any \(n-1\) additive shares. Fix particular values for those observed shares. There is <strong>exactly one</strong> value for the missing share that makes all \(n\) shares sum to \(\alpha\).</p>
<p>The sharing algorithm generates each complete tuple with the correct sum with equal probability: each tuple corresponds to exactly one choice of its \(n-1\) sampled field elements. There are \(p^{n-1}\) such choices. Thus, if \(\mathbf{v}\) denotes any fixed tuple of \(n-1\) observed values,</p>
<div class="math">\[\Pr[\text{coalition sees }\mathbf{v}\mid\text{secret }\alpha]=\frac{1}{p^{n-1}}.\]</div>
<p>The probability is over the dealer’s random choices. It is the same for every possible secret \(\alpha\), so observing the tuple does not favour one secret over another. This proves <strong>perfect privacy</strong>. A smaller coalition cannot learn more, because its view is obtained by discarding some components of an already private view.</p>
<p>For example, observed shares \(6,8\) in \(\mathbb F_{17}\) are compatible with secret \(4\) and missing share \(7\), or secret \(10\) and missing share \(13\). Each observed pair has probability \(1/17^2\) under either secret.</p>
<p>Checking each share separately would be insufficient. Two individually uniform values can reveal a secret together: in a two-party sharing, each share is uniform but their sum is exactly the secret. Security against collusion therefore requires the <em>joint</em> distribution, which the counting argument establishes.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p><strong>Practice.</strong> Four parties hold an additive sharing over \(\mathbb F_{17}\). A coalition sees the fixed three-share tuple \((2,6,10)\). What is the probability of this observation when the secret is \(5\), and why is it unchanged when the secret is \(11\)?</p>',
            'hint': r'<p>For each candidate secret, count compatible complete sharings and compare with the total number the dealer can generate.</p>',
            'solution': r'<p>For secret \(5\), the missing share is \(5-2-6-10=-13=4\). For secret \(11\), it is \(11-2-6-10=-7=10\). In each case there is exactly one compatible complete sharing among \(17^3\) equally likely sharings. The observation therefore has probability \(1/17^3=1/4913\) for either secret. Changing the secret changes the missing share, not the distribution of the coalition’s tuple.</p>',
            'rubric': [r'State probability \(1/17^3\).', 'Explain that each candidate secret uniquely determines the missing share.', 'Use equally likely complete sharings to conclude that the observed-view probability is independent of the secret.'],
        },
    },
    {
        'id': 'input-sharing',
        'title': 'Distinguish the input owner from the share holder',
        'section': 'II · Computing on shares',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.1, pp. 4–5, including the input-sharing diagram.',
        'source_ref': 'lecture',
        'requires': ['additive-privacy'],
        'body': r'''<p>Each party now acts as dealer for its own input. Alice shares \(x_A\), Bob shares \(x_B\), and Charlie shares \(x_C\). A party keeps its own component and sends the other components privately to their intended holders. These private channels must prevent an outside party from collecting all the shares.</p>
<p>The notation \(s_{AB}\) means <strong>a share of Alice’s input held by Bob</strong>: the first subscript is the input owner; the second is the recipient. It does not mean Bob learns Alice’s complete input.</p>
<table><caption>One execution in \(\mathbb F_{17}\)</caption><thead><tr><th scope="col">Input owner</th><th scope="col">Alice holds</th><th scope="col">Bob holds</th><th scope="col">Charlie holds</th></tr></thead><tbody><tr><th scope="row">Alice, \(x_A=4\)</th><td>\(6\)</td><td>\(8\)</td><td>\(7\)</td></tr><tr><th scope="row">Bob, \(x_B=5\)</th><td>\(2\)</td><td>\(9\)</td><td>\(11\)</td></tr><tr><th scope="row">Charlie, \(x_C=3\)</th><td>\(7\)</td><td>\(4\)</td><td>\(9\)</td></tr></tbody></table>
<p>Each row adds to its owner’s input modulo \(17\). Each column shows the components one party needs for the coming computation. For example, Bob has \(s_{AB}=8\), \(s_{BB}=9\), and \(s_{CB}=4\). Bob also knows his own input \(5\) and the random choices he used to share it; the table does not erase that prior knowledge.</p>
{{lab:input-sharing}}
<p>Publishing this entire table would reveal every input. The table is our teaching view across all participants. During the real protocol, a recipient learns only the privately delivered values, together with its own dealer information.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> Charlie receives \(s_{AC}=7\). What does this symbol identify?</p>',
            'choices': ['A component of Alice’s input sharing, delivered to Charlie.', 'A component of Charlie’s input sharing, delivered to Alice.', 'The sum of Alice’s and Charlie’s complete inputs.'],
            'answer': 0,
            'feedback': [r'<p>Correct. The first subscript identifies whose input was shared; the second identifies who holds this component.</p>', r'<p>The subscripts are reversed in that interpretation. A share of Charlie’s input held by Alice is \(s_{CA}\), not \(s_{AC}\).</p>', r'<p>The symbol names one share, not a sum of complete inputs. Alice’s three shares together reconstruct her input.</p>'],
            'hint': r'<p>Read the subscripts as owner first, recipient second.</p>',
            'solution': r'<p>It is Alice’s share sent to Charlie. Charlie cannot reconstruct \(x_A\) from this component alone; he would also need Alice’s and Bob’s components of that same input sharing.</p>',
        },
    },
    {
        'id': 'shared-circuit',
        'title': 'Keep every intermediate wire secret-shared',
        'section': 'II · Computing on shares',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2 and §2.2, pp. 4–5.',
        'source_ref': 'lecture',
        'requires': ['input-sharing'],
        'body': r'''<p>An <strong>arithmetic circuit</strong> describes a computation using addition and multiplication gates. A wire carries a field value from an input or an earlier gate. In the lecture’s construction, usually called the GMW approach, each wire is represented by an additive sharing throughout the evaluation.</p>
<p>For the running example, the first gate produces \(u=x_A+x_B\); the second produces \(z=u x_C\). The letters \(u\) and \(z\) name intermediate and final values. Their sharings are \([u]\) and \([z]\). With inputs \(4,5,3\) in \(\mathbb F_{17}\), the underlying values are \(u=9\) and \(z=27=10\).</p>
<table><caption>The invariant maintained at each stage</caption><thead><tr><th scope="col">Stage</th><th scope="col">What the parties hold</th></tr></thead><tbody><tr><th scope="row">Input sharing</th><td>One component each of \([x_A],[x_B],[x_C]\).</td></tr><tr><th scope="row">Addition gate</th><td>One component each of \([u]\), with components summing to \(x_A+x_B\).</td></tr><tr><th scope="row">Multiplication gate</th><td>One component each of \([z]\), with components summing to \(u x_C\).</td></tr><tr><th scope="row">Output</th><td>Reveal only the components of \([z]\) and add them.</td></tr></tbody></table>
<p>An <strong>invariant</strong> is a property preserved as the computation proceeds. Here it is the equality between a wire’s intended value and the sum of its distributed components. To prove correctness, establish it for input wires, then show that each gate preserves it. When the final shares are opened, their sum is the intended output.</p>
<p>This explains the construction’s organisation: we need a secure rule for addition and a secure rule for multiplication. Applying those rules gate by gate evaluates the circuit. We must additionally argue privacy for the composed execution; the wire invariant alone proves only correct arithmetic.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> A protocol correctly shares every input, then opens every intermediate wire so that the remaining gates are easy to evaluate. Which conclusion follows?</p>',
            'choices': ['It can compute the correct result while violating the MPC privacy definition.', 'Correct input sharing guarantees that every later message is private.', 'If the final arithmetic is correct, a simulator necessarily exists.'],
            'answer': 0,
            'feedback': [r'<p>Correct. The wire values may reveal information not implied by the final output. Correct evaluation and privacy are separate obligations.</p>', r'<p>Input sharing protects the initial distribution of inputs. Later openings can reveal additional information, as the zero-multiplier example showed.</p>', r'<p>Correctness does not construct a simulator. The simulator must reproduce intermediate messages using only corrupt inputs and the final output.</p>'],
            'hint': r'<p>Recall the circuit with a zero multiplier and a publicly revealed intermediate sum.</p>',
            'solution': r'<p>The protocol may be correct but insecure. For example, publishing \(x_A+x_B\) reveals information to Charlie even when \(x_C=0\) makes the permitted final output always zero.</p>',
        },
    },
    {
        'id': 'local-addition',
        'title': 'Add shares locally and prove the sum is right',
        'section': 'II · Computing on shares',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.3, p. 5.',
        'source_ref': 'lecture',
        'requires': ['shared-circuit'],
        'body': r'''<p>Suppose a gate’s input values are \(x\) and \(y\). From here, \(x_i\) and \(y_i\) denote <strong>party \(P_i\)'s components of these wire sharings</strong>, rather than the original input owned by that party. Thus \(x=\sum_i x_i\) and \(y=\sum_i y_i\).</p>
<p>Each party forms its output component \(z_i=x_i+y_i\). Adding all components gives</p>
<div class="math">\[\sum_{i=1}^{n}z_i=\sum_{i=1}^{n}(x_i+y_i)=\left(\sum_{i=1}^{n}x_i\right)+\left(\sum_{i=1}^{n}y_i\right)=x+y.\]</div>
<p>The middle equality simply regroups the additions. Therefore the resulting components form \([x+y]\), exactly the sharing required by the next wire. Party \(P_i\) already holds both numbers needed for its addition, so it sends no message.</p>
<p>In our \(\mathbb F_{17}\) example, the shares of Alice’s input are \((6,8,7)\), and those of Bob’s input are \((2,9,11)\). The parties compute</p>
<div class="math">\[(6+2,\;8+9,\;7+11)=(8,0,1).\]</div>
<p>These components sum to \(9=4+5\). Alice sees her output component \(8\), Bob sees \(0\), and Charlie sees \(1\). None needs to open the sum.</p>
{{lab:addition}}
<p>Local computation cannot give the coalition information beyond what it could already calculate from its existing views. This is why addition requires no new cryptographic message. Do not infer that all derived sharings are independent; their values satisfy the circuit’s arithmetic relations.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> In \(\mathbb F_{17}\), Bob holds \(x_B=12\) and \(y_B=9\), meaning his components of two wire sharings. What component should he use for their sum?</p>',
            'answer': 4,
            'hint': r'<p>Bob applies the gate to his own components; he does not reconstruct either input wire.</p>',
            'solution': r'<p>Bob uses \(z_B=12+9=21=4\pmod {17}\). This is one component of the output sharing, not the secret value \(x+y\). The latter is obtained only by adding every party’s output component.</p>',
        },
    },
    {
        'id': 'public-constants',
        'title': 'Treat a public constant differently from a secret wire',
        'section': 'II · Computing on shares',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.4, p. 6.',
        'source_ref': 'lecture',
        'requires': ['local-addition'],
        'body': r'''<p>A <strong>public constant</strong> \(k\in\mathbb F_p\) is known to every party. This makes two more gate operations possible without communication.</p>
<p>For multiplication by \(k\), every party multiplies its component by \(k\). If \([x]\) has components \(x_1,\ldots,x_n\), the new components satisfy</p>
<div class="math">\[kx_1+\cdots+kx_n=k(x_1+\cdots+x_n)=kx.\]</div>
<p>So \([kx]\) is obtained by scaling all components. For addition of \(k\), however, we add it to <strong>exactly one designated component</strong>, say party \(P_1\)'s:</p>
<div class="math">\[[x+k]=(x_1+k,x_2,\ldots,x_n).\]</div>
<p>The sum increases by \(k\) once. If everyone instead added \(k\), the sum would increase by \(nk\), which is generally a different value. Equivalently, the public constant has the simple sharing \((k,0,\ldots,0)\).</p>
<p>For example, \((8,0,1)\) shares \(9\) in \(\mathbb F_{17}\). To add public \(5\), let Alice change her component: \((13,0,1)\) shares \(14\). To multiply the original sharing by public \(5\), all parties scale: \((6,0,5)\) shares \(11=5\cdot9\pmod {17}\).</p>
{{lab:constants}}
<p>The distinction will be essential when Beaver multiplication produces a public correction term. We will distribute that correction by adding it once, while multiplying every component by the other public factors.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> Three parties hold a sharing of \(x\) over \(\mathbb F_{17}\). Each adds public \(4\) to its own component. What do the resulting components share?</p>',
            'choices': [r'\(x+4\).', r'\(x+12\).', r'\(4x\).'],
            'answer': 1,
            'feedback': [r'<p>Only one designated party should add \(4\) for this result. Three additions change the reconstructed sum by \(3\cdot4\).</p>', r'<p>Correct. Reconstruction adds all three modified components, so the public constant is counted three times: \(x+3\cdot4=x+12\).</p>', r'<p>Adding \(4\) to each component does not multiply the secret by \(4\). Scalar multiplication would require each party to multiply its component by \(4\).</p>'],
            'hint': r'<p>Write the sum of the three modified components and collect the constant terms.</p>',
            'solution': r'<p>The sum is \((x_1+4)+(x_2+4)+(x_3+4)=x+12\) in \(\mathbb F_{17}\). The correct rule for \([x+4]\) adds \(4\) to only one component.</p>',
        },
    },
    {
        'id': 'multiplication-obstacle',
        'title': 'Find the cross terms that local multiplication misses',
        'section': 'III · Beaver multiplication',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.5, p. 6.',
        'source_ref': 'lecture',
        'requires': ['public-constants'],
        'body': r'''<p>For addition, applying the operation to corresponding components worked because addition regroups. Trying the same rule for multiplication fails. With two parties, write \(x=x_1+x_2\) and \(y=y_1+y_2\), where each subscript identifies the component’s holder. Expanding the desired product gives</p>
<div class="math">\[xy=x_1y_1+x_1y_2+x_2y_1+x_2y_2.\]</div>
<p>If party \(P_1\) outputs \(x_1y_1\) and \(P_2\) outputs \(x_2y_2\), reconstruction omits \(x_1y_2\) and \(x_2y_1\). These are called cross terms because their factors belong to different parties. Publishing the factors to calculate them would defeat the purpose of keeping the wires shared.</p>
<p>The same problem occurs with three parties. In the running example, the components of \(u=9\) are \((8,0,1)\), and the components of \(v=3\) are \((7,4,9)\). Local componentwise multiplication gives \((5,0,9)\) modulo \(17\). Their sum is \(14\), but the required product is \(uv=27=10\).</p>
{{lab:cross-terms}}
<p>This calculation disproves that proposed rule. It does not prove that every special multiplication task requires the same amount of communication. Our general shared-wire multiplication will instead use a precomputed random product and a short interaction. Its purpose is to supply the missing algebra without revealing either input wire.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> Two parties have shares \((2,3)\) of \(x=5\) and \((4,6)\) of \(y=10\), all in \(\mathbb F_{17}\). What is the total of the cross terms omitted by local multiplication?</p>',
            'answer': 7,
            'hint': r'<p>The omitted terms multiply each party’s component of one wire by the other party’s component of the other wire.</p>',
            'solution': r'<p>The missing total is \(2\cdot6+3\cdot4=24=7\pmod {17}\). Local products sum to \(2\cdot4+3\cdot6=26=9\); adding the missing \(7\) gives \(16=5\cdot10\pmod {17}\).</p>',
        },
    },
    {
        'id': 'beaver-triple',
        'title': 'Prepare shares of one random product',
        'section': 'III · Beaver multiplication',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.5.1, p. 6.',
        'source_ref': 'lecture',
        'requires': ['multiplication-obstacle'],
        'body': r'''<p>As an intermediate construction, introduce a trusted dealer. Before seeing the parties’ inputs, the dealer samples two <strong>independent uniform</strong> field elements \(a,b\), computes \(c=ab\), and additively shares each value. This collection \([a],[b],[c]\) is a <strong>Beaver triple</strong>.</p>
<p>Party \(P_i\) receives only \(a_i,b_i,c_i\), its components of the three sharings. The secret values satisfy \(c=ab\); individual components generally do <em>not</em> satisfy \(c_i=a_i b_i\). Confusing these equalities would recreate the multiplication error from the previous card.</p>
<table><caption>Our example triple in \(\mathbb F_{17}\)</caption><thead><tr><th scope="col">Secret value</th><th scope="col">Alice</th><th scope="col">Bob</th><th scope="col">Charlie</th></tr></thead><tbody><tr><th scope="row">\(a=6\)</th><td>\(1\)</td><td>\(2\)</td><td>\(3\)</td></tr><tr><th scope="row">\(b=7\)</th><td>\(4\)</td><td>\(5\)</td><td>\(15\)</td></tr><tr><th scope="row">\(c=8=6\cdot7\)</th><td>\(6\)</td><td>\(7\)</td><td>\(12\)</td></tr></tbody></table>
<p>Each row adds to the displayed secret modulo \(17\). The full table is visible for learning; no computing party receives it. The three sharings use independent fresh sharing randomness, subject to their three reconstruction sums.</p>
{{lab:triple}}
<p>The dealer is trusted to generate valid triples, keep the masks secret, and remain separate from the later execution. In particular, it must not collude with a party that observes the masked openings. We will remove this extra trusted participant after understanding how one triple evaluates a multiplication gate.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> Alice’s components in the displayed triple are \(a_A=1,b_A=4,c_A=6\). Because \(1\cdot4\ne6\), should she conclude that the triple is invalid?</p>',
            'choices': ['Yes; every party’s components must themselves form a multiplication triple.', 'No; the required relation concerns the reconstructed values, not each local component.', 'No; any three shared values can serve as a Beaver triple.'],
            'answer': 1,
            'feedback': [r'<p>The relation is \((\sum_i a_i)(\sum_i b_i)=\sum_i c_i\). It does not require \(a_i b_i=c_i\) separately.</p>', r'<p>Correct. Here the reconstructed values are \(6,7,8\), and \(6\cdot7=8\pmod {17}\). A single party cannot verify that global relation from its three components alone.</p>', r'<p>The global product relation is essential. Arbitrary reconstructed \(c\) would add an error to the product produced by the protocol.</p>'],
            'hint': r'<p>Look at the equation the dealer enforces before sharing its values.</p>',
            'solution': r'<p>No. Validity requires \(c=ab\) for the reconstructed values. It does not require \(c_A=a_A b_A\). The displayed triple satisfies the global equality in \(\mathbb F_{17}\).</p>',
        },
    },
    {
        'id': 'beaver-identity',
        'title': 'Rewrite the secret product into operations we can perform',
        'section': 'III · Beaver multiplication',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.5.1, equation (1), p. 6.',
        'source_ref': 'lecture',
        'requires': ['beaver-triple'],
        'body': r'''<p>We have shared gate inputs \([x],[y]\), and a fresh triple \([a],[b],[c]\) with \(c=ab\). Define two differences: \(\delta=x-a\), read “delta”, and \(\varepsilon=y-b\), read “epsilon”. These subtract the random masks from the secret inputs.</p>
<p>Because \(x=\delta+a\) and \(y=\varepsilon+b\), ordinary distributive multiplication gives</p>
<div class="math">\[\begin{aligned}xy&=(\delta+a)(\varepsilon+b)\\&=\delta\varepsilon+\delta b+\varepsilon a+ab\\&=\delta\varepsilon+\delta b+\varepsilon a+c.\end{aligned}\]</div>
<p>The final equality uses the triple’s product relation. Now suppose we can safely make \(\delta\) and \(\varepsilon\) public. The first term becomes a public constant. The next two terms multiply shared values by public constants. The last is already shared. Every required operation is one we have learned:</p>
<div class="math">\[[xy]=[c]+\varepsilon[a]+\delta[b]+[\delta\varepsilon].\]</div>
<p>Here multiplying a sharing by a public value means scaling every component. The notation \([\delta\varepsilon]\) can use the public sharing \((\delta\varepsilon,0,\ldots,0)\): only the designated party adds that term.</p>
<p>For \(x=9,y=3,a=6,b=7\) in \(\mathbb F_{17}\), we get \(\delta=3\), \(\varepsilon=13\), and \(c=8\). Substitution gives \(8+13\cdot6+3\cdot7+3\cdot13=146=10\), which is the desired \(9\cdot3\pmod {17}\).</p>
<p>The algebra proves correctness provided the triple is valid and the differences are opened correctly. Privacy requires a separate argument that those openings conceal the inputs.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p><strong>Practice.</strong> A faulty dealer supplies shares of \(c=ab+e\), where \(e\ne0\) is a field element. Everything else follows Beaver’s rule. Express the reconstructed result in terms of \(x,y,e\).</p>',
            'hint': r'<p>Substitute the faulty value of \(c\) into the product identity; all other terms are unchanged.</p>',
            'solution': r'<p>The result is \(\delta\varepsilon+\delta b+\varepsilon a+(ab+e)\). The first four terms, with \(ab\) instead of \(c\), equal \(xy\). Hence reconstruction gives \(xy+e\). A valid global triple relation is necessary for correctness; merely sharing three values does not enforce it.</p>',
            'rubric': [r'Substitute \(c=ab+e\) into the recombination equation.', r'Identify the remaining four terms as \(xy\), giving result \(xy+e\).'],
        },
    },
    {
        'id': 'beaver-opening',
        'title': 'Open the masked differences, not the input wires',
        'section': 'III · Beaver multiplication',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.5.1, Step 1, p. 7.',
        'source_ref': 'lecture',
        'requires': ['beaver-identity'],
        'body': r'''<p>Each party already holds components of the input wires and the triple. Party \(P_i\) locally subtracts \(a_i\) from its component \(x_i\), and \(b_i\) from its component \(y_i\). Call the results \(\delta_i=x_i-a_i\) and \(\varepsilon_i=y_i-b_i\). These are shares of the two masked differences.</p>
<p>The parties reveal those components to one another. Each recipient adds them:</p>
<div class="math">\[\delta=\sum_i\delta_i=x-a,\qquad\varepsilon=\sum_i\varepsilon_i=y-b.\]</div>
<p>This operation is called <strong>opening</strong> a sharing. Everyone learns the reconstructed value. Here we open only \([\delta]\) and \([\varepsilon]\); the original inputs and the masks remain shared.</p>
<table><caption>Opening the running multiplication in \(\mathbb F_{17}\)</caption><thead><tr><th scope="col">Party</th><th scope="col">\(\delta_i=x_i-a_i\)</th><th scope="col">\(\varepsilon_i=y_i-b_i\)</th></tr></thead><tbody><tr><th scope="row">Alice</th><td>\(8-1=7\)</td><td>\(7-4=3\)</td></tr><tr><th scope="row">Bob</th><td>\(0-2=15\)</td><td>\(4-5=16\)</td></tr><tr><th scope="row">Charlie</th><td>\(1-3=15\)</td><td>\(9-15=11\)</td></tr></tbody></table>
<p>The first column sums to \(37=3\), so \(\delta=3\). The second sums to \(30=13\), so \(\varepsilon=13\). Both openings can be sent together: neither one needs the result of the other.</p>
{{lab:beaver}}
<p>At this point \(\delta\) and \(\varepsilon\) are public constants, while \(a,b,c,x,y\) remain shared. It is therefore safe <em>arithmetically</em> to use the differences as public factors in the identity. The next two cards complete the calculation and justify why revealing these differences preserves privacy.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> In another multiplication over \(\mathbb F_{17}\), the parties broadcast difference components \(11,8,14\). What public masked value do they reconstruct?</p>',
            'answer': 16,
            'hint': r'<p>Opening an additive sharing means adding its components in the field.</p>',
            'solution': r'<p>They reconstruct \(11+8+14=33=16\pmod {17}\). This reveals the masked difference, such as \(x-a\), rather than either of its two terms separately.</p>',
        },
    },
    {
        'id': 'beaver-combine',
        'title': 'Construct the output share held by each party',
        'section': 'III · Beaver multiplication',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.5.1, Steps 2–3, p. 7.',
        'source_ref': 'lecture',
        'requires': ['beaver-opening'],
        'body': r'''<p>After the openings, all parties know \(\delta\) and \(\varepsilon\). Let \(z_i\) be party \(P_i\)'s output component. If Alice is the designated party that adds the public correction, the component rules are</p>
<div class="math">\[\begin{aligned}z_A&=c_A+\varepsilon a_A+\delta b_A+\delta\varepsilon,\\z_i&=c_i+\varepsilon a_i+\delta b_i\quad(i\ne A).\end{aligned}\]</div>
<p>Every term uses either that party’s own triple component or a public value. No further message is needed for this gate. Summing the rules adds the correction once and reconstructs \(c+\varepsilon a+\delta b+\delta\varepsilon=xy\), by the identity we derived.</p>
<p>In the running \(\mathbb F_{17}\) example, \(\delta=3\), \(\varepsilon=13\), and the public correction is \(\delta\varepsilon=39=5\). The parties obtain:</p>
<table><caption>Each row is local computation</caption><thead><tr><th scope="col">Party</th><th scope="col">Calculation modulo \(17\)</th><th scope="col">Output component</th></tr></thead><tbody><tr><th scope="row">Alice</th><td>\(6+13\cdot1+3\cdot4+5\)</td><td>\(2\)</td></tr><tr><th scope="row">Bob</th><td>\(7+13\cdot2+3\cdot5\)</td><td>\(14\)</td></tr><tr><th scope="row">Charlie</th><td>\(12+13\cdot3+3\cdot15\)</td><td>\(11\)</td></tr></tbody></table>
<p>The resulting sharing is \([xy]=(2,14,11)\). If this is an intermediate gate, the components stay private and feed the next gate. In our example it is the final output, so the parties reveal them and reconstruct \(2+14+11=27=10\).</p>
<p>This equals \((4+5)\cdot3\pmod {17}\), the agreed circuit output. A field computation returns a residue modulo \(p\); it is not automatically an unrestricted integer calculation. When ordinary integers are intended, their encoding and possible wraparound must be handled as part of the chosen function.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> Bob holds triple components \(a_B=5,b_B=7,c_B=9\) in \(\mathbb F_{17}\). The openings give \(\delta=4,\varepsilon=2\). Alice, not Bob, adds the public correction. What output component does Bob compute?</p>',
            'answer': 13,
            'hint': r'<p>Use Bob’s three components and the two public multipliers. Do not add the public correction a second time.</p>',
            'solution': r'<p>Bob computes \(z_B=c_B+\varepsilon a_B+\delta b_B=9+2\cdot5+4\cdot7=47=13\pmod {17}\). The term \(\delta\varepsilon\) belongs only to Alice’s component under this convention.</p>',
        },
    },
    {
        'id': 'mask-privacy',
        'title': 'Explain why opening a fresh masked value is private',
        'section': 'III · Beaver multiplication',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.5.1 and §2.6, pp. 7–8; expanded masking and simulation argument.',
        'source_ref': 'lecture',
        'requires': ['beaver-combine'],
        'body': r'''<p>Fix a wire value \(x\). Let its mask \(a\) be uniform in \(\mathbb F_p\), independent of \(x\). For any possible observed difference \(d\), the equation \(x-a=d\) holds for exactly one mask, namely \(a=x-d\). Hence</p>
<div class="math">\[\Pr[\delta=d\mid x]=\Pr[a=x-d]=1/p.\]</div>
<p>This probability is the same for every \(x\). That is the precise reason the public difference \(\delta=x-a\) does not reveal \(x\). The analogous argument applies to \(\varepsilon=y-b\). Since the masks are independent, each observed pair of differences has probability \(1/p^2\), independent of \((x,y)\).</p>
{{lab:masks}}
<p>We must also account for the coalition’s triple components. With independently random additive sharings of \(a,b,c=ab\), any coalition missing at least one party sees components whose joint distribution is independent of the full values \(a,b\). Each candidate pair of full masks is equally likely, even after those components are fixed. The masking argument therefore still applies to that coalition.</p>
<p>A simulator for one gate can sample uniform public differences, keep the corrupted parties’ broadcasts consistent with their known components, and choose the honest parties’ broadcasts to have the required totals. Corrupted output components then follow from the recombination rule. This preserves correlations: for example, a corrupted party’s broadcast must equal its known input component minus its known mask component.</p>
<p>A full execution also keeps successive local calculations consistent and simulates the final opening subject to the given output. Sampling <em>every message independently</em> would fail those checks. The online security argument uses correct, fresh triples and the semi-honest model; it does not protect against fabricated openings.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p><strong>Practice.</strong> A dealer chooses one uniform mask \(a\) and sets \(b=a\), then uses this otherwise valid triple for one multiplication. Show one relation about the secret inputs that the two public differences reveal.</p>',
            'hint': r'<p>Subtract the two opened differences. The same mask appears in both.</p>',
            'solution': r'<p>The openings are \(\delta=x-a\) and \(\varepsilon=y-a\). Subtracting gives \(\delta-\varepsilon=x-y\). Thus the transcript reveals the difference of the secret inputs, even though each opening separately is uniform. This relation is not generally implied by the allowed product output, so independent masks are required. For example, products \(1\cdot6\) and \(2\cdot3\) are both \(6\) in \(\mathbb F_{17}\), but the input differences are \(12\) and \(16\).</p>',
            'rubric': [r'Derive \(\delta-\varepsilon=x-y\).', 'Explain that individually uniform openings need not be jointly private.', 'State that the masks must be independent; a correct product relation alone is insufficient.'],
        },
    },
    {
        'id': 'mask-reuse',
        'title': 'Use a triple once, even when the product stays secret',
        'section': 'III · Beaver multiplication',
        'kind': 'lesson',
        'source': 'Lecture 17–19, single-use condition in §2.5.1, p. 7; explicit reuse attack added.',
        'source_ref': 'lecture',
        'requires': ['mask-privacy'],
        'body': r'''<p>The same mask must not protect two different input values. To distinguish two executions, write their inputs as \(x^{(1)}\) and \(x^{(2)}\). Reusing \(a\) produces public differences</p>
<div class="math">\[\delta^{(1)}=x^{(1)}-a,\qquad\delta^{(2)}=x^{(2)}-a.\]</div>
<p>Anyone observing both messages can subtract them. The mask cancels:</p>
<div class="math">\[\delta^{(2)}-\delta^{(1)}=x^{(2)}-x^{(1)}.\]</div>
<p>This is extra information even if neither input is individually recovered. If one input becomes known, the observer also recovers the other by adding the disclosed difference.</p>
<p>For example, in \(\mathbb F_{17}\), reusing \(a=6\) for inputs \(9\) and \(12\) reveals differences \(3\) and \(6\). Their difference \(3\) reveals that the second input is the first plus \(3\). Knowing the first input \(9\) then reveals the second as \(12\).</p>
{{lab:reuse}}
<p>Refreshing only the additive components while keeping the same underlying \(a\) does not fix the problem: opening reconstructs the same masked values, regardless of how they were split. Fresh triples must contain fresh independent masks, and a consumed triple must never be assigned to another gate.</p>
<p>The leak happens when the masked differences are opened. Keeping the final product shared does not remove information already present in the public transcript. This is why preprocessing supplies enough distinct triples for all multiplication gates that will execute.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> In \(\mathbb F_{17}\), the same mask protects two inputs. The public differences are \(\delta^{(1)}=15\) and \(\delta^{(2)}=4\). Later the first input is revealed as \(x^{(1)}=7\). What is the second input?</p>',
            'answer': 13,
            'hint': r'<p>Compute \(\delta^{(2)}-\delta^{(1)}\) modulo \(17\), then add that difference to the known first input.</p>',
            'solution': r'<p>The disclosed input difference is \(4-15=-11=6\pmod {17}\). Therefore \(x^{(2)}=7+6=13\pmod {17}\). Equivalently, the first opening reveals the reused mask as \(7-15=9\), and the second input is \(4+9=13\).</p>',
        },
    },
    {
        'id': 'remove-dealer',
        'title': 'Move expensive cryptography into preprocessing',
        'section': 'IV · From a gate to a protocol',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.5.2 and §2.6, pp. 7–8.',
        'source_ref': 'lecture',
        'requires': ['mask-reuse'],
        'body': r'''<p>A trusted dealer made the multiplication mechanism easy to understand, but it is an additional trust assumption. The lecture next replaces the dealer with a specialised protocol for generating shared random products. This leads to two phases.</p>
<p>In <strong>preprocessing</strong>, also called the offline phase, parties generate a supply of valid triples without using their actual inputs. In the <strong>online phase</strong>, they share the inputs, evaluate the circuit, and consume one triple for each ordinary multiplication gate. The triple values do not depend on which function will use them, although the number of triples needed depends on the circuit.</p>
<p>The lecture sketches a construction using <strong>somewhat homomorphic encryption</strong>: encryption that supports enough arithmetic on encrypted data for the required computation. Parties jointly generate a public encryption key while keeping the corresponding decryption key secret-shared. They encrypt their components of \(a\) and \(b\), then evaluate the encrypted arithmetic for</p>
<div class="math">\[ab=\left(\sum_i a_i\right)\left(\sum_i b_i\right).\]</div>
<p>A distributed decryption procedure produces shares of this result, not the plaintext product for everyone. No individual party reconstructs the decryption key. The notes present this as a construction outline; a complete protocol also has to establish the security of joint key generation, evaluation and decryption to shares.</p>
<p>Given ideal fresh triples, the online masking and sharing argument is information-theoretic: it does not rely on limited computing power. An encryption-based preprocessing protocol relies on computational assumptions, so the complete implemented construction inherits those assumptions. The online phase being information-theoretic does not make the full protocol unconditionally secure.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> A dealer retains the full mask \(a=6\) and later reads the public opening \(\delta=x-a=3\) in \(\mathbb F_{17}\). What follows?</p>',
            'choices': [r'It recovers \(x=9\); the dealer must remain outside the online observation/collusion model.', 'The value remains hidden because the parties only opened a masked difference.', 'The dealer needs the full multiplication output before recovering the input.'],
            'answer': 0,
            'feedback': [r'<p>Correct. Knowing the mask removes the protection: \(x=a+\delta=9\). The trusted-dealer construction assumes that this information is not combined.</p>', r'<p>A masked difference is private only from someone who lacks the mask. The dealer knows \(a\), so it can undo the subtraction.</p>', r'<p>The product output is unnecessary. The opening and the retained mask already give \(x\) directly.</p>'],
            'hint': r'<p>Solve \(\delta=x-a\) for \(x\) when \(a\) is known.</p>',
            'solution': r'<p>The dealer computes \(x=a+\delta=6+3=9\). This is why the initial model requires a trusted, noncolluding dealer that does not obtain the online openings, and why dealer-free preprocessing is a separate security problem.</p>',
        },
    },
    {
        'id': 'mpc-cost',
        'title': 'Count messages from the gates that need interaction',
        'section': 'IV · From a gate to a protocol',
        'kind': 'lesson',
        'source': 'Lecture 17–19, §2.6, p. 8; explicit communication units and setup qualifications.',
        'source_ref': 'lecture',
        'requires': ['remove-dealer'],
        'body': r'''<p>Addition gates and operations with public constants use local computation. A general multiplication gate consumes one triple and opens two masked field elements. This distinction explains why counting gates alone is not enough to predict MPC communication.</p>
<p>Let \(G\) be the total number of arithmetic gates, \(M\) the number of secret-by-secret multiplication gates, and \(n\) the number of parties. For a fixed \(n\), each party performs a constant amount of field arithmetic per gate, giving work proportional to \(G\).</p>
<p>During multiplication, each party broadcasts two components, one for each masked difference. Thus gate evaluation sends \(2nM\) field elements when a broadcast counts as one transmission. If implemented by a separate message to each of the other \(n-1\) parties, this becomes \(2n(n-1)M\) field-element deliveries. One field element requires approximately \(\lceil\log_2 p\rceil\) bits to encode.</p>
{{lab:cost}}
<p>These counts exclude the initial input sharing, final output opening, and preprocessing. Those have their own cost even when \(M=0\). For example, the basic input-sharing step with one input per party sends \(n(n-1)\) components privately.</p>
<p>Communication <em>rounds</em> measure sequential waits, not total messages. Independent multiplication gates can open their differences together. A multiplication whose input depends on an earlier multiplication must wait for that earlier output sharing. Consequently the number of successive multiplication layers matters for online latency; many parallel gates can increase communication without adding the same number of waits.</p>
<p>The expensive cryptographic preprocessing depends on how triples are generated. The simple per-gate count describes their consumption and the online arithmetic, not a measured running time for a production system.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> Five parties hold shared values \([x],[y],[z]\) and a public constant \(k\). They evaluate \(k(x+y)+yz\). How many field elements are broadcast for masked openings? Count each broadcast once and exclude input sharing, output opening and preprocessing.</p>',
            'answer': 10,
            'hint': r'<p>First identify which product has two secret factors. Multiplication by the public \(k\) is local.</p>',
            'solution': r'<p>Only \(yz\) multiplies two secret values, so it uses one Beaver triple and opens two masked differences. Each of the five parties broadcasts two field elements: \(2\cdot5\cdot1=10\). The sums and multiplication by public \(k\) are local. Input sharing, output opening and preprocessing are excluded from this count.</p>',
        },
    },
]

SOURCE_ISSUES = [
    'Lecture p. 4: expand additive privacy to the joint distribution of every coalition of n−1 shares; uniformity of one sum or each separate share is not by itself a joint-view proof.',
    'Lecture pp. 2–3 and 8: privacy permits all inferences from corrupt inputs and the agreed output. It does not mean that no honest input can ever be inferred after output reconstruction.',
    'Lecture p. 6: the trusted dealer is an additional noncollusion and observation assumption. A dealer retaining a and obtaining delta=x−a recovers x; merely having no function input does not itself imply trust.',
    'Lecture pp. 6–7: Beaver triples need independently uniform fresh masks, independently randomized additive sharings, and one-time use. The public delta·epsilon correction is added to exactly one component.',
    'Lecture p. 8: the full simulator must preserve the relationships among corrupt inputs, random coins, masked broadcasts, intermediate components and the supplied final output. Independently sampling every message as a uniform value is not a valid full simulation.',
    'Lecture pp. 7–8: information-theoretic online security assumes ideal correct fresh triples and appropriate private channels. Encryption-based preprocessing makes the complete construction computationally secure; threshold key generation and decryption-to-shares are an outline in these notes.',
    'Lecture p. 8: communication proportional to multiplication count describes gate evaluation for fixed party count. Input distribution, output reconstruction, preprocessing and the cost of implementing a broadcast are additional; communication volume is distinct from multiplication-layer latency.',
    'All numerical core examples use F17. These examples teach field arithmetic and are not secure parameter choices or an implementation of an actual cryptographic protocol.',
]
