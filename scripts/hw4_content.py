r"""HW4 authoring source, shared by Chapter 4 and the homework-only deck."""

def lab(key, title, content):
 return f'<figure class="learning pir-lab" data-pir-lab="{key}"><figcaption>{title}</figcaption>{content}</figure>'

HW = {}
def exercise(key, title, question, steps, requires, pages, visual=''):
 HW[key]=dict(id='hw4-'+key,title='HW4 '+key+' · '+title,question=question,steps=steps,
              requires=requires,source='HW4 pp. '+pages,visual=visual,kind='homework')

exercise('1a','An ideal oracle and its cryptographic implementation',r'''
<p>Assume \(\mathrm P=\mathrm{NP}\) in the standard model, without a random oracle. Is the PLONK polynomial IOP still sound?</p>''',[
 r'''A polynomial interactive oracle proof (Poly-IOP) gives the verifier an ideal interface to fixed polynomials with enforced degree bounds. Soundness means a false claim is accepted only with the stated small probability; it does not mean the prover's witness is hidden.''',
 r'''Its algebraic tests choose random points <em>after</em> the relevant polynomials have been fixed. A false degree-bounded identity can hold at only a bounded number of field points. This root-counting fact does not depend on the prover's computing time.''',
 r'''Thus the intended answer is <strong>true</strong> for the ideal Poly-IOP, including its required consistency checks. The hypothesis \(\mathrm P=\mathrm{NP}\) does not invalidate a field theorem. It can, however, invalidate the computational commitments used to implement those oracles. Soundness of the ideal object must be distinguished from security of a deployed SNARG.'''
],['proof-models'],'1')

exercise('1b','Single-server PIR when P equals NP',r'''
<p>Assume \(\mathrm P=\mathrm{NP}\), without a random oracle. Do secure single-server PIR schemes with sublinear communication exist in the setting of this course?</p>''',[
 r'''Private information retrieval (PIR) hides the requested index from the server. “Sublinear communication” means the number of transmitted bits grows more slowly than database size \(n\); downloading the entire database is excluded from the question.''',
 r'''For a single server, information-theoretic query privacy cannot provide this saving in the standard PIR setting. The single-server constructions in the lecture instead use cryptographic encryption: the server can compute on the query but cannot efficiently identify its plaintext.''',
 r'''The intended answer is <strong>false</strong>. The computational hardness needed for nontrivial single-server PIR does not survive \(\mathrm P=\mathrm{NP}\). Merely possessing encryption algorithms would not suffice; their privacy assumption must remain secure. The whole-database download remains private, but has linear communication.'''
],['single-server'],'1')

exercise('1c','Two servers need a separation assumption',r'''
<p>Assume \(\mathrm P=\mathrm{NP}\). Can secure two-server PIR with sublinear communication still exist?</p>''',[
 r'''The two servers hold identical copies of the database but do not share their query views. For a matrix with \(C\) columns, choose a uniform bit vector \(q_0\), and set \(q_1=q_0\oplus e_j\), where \(e_j\) has a 1 only in the requested column.''',
 r'''For every target \(j\), each individual share is uniform among the \(2^C\) bit vectors. To see this for server 1's share \(q_1\), fix any possible value \(v\). Exactly one mask, \(q_0=v\oplus e_j\), produces it. Thus \(\Pr[q_1=v]=2^{-C}\), independently of \(j\). Unlimited computation cannot distinguish identical distributions.''',
 r'''With roughly \(\sqrt n\) rows and columns, two queries and two answers use \(O(\sqrt n)\) bits. Therefore the answer is <strong>true</strong>: privacy is information-theoretic, conditional on non-collusion. If the servers combine their queries, \(q_0\oplus q_1=e_j\) reveals the column. Correct output still assumes honest answering; privacy alone does not prevent a server from returning a wrong answer.'''
],['pir-assumptions'],'1')

