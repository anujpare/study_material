r"""Undergraduate-level editorial pass for Chapters 3/4; preserve assigned work.
Full replacements teach missing links; retained lessons were reviewed for their
specific inferential task, recorded in the coverage audit.
"""
import re
from teaching_visuals import protocol,path
NEW={'snarks':{},'pir':{}}
def s(key,body):NEW['snarks'][key]=body
def p(key,body):NEW['pir'][key]=body

s('snarg-goal',r'''
<p>Suppose a server applies a hash function a million times and claims that the final output is \(y\). Checking every intermediate hash would repeat essentially the entire computation. We want a proof that is short to transmit and much cheaper to verify, even when producing it requires substantial work.</p>
<p>A <strong>SNARG</strong> is a <strong>succinct non-interactive argument</strong>. “Non-interactive” means that the prover sends one proof string; “argument” means soundness against PPT provers. The lecture’s succinctness convention requires both short proofs and fast verification. For public statement \(x\), witness \(w\), and security parameter \(\lambda\), it writes these as</p>
\[|\pi|=O(\lambda,\operatorname{polylog}(|x|,|w|)),\qquad
T_V=O(\lambda,|x|,\operatorname{polylog}(|w|)).\]
<p>The notes use multi-argument O notation to collect the allowed costs. The essential restrictions are polynomial dependence on logarithmic witness/input sizes for proof length, and only linear dependence on the public-input length for verification, in addition to the security-parameter costs. A merely polynomial-time verifier does not automatically meet that stronger requirement.</p>
<p>A <strong>SNARK</strong> additionally has an argument-of-knowledge guarantee: successful proving permits witness extraction under its definition. Zero knowledge is another separate property. This chapter first builds the succinct verification machinery, then explains which additional guarantees a full system needs.</p>
'''+path('The construction we will build',[
'Encode a witness or computation so a verifier can check a few carefully chosen values.',
'Use commitments to prevent the prover from changing that encoding after seeing the checks.',
'Use Fiat–Shamir to derive verifier challenges and package the required answers into one proof.']))

s('schnorr-recap',r'''
<p>To understand how we remove interaction, recall the Schnorr proof of knowledge of \(x\) with \(h=g^x\). The public group has prime order \(q\), with generator \(g\); all exponents are in \(\mathbb Z_q\).</p>
'''+protocol('snarks-schnorr','The challenge arrives after the first message','Prover','Verifier','Knows x and samples uniform r.','Knows g,h,q.',[
('left',r'\(u=g^r\)','The first message fixes the prover’s random contribution.'),
('right',r'Uniform \(c\in\mathbb Z_q\)','The verifier chooses c independently after receiving u.'),
('left',r'\(z=r+cx\pmod q\)','The verifier accepts exactly when gᶻ = u·hᶜ.')])+r'''
<p>If the prover could choose \(c\) before \(u\), it could sample \(c,z\) and set \(u=g^zh^{-c}\), passing the equation without knowing \(x\). This reverse construction is the honest-verifier simulator. The original timing prevents it from being used as a live cheating strategy.</p>
<p>Fiat–Shamir must replace that timing constraint with a reproducible challenge the prover still cannot freely choose. The next card shows how the random oracle supplies it.</p>
''')

s('two-routes',r'''
<p>Hashing a challenge can remove interaction, but it does not shorten the information that the verifier needs. For succinctness, we first design a proof in an ideal model where the verifier can query a fixed encoded object without receiving all of it. An <strong>interactive oracle proof</strong> (IOP) allows such objects to be supplied in rounds.</p>
<table><thead><tr><th>Oracle interface</th><th>What one query returns</th></tr></thead><tbody><tr><td>PCP</td><td>A bit at a specified position of a fixed encoded proof.</td></tr><tr><td>Linear IOP</td><td>The inner product of a supplied weight vector with the fixed proof vector.</td></tr><tr><td>Polynomial IOP</td><td>The value of a fixed, degree-bounded polynomial at a supplied point.</td></tr></tbody></table>
<p>The prover chooses the object, but cannot invent new answers after learning the query. Soundness in this ideal model can therefore be information-theoretic. Cryptography is used later to enforce the same consistency against an efficient prover.</p>
<p>For a linear query with weights \((1,r,r^2)\) and proof vector \((a_0,a_1,a_2)\), the answer is \(a_0+a_1r+a_2r^2\). Thus polynomial evaluation is a particular linear query to the coefficient vector. This connects the interfaces without identifying their different degree or query restrictions.</p>
'''+path('Two implementations of the same plan',[
'For the PCP route, authenticate queried bits using a Merkle root and paths. HW3 develops this construction.',
'For the polynomial route, authenticate evaluations using polynomial commitments. Algebraic identities then check the computation’s constraints.',
'In either route, derive the challenges only after the relevant commitments are fixed.']))

