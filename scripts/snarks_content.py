"""Chapter 3: dependency-ordered teaching source. See TEACHING_GUIDE.md."""
from hw3_content import HW, lab

CARDS = []
def card(key, title, body, pages, requires=(), homework=()):
    CARDS.append(dict(id=key, title=title, body=body, source='Lectures 9–12 pp. '+pages,
                      requires=list(requires), kind='theory'))
    for exercise in homework:
        CARDS.append(dict(HW[exercise], kind='homework'))

card('snarg-goal', 'Verify a computation with a short proof', r'''
<p>A prover has done a long computation. A verifier wants to check its result without repeating all that work. We describe the claim by a public <strong>statement</strong> \(x\) and supporting <strong>witness</strong> \(w\). An efficiently checkable relation \(R(x,w)=1\) means that this witness establishes the claim. For example, the statement can specify an arithmetic circuit and its output; the witness supplies private inputs that produce that output.</p>
<p>A <strong>succinct non-interactive argument</strong> (SNARG) is one short proof message. “Succinct” means its length grows only polynomially in the security parameter \(\lambda\) and logarithmically in the statement and witness lengths. The notation \(|w|\) means the number of bits in \(w\); \(\log_2 |w|\) grows by just 1 when that length doubles.</p>
<p>The verifier must still read the public input. The notes allow time \(O(|x|)+\operatorname{poly}(\lambda,\log |w|)\). Here \(O\) is an upper growth bound, and “poly” allows fixed powers of its arguments. A <strong>SNARK</strong> adds a knowledge guarantee: successful proving must imply possession of a witness in the extraction sense explained next.</p>
<figure class="learning"><figcaption>The task</figcaption><div class="snark-flow"><span>Public claim x + private witness w</span><span>↓ prover computes a short proof π</span><span>Verifier reads x and checks π</span></div><p>A short proof need not hide the witness. Privacy is a separate property.</p></figure>
''', '1')

card('proof-properties', 'What does each guarantee promise?', r'''
<p>Keep four questions separate when reading a proof-system theorem. A <strong>language</strong> \(L\) is the set of statements for which a valid witness exists; \(x\in L\) means the statement is true.</p>
<table><thead><tr><th>Property</th><th>Question it answers</th></tr></thead><tbody><tr><td>Completeness</td><td>Does an honest proof of a true statement pass?</td></tr><tr><td>Soundness</td><td>Can a false statement pass?</td></tr><tr><td>Knowledge</td><td>Can a witness be extracted from a sufficiently successful prover?</td></tr><tr><td>Zero knowledge</td><td>Can the verifier’s view be simulated without the witness?</td></tr></tbody></table>
<p><strong>Soundness error</strong> bounds acceptance on false statements. <strong>Knowledge error</strong> is the acceptance threshold above which the extraction guarantee applies. An extractor is an efficient algorithm that can interact with a prover, possibly restoring it to an earlier state to ask a different challenge. It has more access than a spectator reading one proof.</p>
<p>A proof’s soundness holds even against an unlimited prover; an <strong>argument</strong> restricts the attacker to efficient computation. “Efficient” means polynomial time. An error is <strong>negligible</strong> if it eventually falls below every inverse fixed power of \(\lambda\), such as \(1/\lambda^2\) and \(1/\lambda^{100}\). A small constant does not meet that definition.</p>
''', '1–2', ['snarg-goal'], ['1a'])

card('setup-models', 'What information exists before the proof?', r'''
<p>Non-interactive means the prover sends one proof without receiving a fresh verifier challenge. How can that message avoid being fabricated by the same kind of simulator that zero knowledge promises? The answer depends on the public setup available to the algorithms.</p>
<table><thead><tr><th>Model</th><th>Available resource</th></tr></thead><tbody><tr><td>Plain model</td><td>Only the statement and public algorithms; no special setup.</td></tr><tr><td>CRS model</td><td>A common reference string sampled before proofs begin. Its generation and any secret setup information are part of the theorem.</td></tr><tr><td>Random-oracle model</td><td>Access to an ideal random function: each new input receives a uniform answer; a repeated input receives the same answer.</td></tr></tbody></table>
<p>In a CRS theorem, the simulator may generate a simulated setup with extra secret information. In a random-oracle theorem, it may be allowed to program oracle answers consistently. These simulation powers need not be available to an actual cheating prover. In the plain model, that distinction is missing.</p>
<p>NP consists of problems with efficiently checkable witnesses. BPP consists of problems an efficient randomized algorithm can decide with error at most \(1/3\). These names will let us state the limitation of plain-model NIZKs precisely in the next exercise. “Standard model” excludes an ideal random oracle but may still allow a CRS.</p>
''', '1–2; model clarification for HW3', ['proof-properties'], ['1b'])

card('schnorr-recap', 'The three messages we will remove', r'''
<p>Schnorr proves knowledge of an exponent \(x\) such that \(h=g^x\). The public group has prime order \(q\), meaning it contains \(q\) elements, and generator \(g\), whose powers reach them all. Exponents belong to \(\mathbb Z_q=\{0,\ldots,q-1\}\); addition and multiplication of exponents keep the remainder modulo \(q\).</p>
<figure class="learning"><figcaption>Schnorr’s interactive transcript</figcaption><div class="snark-flow"><span>Prover samples uniform r; sends u = gʳ →</span><span>← Verifier sends uniform challenge c</span><span>Prover sends z = r + cx mod q →</span><span>Verifier checks gᶻ = u · hᶜ</span></div></figure>
<p>The triple \((u,c,z)\) is the <strong>transcript</strong>, or recorded conversation. The verifier’s unpredictable challenge prevents the prover from first choosing \(c,z\) and then manufacturing \(u=g^z h^{-c}\). That reverse construction passes the equation without knowing \(x\); it is exactly what the honest-verifier simulator does.</p>
<p>A <strong>Sigma protocol</strong> has this first-message/challenge/response form, completeness, honest-verifier zero knowledge and <strong>special soundness</strong>: two accepting transcripts with the same first message and different challenges allow extraction of a witness. Three messages alone do not establish these properties.</p>
''', '1; prerequisite from Chapter 2', ['setup-models'])