exercise('1d','An empty proof is not automatically fast verification',r'''
<p>Assume \(\mathrm P=\mathrm{NP}\). Does this alone establish that all NP languages have a SNARG under the lecture's succinct-verification requirement?</p>''',[
 r'''P contains decision problems solvable in polynomial time; NP contains problems with efficiently checkable witnesses. If \(\mathrm P=\mathrm{NP}\), the verifier can decide an NP statement without receiving a witness. An empty proof therefore gives perfect completeness and soundness.''',
 r'''That establishes short <em>communication</em>. The lecture also asks for verification time \(O(|x|)+\operatorname{poly}(\lambda,\log|w|)\), where \(x\) is the public statement, \(w\) the witness and \(\lambda\) the security parameter. Reading the input is allowed, but a general polynomial-time decision algorithm may take much longer.''',
 r'''For example, a running time of \(|x|^3\) is polynomial, yet the assertion “polynomial time” supplies no nearly linear bound in \(|x|\). Thus the intended answer is <strong>false in the sense that the conclusion does not follow from this argument</strong>. The supplied solution's “unlikely” qualification is not an unconditional impossibility proof. If “succinct” meant only a short proof, the empty-proof observation would answer a different, weaker question.'''
],['succinctness-review'],'1')

exercise('2a','Prove that the low coefficients vanish',r'''
<p>Let \(f\) have degree at most \(d\) over a field \(\mathbb F\), and let \(0\le i<d\). Give a polynomial IOP proving that the coefficients of \(X^0,\ldots,X^{i-1}\) are all zero, with perfect completeness and error at most \(d/|\mathbb F|\).</p>''',[
 r'''Multiplying a polynomial by \(X^i\) shifts every coefficient up by \(i\) positions. Therefore the claim is equivalent to the existence of a polynomial \(g\), of degree at most \(d-i\), such that \(f(X)=X^i g(X)\). For example, \(f=3X^2+5X^3\) uses \(i=2\) and \(g=3+5X\).''',
 r'''Fix the oracle for the claimed \(f\), with degree bound \(d\), and the prover's oracle for \(g\), with degree bound \(d-i\), before choosing a uniform random \(r\in\mathbb F\). Query the two values and accept exactly when \[f(r)=r^i g(r).\] We use an ideal bounded-degree oracle as specified by the exercise; ordinary uncommitted replies do not provide that guarantee.''',
 r'''For a true claim, the factorization is an identity, so every challenge passes: perfect completeness. For a false claim, \(h=f-X^i g\) is nonzero for every permitted \(g\). Its degree is at most \(d\), because \(\deg(X^i g)\le i+(d-i)=d\).''',
 r'''Over a field, where every nonzero element has an inverse, a nonzero degree-at-most-\(d\) polynomial has at most \(d\) roots. Hence a uniform challenge passes with probability at most \(\min(1,d/|\mathbb F|)\). If \(i=0\), there are no lower coefficients to exclude and the honest choice is simply \(g=f\).'''
],['coefficient-shift'],'1–2',lab('coefficient-shift','Watch what multiplying by Xⁱ does',
 '<p>For g(X) = 3 + 5X, multiplying by X² produces f(X) = 3X² + 5X³. The coefficient positions below 2 are empty.</p><div class="pir-strip" data-shift-strip><span>X⁰: 0</span><span>X¹: 0</span><span>X²: 3</span><span>X³: 5</span></div>'))

exercise('2b','Isolate one coefficient',r'''
<p>Prove that coefficient \(a_i\) of \(f(X)=a_0+\cdots+a_dX^d\) equals a public value \(\beta\). Give a polynomial IOP with perfect completeness and soundness error at most \(d/|\mathbb F|\).</p>''',[
 r'''Separate the terms below position \(i\), the claimed term at \(i\), and the terms above it: \[f(X)=f_L(X)+\beta X^i+X^{i+1}f_R(X).\] The subscript L means the lower-degree part; R means the remaining higher-degree part after shifting it down by \(i+1\).''',
 r'''Require \(\deg f_L\le i-1\) and \(\deg f_R\le d-i-1\). These bounds prevent either side part from altering coefficient \(i\). At the endpoints, use \(f_L=0\) when \(i=0\), and \(f_R=0\) when \(i=d\); no negative-degree nonzero polynomial is requested.''',
 r'''Fix the oracles for \(f,f_L,f_R\) with those bounds, then sample uniform \(r\). Accept precisely when \[f(r)=f_L(r)+\beta r^i+r^{i+1}f_R(r).\] An honest decomposition passes for every \(r\).''',
 r'''If the actual coefficient differs from \(\beta\), the difference between the two sides is a nonzero polynomial of degree at most \(d\). It has at most \(d\) roots, so the error is at most \(\min(1,d/|\mathbb F|)\). The degree limits are doing essential work: an unrestricted lower part could conceal an incorrect claimed coefficient.'''
],['coefficient-split'],'2',lab('coefficient-split','Which terms can affect the selected position?',
 '<p>In f(X) = 4 + 2X + 7X² + 3X³, the coefficient at i = 2 is 7. The lower part is 4 + 2X and the upper part is X³ · 3.</p><div class="pir-strip" data-coefficient-strip><span>4 · X⁰</span><span>2 · X¹</span><span class="is-hit">7 · X²</span><span>3 · X³</span></div>'))