s('pcp',r'''
<p>A <strong>probabilistically checkable proof</strong> (PCP) encodes a witness into a longer proof string \(\pi\), designed so that a small number of local checks can detect a false claim. The PCP theorem does not say that a few random bits of an ordinary witness are enough.</p>
<p>The version supplied for HW3 has proof length \(M=\operatorname{poly}(n)\), where \(n=|x|\), and a randomized verifier that reads a constant number \(k\) of proof positions. Its guarantees are</p>
\[\begin{aligned}
x\in L&\Rightarrow\exists\pi:\Pr[V^\pi(x)=1]=1,\\
x\notin L&\Rightarrow\forall\pi:\Pr[V^\pi(x)=1]\le1/2.
\end{aligned}\]
<p>The superscript means query access to the fixed string \(\pi\). The probability is over verifier randomness. On a false statement, the bound holds for <em>every</em> fixed proof, including one chosen by an unbounded prover.</p>
<p>HW3 assumes nonadaptive queries: their positions are selected from \(x\) and verifier randomness before the answers are seen. The verifier then applies a specified local predicate to those bits. The lecture highlights constant-query PCPs, including its three-query illustration; the homework construction works with its stated constant \(k\).</p>
<p>The remaining challenge is to prevent a real prover from choosing its answers after seeing those positions. A short vector commitment will replace the ideal fixed-proof interface.</p>
''')

s('pcp-protocol',r'''
<p>The prover first fixes a PCP proof by sending its Merkle root. Only then does the verifier choose the random tests. The protocol must authenticate the answers <em>and</em> check what those answers say about the public claim.</p>
'''+protocol('pcp-protocol','A root fixes the proof before positions are requested','Prover','Verifier','Has the PCP string and its Merkle tree.','Has x and the PCP verification algorithm.',[
('left',r'Merkle root \(c\)','This binds the indexed proof bits before the tests are selected.'),
('right',r'Positions for \(\lambda\) fresh PCP tests','Each test asks for a constant number of bits.'),
('left','Requested bits and their authentication paths','The paths connect each claimed index and bit to c.'),
('local-right','Check every path and every PCP predicate','A correct path authenticates a bit; it does not establish that the bit passes the logical test.')])+r'''
<p>For a false statement, the fixed proof passes each independently sampled PCP test with probability at most \(1/2\). Requiring every test to pass gives \(2^{-\lambda}\), plus the negligible probability of breaking the commitment’s binding guarantee. The result is a computational argument because the commitment is what enforces consistency in the real protocol.</p>
{{LAB}}
''')

s('polynomial-language',r'''
<p>A polynomial oracle promises more than a function that returns field values. It commits to one <em>formal polynomial</em> \(f\in\mathbb F[X]_{\le d}\), with a fixed degree limit. Formal equality means equality of all coefficients; agreement at a few points is only evidence for that equality.</p>
<p>This distinction matters over finite fields. In \(\mathbb F_7\), the nonzero formal polynomial \(X^7-X\) evaluates to zero at all seven field elements. Its degree is large enough that the root bound permits this. We therefore need the degree to be small relative to the field if a random evaluation is to be informative.</p>
<p>The notation \(\mathbb F[X]_{\le d}\) means polynomials whose coefficients lie in \(\mathbb F\) and whose degree is at most \(d\). The zero polynomial has all coefficients zero and is allowed even when the bound is zero. A prover cannot evade the limit by choosing a different high-degree polynomial after learning the evaluation point.</p>
<p>We will use that fixed-degree promise to connect a global identity to one local check. The next card proves the root bound that makes the connection work.</p>
''')

