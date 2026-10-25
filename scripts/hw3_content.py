r"""Single source for HW3, reused verbatim at its prerequisite point in Chapter 3.

Math is written as \(inline\) or \[display\] and rendered at build time.
"""
def lab(kind, title, body):
    return f'<figure class="learning snark-lab" data-snark-lab="{kind}"><figcaption>{title}</figcaption>{body}</figure>'

HW = {}
def exercise(key, title, question, steps, requires, pages, visual=''):
    HW[key] = dict(id='hw-'+key, title='HW3 '+key+' · '+title, question=question,
                   steps=steps, requires=requires, source='HW3 pp. '+pages, visual=visual)

exercise('1a', 'Knowledge implies soundness',
 r'''<p>An interactive proof has soundness error greater than \(1/3\): some prover convinces the verifier of a false statement with probability greater than \(1/3\). Can it have knowledge error less than \(1/3\)? Explain your answer.</p>''', [
 r'''Soundness concerns false statements. If the public statement \(x\) is false, there is no witness \(w\) satisfying the relation \(R(x,w)=1\).''',
 r'''Knowledge error \(\kappa\) is the acceptance threshold above which the proof-of-knowledge guarantee requires an efficient extractor to recover a valid witness from the prover. The extractor may interact with and rewind that prover; it does not simply read the transcript.''',
 r'''The cheating prover in the question succeeds with probability greater than \(1/3\). If \(\kappa<1/3\), that success would trigger extraction on a false statement. This is impossible because no valid witness exists. Thus the sheet’s claim that such a knowledge error is impossible is <strong>true</strong>.'''
 ], ['proof-properties'], '1')

exercise('1b', 'Which setup model?',
 r'''<p>The sheet asks whether we can construct non-interactive zero-knowledge proofs for NP “in the standard model (without a random oracle)”. Explain why the setup model matters.</p>''', [
 r'''A language \(L\) is the set of true statements. NP means a true statement has a short witness that can be checked efficiently. BPP means an efficient randomized algorithm decides membership, with error at most \(1/3\) on each input. Neither definition says every NP problem is in BPP.''',
 r'''In the <strong>plain model</strong>, the verifier has only the statement, proof and public algorithm description. There is no trusted common reference string (CRS) and no random oracle. A NIZK simulator produces an accepted-looking proof for a true statement without its witness.''',
 r'''Run that simulator on the input and give its output to the verifier. On true inputs, zero knowledge and completeness imply high acceptance. On false inputs, soundness bounds acceptance, because the simulator is an efficient candidate prover. A standard bounded-time simulation (with a timeout if needed) therefore gives a BPP decision procedure.''',
 r'''Consequently, plain-model NIZKs for <em>all</em> NP languages would imply \(\mathrm{NP}\subseteq\mathrm{BPP}\), which is not expected. This is the intended “likely false” answer. But <strong>standard model does not necessarily mean plain model</strong>: a CRS is compatible with the standard model, and CRS-based NIZKs for NP exist under suitable assumptions. “No random oracle” alone does not justify an impossibility claim.'''
 ], ['setup-models'], '1')

exercise('1c', 'A root bound needs a field',
 r'''<p>True or false: \(f(X)=2X^2+4X\) has at most two roots in \(\mathbb Z_6\). Here \(\mathbb Z_6\) means arithmetic modulo 6, and a root is an input at which the polynomial evaluates to zero.</p>''', [
 r'''The degree is 2, because the highest nonzero term is \(2X^2\). The theorem “a nonzero degree-\(d\) polynomial has at most \(d\) roots” requires a <strong>field</strong>, where every nonzero element has a multiplicative inverse.''',
 r'''Modulo 6, \(2\cdot3=0\) even though neither factor is zero. Thus \(\mathbb Z_6\) is not a field; we cannot cancel a nonzero factor as the root-bound proof requires.''',
 r'''Evaluate all six inputs: \[\begin{array}{c|rrrrrr}X&0&1&2&3&4&5\\\hline f(X)\bmod6&0&0&4&0&0&4\end{array}\] The roots are \(0,1,3,4\). There are four of them, so the claim is <strong>false</strong>.'''
 ], ['root-bound'], '1', lab('roots', 'Where does the root bound apply?',
 '<p>Each tile is one allowed input. The four highlighted roots modulo 6 already disprove the claim.</p><div class="snark-grid" data-roots><span>0 → 0 ✓</span><span>1 → 0 ✓</span><span>2 → 4</span><span>3 → 0 ✓</span><span>4 → 0 ✓</span><span>5 → 4</span></div>'))