exercise('2c','An inner product hidden in a product polynomial',r'''
<p>Let \(f(X)=\sum_{j=0}^d a_jX^j\) and \(g(X)=\sum_{j=0}^d b_jX^j\). Prove that \(a_0b_d+a_1b_{d-1}+\cdots+a_db_0=z\), using polynomial oracles of degree at most \(2d\), with perfect completeness and error at most \(4d/|\mathbb F|\).</p>''',[
 r'''An inner product multiplies corresponding entries and adds them. Here the coefficient list of \(g\) is reversed. In the expansion of \(h=fg\), a product \(a_jb_k X^{j+k}\) contributes to coefficient \(d\) exactly when \(j+k=d\). Thus that coefficient is the requested inner product.''',
 r'''Fix degree-at-most-\(d\) oracles for \(f,g\), and a degree-at-most-\(2d\) oracle for a proposed product \(h\). On a uniform random \(r\), check \(h(r)=f(r)g(r)\). A false product identity differs by a nonzero degree-at-most-\(2d\) polynomial, so this check has error at most \(2d/|\mathbb F|\).''',
 r'''To check the middle coefficient of \(h\), use the previous construction: \[h(X)=h_L(X)+zX^d+X^{d+1}h_R(X),\] with both side polynomials of degree at most \(d-1\) (both zero if \(d=0\)). Fix these oracles before sampling a fresh uniform \(t\), then check the corresponding equality at \(t\). A false coefficient identity has degree at most \(2d\) and the same error bound.''',
 r'''Accept only if both checks pass. If the claimed inner product is wrong, at least one of the two identities is false. The union bound gives the requested conservative bound \(\min(1,4d/|\mathbb F|)\). No independence of the prover's choices is needed for that addition of error bounds. If the claims are true, both identities hold at every point, giving perfect completeness.'''
],['product-coefficient'],'2–3',lab('product-coefficient','Find the terms whose degrees add to d',
 '<p>For f(X) = 1 + 2X + 3X² and g(X) = 4 + 5X + 6X² over F₁₀₁, the X² coefficient is 1·6 + 2·5 + 3·4 = 28.</p><div data-product-grid class="pir-product-grid"><span>1·6</span><span>2·5</span><span>3·4</span></div>'))

exercise('3a','Compute a commitment without knowing α',r'''
<p>A prime-order group \(G\) has generator \(g\) and order \(p\). Setup publishes \(g,g^\alpha,g^{\alpha^2},\ldots,g^{\alpha^d}\), while \(\alpha\in\mathbb Z_p^*\), a nonzero remainder modulo \(p\), stays unknown. Given the coefficients of \(f\in\mathbb F_p[X]_{\le d}\), compute \(c=g^{f(\alpha)}\).</p>''',[
 r'''Write \(f(X)=\sum_{j=0}^d f_jX^j\). The prover knows the scalars \(f_j\), and setup supplies each group element \(g^{\alpha^j}\). It does not supply the exponent \(\alpha^j\) itself.''',
 r'''Raise each supplied group element to its known coefficient, then multiply the results: \[c=\prod_{j=0}^d\left(g^{\alpha^j}\right)^{f_j}.\] The \(j=0\) element is \(g\), since \(\alpha^0=1\).''',
 r'''The power rules show why this works: multiplying powers of the same base adds their exponents, so the result is \(g^{\sum_j f_j\alpha^j}=g^{f(\alpha)}\). Exponent arithmetic is modulo group order \(p\). At no step did we recover \(\alpha\) or multiply two unknown exponents ourselves.'''
],['powers-setup'],'3',lab('powers-setup','Public group elements can encode hidden powers',
 '<p>For arithmetic only, use the order-11 subgroup generated by 2 modulo 23 and setup exponent α = 3. For f(X) = 4 + 2X + X², the public elements are 2, 8, 6. Compute 2⁴ · 8² · 6 mod 23 = 3, which equals 2⁸ because f(3) = 8 modulo 11.</p><div data-powers-output class="pir-equation">Commitment c = 3.</div><p>The displayed α makes this a teaching example, not a secure setup.</p>'))