card('fiat-shamir', 'Replace the challenge with a hash', r'''
<p>Fiat–Shamir makes the challenge reproducible by a future verifier. First fix the statement and first message; then compute their hash:</p>
\[c=H(h,u),\qquad z=r+cx\pmod q.\]
<p>The prover sends \((u,z)\). The verifier derives \(c\) itself and runs the original check. In the random-oracle model, each fresh input has an unpredictable uniform answer. The prover can choose \(u\), but cannot choose the answer after fixing \(u\). It can, however, try several first messages. We will account for those attempts shortly.</p>
<p>Bind the <strong>whole public context</strong> into the hash: statement, protocol identity, parameters and prior messages. Otherwise the same hash input might accidentally serve different claims or protocols. The short notation \(H(h,u)\) suppresses fixed context, not a security requirement.</p>
<p>The transform needs a security argument for the particular protocol and model. It does not turn computational privacy into statistical privacy: the former protects against efficient observers, while the latter also protects against unlimited distinguishing computation.</p>
''', '1, 7–8', ['schnorr-recap'], ['2a','2b','1d'])

card('transferability', 'A public proof and an interactive recording', r'''
<p>A non-interactive proof has a public verification rule. Anyone who has the same statement, proof and public setup can apply it. Passing the proof to another person preserves this check.</p>
<p>An interactive ZK recording has a different meaning. Its simulator can create an indistinguishable transcript without the witness. For Schnorr, choose uniform \(c,z\), then compute \(u=g^z h^{-c}\). This makes the verification equation hold. In a real execution, \(u\) must have been sent before an independently chosen challenge; the recording alone cannot establish that ordering happened with a real prover.</p>
<figure class="learning"><figcaption>What can the next verifier establish?</figcaption><div class="snark-flow"><span>NIZK proof → recompute its public verification</span><span>Interactive recording → could also be a simulator’s output</span></div></figure>
<p>This is why “a convincing interaction happened” and “these three values satisfy the equation” are different claims.</p>
<p>For a Fiat–Shamir proof, the simulator’s reverse-generated triple must also satisfy \(c=H(h,u)\). A random-oracle simulation can program that oracle answer consistently, under the theorem’s rules. An ordinary prover cannot set the oracle’s answer. This extra simulation capability explains why a NIZK simulator does not automatically give everyone a way to forge publicly verified proofs.</p>
''', '1; HW3 prerequisite', ['fiat-shamir'], ['2d'])

card('challenge-search', 'Count challenges before counting attempts', r'''
<p>Suppose a cheating prover fixes \(u,z\) and then queries \(H(h,u)\). For Schnorr with \(h\ne1\), exactly one of the \(q\) challenges satisfies \(g^z=u h^c\). This follows because nonidentity \(h\) generates the prime-order group, so distinct exponents give distinct powers.</p>
<p>A uniform hash answer hits that challenge with probability \(1/q\). If the attacker tests \(Q\) candidates, the <strong>union bound</strong> adds their individual success bounds, giving at most \(Q/q\), capped at 1. This remains an upper bound without assuming the success events are independent. A repeated oracle input gives the same challenge, not another random opportunity.</p>
<p>For a one-bit challenge there are only two possibilities. An attainable cheating success of \(1/2\) is already too large, even before the attacker searches. The next two exercises separate this small-challenge failure from the general counting argument.</p>
''', '1; HW3 prerequisite', ['fiat-shamir'], ['2c','3a'])

card('parallel-amplification', 'Make the entire challenge hard to guess', r'''
<p>Run \(\lambda\) copies of a one-bit-challenge Sigma protocol in <strong>parallel</strong>: send all first messages, receive all challenges, then send all responses. The verifier accepts only if every copy passes.</p>
<p>Why does this help even against a malicious prover that correlates its messages? Fix its whole first-message vector on a false statement. Special soundness implies that a coordinate cannot answer both 0 and 1: if it could, extraction would produce a witness for a false statement. Thus at most one full challenge vector can pass.</p>
\[\underbrace{2\times\cdots\times2}_{\lambda\text{ challenge bits}}=2^\lambda,
\qquad \Pr[\text{accept a false claim}]\le 2^{-\lambda}.\]
<p>The verifier chooses uniformly among all these vectors. We count acceptable vectors rather than assuming a cheating prover behaves like independent honest copies. Fiat–Shamir must then hash the statement and <em>all</em> first messages to obtain the entire vector.</p>
''', '2; HW3 prerequisite', ['schnorr-recap','challenge-search'], ['3b'])

card('two-routes', 'Two routes to a succinct proof', r'''
<p>So far, hashing has removed interaction but has not made a long proof short. Succinctness needs a verifier that can check a large proof by inspecting only a few carefully chosen values. An <strong>oracle interface</strong> lets the verifier request selected entries of a fixed object without receiving the whole object.</p>
<figure class="learning"><figcaption>Where the chapter is going</figcaption><div class="snark-flow"><span>Route A: PCP → query a few encoded proof bits</span><span>Route B: polynomial IOP → query a few polynomial values</span><span>↓ authenticate the permitted answers with commitments</span><span>↓ derive verifier challenges with Fiat–Shamir</span><span>One short proof containing commitments and openings</span></div></figure>
<p>A <strong>PCP</strong> is a probabilistically checkable proof. An <strong>IOP</strong> is an interactive oracle proof: the prover supplies fixed objects in rounds, and the verifier queries them. “Fixed” matters; a prover allowed to invent each answer after seeing the query would evade consistency checks.</p>
<p>The notes also introduce a <strong>linear-query IOP</strong>. A query supplies weights for a vector; its answer is the <strong>inner product</strong>, found by multiplying corresponding entries and adding. For vector \((v_0,v_1,v_2)\) and weights \((1,r,r^2)\), the answer is \(v_0+rv_1+r^2v_2\). These are exactly the weights used to evaluate a polynomial from its coefficients, which connects the two oracle interfaces.</p>
<p>We first build Route A for HW3, then develop the algebra that makes Route B useful for arithmetic circuits.</p>
''', '2–3', ['parallel-amplification'])