exercise('1d', 'Hashing does not strengthen privacy',
 r'''<p>True or false: applying Fiat–Shamir to a Sigma protocol always gives statistical zero knowledge.</p>''', [
 r'''A Sigma protocol has a first message, a random challenge and a response. Its honest-verifier zero-knowledge property may be only <strong>computational</strong>: efficient observers cannot distinguish a real transcript from a simulated one, but an unlimited observer might.''',
 r'''Fiat–Shamir replaces the verifier’s challenge with a hash of the statement and first message. It changes how the challenge is obtained. It does not remove information that an unlimited observer could already recover from those messages.''',
 r'''The claim is <strong>false</strong>. Statistical zero knowledge must hold even against unlimited distinguishing computation; computational HVZK is not enough to conclude that stronger property. Any Fiat–Shamir security claim also needs the appropriate random-oracle theorem and protocol assumptions.'''
 ], ['fiat-shamir'], '1')

exercise('2a', 'Construct the Schnorr proof',
 r'''<p>In Schnorr’s protocol, \(g\) generates a group of prime order \(q\), the public value is \(h=g^x\), and the prover knows secret exponent \(x\). Use Fiat–Shamir to construct a non-interactive proof. What is \(\pi\)?</p>''', [
 r'''The interactive prover first chooses a fresh uniform \(r\in\mathbb Z_q\) and sends \(u=g^r\). The symbol \(\mathbb Z_q\) means exponents are reduced modulo \(q\). Fresh \(r\) prevents different proofs from exposing equations with reused secret randomness.''',
 r'''Replace the verifier’s uniform challenge with \(c=H(h,u)\in\mathbb Z_q\). In this model, a random oracle assigns an independent uniform challenge to each new encoded input and remembers the answer for repeats. The verifier can compute the same challenge.''',
 r'''Compute the response \(z=r+cx\pmod q\) and send \[\pi=(u,z).\] The challenge need not be sent because it can be recomputed. In an implementation, also bind the protocol name and group parameters into an unambiguous hash input; \(H(h,u)\) is the sheet’s abbreviated notation.'''
 ], ['schnorr-recap','fiat-shamir'], '2')

exercise('2b', 'Verify, then explain the equation',
 r'''<p>Write the verifier for the proof \(\pi=(u,z)\) of knowledge of \(x\) such that \(h=g^x\).</p>''', [
 r'''Parse the proof. Check that the public parameters and \(h,u\) are valid elements of the intended prime-order group, and that \(z\) is a valid scalar in \(\mathbb Z_q\). These checks keep the algebra in the domain the protocol assumes.''',
 r'''Recompute \(c=H(h,u)\) using exactly the prover’s encoding and hash domain. Accept precisely when \[g^z=u\,h^c.\] The verifier uses public \(h\); it does not need the secret \(x\).''',
 r'''To check completeness, substitute the honest response: \[g^z=g^{r+cx}=g^r(g^x)^c=u\,h^c.\] Adding exponents corresponds to multiplying group elements. This identity explains why every honest proof passes; by itself it does not prove soundness against a cheating prover.'''
 ], ['fiat-shamir'], '2', lab('schnorr', 'Check an actual transcript',
 '<p>For arithmetic you can inspect, use the order-11 subgroup modulo 23, with g = 2, x = 3, h = 8 and r = 4, so u = 16. The stored challenge for this example is c = 2. The honest response is z = 10.</p><div class="snark-equation" data-schnorr-result>2¹⁰ mod 23 = 12; 16 · 8² mod 23 = 12. Accept.</div><p>These tiny parameters make the arithmetic visible; they provide no cryptographic security.</p>'))