exercise('3b','Why the binding guarantee is computational',r'''
<p>Is the commitment \(c=g^{f(\alpha)}\) statistically or computationally binding? Explain the role of the hidden setup exponent.</p>''',[
 r'''Binding prevents the prover from using different polynomials as explanations of the same commitment. Statistical binding must hold even against an unlimited attacker. Computational binding restricts the attacker to efficient algorithms.''',
 r'''For degree limit \(d\ge1\), an unlimited attacker can recover \(\alpha\) from \(g^\alpha\) by enumerating discrete logarithms. For any nonzero field scalar \(t\), set \(f'(X)=f(X)+t(X-\alpha)\). This changes the polynomial while preserving \(f'(\alpha)=f(\alpha)\), so the commitments agree.''',
 r'''Therefore the scheme is <strong>not statistically binding</strong> for \(d\ge1\). The intended guarantee is computational binding under the appropriate polynomial-commitment hardness assumptions for the chosen group and setup. “Many collisions exist” does not prove they are hard to find, and unknown \(\alpha\) alone is not a proof of that assumption.''',
 r'''The boundary case \(d=0\) commits only to constants: the map \(a\mapsto g^a\) is one-to-one modulo \(p\), so this particular collision argument does not apply. Also, binding does not assert hiding; the deterministic commitment is not automatically a private encoding of the polynomial.'''
],['powers-setup'],'3')

exercise('3c','Turn an opening into a quotient identity',r'''
<p>To open the commitment at a public point \(z\) with claimed value \(y\), describe the quotient polynomial used to prove \(f(z)=y\).</p>''',[
 r'''The claim is equivalent to \(f(X)-y\) having root \(z\). Polynomial division by \(X-z\) gives a constant remainder equal to \(f(z)-y\). The remainder is zero exactly when the opening claim is true.''',
 r'''For a valid opening, define \[q(X)=\frac{f(X)-y}{X-z},\qquad f(X)-y=(X-z)q(X).\] This is polynomial division, not division of the two values at \(X=z\). We never compute \(0/0\). If \(f\) has degree at most \(d\ge1\), then \(q\) has degree at most \(d-1\).''',
 r'''For example, over \(\mathbb F_{11}\), let \(f=X^2+2X+4\), \(z=1\) and \(y=7\). Then \(f-y=X^2+2X-3=(X-1)(X+3)\), so \(q=X+3\). The prover can compute a group encoding \(g^{q(\alpha)}\) by the same coefficient method as in part (a).'''
],['point-quotient'],'3')

exercise('3d','Check the identity in the exponent',r'''
<p>Suppose \(\operatorname{VerifProd}(g^a,g^b,g^c)\) checks whether \(c=ab\) in \(\mathbb F_p\). Given commitment \(c_f=g^{f(\alpha)}\), opening proof \(\pi=g^{q(\alpha)}\), point \(z\) and value \(y\), describe verification of \(f(z)=y\).</p>''',[
 r'''The opening identity is \(f(X)-y=(X-z)q(X)\). At the setup point, it requires \[f(\alpha)-y=(\alpha-z)q(\alpha).\] The verifier needs a product check on these exponents; ordinary group multiplication would add them instead.''',
 r'''Compute \(A=\pi\), \(B=g^\alpha/g^z\), and \(C=c_f/g^y\). Group division means multiplication by the group inverse. All these inputs are available from the proof, setup and public scalars; no discrete logarithms are required.''',
 r'''After checking that the supplied elements belong to the intended group, accept when \(\operatorname{VerifProd}(A,B,C)=1\). Handle zero exponents too: a zero exponent is the identity group element 1. If \(A=1\) or \(B=1\), accept the product equation exactly when \(C=1\); if neither is 1 but \(C=1\), reject. These cases extend the sheet's stated nonzero-exponent interface to legitimate zero values.''',
 r'''Honest openings satisfy the equation, so verification is complete. For a dishonest prover, negligible evaluation-binding error relies on the appropriate PCS hardness theorem. The hidden setup point \(\alpha\) was chosen before the adversary saw its encoded powers; it is not a fresh independent challenge chosen after the proof. A bare root-counting argument at \(\alpha\) would therefore leave a security gap.'''
],['exponent-product'],'3–4',lab('opening-check','Separate the public check from the hidden exponents',
 '<p>Use g = 2 modulo 23, group order 11, α = 3, and f(X) = X² + 2X + 4. The commitment is c = 3. At z = 1, the honest value is y = 7 and proof π = 18. The check receives (A, B, C) = (18, 4, 2).</p><div data-opening-output class="pir-equation">Exponents: 6 · 2 = 1 modulo 11. The product check accepts.</div><p>The example reveals tiny exponents to explain the check; it does not implement a secure pairing group.</p>'))