s('polynomial-commitment',r'''
<p>A <strong>polynomial commitment scheme</strong> (PCS) lets a prover bind itself to a polynomial and later authenticate an evaluation without sending all its coefficients. The lecture defines four algorithms:</p>
<table><thead><tr><th>Algorithm</th><th>Its input and output</th></tr></thead><tbody><tr><td>Setup(d,λ) → pp</td><td>Generate public parameters for a degree limit and security parameter.</td></tr><tr><td>Commit(pp,f) → c</td><td>Publish a commitment to f ∈ F[X]≤d.</td></tr><tr><td>Open(pp,f,r) → π</td><td>Produce evidence for the claimed value y = f(r).</td></tr><tr><td>Verify(pp,c,r,y,π)</td><td>Accept or reject that evaluation claim.</td></tr></tbody></table>
<p><strong>Correctness</strong> requires every honestly generated opening to verify:</p>
\[\Pr[\operatorname{Verify}(pp,c,r,f(r),\pi)=1]=1,\]
<p>where \(pp,c,\pi\) are generated by Setup, Commit and Open, for every allowed \(f,r\). The probability includes their random choices.</p>
<p><strong>Evaluation binding</strong> says that every PPT \(A(pp)\) has negligible probability of producing \((c,r,y,\pi,y',\pi')\) with</p>
\[y\ne y',\qquad\operatorname{Verify}(pp,c,r,y,\pi)=
\operatorname{Verify}(pp,c,r,y',\pi')=1.\]
<p>Both accepted claims concern the same commitment and evaluation point. The compiler must additionally justify treating the accepted answers as evaluations of one polynomial within the degree bound. The displayed evaluation-binding game alone is not that whole theorem. Hiding is also a separate property.</p>
''')

s('polynomial-compiler',r'''
<p>We can now replace the ideal polynomial interfaces in ZeroTest with commitments. The algebra remains the same; what changes is how the verifier trusts the evaluation answers.</p>
'''+protocol('polynomial-compiler','Keep the commitment before the random evaluation point','Prover','Verifier','Has f and a proposed quotient q.','Knows the public domain Ω and PCS parameters.',[
('left',r'\(c_f=\operatorname{Commit}(f),\ c_q=\operatorname{Commit}(q)\)','The degree bounds and both polynomials are fixed before r is chosen.'),
('right',r'Uniform \(r\in\mathbb F\)','This selects a random identity test.'),
('left',r'\(f(r),q(r)\) and both opening proofs','The answers must verify against the original commitments.'),
('local-right',r'Check openings and \(f(r)=Z_\Omega(r)q(r)\)','Authentication and the algebraic condition are both required.')])+r'''
<p>If the prover knew \(r\) before fixing \(q\), it could often choose a constant just to satisfy the one displayed equation. The root-bound argument would then be invalid: the false polynomial would depend on the point at which it was tested.</p>
<p>Fiat–Shamir replaces the challenge message by a hash of the statement, public context and preceding commitments. A compiler theorem must account for the PCS guarantees, all challenge rounds and the random-oracle model. A three-message outline alone does not establish Sigma properties or zero knowledge.</p>
''')

s('zero-test',r'''
<p>Suppose the claim is that a degree-at-most-\(d\) polynomial \(f\) is zero at every point of a public set \(\Omega\), with \(|\Omega|=k\le d\). We need to verify many equalities, but the factorization from the previous card expresses all of them as one identity:</p>
\[f(X)=Z_\Omega(X)q(X).\]
<p>The prover supplies a degree-bounded quotient oracle \(q\), fixed before the challenge. The verifier chooses uniform \(r\in\mathbb F\), queries \(f(r)\) and \(q(r)\), computes \(Z_\Omega(r)\), and accepts if \(f(r)=Z_\Omega(r)q(r)\). An honest factorization passes at every point, giving perfect completeness.</p>
<p>For a false claim, no permitted quotient makes the identity hold. Therefore \(h=f-Z_\Omega q\) is nonzero. Under the lecture’s loose bound \(\deg q\le d\), its degree is at most \(d+k\le2d\). The root bound gives soundness error at most \(\min(1,2d/|\mathbb F|)\).</p>
<p>The honest nonzero quotient needs degree only \(d-k\), but the looser oracle limit explains the lecture’s \(2d\) estimate. Verification multiplies rather than divides: it remains defined when \(r\in\Omega\), where \(Z_\Omega(r)=0\). The verifier’s cost of evaluating this public polynomial must also be counted when assessing succinctness.</p>
''')

p('pir-contract',r'''
<p>A PIR protocol separates the requested position from the information the server observes. The client runs a query algorithm on index \(i\), retains its local state, and later uses that state to reconstruct \(X_i\) from the server’s answer. Two-server schemes send one query to each replica.</p>
<p><strong>Correctness</strong> requires reconstruction to return the requested value when the parties follow the protocol, with probability 1 in our basic two-server construction or with the stated negligible failure probability in a cryptographic scheme.</p>
<p><strong>Query privacy</strong> compares any two allowed indices \(i,j\) for the same database and public parameters. If \(\operatorname{View}_b(X,i)\) denotes everything server \(b\) receives and computes, information-theoretic privacy in our scheme gives</p>
\[\operatorname{View}_b(X,i)\equiv\operatorname{View}_b(X,j).
\]
<p>For computational privacy, replace equality of distributions by \(\approx_c\): every PPT distinguisher has negligible output-probability gap between the two views as the security parameter grows. In a two-server scheme this comparison concerns either server’s individual view, not their pooled information.</p>
<p>Communication counts uploaded queries and downloaded answers in bits. We seek a sublinear total, meaning \(T(n)/n\to0\). Privacy does not by itself ensure correct answers from a malicious server, hide that a request occurred, or restrict the client to learning only one database item.</p>
''')