card('pcp', 'Why a few proof bits can be enough', r'''
<p>The PCP theorem supplies an encoding algorithm. Given statement \(x\) and witness \(w\), it produces a proof string \(\pi\) with length \(M\), polynomial in the statement length \(n\). A randomized verifier selects a constant number \(k\) of positions and applies a specified logical test to their bits and the statement.</p>
<p>The encoding is designed so that a false statement cannot have a proof string that passes too many of these tests. This is the substantive theorem; sampling a few bits of an arbitrary witness would not give it.</p>
<table><tbody><tr><th>True statement</th><td>The correctly encoded proof passes every test: perfect completeness.</td></tr><tr><th>False statement</th><td>Every fixed proof string passes a random test with probability at most 1/2.</td></tr></tbody></table>
<p>In HW3, queries are <strong>nonadaptive</strong>: all positions are chosen from the public statement and verifier randomness before any requested bits are seen. That lets the verifier request them in one batch. The local test, also called a <strong>predicate</strong>, is a yes/no rule on those answers.</p>
''', '2–3', ['two-routes'])

card('merkle-oracle', 'Commit to the proof before revealing queries', r'''
<p>A vector commitment binds a public commitment to an indexed list of values. For a Merkle tree, hash the proof bits as ordered leaves, hash ordered pairs of child digests, and continue until one root remains. An <strong>authentication path</strong> supplies one sibling digest at each level; the index determines left versus right at every step.</p>
<figure class="learning"><figcaption>Authenticate one position</figcaption><div class="snark-flow"><span>Claimed bit at index i + sibling digest</span><span>↓ hash in the order specified by i</span><span>Parent digest + next sibling → … → root</span><span>Compare the recomputed root with the root sent first</span></div></figure>
<p>For a balanced tree with \(M\) leaves there are \(\lceil\log_2 M\rceil\) levels. If each digest has \(\lambda\) bits, an opening uses \(O(\lambda\log M)\) bits. The prover retains the proof and tree; the root by itself is not enough to generate an opening.</p>
<p>Computational binding prevents an efficient prover from changing the bit at an authenticated position after committing. It does not say the committed bits form a valid PCP proof. Verification must check that next.</p>
''', '2–3; HW1 prerequisite', ['pcp'])

card('pcp-protocol', 'Authentication and truth are different checks', r'''
<p>The prover sends one Merkle root. The verifier then chooses the random coins for \(\lambda\) independent PCP tests and sends their query positions. The prover returns all requested bits with their paths.</p>
''' + lab('pcp-checks', 'Both checks must pass',
 '<div class="snark-flow"><span>1. Paths authenticate bits at the requested positions</span><span>↓</span><span>2. The PCP’s logical predicate accepts those bits</span></div><p data-pcp-result>Valid paths with a failed logical test must be rejected.</p>') + r'''
<p>For a true claim, the correct PCP and honest openings pass both checks. For a false claim, binding keeps the proof fixed while the verifier samples tests. Each test accepts with probability at most \(1/2\); independent choices of verifier randomness give an all-pass bound \(2^{-\lambda}\). Add the negligible probability of an efficient attacker breaking binding.</p>
<p>This is a computational <em>argument</em>. Repetition can reuse the same committed proof; it is the verifier’s tests that must be fresh and independent.</p>
''', '2–3', ['merkle-oracle'])

card('pcp-cost', 'Count the communication in bits', r'''
<p>Let \(n\) be statement length, \(M=\operatorname{poly}(n)\) PCP length, \(k\) the constant number of queries per test, and \(\lambda\) the number of repetitions and digest length. Keeping these names separate prevents a short root from being confused with a short proof.</p>
<table><thead><tr><th>Message</th><th>Bits sent</th></tr></thead><tbody><tr><td>Root</td><td>λ</td></tr><tr><td>kλ query indices</td><td>O(λ log M)</td></tr><tr><td>kλ bits and paths</td><td>O(λ² log M)</td></tr></tbody></table>
<p>Why does \(\log M\) become \(O(\log n)\)? If \(M\le n^a\) for a fixed constant \(a\), then \(\log M\le a\log n\). Thus total communication is \(O(\lambda^2\log n)\). Polynomial growth in a logarithm is called <strong>polylogarithmic</strong>.</p>
<p>The verifier still reads the public input and runs the PCP’s query-selection and test algorithms. The HW3 theorem promises those algorithms are efficient; its communication calculation alone does not establish the stronger nearly linear verification time in the lecture’s SNARG definition.</p>
''', '1–3', ['pcp-protocol'], ['4a'])

card('pcp-fiat-shamir', 'Hash the root to derive the tests', r'''
<p>The PCP protocol’s middle message comes from public randomness. Once the statement \(x\) and root \(c\) are fixed, Fiat–Shamir can derive the verifier’s test randomness from \(H(x,c,\text{context})\). That randomness determines the requested positions and the local checks.</p>
<figure class="learning"><figcaption>What is in the non-interactive proof?</figcaption><div class="snark-flow"><span>Root c + queried bits + their openings</span><span>↓ verifier hashes (x, c, context)</span><span>Reconstruct queries → check paths → check PCP predicates</span></div></figure>
<p>The root must be fixed before the random-oracle answer is known. Trying polynomially many roots costs polynomially many attempts against the amplified error. Distinct domain labels separate challenge hashing from the hashes that build the Merkle tree.</p>
<p>This establishes the homework’s succinct communication route. It does not supply zero knowledge, knowledge extraction or a faster PCP verifier by itself. Next we turn to polynomial oracles, which encode the structure of computations more directly.</p>
''', '3, 7–8', ['pcp-cost','fiat-shamir'], ['4b'])