exercise('3e','Break binding with an exponent-division capability',r'''
<p>Assume \(z\ne\alpha\) and an efficient algorithm \(D_z\) that maps any group element \(g^x\) to \(g^{x/(\alpha-z)}\). Show how it breaks evaluation binding at point \(z\).</p>''',[
 r'''Evaluation binding prevents two accepted values for the same commitment at the same point. Start with an honestly committed polynomial and a valid opening to \(y=f(z)\). Choose a different value \(y'\ne y\).''',
 r'''Compute the group element \(U=c_f/g^{y'}=g^{f(\alpha)-y'}\). We know \(U\), not necessarily its exponent \(f(\alpha)-y'\). This distinction corrects the supplied solution's shorthand that calls the group element itself “x”.''',
 r'''Run the assumed algorithm on \(U\): \[\pi'=D_z(U)=g^{(f(\alpha)-y')/(\alpha-z)}.\] This denominator has an inverse in \(\mathbb F_p\) because \(z\ne\alpha\).''',
 r'''The exponent of \(\pi'\), multiplied by \(\alpha-z\), is exactly \(f(\alpha)-y'\). Hence the verifier's product check accepts the false value \(y'\), along with the already valid opening to \(y\). That is an evaluation-binding break. The forged group element need not be a commitment to a genuine quotient polynomial; the verification equation alone cannot tell under the assumed extra capability.'''
],['exponent-product'],'4')

exercise('4a','Build equality from Boolean gates',r'''
<p>Using NOT, AND and OR gates, build a circuit \(C_{\mathrm{EQ}}\) that outputs 1 exactly when two bit strings \((a_1,\ldots,a_m)\) and \((b_1,\ldots,b_m)\) agree at every position.</p>''',[
 r'''For one position, equality has two accepting cases: both bits are 1, or both are 0. Writing these cases with the specified gates gives \(a_k\land b_k\) and \((\neg a_k)\land(\neg b_k)\).''',
 r'''Combine those cases with OR, written \(\lor\): \[E_k=(a_k\land b_k)\lor(\neg a_k\land\neg b_k).\] Its outputs on \((0,0),(0,1),(1,0),(1,1)\) are respectively \(1,0,0,1\).''',
 r'''Require every position to pass: \[C_{\mathrm{EQ}}(a,b)=E_1\land E_2\land\cdots\land E_m.\] If any pair differs, its \(E_k=0\) forces the result to 0. If all pairs agree, all \(E_k=1\) and the result is 1. Two-input gates can be arranged in a tree; one large multi-input gate is not required.'''
],['binary-gates'],'4',lab('equality-circuit','Follow each bit comparison into the final AND',
 '<p>Compare a = 101 and b = 111. The position tests are 1, 0, 1, so the strings are unequal.</p><div data-equality-circuit class="pir-flow"><span>1 = 1 → 1</span><span>0 = 1 → 0</span><span>1 = 1 → 1</span><span>AND of 1, 0, 1 → 0</span></div>'))