exercise('2c', 'Bound a restricted guessing attack',
 r'''<p>A cheating prover chooses a response \(z\), then a first message \(u\), before asking for \(H(h,u)\). Explain the bound \(Q/q\) for \(Q\) tested candidate proofs. Assume \(h\ne1\), where 1 is the group identity.</p>''', [
 r'''Acceptance requires \(g^z=u h^c\). Once \(u,z\) are fixed, the right side must match one fixed group element. Because the group has prime order and \(h\ne1\), the map \(c\mapsto h^c\) takes each of the \(q\) scalars to a different group element. Exactly one challenge can work.''',
 r'''A fresh random-oracle answer is uniform among those \(q\) challenges, so this attempt succeeds with probability \(1/q\). Repeating the same oracle input returns the stored answer; it is not a fresh random attempt.''',
 r'''The union bound says the chance that any of \(Q\) events occurs is at most the sum of their probabilities. Applying it to the tested candidates gives \[\Pr[\text{some candidate passes}]\le\min(1,Q/q).\] The argument is for this prescribed guessing strategy, not a full proof of knowledge for arbitrary attacks.''',
 r'''Here \(Q\) counts all tested candidates. If an attacker makes \(Q\) oracle queries and then submits one additional, unqueried candidate, the same counting argument gives \((Q+1)/q\), capped at 1. Also, when \(h=1\), the witness \(x=0\) is already public; the “unknown nonzero exponent” argument does not apply.'''
 ], ['challenge-search'], '2')

exercise('2d', 'Can a proof be passed on?',
 r'''<p>A verifier accepts a NIZK for a statement. Can it convince another verifier? Compare this with passing on the recorded conversation from an interactive zero-knowledge proof.</p>''', [
 r'''A publicly verifiable NIZK is a proof string \(\pi\). A second verifier with the same statement and public setup can run the same verification algorithm on that string. Copying the proof does not require knowing its witness.''',
 r'''For an interactive ZK proof, the first verifier’s recorded view includes its challenges and the prover’s responses. Zero knowledge promises that an efficient simulator can generate an indistinguishable view without the witness.''',
 r'''Therefore that recorded view alone does not establish to a third party that a real prover participated: it could have been simulated. The distinction is between a transferable public proof and a simulatable record of an interaction. This argument concerns recordings; it is not a claim that every live relay attack is impossible.'''
 ], ['transferability'], '2')

exercise('3a', 'A one-bit hash challenge is insufficient',
 r'''<p>A Sigma protocol has an efficient cheating strategy on a false statement that is accepted with probability \(1/2\). Show why applying Fiat–Shamir directly fails to give negligible soundness error.</p>''', [
 r'''Run the cheating strategy to produce its first message \(u\) on the false statement \(y\). Fix \(u\) before querying \(H(y,u)\). The random-oracle answer has the same uniform challenge distribution as the interactive verifier’s challenge.''',
 r'''Give this challenge to the cheating strategy and submit the resulting response with \(u\). The acceptance probability is still \(1/2\), by the assumed attainable cheating success of the original strategy.''',
 r'''A constant \(1/2\) does not shrink as the security parameter grows, so it is not negligible. One efficient attempt already violates the desired soundness guarantee. An <em>upper bound</em> of \(1/2\) alone would not prove an attack exists; this question uses error \(1/2\) as an attainable value.'''
 ], ['challenge-search'], '3')

exercise('3b', 'Amplify before applying Fiat–Shamir',
 r'''<p>Starting from the one-bit-challenge Sigma protocol, construct a three-message protocol with negligible soundness error. Then explain how to make it non-interactive.</p>''', [
 r'''Let \(\lambda\) be the security parameter. Send \(\lambda\) first messages together, receive a vector of \(\lambda\) independent uniform challenge bits, and send all \(\lambda\) responses together. Accept only if every copy accepts. These are still three messages, each now a batch.''',
 r'''Fix any first-message vector on a false statement. Special soundness says that two accepted responses to different challenges for the <em>same</em> first message would yield a witness. Since the statement is false, no such witness exists. Thus each coordinate can answer at most one of its two challenges, even if a malicious prover correlated its first messages.''',
 r'''At most one of the \(2^\lambda\) equally likely challenge vectors can pass all coordinates, so the soundness error is at most \(2^{-\lambda}\), which is negligible. Honest executions retain completeness; independent honest-verifier simulators reproduce the joint honest transcript distribution. Special soundness for the parallel protocol follows by extracting from any coordinate whose challenge differs.''',
 r'''For Fiat–Shamir, derive the whole challenge vector at once: \[(c_1,\ldots,c_\lambda)=H(y,u_1,\ldots,u_\lambda).\] Hash only after fixing every first message. Return those messages and their responses. Under the appropriate random-oracle security argument, polynomially many attempts cannot overcome an exponentially large challenge space.'''
 ], ['parallel-amplification'], '3', lab('challenge-space', 'One acceptable vector among all vectors',
 '<p>With 3 challenge bits there are 8 possible vectors. For a fixed first-message vector on a false statement, at most one is answerable.</p><div class="snark-grid" data-vectors><span class="is-hit">000 ✓</span><span>001</span><span>010</span><span>011</span><span>100</span><span>101</span><span>110</span><span>111</span></div>'))