card('finite-fields', 'Arithmetic where division has a precise meaning', r'''
<p>For the polynomial route, we work in a <strong>finite field</strong> \(\mathbb F_p\) for a prime number \(p\). Its elements are \(0,1,\ldots,p-1\). Add and multiply normally, then keep the remainder modulo \(p\). For example, in \(\mathbb F_7\), \(5+4=2\) and \(3\cdot5=1\).</p>
<p>The second equality says 5 is the <strong>multiplicative inverse</strong> of 3. Dividing by 3 therefore means multiplying by 5. Every nonzero field element has an inverse; zero does not. This is what allows cancellation: if \(ab=0\) and \(a\ne0\), multiplying by \(a^{-1}\) gives \(b=0\).</p>
<p>Primality is essential for this familiar remainder construction. Modulo 6, \(2\cdot3=0\), so multiplying nonzero elements can give zero. Such elements are called <strong>zero divisors</strong>. Arithmetic modulo 6 is valid arithmetic, but it is not a field and cannot support every theorem we are about to use.</p>
<p>Field elements represent computation values in these proofs. Equality modulo \(p\) is not automatically equality of unrestricted integers; integer claims need appropriate encoding and range constraints.</p>
''', '4–6; algebra prerequisites', ['two-routes'])

card('polynomial-language', 'Read a polynomial as a rule with coefficients', r'''
<p>A polynomial \(f(X)=a_0+a_1X+\cdots+a_dX^d\) is specified by its coefficients \(a_0,\ldots,a_d\). The capital \(X\) is a formal input symbol. To evaluate at \(r\), substitute \(X=r\) and do the arithmetic in the field.</p>
<p>If \(a_d\ne0\), the <strong>degree</strong> is \(d\), the largest exponent with nonzero coefficient. The notation \(f\in\mathbb F[X]_{\le d}\) reads “f is a polynomial over field F with degree at most d.” A <strong>root</strong> is a value \(r\) satisfying \(f(r)=0\).</p>
<p>For \(f(X)=X^2-4\) over \(\mathbb F_7\), both 2 and 5 are roots: their squares are 4 modulo 7. Yet \(f(0)=3\), so this is not the zero polynomial. The <strong>zero polynomial</strong> has every coefficient zero; it evaluates to zero at every input.</p>
<p>We will distinguish two tasks: testing whether two formal polynomials are identical, and testing whether one polynomial is zero on a specified set of points. They need different algebraic statements.</p>
''', '4–6', ['finite-fields'])

card('root-bound', 'Why degree limits the number of roots', r'''
<p>Over a field, a nonzero polynomial of degree \(d\) has at most \(d\) distinct roots. Here is the link between a root and the degree: if \(f(a)=0\), polynomial division gives \(f(X)=(X-a)g(X)\), with \(g\) one degree smaller. The remainder is the constant \(f(a)\), so it vanishes.</p>
<p>If a different value \(b\) is also a root, then \(0=(b-a)g(b)\). Since \(b-a\ne0\) has an inverse, \(g(b)=0\). Thus every additional root belongs to the lower-degree polynomial \(g\). Repeating this argument uses one degree per distinct root; a nonzero constant has no roots.</p>
<figure class="learning"><figcaption>One factor for each distinct root</figcaption><div class="snark-flow"><span>Root a → factor (X − a)</span><span>Different root b → another factor (X − b)</span><span>d + 1 distinct roots would require degree at least d + 1</span></div></figure>
<p>The cancellation step explains exactly why “over a field” cannot be dropped. The next exercise tests that condition.</p>
''', '5', ['polynomial-language'], ['1c'])

card('polynomial-equality', 'One random evaluation tests an identity', r'''
<p>Suppose \(f\) and \(g\) each have degree at most \(d\). If they differ as formal polynomials, their difference \(h=f-g\) is nonzero and has degree at most \(d\). They agree at \(r\) exactly when \(h(r)=0\).</p>
<p>Fix both polynomials first, then sample uniform \(r\in\mathbb F\). The root bound limits their agreement to at most \(d\) field elements:</p>
\[\Pr[f(r)=g(r)\mid f\ne g]\le \min(1,d/|\mathbb F|).\]
<p>The denominator \(|\mathbb F|\) is the number of field elements. Choose a field much larger than the degree to make this error small. If the prover learned \(r\) first, it could manufacture a different polynomial that agrees just there; the order of commitment and challenge is essential.</p>
''' + lab('equality', 'See the inputs that a false identity can fool',
 '<p>Take h(X) = (X − 1)(X − 3) over F₇. Only inputs 1 and 3 give zero, so a random test misses the difference with probability 2/7.</p><div data-equality-plot class="snark-grid"><span>0 → 3</span><span class="is-hit">1 → 0</span><span>2 → 6</span><span class="is-hit">3 → 0</span><span>4 → 3</span><span>5 → 1</span><span>6 → 1</span></div>') + r'''
''', '5', ['root-bound'])

card('schwartz-zippel', 'More variables: count total degree', r'''
<p>A multivariable polynomial uses several input symbols. For example, over \(\mathbb F_7\),</p>
\[h(X,Y,Z)=3X^2Y^3Z+2XY^2.\]
<p>The first term has <strong>total degree</strong> \(2+3+1=6\); the second has total degree \(1+2=3\). The polynomial’s total degree is the maximum, 6. We count exponents <em>within</em> each term, then take the largest count.</p>
<p>The <strong>Schwartz–Zippel lemma</strong> extends the root test: for a nonzero formal polynomial of total degree \(d\), choose each input independently and uniformly from the same finite subset \(S\) of a field. Then</p>
\[\Pr[h(r_1,\ldots,r_m)=0]\le\min(1,d/|S|).\]
<p>The polynomial must be fixed before sampling the inputs. To test a proposed multivariable identity, subtract its two sides and apply this lemma to the difference. The rest of our PLONK outline uses univariate polynomials, meaning one input variable, but the same “false identity has few random zeros” idea underlies both tests.</p>
''', '5', ['polynomial-equality'])