exercise('4b','Use an encrypted binary address',r'''
<p>Using a secret-key fully homomorphic encryption (FHE) scheme for Boolean circuits, construct one-round single-server PIR on a database of \(n\ge2\) bits with \(O(\log n)\) uploaded ciphertexts and one returned ciphertext.</p>''',[
 r'''Use \(\ell=\lceil\log_2 n\rceil\) address bits. Number records 1 through \(n\), but encode record \(i\) by the binary representation of \(i-1\), padded to \(\ell\) bits. For example, eight records use addresses 000 through 111; trying to encode record 8 as the number 8 would incorrectly need four bits.''',
 r'''The client encrypts its \(\ell\) address bits with fresh encryption randomness, and also sends encryptions of 0 and 1. It keeps the secret key. These constants let the server represent each public address and database bit as ciphertext inputs even though it cannot run secret-key encryption itself. Supply any needed query-independent public evaluation material separately.''',
 r'''For each record \(j\), the server homomorphically evaluates the equality circuit between the encrypted address and the constant address \(j-1\). The result encrypts a selection bit \(s_j\): 1 for the requested record and 0 for all others. It then computes an encrypted AND of \(s_j\) with the database bit \(X_j\), represented by the supplied encrypted constant.''',
 r'''OR the \(n\) masked results together and return that one ciphertext. Exactly one selector is 1 for a valid address, so all other terms are 0 and the plaintext result is \(X_i\). The client decrypts it. FHE correctness must hold for this entire circuit and the chosen parameters.''',
 r'''Upload is \(\ell+2=O(\log n)\) ciphertexts; download is one. Compactness means evaluation does not make the final ciphertext length grow with the entire evaluated circuit. Query privacy follows from the encryption scheme's security for the joint collection of encrypted bits. It is computational privacy, and the server still evaluates a database-wide circuit—short communication is not sublinear server work.'''
],['fhe-selection'],'4–5',lab('fhe-lookup','See the selection circuit beneath the encryption',
 '<p>For database bits 1,0,1,1,0,0,1,0 and record 3 (address 010), only its equality selector is 1. AND with each database bit and OR the results to obtain 1.</p><div data-fhe-table class="pir-mini-table"><table><thead><tr><th>Address</th><th>Data</th><th>Equal</th><th>Masked</th></tr></thead><tbody><tr><th>000</th><td>1</td><td>0</td><td>0</td></tr><tr><th>001</th><td>0</td><td>0</td><td>0</td></tr><tr><th>010</th><td>1</td><td>1</td><td>1</td></tr><tr><th>011</th><td>1</td><td>0</td><td>0</td></tr><tr><th>100</th><td>0</td><td>0</td><td>0</td></tr><tr><th>101</th><td>0</td><td>0</td><td>0</td></tr><tr><th>110</th><td>1</td><td>0</td><td>0</td></tr><tr><th>111</th><td>0</td><td>0</td><td>0</td></tr></tbody></table></div><p>The visualization exposes plaintext intermediate values for learning. The server in the protocol receives ciphertexts instead.</p>'))

exercise('4c','Track the specified noise through the whole circuit',r'''
<p>Fresh ciphertexts have noise magnitude 2. In this exercise's model, AND multiplies its input noise magnitudes, OR adds them, and NOT leaves noise unchanged. What noise does the construction in 4(b), using the equality circuit from 4(a), produce?</p>''',[
 r'''For one pair of encrypted address bits, each AND in \((a\land b)\lor(\neg a\land\neg b)\) has noise \(2\cdot2=4\). NOT changes nothing. The final OR gives \(4+4=8\). This count uses the specified full equality subcircuit, including encrypted constants.''',
 r'''AND the equality results for all \(\ell\) address positions. Multiplication of their noise magnitudes gives \(8^\ell\). If \(n\) is a power of two, \(\ell=\log_2 n\), so \(8^\ell=(2^3)^\ell=(2^\ell)^3=n^3\).''',
 r'''AND each selector with an encryption of the database bit. That fresh input has noise 2, producing \(2\cdot8^\ell\) for each record. OR the \(n\) masked terms: their magnitudes add, giving \[\varepsilon_{\mathrm{out}}=2n\,8^{\lceil\log_2 n\rceil}.\] For power-of-two \(n\), this simplifies to the sheet's \(2n^4\).''',
 r'''This is a bookkeeping model for this circuit, not a universal noise law for every FHE scheme. Simplifying gates against public constants or using an additional procedure to reduce noise would change the calculation. No decryption threshold is supplied, so the magnitude alone cannot tell us whether a particular cryptosystem's parameters are sufficient.'''
],['noise-model'],'5',lab('noise','Propagate the noise stage by stage',
 '<p>For n = 8, the address has 3 bits. One equality position has noise 8; their AND has 512; masking one record gives 1,024; the final OR gives 8,192.</p><div data-noise-stages class="pir-flow"><span>8 → 512 → 1,024 → 8,192</span></div>'))

assert len(HW)==15

from homework_visuals import LATER_VISUALS
for key,figure in LATER_VISUALS['hw4'].items():
 HW[key]['visual'] += figure