exercise('4a', 'Build a succinct interactive argument',
 r'''<p>A PCP prover produces a bit string of length \(M=\operatorname{poly}(n)\) for a statement of length \(n\). A PCP verifier reads a constant number \(k\) of positions chosen before seeing their bits, has perfect completeness and soundness error \(1/2\). A Merkle commitment has \(\lambda\) bits and position openings of \(O(\lambda\log M)\) bits. Construct a three-message argument with negligible soundness error and total communication \(\operatorname{poly}(\lambda,\log n)\).</p>''', [
 r'''A PCP is a specially encoded proof whose randomly selected local tests detect false statements. It is not an ordinary witness with arbitrary bits sampled. Compute the PCP string, commit to all its indexed bits with a Merkle root \(c\), and send \(c\). Keep the string and tree so openings can be produced.''',
 r'''The verifier independently chooses the random coins for \(\lambda\) PCP tests and sends all requested positions in one batch. Nonadaptive means the positions depend on the statement and coins, not on previously returned bits. The prover replies with each requested bit and its authentication path, all in a third message.''',
 r'''Perform <strong>both</strong> checks: each opening must authenticate the returned bit at its requested position under \(c\), and each PCP test must accept when run on those bits. A valid Merkle path only proves “this bit was committed”; it does not prove the statement is true.''',
 r'''For a true statement, honest PCP bits pass every local test and every opening verifies, giving perfect completeness. For a false statement, binding prevents the efficient prover from changing the committed proof after seeing queries. For a fixed proof, each independent PCP test accepts with probability at most \(1/2\). All tests pass with probability at most \(2^{-\lambda}\), plus a negligible term for breaking commitment binding.''',
 r'''There are \(k\lambda\) openings. Since \(k\) is constant and \(\log M=O(\log n)\), their total size is \[O(\lambda)\cdot O(\lambda\log n)=O(\lambda^2\log n).\] The root costs \(\lambda\) bits and indices cost \(O(\lambda\log n)\), so they do not increase this bound. This proves the requested succinct <em>communication</em>; the stated PCP theorem alone does not promise a nearly linear verifier running time. The guarantee is an argument because Merkle binding assumes a computationally bounded attacker.'''
 ], ['pcp-cost'], '3–5')

exercise('4b', 'Remove the PCP challenge message',
 r'''<p>Convert the succinct argument in part 4(a) into a non-interactive argument in the random-oracle model.</p>''', [
 r'''First compute the PCP string and its root \(c\). Then hash an unambiguous encoding of the public statement, root and protocol parameters. Use the random-oracle output to derive the independent verifier randomness for all \(\lambda\) PCP tests; those coins determine their query positions.''',
 r'''The proof contains \(c\), the requested bits and their position openings. The verifier recomputes the challenge from the same context, authenticates the openings and runs every PCP local predicate. It accepts only if all checks pass.''',
 r'''Fixing the root before hashing prevents tailoring the committed proof to a challenge already known. An attacker can try several roots, but the amplified per-attempt error is exponentially small; a polynomial number of attempts still gives negligible error in the intended random-oracle argument. The Merkle hash and challenge hash need distinct domain labels so the two roles are not confused.''',
 r'''The proof stays short and is now one message: a succinct non-interactive argument, or SNARG, in the communication sense established in 4(a). Neither zero knowledge nor knowledge extraction was established by this construction. “Non-interactive” alone supplies neither property.'''
 ], ['pcp-fiat-shamir'], '5')