card('interpolation', 'Turn a table of values into one polynomial', r'''
<p>For \(N\) distinct field points \(a_0,\ldots,a_{N-1}\) and chosen values \(v_0,\ldots,v_{N-1}\), there is exactly one polynomial of degree less than \(N\) with \(f(a_i)=v_i\). This is <strong>interpolation</strong>. It lets us encode a computation’s table of wire values as a polynomial.</p>
<p>To see existence, build a polynomial \(L_i\) that is 1 at \(a_i\) and 0 at every other table point:</p>
\[L_i(X)=\prod_{j\ne i}\frac{X-a_j}{a_i-a_j},\qquad f(X)=\sum_{i=0}^{N-1}v_iL_i(X).\]
<p>The symbol \(\prod\) means multiply the listed factors, and \(\sum\) means add the listed terms. The denominators are invertible because the points are distinct. At \(a_i\), only term \(i\) remains, giving exactly \(v_i\). Each basis polynomial has degree \(N-1\). For uniqueness, two such interpolants would differ by a degree-below-\(N\) polynomial with \(N\) roots, contradicting the root bound.</p>
''' + lab('interpolation', 'Change a table entry; reconstruct the encoding',
 '<p>Over F₇, the table f(0) = 3, f(1) = 1, f(2) = 2 gives f(X) = 5X² + 3. Substituting the three inputs recovers 3, 1 and 2 modulo 7.</p><div data-interpolation-table class="snark-grid"><span>0 → 3</span><span>1 → 1</span><span>2 → 2</span></div>') + r'''
''', '4, 9', ['polynomial-equality'])

card('vanishing-polynomial', 'Zero on a set is not zero everywhere', r'''
<p>We often need \(f(a)=0\) only for a specified set of distinct points \(\Omega\), read “Omega”. Define the <strong>vanishing polynomial</strong></p>
\[Z_\Omega(X)=\prod_{a\in\Omega}(X-a).\]
<p>It has exactly the requested roots and degree \(|\Omega|\). The factor argument from the root bound shows that \(f\) vanishes at all points in \(\Omega\) exactly when \(Z_\Omega\) divides \(f\). “Divides” means a polynomial \(q\) exists with \(f=Z_\Omega q\), with no remainder.</p>
<figure class="learning"><figcaption>A concrete factorization</figcaption><p>For Ω = {1, 2}, ZΩ(X) = (X − 1)(X − 2).</p><p>f(X) = X³ − 7X + 6 = ZΩ(X) · (X + 3).</p><p>Thus f vanishes at 1 and 2, even though f is not the zero polynomial. This identity also holds over F₉₇.</p></figure>
<p>The <strong>quotient</strong> \(q\) is a polynomial that certifies all those individual zero conditions at once. Next we will test its claimed factorization at a random point.</p>
''', '6', ['interpolation'])

card('zero-test', 'Check many zero conditions with one identity', r'''
<p>To prove that a degree-at-most-\(d\) polynomial \(f\) vanishes on \(\Omega\), the prover supplies a quotient polynomial \(q\). Fix both polynomials before choosing uniform \(r\), then test</p>
\[f(r)=Z_\Omega(r)\,q(r).\]
<p>For an honest quotient this equality always holds. If \(f\) does not vanish on \(\Omega\), no polynomial \(q\) can make the identity true everywhere. Apply the random equality test to \(h=f-Z_\Omega q\).</p>
<p>Suppose \(|\Omega|=k\le d\) and the oracle enforces the loose bound \(\deg q\le d\). Then \(\deg h\le d+k\le2d\), so a false claim passes with probability at most \(2d/|\mathbb F|\), capped at 1. An honest nonzero quotient actually has degree at most \(d-k\); the lecture uses the looser bound for a simple error estimate.</p>
<p>This <strong>ZeroTest</strong> uses two prover evaluations, \(f(r)\) and \(q(r)\), plus the verifier’s computation of \(Z_\Omega(r)\). Check the multiplication equation directly: dividing by \(Z_\Omega(r)\) would be undefined if the random point happened to be in \(\Omega\).</p>
''', '6', ['vanishing-polynomial'])

card('fibonacci-iop', 'Encode an entire recurrence', r'''
<p>Use the Fibonacci convention \(F_0=0,F_1=1\), with \(F_i=F_{i-1}+F_{i-2}\). Interpolate a degree-at-most-100 polynomial \(f\) with \(f(i)=F_i\) for \(i=0,\ldots,100\). The claim is that the last value is \(y=354224848179261915075\).</p>
<p>The verifier checks the endpoints \(f(0)=0\), \(f(1)=1\), \(f(100)=y\). To check all recurrence steps, define</p>
\[D(X)=f(X)-f(X-1)-f(X-2).\]
<p>Require \(D\) to vanish on \(\Omega=\{2,\ldots,100\}\). The prover fixes \(f\) and a quotient \(q\); after a random \(r\), the verifier checks</p>
\[f(r)-f(r-1)-f(r-2)=Z_\Omega(r)q(r).\]
<p>This uses seven polynomial evaluations: three endpoints, three shifted values at the random point, and one quotient value. The verifier derives \(D(r)\) from the same \(f\), so an unrelated “recurrence polynomial” cannot be substituted.</p>
<p>Work in a prime field with enough distinct points and, for this example’s integer interpretation, prime greater than \(y\). The recurrence fixes every value, all below that prime. The lecture writes initial values 1,1 but prints the answer for 0,1; this deck uses the consistent 0,1 convention. Also, few oracle queries alone do not make computing \(Z_\Omega(r)\) fast; we address that cost later.</p>
''', '4, 6', ['zero-test'])