p('query-shares',r'''
<p>Represent the requested index by the one-hot vector \(e_i\), whose only nonzero entry is at position \(i\). The inner product \(X\cdot e_i\) selects \(X_i\). In this protocol the arithmetic is in \(\mathbb F_2\): products are AND and sums are XOR.</p>
<p>Sending \(e_i\) would reveal the request. Instead, choose a uniform random vector \(q_0\in\{0,1\}^n\) and set \(q_1=q_0\oplus e_i\). Give one vector to each server. This is <strong>additive secret sharing</strong> of the selector, since \(q_0\oplus q_1=e_i\).</p>
<p>Why is either share private? For any fixed target \(i\) and any possible value \(v\), exactly one mask \(q_0=v\oplus e_i\) produces \(q_1=v\). Hence</p>
\[\Pr[q_1=v\mid i]=2^{-n},\]
<p>independently of the target. Server 0’s share is uniform by construction, so neither individual distribution reveals the index. Combining the shares does reveal the selector; this is why the servers must not collude.</p>
{{LAB}}
<p>Each request uses a fresh independent mask. Reusing a mask would create relations between queries that the single-request distribution argument does not protect.</p>
''')

p('flat-pir',r'''
<p>Both servers hold the same database \(X\). Each can compute an inner product with its own query share without learning the selector. The client combines their answers to cancel the mask.</p>
'''+protocol('two-server-pir','Each server sees only its own labelled message','Client','Server replicas','Knows i and samples q₀; sets q₁ = q₀ XOR eᵢ.','Both hold X. They keep their views separate.',[
('left',r'\(q_0\) to server 0; \(q_1\) to server 1','The diagram groups the replicas for space; neither receives the other share.'),
('local-right',r'Server \(b\) computes \(a_b=X\cdot q_b\)','The computation is the XOR of the selected database bits.'),
('right',r'\(a_0\) from server 0; \(a_1\) from server 1','Each server returns one bit to the client.'),
('local-left',r'\(a_0\oplus a_1=X\cdot(q_0\oplus q_1)=X_i\)','Linearity lets the client combine the answers exactly as it combines the shares.')])+r'''
<p>The individual query distributions are private, and an honest server’s answer is a function only of its own query and the database. Correctness follows from the displayed cancellation. But communication is \(2n+2\) bits: the two length-\(n\) queries are still expensive.</p>
<p>For records of \(B\) bits, the same selector can be applied at each bit position within the records. The queries stay length \(n\), while the two answers contain \(B\) bits each. This suggests arranging the original bit database into fewer, longer records—the matrix construction next.</p>
''')

p('binary-gates',r'''
<p>The encrypted one-hot selector contains one component per record. We can describe the target much more compactly with a binary address, provided the server can perform a richer computation on that address.</p>
<p>For \(n\) records numbered 1 through \(n\), encode record \(i\) by the binary representation of \(i-1\), using \(\ell=\lceil\log_2 n\rceil\) bits. Thus for eight records the addresses run from 000 to 111. Using \(i\) itself would wrongly require a fourth bit for the last record.</p>
<p>The server will compare the encrypted address with each public record address. An equality circuit outputs a selector bit that is 1 for the matching address and 0 elsewhere. Fully homomorphic encryption lets the server evaluate that Boolean circuit while the address stays encrypted.</p>
<p>The next exercise constructs equality using the specified NOT, AND and OR gates. The gate representation matters because HW4 later assigns a noise-growth rule to each gate; an equivalent simplified circuit need not have the same noise calculation.</p>
''')

p('powers-setup',r'''
<p>HW4 returns to a prime-order cyclic group \(G\), now with order \(p\) and generator \(g\). The letter changes from earlier group examples, but the distinction remains the same: polynomial coefficients and exponents lie in \(\mathbb F_p\), while commitments are group elements.</p>
<p>Setup chooses a hidden nonzero \(\alpha\in\mathbb F_p\) and publishes</p>
\[g,\ g^\alpha,\ g^{\alpha^2},\ldots,g^{\alpha^d}.\]
<p>Each published item is a group element. Seeing \(g^{\alpha^2}\) is not the same as knowing \(\alpha^2\). However, the prover can raise that group element to a coefficient it knows, and can multiply the resulting group elements. Those operations correspond to scalar multiplication and addition of exponents.</p>
<p>Consequently the public powers contain exactly the encoded building blocks needed to form \(g^{f(\alpha)}\) from the coefficients of a degree-at-most-\(d\) polynomial. Parts 3(a–b) ask you to derive this computation and then distinguish the existence of colliding polynomials from the difficulty of finding them.</p>
''')