card('polynomial-commitment', 'Authenticate a polynomial evaluation', r'''
<p>A polynomial oracle promises that answers come from one fixed polynomial with a degree bound. A <strong>polynomial commitment scheme</strong> (PCS) is the cryptographic interface used to implement that promise.</p>
<table><thead><tr><th>Algorithm</th><th>Meaning</th></tr></thead><tbody><tr><td>Setup(d, λ) → pp</td><td>Generate public parameters for the degree limit d and security parameter λ.</td></tr><tr><td>Commit(pp, f) → c</td><td>Commit to f. The prover retains f and any opening state.</td></tr><tr><td>Open(pp, f, r) → πeval</td><td>Prove the claimed value y = f(r) at point r.</td></tr><tr><td>Verify(pp, c, r, y, πeval)</td><td>Check that opening against the commitment.</td></tr></tbody></table>
<p><strong>Correctness</strong> means honest openings verify. <strong>Evaluation binding</strong> prevents an efficient prover from opening the same commitment at the same point to two different values.</p>
<p>For our oracle reasoning, the chosen PCS and its security theorem must also justify treating all accepted answers as evaluations of a committed polynomial within the stated degree bound. Evaluation binding alone is not a complete compiler theorem. A commitment may also reveal information; hiding needs its own guarantee or an appropriate randomized encoding.</p>
''', '7', ['fibonacci-iop'])

card('polynomial-compiler', 'The order of commitments makes the test meaningful', r'''
<p>Replace the abstract ZeroTest oracles by polynomial commitments. The prover commits to \(f\) and \(q\) before the verifier chooses \(r\). It then opens both at \(r\). The verifier checks the openings and the equation \(f(r)=Z_\Omega(r)q(r)\).</p>
<figure class="learning"><figcaption>From an oracle test to a proof</figcaption><div class="snark-flow"><span>Commit to all challenge-independent polynomials</span><span>↓ choose r, or derive r from the public context and commitments</span><span>Open the required evaluations</span><span>↓ verify openings, degree guarantees and algebraic checks</span></div></figure>
<p>If \(r\) were known before committing to \(q\), a dishonest prover could often choose a constant quotient just to satisfy the one equation at \(r\). Fixing the polynomial first is what permits the root-bound argument.</p>
<p>Fiat–Shamir hashes the statement and commitments to derive the challenge. An IOP-to-argument security theorem must justify this compilation, including the PCS guarantees and oracle model. Its three-message shape alone does not make the protocol a Sigma protocol or prove zero knowledge.</p>
''', '7–8', ['polynomial-commitment','fiat-shamir'])

card('arithmetic-circuit', 'A computation becomes a public relation', r'''
<p>An <strong>arithmetic circuit</strong> is a network of addition and multiplication gates over a field. Wires carry field elements. Public inputs \(x\) are known to the verifier; private inputs \(w\) are the witness. Circuit satisfaction is usually written \(C(x,w)=0\): the designated output must be zero.</p>
<p>Our running example over \(\mathbb F_{97}\) computes \((x_1x_2)(x_2+w_1)\). For public \(x_1=2,x_2=4\) and private \(w_1=3\), the intermediate results are \(8\) and \(7\), giving output \(56\).</p>
<figure class="learning"><figcaption>Follow the wires through three gates</figcaption>
<div class="circuit-layout"><svg class="circuit-map" viewBox="0 0 330 310" role="img" aria-label="Public x1 equals 2 and public x2 equals 4 feed multiplication gate 0, producing 8. x2 also feeds addition gate 1 with private w1 equals 3, producing 7. Gate 2 multiplies 8 and 7 to produce 56.">
<g class="circuit-wire"><path d="M40 44V80H91V111M165 44V80H119V111M165 80H226V111M290 44V80H254V111M105 159V201H161V224M240 159V201H189V224M175 272V287"/></g>
<g class="circuit-node"><circle cx="105" cy="135" r="24"/><circle cx="240" cy="135" r="24"/><circle cx="175" cy="248" r="24"/></g>
</svg><div class="circuit-labels" aria-hidden="true"><span style="left:12.12%;top:8%">x₁ = 2</span><span style="left:50%;top:8%">x₂ = 4</span><span style="left:87.88%;top:8%">w₁ = 3</span><span style="left:31.82%;top:43.55%">×</span><span style="left:72.73%;top:43.55%">+</span><span style="left:53.03%;top:80%">×</span><span style="left:25.76%;top:58%">8</span><span style="left:78.79%;top:58%">7</span><span style="left:53.03%;top:97%">56</span></div></div></figure>
<p>To state this as a zero-output relation with public target \(y\), use \(C(x,w)=(x_1x_2)(x_2+w_1)-y\). In the trace diagrams we display the three-gate computation fragment and check its output equals \(y=56\); adding the final subtraction gives the normalized zero-output circuit. We do not claim the displayed fragment itself outputs zero.</p>
''', '8–9', ['polynomial-compiler'])

card('execution-trace', 'Write down what every gate claims happened', r'''
<p>An <strong>execution trace</strong> lists the values on the circuit’s wires. Each gate has three slots: left input, right input and output. We also reserve slots for the original public and private inputs.</p>
<table><thead><tr><th>Gate</th><th>Left</th><th>Right</th><th>Output</th></tr></thead><tbody><tr><td>0: multiply</td><td>2</td><td>4</td><td>8</td></tr><tr><td>1: add</td><td>4</td><td>3</td><td>7</td></tr><tr><td>2: multiply</td><td>8</td><td>7</td><td>56</td></tr></tbody></table>
<p>There are \(3|C|+|I|\) slots, where \(|C|\) counts gates and \(|I|\) counts original inputs. For three gates and three inputs, \(N=12\). Use \(N\) for this table size; its interpolating polynomial will have degree <em>less than</em> \(N\).</p>
<p>The two appearances of 4 in the gate table are copies of input \(x_2\), which also has an original-input slot. A dishonest table could put different values in those slots. Checking each gate’s arithmetic is therefore not enough: later we must also check that connected wires agree.</p>
''', '9', ['arithmetic-circuit'])

card('roots-of-unity', 'Choose distinct addresses with a useful pattern', r'''
<p>We want \(N\) distinct field points at which to store the trace. A <strong>primitive N-th root of unity</strong> \(\omega\) has \(\omega^N=1\), with no smaller positive exponent giving 1. Its powers \(1,\omega,\ldots,\omega^{N-1}\) are therefore distinct.</p>
<p>In \(\mathbb F_{97}\), \(\omega=6\) has order 12. Its first twelve powers give the addresses for our twelve slots. Multiplying an address by \(\omega\) advances one slot; after the last slot it wraps back to 1. This multiplicative pattern will let one formula refer to a gate’s three adjacent slots.</p>
''' + lab('unity', 'Does the candidate give twelve different addresses?',
 '<div data-unity-grid class="snark-grid"><span>ω⁰ = 1</span><span>ω¹ = 6</span><span>ω² = 36</span><span>ω³ = 22</span><span>ω⁴ = 35</span><span>ω⁵ = 16</span><span>ω⁶ = 96</span><span>ω⁷ = 91</span><span>ω⁸ = 61</span><span>ω⁹ = 75</span><span>ω¹⁰ = 62</span><span>ω¹¹ = 81</span></div><p data-unity-result>6¹² = 1 modulo 97, with no repetition among the twelve addresses.</p>') + r'''
<p>Merely satisfying \(\omega^N=1\) is insufficient: \(\omega=1\) satisfies that equation but repeats the same address. Distinct points are required for interpolation. Choose a field that contains a primitive root of the required order.</p>
''', '9', ['execution-trace','interpolation'])

card('trace-polynomial', 'Put the table into a polynomial', r'''
<p>Interpolate \(f\), the trace polynomial, so it returns each trace value at its assigned address. Gate \(\ell\) uses addresses \(\omega^{3\ell}\), \(\omega^{3\ell+1}\), \(\omega^{3\ell+2}\) for left, right and output. Here \(\ell\) starts at 0.</p>
<p>Original input \(j\), starting at 1, is stored at \(\omega^{-j}\). Negative exponents mean inverses: since \(\omega^{12}=1\), \(\omega^{-1}=\omega^{11}\). Thus our inputs occupy exponents 11, 10 and 9, after the nine gate slots.</p>
''' + lab('trace', 'Which slots represent the same wire?',
 '<p>Read each tile as “exponent: stored value”. The field address is ω raised to that exponent; the stored value is f at that address.</p><div data-trace-grid class="snark-grid"><span>0: 2</span><span>1: 4</span><span>2: 8</span><span>3: 4</span><span>4: 3</span><span>5: 7</span><span>6: 8</span><span>7: 7</span><span>8: 56</span><span>9: 3</span><span>10: 4</span><span>11: 2</span></div>') + r'''
<p>There is exactly one interpolant of degree less than 12. It encodes <em>any</em> twelve field values, including dishonest ones. Interpolation provides a compact algebraic representation; the constraints on the next cards establish that the encoded table is valid.</p>
''', '9', ['roots-of-unity'])

card('four-obligations', 'What makes a trace a correct computation?', r'''
<p>A trace must meet four independent requirements. Public-input slots must equal the claimed inputs; the output slot must equal the public target; each gate must compute its operation; and every copy of a wire must agree.</p>
''' + lab('obligations', 'Change one requirement while keeping the others valid',
 '<p>The valid example uses public inputs 2, 4 and target 56. Its private input is 3. All arithmetic below is modulo 97.</p><div data-obligation-trace><p>Inputs: 2, 4, 3. Gates: (2,4 → 8), (4,3 → 7), (8,7 → 56).</p></div><div data-obligation-result class="snark-grid"><span>Public inputs: pass</span><span>Output: pass</span><span>Gates: pass</span><span>Wire copies: pass</span></div>') + r'''
<p>The private input is allowed to change between candidate witnesses; the verifier does not know it. Its repeated appearances must still agree. The interactive alternatives each satisfy three requirements while violating exactly one, showing why none can simply be omitted.</p>
''', '9–11', ['trace-polynomial'])

card('boundary-conditions', 'Bind the trace to the public claim', r'''
<p>For our fragment, the output condition is \(f(\omega^8)=56\). For a normalized full circuit, the corresponding final-output condition is zero. A single authenticated evaluation checks this boundary.</p>
<p>Let \(\Omega_I\) be the addresses of the <em>public</em> inputs. Interpolate \(f_{\mathrm{in}}\) on those addresses from the values the verifier knows. Then</p>
\[D(X)=f(X)-f_{\mathrm{in}}(X)\]
<p>must vanish on \(\Omega_I\). ZeroTest certifies all public-input equalities together. For the displayed fragment, \(\Omega_I=\{\omega^{11},\omega^{10}\}\) carries 2 and 4; the private input at \(\omega^9\) is not a public-input condition.</p>
<p>If a protocol provides a separate oracle for \(D\), it must also establish \(D=f-f_{\mathrm{in}}\). Otherwise a dishonest prover could supply the zero polynomial as \(D\) while leaving incorrect inputs in \(f\). Deriving \(D(r)\) directly from authenticated evaluations of the same \(f\) avoids that substitution.</p>
<p>Computing the public-input encoding may take time proportional to the number of public inputs. That is compatible with the verifier’s unavoidable cost of reading them.</p>
''', '9–10', ['four-obligations','zero-test'])

card('gate-selector', 'One equation chooses addition or multiplication', r'''
<p>A public <strong>selector polynomial</strong> \(s\) describes the circuit’s gate types. At a gate’s left address \(a=\omega^{3\ell}\), set \(s(a)=1\) for addition and \(s(a)=0\) for multiplication. Fix its values on the remaining trace-domain points as part of the public encoding, then interpolate.</p>
<p>Write \(L=f(a)\), \(R=f(\omega a)\), \(O=f(\omega^2 a)\). These are the same gate’s left, right and output values. Its residual is</p>
\[s(a)(L+R)+(1-s(a))LR-O.\]
<p>For \(s(a)=1\), the multiplication term disappears, leaving \(L+R-O\). For \(s(a)=0\), the addition term disappears, leaving \(LR-O\). The residual is zero exactly when the selected operation agrees with the claimed output.</p>
''' + lab('selector', 'Make a gate pass or fail',
 '<p>For L = 4, R = 3 and O = 7, addition has residual 0; multiplication has residual 5 in F₉₇.</p><div data-selector-result class="snark-equation">Addition: 4 + 3 − 7 = 0. This gate passes.</div>') + r'''
''', '10', ['boundary-conditions'])