p('point-quotient',r'''
<p>To open a polynomial commitment, the prover claims \(f(z)=y\). Here \(z\) is an evaluation point; in the earlier coefficient exercise it named the claimed inner product. We need an algebraic condition that relates this public claim to the committed polynomial.</p>
<p>Polynomial division by \(X-z\) gives a constant remainder:</p>
\[f(X)-y=(X-z)q(X)+r_0.\]
<p>Substituting \(X=z\) gives \(r_0=f(z)-y\). Thus the claim is true exactly when the remainder is zero, or equivalently when \(f-y\) is divisible by \(X-z\). This is ZeroTest on the one-point domain \(\{z\}\), whose vanishing polynomial is \(X-z\).</p>
'''+path('How an evaluation becomes an opening proof',[
'The claimed value y determines the polynomial f − y.',
'If the claim is true, division by X − z produces a genuine polynomial quotient q with no remainder.',
'The prover encodes q at the hidden setup point, just as it encoded f.',
'The verifier uses the identity f(α) − y = (α − z)q(α) to relate the two encodings.'])+r'''
<p>The quotient is computed as a polynomial. Nothing requires evaluating a fraction as \(0/0\) at \(X=z\). The next exercise constructs it explicitly.</p>
''')

# Plain prose replacements remove elementary detours and compressed instructions.
EDITS={
 'snarks':{
 'proof-properties':[("An error is <strong>negligible</strong> if it eventually falls below every inverse fixed power of \\(\\lambda\\), such as \\(1/\\lambda^2\\) and \\(1/\\lambda^{100}\\). A small constant does not meet that definition.","The formal PPT and negligible-function definitions from Chapter 1 apply to these computational guarantees.")],
 'interpolation':[("The symbol \\(\\prod\\) means multiply the listed factors, and \\(\\sum\\) means add the listed terms. ","")],
 'schwartz-zippel':[("A multivariable polynomial uses several input symbols. For example, over \\(\\mathbb F_7\\),","The degree controlling a multivariate random check is the <em>total</em> degree. For example, consider this polynomial over \\(\\mathbb F_7\\):")],
 'wire-permutation':[("A <strong>permutation</strong> rearranges positions, using each position exactly once. For every wire, cycle through all trace slots that represent that wire.","The wiring check can be encoded by a permutation of trace positions. For each physical wire, place all slots carrying that wire into one cycle.")],
 },
 'pir':{
 'matrix-layout':[("A matrix is simply a rectangular table; the entry", "The entry")],
 'communication-balance':[("the ceiling symbol means round up to an integer. ","")],
 'product-coefficient':[("When multiplying polynomials, multiply every term of the first by every term of the second, then collect equal powers. A product", "The useful feature of polynomial multiplication here is that coefficient positions combine. A product")],
 'succinctness-review':[("Vertical bars mean the bit length of a string. The notation “poly” allows fixed powers of its arguments.","Here |x| and |w| are the statement and witness lengths, and “poly” permits fixed powers of its arguments.")],
 'field-review':[("A polynomial \\(f(X)=a_0+a_1X+\\cdots+a_dX^d\\) has coefficients \\(a_j\\); its degree is the largest index of a nonzero coefficient. A root is an input \\(r\\) for which \\(f(r)=0\\).","The identities we test are formal polynomial identities, with coefficients in that field. Their degree bounds constrain how often a false identity can pass a random evaluation test.")],
 }}

def revise(deck,cards):
    for card in cards:
        if card['kind']!='theory':continue
        key=card['id'];body=card['body']
        if key in NEW[deck]:
            updated=NEW[deck][key]
            if '{{LAB}}' in updated:
                lab=re.search(r'<figure class="learning (?:snark|pir)-lab".*?</figure>',body,re.S)
                assert lab,key
                updated=updated.replace('{{LAB}}',lab[0])
            body=updated
        for before,after in EDITS.get(deck,{}).get(key,[]):
            assert before in body,(deck,key,before)
            body=body.replace(before,after)
        card['body']=body
    if deck=='pir':
        cards[:]=[c for c in cards if c['id']!='bit-selection']
        for c in cards:
            c['requires']=['pir-contract' if r=='bit-selection' else r for r in c['requires']]
            if c['id']=='query-shares':c['aliases']=['bit-selection']