card('gate-polynomial', 'Apply that equation to every gate', r'''
<p>Replace the gate address \(a\) by a formal input \(X\). This creates the polynomial</p>
\[\begin{aligned}G(X)={}&s(X)\bigl(f(X)+f(\omega X)\bigr)\\
&+(1-s(X))f(X)f(\omega X)\\
&-f(\omega^2X).\end{aligned}\]
<p>We require \(G\) to vanish on \(\Omega_G=\{\omega^{3\ell}:0\le\ell<|C|\}\), the set of gate-left addresses. At each of these points, the formula is exactly the gate residual from the previous card. We do not demand that it vanish at unrelated field points.</p>
<p>Use a quotient \(q_G\) to check \(G(r)=Z_{\Omega_G}(r)q_G(r)\). The verifier computes the left side using openings of \(f\) at \(r,\omega r,\omega^2r\), plus the fixed selector value \(s(r)\). It also opens \(q_G(r)\). These are a constant number of evaluations regardless of gate count.</p>
<p>If both \(f\) and \(s\) have degree below \(N\), multiplication makes \(\deg G\le3N-3\). The quotient degree bound and field size must accommodate this larger degree; the trace’s degree bound alone is not enough.</p>
''', '10', ['gate-selector'])

card('wire-permutation', 'Local arithmetic does not connect the gates', r'''
<p>A <strong>permutation</strong> rearranges positions, using each position exactly once. For every wire, cycle through all trace slots that represent that wire. Call the resulting permutation \(\sigma\). Requiring each value to equal the value at its successor forces all copies in a cycle to agree.</p>
<figure class="learning"><figcaption>Wire cycles in our twelve-slot trace</figcaption><div class="snark-flow"><span>x₁: 11 → 0 → 11</span><span>x₂: 10 → 1 → 3 → 10</span><span>w₁: 9 → 4 → 9</span><span>Gate 0 output: 2 → 6 → 2</span><span>Gate 1 output: 5 → 7 → 5</span><span>Final output: 8 → 8</span></div><p>These numbers are slot exponents, not field addresses or wire values.</p></figure>
\[f(\omega^i)=f(\omega^{\sigma(i)})\quad\text{for every slot }i.\]
<p>The private input’s two slots are included: privacy does not excuse inconsistent copies. Conceptually, form the polynomial whose domain values are the permuted trace and require equality on the domain. A real proof must also authenticate that permutation relationship; supplying an arbitrary second polynomial would not establish it.</p>
<p>The notes outline this wiring check but do not derive the full PLONK permutation argument. This card states the required relation and its role, without presenting the outline as a complete cryptographic construction.</p>
''', '11', ['gate-polynomial'])

card('fast-vanishing', 'A short formula removes a hidden linear cost', r'''
<p>Querying only a few values is useful only if the verifier can also compute its own expressions quickly. Directly evaluating \(Z_\Omega(r)=\prod_{a\in\Omega}(r-a)\) uses one factor per domain point.</p>
<p>For the <em>full</em> domain of \(N\) distinct powers of a primitive \(N\)-th root, every address satisfies \(X^N-1=0\). Both this polynomial and \(Z_\Omega\) are monic of degree \(N\) with the same roots, so</p>
\[Z_\Omega(X)=X^N-1.\]
<figure class="learning"><figcaption>Evaluate r¹² − 1 by repeated squaring</figcaption><div class="snark-flow"><span>r² = r · r</span><span>r⁴ = r² · r²</span><span>r⁸ = r⁴ · r⁴</span><span>r¹² = r⁸ · r⁴; then subtract 1</span></div></figure>
<p>Repeated squaring needs \(O(\log N)\) field multiplications. It is the structured domain that makes this fast; merely precomputing the coefficients of a degree-\(N\) polynomial would still leave many evaluation operations.</p>
<p>The formula applies to the full root domain. Public-input and gate subsets need their own efficient formulas or authenticated preprocessed polynomials. In our twelve-slot example, the three gate addresses are only a subset; substituting \(X^{12}-1\) for their vanishing polynomial would impose a different condition.</p>
''', '6, 10–11', ['wire-permutation'])

card('construction-map', 'Assemble the argument and state its scope', r'''
<figure class="learning"><figcaption>Which work happens when?</figcaption><div class="snark-flow"><span>Universal setup: PCS parameters for a maximum degree</span><span>↓ circuit preprocessing: fixed selectors, wiring and domains</span><span>↓ instance: evaluate the witness, interpolate the trace and construct quotient polynomials</span><span>↓ commit, derive challenges and open the required evaluations in protocol order</span><span>↓ verify input, output, gate and wiring conditions</span></div></figure>
<p>The circuit-dependent work can be reused across many statements about the same circuit. Universal setup supports different circuits up to its degree limit; it does not mean every circuit needs no preprocessing.</p>
<p>The conceptual chain is now connected: interpolation encodes a trace; constraints say what makes it valid; quotient identities turn many constraints into a few random checks; polynomial commitments authenticate the answers; Fiat–Shamir removes verifier messages under the relevant security theorem.</p>
<p>The lecture sketches this route to PLONK. A complete implementation additionally specifies its permutation protocol, all challenge rounds, degree enforcement and security assumptions. Zero knowledge requires suitable blinding, meaning randomization that conceals witness information while preserving the checked constraints. Knowledge extraction requires a separate proof-of-knowledge argument. Neither follows just from short proofs.</p>
''', '11–12', ['fast-vanishing'])

from later_teaching import revise
revise('snarks',CARDS)

assert len([c for c in CARDS if c['kind']=='theory']) == 36
assert len(CARDS) == 48
