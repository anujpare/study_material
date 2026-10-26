r"""Reviewed replacements for Chapters 1/2. No automatic elementary primers.

Every retained original lesson is classified in teaching-audit.json. Removed IDs
are bookmark aliases, not hidden extra cards in the learning sequence.
"""
from teaching_visuals import protocol,path
REVISIONS={'commitment':{},'zero-knowledge':{}}
def c(n,title,body):REVISIONS['commitment'][n]=(title,body)
def z(n,title,body):REVISIONS['zero-knowledge'][n]=(title,body)

c(1,'What this chapter will establish',r'''
<p>A cryptographic claim needs a more precise meaning than “the secret seems safe”. We must say what the attacker receives, what it may do, and what would count as success. The first part of this chapter develops that language; we will then use it to prove security of commitments and pseudorandom functions.</p>
<p>A <strong>commitment</strong> lets a sender fix a message now and reveal it later. Its two requirements pull in different directions: the published value must conceal the message, but must also prevent the sender from changing it. We will see why satisfying only one requirement is easy, and how Pedersen commitments achieve both under the appropriate assumptions.</p>
'''+path('The chapter’s reasoning',[
'First specify efficient attackers and negligible probabilities. These give a precise meaning to computational security.',
'Use that definition to compare two experiments, then formulate hiding and binding for commitments.',
'Prove security first in the random-oracle model and then using prime-order groups and a discrete-logarithm assumption.',
'Apply the same proof techniques to pseudorandom functions and authenticated openings of vectors.']))

c(10,'Security parameter λ and PPT attackers',r'''
<p>A security claim describes a <em>family</em> of systems, indexed by a positive integer \(\lambda\), called the <strong>security parameter</strong>. Increasing \(\lambda\) makes the security-relevant objects larger. For example, a construction may use \(\lambda\) random bits or a group whose elements have length proportional to \(\lambda\). The parameter is public; hiding its value is not part of security.</p>
<p><strong>PPT</strong> stands for <strong>probabilistic polynomial time</strong>. An attacker is a randomized algorithm whose running time is bounded by a fixed polynomial in its input length, and hence in \(\lambda\) for the polynomial-size inputs used here. It can perform any computation within that bound and choose later actions from earlier observations. An oracle or protocol definition must separately state which queries and messages it may make.</p>
<p>The notation \(A(1^\lambda,\ldots)\) gives the attacker the security parameter in unary: \(1^\lambda\) is a string of \(\lambda\) ones. This makes “polynomial in input length” agree with “polynomial in the security parameter”. It does not reveal a key.</p>
<p>Computational security quantifies over <em>every</em> such attacker. We cannot prove it by testing a few attack programs. Instead, we bound an arbitrary attacker’s success, usually by showing that a successful attack would solve a problem assumed hard. An asymptotic guarantee still needs concrete parameter choices before it says anything about a particular implementation.</p>
''')

c(7,'P and NP distinguish deciding from verifying',r'''
<p>Many cryptographic statements have an efficiently checkable witness. For example, the public statement \(x\) may describe a circuit and a required output; a witness \(w\) gives inputs producing that output. A relation \(R(x,w)=1\) means that the proposed witness passes the prescribed check.</p>
\[L=\{x:\exists w,\ |w|\le p(|x|)\text{ and }R(x,w)=1\}.\]
<p>This describes an <strong>NP language</strong> when \(p\) is a polynomial and \(R\) is computable in deterministic polynomial time. A language is a set of yes-instances. The definition says that every yes-instance has a polynomial-size witness that can be checked efficiently. It does not say that we can find that witness efficiently.</p>
<p><strong>P</strong> consists of languages whose membership can itself be decided in deterministic polynomial time. Thus \(\mathrm P\subseteq\mathrm{NP}\). The hypothesis \(\mathrm P=\mathrm{NP}\), used in several homework questions, would make efficient witness checking imply efficient decision. Witness search can then be recovered by repeatedly asking whether a partial witness has a valid completion.</p>
<p>NP stands for <em>nondeterministic polynomial time</em>, not “not polynomial”. Exhibiting an exponential exhaustive search does not prove that an NP problem has no better algorithm.</p>
''')

c(12,'Negligible means smaller than every inverse polynomial',r'''
<p>Computational security permits a small chance of failure. The important requirement is how that chance changes as \(\lambda\) grows. A function \(\mu:\mathbb N\to\mathbb R_{\ge0}\) is <strong>negligible</strong> if</p>
\[\forall c>0\ \exists\lambda_0\ \forall\lambda\ge\lambda_0:
\quad \mu(\lambda)<\lambda^{-c}.\]
<p>Read the quantifiers in order. Someone first chooses any fixed inverse-power threshold, such as \(1/\lambda^{100}\). We must then be able to choose a point \(\lambda_0\) beyond which our function always lies below that threshold. The threshold may be arbitrarily strict, but its exponent stays fixed while \(\lambda\) grows.</p>
<p>This is stronger than tending to zero. For example, \(1/\lambda^5\) tends to zero but never falls below \(1/\lambda^6\) once \(\lambda>1\). In contrast, \(2^{-\lambda}\) eventually falls below every inverse fixed power because exponential growth outpaces every fixed polynomial.</p>
<p>“Non-negligible” is the negation of this definition: for some fixed \(c>0\), the probability is at least \(\lambda^{-c}\) at infinitely many security parameters. It need not be large at every parameter. This distinction matters when a theorem rules out every PPT attacker with a non-negligible success probability.</p>
''')

c(13,'Why polynomially many attempts can remain safe',r'''
<p>Suppose a security proof bounds each attempted guess by \(2^{-\lambda}\), and the attacker makes at most \(Q(\lambda)\le\lambda^k\) attempts. If the bound applies to the relevant events, the union bound gives a total failure probability of at most \(\lambda^k2^{-\lambda}\).</p>
<p>To check negligibility, choose any \(c>0\). The required inequality is</p>
\[\frac{\lambda^k}{2^\lambda}<\frac1{\lambda^c}
\quad\Longleftrightarrow\quad 2^\lambda>\lambda^{k+c}.\]
<p>The right-hand inequality eventually holds for every fixed \(k+c\). Therefore polynomially many opportunities do not destroy the negligible bound. The same reasoning handles birthday bounds such as \(Q(\lambda)^2/2^\lambda\).</p>
<p>This is why security definitions combine polynomial-time attackers with negligible failure. The two conditions are designed to remain useful when an efficient attacker repeats an experiment. The plot lets you compare a candidate function with a chosen threshold; the argument above explains the claim for all sufficiently large parameters.</p>
''')

c(22,'Computational indistinguishability: the exact definition',r'''
<p>Let \(X=\{X_\lambda\}_\lambda\) and \(Y=\{Y_\lambda\}_\lambda\) be families of distributions, called <strong>ensembles</strong>. For a fixed security parameter, a distinguisher \(D\) receives one sample drawn from either \(X_\lambda\) or \(Y_\lambda\), together with \(1^\lambda\), and outputs a bit. Its algorithm is the same in both experiments.</p>
\[\begin{aligned}
p_X(\lambda)&=\Pr[D(1^\lambda,X_\lambda)=1],\\
p_Y(\lambda)&=\Pr[D(1^\lambda,Y_\lambda)=1],\\[4pt]
\operatorname{Adv}_D(\lambda)&=|p_X(\lambda)-p_Y(\lambda)|.
\end{aligned}\]
<p>Each probability includes both the sampling of the input and the distinguisher’s own random choices. The output 1 is simply a decision label. We compare how often the same test uses that label under the two input distributions.</p>
<p>We write \(X\approx_cY\), meaning <strong>computational indistinguishability</strong>, precisely when</p>
\[\begin{gathered}
\forall\text{ PPT }D\quad\exists\text{ negligible }\mu_D\\
\forall\lambda:\operatorname{Adv}_D(\lambda)\le\mu_D(\lambda).
\end{gathered}\]
<p>This says that <em>every</em> efficient randomized test has negligible advantage. The bound may depend on the test. We do not demand identical distributions or identical samples. We demand that no allowed computation extracts a reliably different signal from them. The base definition supplies a sample; additional oracle access must be included explicitly in the experiment.</p>
'''+protocol('indistinguishability','Apply the same test in either experiment','Sampler','Distinguisher','Uses either Xλ or Yλ.','Knows λ and the public experiment, but not which sampler was selected.',[
('left',r"A sample \(s\)",'Only the sampled value is sent; its origin is hidden.'),
('local-right',r"\(D(1^\lambda,s)\in\{0,1\}\)",'Across repeated experiments, compare the probability of output 1 under the two sampling rules.')])+r'''
<p>If those probabilities are 0.7 and 0.3, the advantage in this convention is 0.4. In an equally likely hidden-world guessing game, the corresponding optimally oriented success probability is \(1/2+0.4/2=0.7\). Some texts call the excess over \(1/2\) the advantage; that convention differs by a factor of two.</p>
''')

c(19,'Statistical distance removes the computational restriction',r'''
<p>A distribution can conceal information because the information is absent, or because extracting it is computationally difficult. To express the first possibility, compare the distributions directly. For finite distributions \(P,Q\) on the same set \(S\), their <strong>statistical distance</strong> is</p>
\[\begin{aligned}
\Delta(P,Q)&=\frac12\sum_{s\in S}|P(s)-Q(s)|\\
&=\max_{T\subseteq S}|\Pr[P\in T]-\Pr[Q\in T]|.
\end{aligned}\]
<p>The second expression has a useful interpretation. An unrestricted distinguisher can choose any set \(T\), then answer 1 exactly when the sample lies in it. Statistical distance is the largest advantage any such test can achieve, regardless of the cost of deciding membership in \(T\).</p>
<p>For Bernoulli distributions with probabilities 0.6 and 0.4 of output 1, the distance is 0.2. Choosing \(T=\{1\}\) achieves that gap. We call ensembles <strong>statistically indistinguishable</strong>, written \(X\approx_sY\), when \(\Delta(X_\lambda,Y_\lambda)\) is negligible. Distance zero gives <strong>perfect indistinguishability</strong>.</p>
<p>Statistical indistinguishability implies computational indistinguishability: restricting the available tests cannot increase their maximum advantage. The converse need not hold, because the best statistical test might be computationally infeasible.</p>
''')

c(16,'What a computational security claim does—and does not—promise',r'''
<p>“Computationally secure” means secure against every PPT attacker in the specified experiment, with only negligible failure or distinguishing advantage. The experiment is part of the claim. For message privacy, the attacker tries to distinguish messages; for binding, it tries to produce two inconsistent valid openings.</p>
<p>An unlimited attacker may succeed even when every efficient attacker fails. For example, a deterministic function might turn a uniform λ-bit input into a 2λ-bit output. Its outputs occupy at most 2<sup>λ</sup> of the 2<sup>2λ</sup> possible strings, so an unlimited observer could enumerate that small output set. Computational indistinguishability would require that no PPT observer can efficiently exploit this difference; the size count alone neither proves nor disproves that requirement.</p>
<p>An information-theoretic guarantee removes the computational restriction. A perfect guarantee allows no relevant gap at all; a statistical guarantee permits a negligible one. The observation model still matters: unlimited computation does not grant secret keys or observations that the experiment withholds.</p>
<p>We will state hiding and binding separately for each commitment scheme. One can be perfect while the other relies on a computational assumption. Calling the entire scheme “secure” without naming those two guarantees conceals the distinction the homework asks you to analyse.</p>
''')

c(20,'A commitment must hide a choice and prevent changing it',r'''
<p>Suppose two participants must choose messages before learning each other’s choice. The first sender cannot reveal its message immediately, because the other participant could then adapt its own choice. Sending a hidden representation is useful only if the sender also cannot revise it later.</p>
<p>The lecture’s rock–paper–scissors example makes both attacks concrete. Sending \(H(m)\) fails to hide one of three possible moves: the receiver can hash all three and compare. Encrypting the move can hide it, but encryption alone does not guarantee that a later opening fixes a unique move.</p>
<p>For example, with a one-time pad over \(\mathbb Z_3\), send \(c=m+k\pmod3\) and later reveal \((m,k)\). After seeing the other choice, the sender can instead claim any \(m'\) and reveal \(k'=c-m'\). The receiver still obtains \(m'+k'=c\), so the check cannot detect the change.</p>
<p>A <strong>commitment scheme</strong> addresses both problems: <em>hiding</em> protects the message from the receiver before opening, and <em>binding</em> prevents the sender from producing inconsistent openings. Neither property follows from the other.</p>
''')

c(23,'Commit, open, and state the two security requirements',r'''
<p>For the non-interactive schemes in this chapter, a public algorithm maps a message \(m\in\mathcal M\) and randomizer \(r\in\mathcal R\) to a commitment \(c\in\mathcal C\): \(c=\operatorname{Com}(m;r)\). The semicolon distinguishes the chosen message from the algorithm’s random input. Parameters and spaces may depend on \(\lambda\).</p>
'''+protocol('commitment','The receiver sees the message only at opening','Sender','Receiver','Knows m and samples fresh r.','Knows the public commitment algorithm.',[
('left',r"\(c=\operatorname{Com}(m;r)\)",'The sender publishes c and retains the opening (m,r).'),
('left',r"\((m,r)\), when opening is due",'The receiver now learns the claimed message and randomizer.'),
('local-right',r"Check \(c=\operatorname{Com}(m;r)\)",'Accept the opening only if recomputation agrees with the value sent earlier.')])+r'''
<p><strong>Statistical hiding</strong> requires the distributions \(\operatorname{Com}(m_0;R)\) and \(\operatorname{Com}(m_1;R)\) to be negligibly close for any allowed candidate messages, with \(R\) freshly uniform. Perfect hiding makes them identical. Computational hiding instead requires computational indistinguishability.</p>
<p><strong>Computational binding</strong> requires that every PPT attacker has negligible probability of outputting \((m,r,m',r')\) such that</p>
\[m\ne m'\quad\text{and}\quad
\operatorname{Com}(m;r)=\operatorname{Com}(m';r').\]
<p>The attacker chooses both openings. The success probability includes setup randomness, if present, and the attacker’s coins. Statistical binding removes its computation limit; perfect binding rules out two valid distinct-message openings altogether.</p>
''')

c(24,'Why hiding and binding require different kinds of security',r'''
<p>Perfect hiding says that the receiver sees the same commitment distribution for every message. Fix two messages \(m_0\ne m_1\) and a commitment value \(c\) that occurs with positive probability for \(m_0\). It must also occur for \(m_1\), so both messages have some valid randomizer opening to \(c\).</p>
<p>Those openings exist even if nobody can efficiently find both. An unlimited sender can search the finite randomizer spaces until it obtains them. Thus perfect hiding is incompatible with perfect binding in this nontrivial setting.</p>
<p>The same tension persists with negligible statistical errors: almost all mass of the two hiding distributions overlaps, providing openings to both messages that an unbounded search can find. A construction must therefore restrict computation on at least one side. Pedersen uses perfect hiding and computational binding; later examples show the opposite tradeoff.</p>
<p>This explains why the existence of alternative openings is not by itself a break of <em>computational</em> binding. A break must be an efficient method of finding them with non-negligible probability.</p>
''')

c(27,'A randomizer repairs the small-message hash attack',r'''
<p>To commit to a short message, choose a secret uniform \(\lambda\)-bit randomizer and publish</p>
\[c=H(m\parallel r),\qquad r\overset{\$}{\leftarrow}\{0,1\}^{\lambda}.\]
<p>The symbol \(\parallel\) denotes an unambiguous concatenation. Even if the message has only a few possible values, the receiver cannot test one candidate merely by hashing it: the correct hash input also contains the unknown \(r\). Opening reveals \((m,r)\), allowing the receiver to recompute the hash.</p>
<p>We still need to justify two claims. For hiding, why do the hash output and the attacker’s queries fail to reveal the message? For binding, why can the sender not find two different message–randomizer pairs with the same hash?</p>
<p>Collision resistance addresses the second question but does not settle the first. A function can reveal a message bit while retaining collision resistance in another part of its output. The next card introduces the stronger ideal model under which we can prove both claims.</p>
''')

c(28,'A random oracle is a fixed random function accessed by queries',r'''
<p>In the <strong>random-oracle model</strong>, \(H\) behaves as a uniformly sampled function. Each distinct input receives an independent uniform output; every repetition of an input receives its previous output. Both honest parties and the adversary can query this same function.</p>
<p>A proof need not store the enormous complete table in advance. It can use <strong>lazy sampling</strong>: store only the input–output pairs that have actually been requested. This produces exactly the same distribution for every possible sequence of queries, including adaptively chosen queries.</p>
'''+protocol('random-oracle','New inputs are sampled; repeated inputs are remembered','Attacker','Oracle','Chooses queries using the answers already received.','Starts with an empty table T.',[
('left',r"A query \(u\)",'The input may be any string allowed by the model.'),
('local-right',r"If \(u\notin T\), sample and store \(T[u]\)",'For an existing input, retain the existing value.'),
('right',r"The stored value \(T[u]\)",'This rule preserves both independent fresh answers and consistency on repeats.')])+r'''
<p>A concrete hash such as SHA-3 is a fixed algorithm, not an independently sampled table entry for every possible input. A random-oracle proof therefore establishes security in an ideal model. Replacing the oracle by a real hash is a separate modelling step, not a consequence of collision resistance alone.</p>
''')

c(29,'Hiding follows until the attacker queries the hidden input',r'''
<p>Consider the published value \(c=H(m\parallel r)\) with a uniform \(\lambda\)-bit \(r\). Imagine a comparison experiment in which \(c\) is sampled independently. Until the attacker asks for the particular input \(m\parallel r\), the oracle’s other replies have the same distribution in both experiments.</p>
<p>This is the useful event to analyse: <em>has the attacker queried the hidden input?</em> Before that happens, the answers supply no information about the remaining randomizer candidates. With at most \(Q\) distinct guesses, the probability of finding a uniform hidden randomizer is at most</p>
\[\Pr[\mathrm{hit}]\le\min\{1,Q/2^\lambda\}.\]
<p>The counting uses the whole search, so it remains valid when a new guess depends on earlier failed guesses. We do not assume that its conditional success probability remains \(2^{-\lambda}\) after failures.</p>
<p>The real and comparison experiments can differ only on this event. Each candidate-message experiment is therefore close to the independent one; a triangle inequality gives at most twice this bound when comparing two messages. Since a PPT attacker makes polynomially many queries, either bound is negligible. That is the computational-hiding argument.</p>
''')

c(30,'Practice · Random-oracle guessing bound',r'''
<p>In \(c=H(m\parallel r)\), the randomizer \(r\) is uniform over \(\{0,1\}^{\lambda}\). An attacker makes at most \(Q(\lambda)\) random-oracle queries. Bound the probability that it queries the hidden input \(m\parallel r\), and explain why the bound is negligible when \(Q\) is polynomial.</p>
<details class="solution"><summary>Reveal step-by-step solution</summary><div class="solution-content"><ol>
<li><p>Before the hidden input is queried, the oracle replies do not identify the remaining randomizer. The search therefore has at most \(Q(\lambda)\) opportunities to locate one uniformly hidden value among \(2^\lambda\) candidates. Queries with a wrong message or a repeated randomizer cannot increase that coverage. Thus</p>
\[\Pr[\mathrm{hit}]\le\min\left\{1,\frac{Q(\lambda)}{2^\lambda}\right\}.\]</li>
<li><p>Because \(Q\) is polynomial, there is a fixed \(k\) for which \(Q(\lambda)\le\lambda^k\) for all sufficiently large \(\lambda\). To prove negligibility, choose any constant \(d>0\). We need the bound to become smaller than \(\lambda^{-d}\).</p>
\[\frac{\lambda^k}{2^\lambda}<\lambda^{-d}
\quad\Longleftrightarrow\quad
2^\lambda>\lambda^{k+d}.\]</li>
<li><p>The exponential eventually exceeds this fixed polynomial. Since the argument works for every \(d\), the hit probability is negligible. This is the event used by the hiding proof: until it occurs, the commitment can be replaced by an independent random output without changing what the attacker observes.</p></li>
</ol></div></details>
''')

c(31,'Binding reduces to finding a random-oracle collision',r'''
<p>Two accepted openings with different messages give distinct encoded inputs \(u=m\parallel r\) and \(u'=m'\parallel r'\) with \(H(u)=H(u')\). Thus a binding attack provides a collision in the oracle.</p>
<p>If the oracle output has \(\lambda\) bits, the output at a fresh input is uniform even after all earlier answers are known. Among \(Q\) distinct queried inputs there are \(Q(Q-1)/2\) pairs. Each pair collides with probability \(2^{-\lambda}\), so</p>
\[\Pr[\text{some collision}]\le
\min\left\{1,\frac{Q(Q-1)}{2^{\lambda+1}}\right\}.\]
<p>If the attacker outputs openings it never queried, include their two inputs as additional oracle queries before applying the bound. This accounts for all ways its final check can succeed.</p>
<p>The bound becomes substantial around \(Q=2^{\lambda/2}\), which is the birthday effect. That is faster than guessing one specified hidden input, but still exponential in \(\lambda\). Polynomially many queries give negligible binding failure. The result remains a theorem about the random-oracle model.</p>
''')

c(35,'Division in the exponent uses a finite field',r'''
<p>Cryptographic equations often use exponents in \(\mathbb Z_q\), with arithmetic modulo a prime \(q\). This set is a <strong>field</strong>: every nonzero element has a multiplicative inverse. Consequently we can solve a linear equation by division, provided the divisor is nonzero modulo \(q\).</p>
<p>For example, \(3x=7\) in \(\mathbb Z_{11}\). Since \(3\cdot4=1\pmod{11}\), multiplying by 4 gives \(x=28=6\pmod{11}\). The notation \(7/3\) in this field means \(7\cdot3^{-1}\), not the real number \(7/3\).</p>
<p>Primality matters. Modulo 12, the nonzero value 3 has no inverse, so that division is unavailable. More generally, \(a\) has an inverse modulo \(q\) exactly when \(\gcd(a,q)=1\); a prime modulus guarantees this for every nonzero residue.</p>
<p>Later, two valid openings or proof responses will give an equation \(ax=b\). The crucial proof step will be establishing \(a\ne0\). Only then can we extract the secret as \(x=ba^{-1}\). We introduce the field here because that justification carries the security argument.</p>
''')

c(38,'What “a group of prime order q” actually means',r'''
<p>A <strong>group</strong> \(G\) is a set with an associative operation, an identity element, and an inverse for every element. The operation stays inside \(G\). We write it multiplicatively, but its elements need not be ordinary numbers; in other cryptographic settings they can be points on an elliptic curve.</p>
<p>The <strong>order of the group</strong> is its number of elements. Saying “\(G\) has prime order \(q\)” means exactly \(|G|=q\), where \(q\) is prime. It does not mean that every element is a prime number, or that the operation must reduce modulo \(q\).</p>
<figure class="learning"><figcaption>A complete small example</figcaption><p>Take G = {1, 2, 4}, with multiplication modulo 7. The identity is 1. The products remain in G: 2·2 = 4, 2·4 = 1, and 4·4 = 2 modulo 7. The inverses are 1⁻¹ = 1, 2⁻¹ = 4 and 4⁻¹ = 2.</p><p>There are three elements, so this group has order q = 3. Its elements are represented modulo 7, while its exponents repeat modulo 3.</p></figure>
<p>The group axioms justify cancellation and the usual laws of powers. For example, multiplying \(ab=ac\) by \(a^{-1}\) gives \(b=c\). A cyclic group also lets us describe every element as a power of one generator; that is the next link we need.</p>
''')

c(39,'Generators connect group elements to exponents',r'''
<p>A group is <strong>cyclic</strong> if some element \(g\), called a generator, reaches every element through its powers. In a group of order \(q\), the values \(g^0,\ldots,g^{q-1}\) are distinct and \(g^q=1\). Hence</p>
\[g^a=g^b\quad\Longleftrightarrow\quad a=b\pmod q.\]
<p>For our three-element group, \(g=2\) gives \(2^0=1\), \(2^1=2\), \(2^2=4\), and \(2^3=1\), all modulo 7. This is why group elements and exponents have different arithmetic domains.</p>
<p>Every nonidentity element of a prime-order group is a generator. One reason is Lagrange’s theorem: an element’s order divides the group order. When that order is prime, the only choices are 1 for the identity and \(q\) for every other element. Such a group is therefore cyclic.</p>
<p>Writing \(h=g^x\) tells us that an exponent exists and is unique in \(\mathbb Z_q\). It does <em>not</em> give us an efficient way to recover \(x\) from the representation of \(h\). The gap between existence and efficient recovery is the basis of discrete-logarithm security.</p>
''')

c(48,'The discrete-logarithm assumption is a quantified claim',r'''
<p>Consider a family of efficiently described cyclic groups \(G_\lambda\), of prime order \(q_\lambda\), with generator \(g\). The group parameters are public. Sample \(x\) uniformly from \(\mathbb Z_q\) and publish \(h=g^x\). The <strong>discrete logarithm problem</strong> is to recover \(x\) from those public values.</p>
\[\Pr\!\left[A(1^\lambda,G,q,g,g^x)=x:
 x\overset{\$}{\leftarrow}\mathbb Z_q\right]
\le\mu_A(\lambda).\]
<p>The assumption says that for every PPT algorithm \(A\), some negligible \(\mu_A\) bounds this probability. It includes the random exponent, the attacker’s randomness, and random group setup when that is part of the family. Group operations and exponentiation by a known exponent must be efficient.</p>
<p>For a tiny group, we can enumerate powers and recover the exponent; our examples deliberately allow that so the equations can be checked. The assumption concerns a suitable growing family of cryptographic groups. Prime order alone does not make discrete logarithms hard.</p>
<p>Pedersen’s binding proof will turn any successful double opening into this exact recovery task. Its hiding proof will not use the assumption.</p>
''')

c(43,'A reduction turns a hypothetical attack into a solver',r'''
<p>To prove “discrete-logarithm hardness implies binding”, assume we have an efficient program \(A\) that breaks binding. We then construct a program \(B\) that uses \(A\) to solve a discrete-logarithm challenge. This construction is a <strong>security reduction</strong>.</p>
<p>The reduction has two responsibilities. First, it must supply the attacker with the same distribution of inputs and messages as the attack experiment. Otherwise the attacker’s claimed success probability says nothing about this run. Second, it must transform a successful attack into a correct answer to its own challenge.</p>
'''+path('What must be proved about the reduction',[
'Given a challenge h = gˣ, B constructs the public parameters for A without knowing x.',
'A returns its attack output. B checks the success condition and derives a candidate x from that output.',
'If the simulation is correct and every successful attack yields the right x, B succeeds as often as A.',
'An efficient A with non-negligible success would therefore contradict the discrete-logarithm assumption.']))

c(46,'Pedersen commits with two public generators',r'''
<p>Choose a cyclic group \(G\) of prime order \(q\), with public generators \(g,h\). The sender must not know the discrete logarithm \(x\) satisfying \(h=g^x\). For message \(m\in\mathbb Z_q\), sample uniform \(r\in\mathbb Z_q\) and publish</p>
\[\operatorname{Com}(m;r)=g^m h^r.\]
<p>Opening reveals \((m,r)\), and verification recomputes the product. The message and randomizer are field elements used as exponents; the commitment is a group element. Knowing \(m,r\) makes the forward computation efficient.</p>
<p>The factor \(h^r\) makes the output uniform over the group, concealing the message. At the same time, changing \(m\) while retaining the same commitment requires compensating in the exponent of \(h\). A double opening will reveal the relation between \(g\) and \(h\), which is assumed hard to compute.</p>
<p>The setup condition is therefore substantive. If a party chose \(h=g^x\) and retained \(x\), it could adjust openings. A security theorem must account for how the public generators are generated, rather than merely describe them as “random-looking”.</p>
''')

c(47,'Pedersen’s homomorphism preserves a relation between messages',r'''
<p>Suppose \(c_1=g^{m_1}h^{r_1}\) and \(c_2=g^{m_2}h^{r_2}\). Multiplying the public commitments gives</p>
\[c_1c_2=g^{m_1+m_2}h^{r_1+r_2}
=\operatorname{Com}(m_1+m_2;r_1+r_2).\]
<p>The rearrangement is valid because a cyclic group is commutative. All sums in the exponents are modulo \(q\). The receiver can compute the left side without learning either message; someone who knows both openings can open the result to their sum.</p>
<p>This is a <strong>homomorphic</strong> property: a public operation on commitments corresponds to a specified operation on their hidden messages. Raising a commitment to a known scalar \(a\) similarly produces \(\operatorname{Com}(am;ar)\). Combining these operations supports linear combinations.</p>
<p>The resulting object is still a commitment. The homomorphism does not reveal the sum, and it does not by itself give a way to multiply two unknown messages. Keeping track of the operation supported by the construction prevents that common overextension.</p>
''')

c(49,'Perfect hiding follows from a uniform group mask',r'''
<p>Fix any message \(m\). Because \(h\) is a generator, a uniform \(r\in\mathbb Z_q\) makes \(h^r\) uniform over \(G\). Multiplication by the fixed element \(g^m\) is a bijection of the group, so \(g^m h^r\) is also uniform. Every commitment occurs with probability \(1/q\), independently of the message.</p>
<p>We can express the same fact in exponents to make the unique opening explicit. There is a nonzero \(x\) with \(h=g^x\). For any target \(c=g^t\), the equation \(m+xr=t\pmod q\) has exactly one solution:</p>
\[r=(t-m)x^{-1}\pmod q.\]
<p>The inverse exists because \(x\ne0\) and \(q\) is prime. Each target commitment therefore corresponds to exactly one of the equally likely randomizers, whatever \(m\) is.</p>
<p>This proof may refer to \(x\) and \(t\) without computing them. It proves a statement about distributions, not an algorithm for finding an alternative opening. Thus hiding is perfect even for an unlimited receiver, while the difficulty of finding those exponents can still protect binding against efficient senders.</p>
''')

c(51,'A double Pedersen opening reveals the discrete logarithm',r'''
<p>Suppose an attacker outputs distinct messages \(m,m'\) with valid openings to the same commitment. A reduction receives \(h=g^x\) as its discrete-logarithm challenge and uses those public generators for the attack. Acceptance gives</p>
\[g^m h^r=g^{m'}h^{r'}
\quad\Longrightarrow\quad m+xr=m'+xr'\pmod q.\]
<p>The implication uses that \(g\) has order \(q\). Rearranging yields \(x(r-r')=m'-m\). If \(r=r'\pmod q\), this equation would force \(m=m'\), contradicting a successful binding attack. Thus the nonzero difference has an inverse, and</p>
\[x=(m'-m)(r-r')^{-1}\pmod q.\]
'''+protocol('pedersen-reduction','The attack output solves the reduction’s challenge','Reduction B','Binding attacker A','Receives g,h and must find x with h = gˣ.','Attempts to produce two different openings.',[
('left',r"The public generators \((g,h)\)",'These are the parameters in the binding experiment.'),
('right',r"\((m,r),(m',r')\) with one common commitment",'A successful response has distinct messages and passes both opening checks.'),
('local-left',r"\(x=(m'-m)/(r-r')\) in \(\mathbb Z_q\)",'The proven nonzero denominator makes this computation valid.')])+r'''
<p>If the discrete-logarithm challenge has h = 1, the reduction immediately returns x = 0; otherwise h is a valid generator for the attack. Every successful double opening yields the right logarithm. Apart from efficient checking and field arithmetic, the reduction runs the attacker once. Consequently a non-negligibly successful PPT binding attacker would contradict the discrete-logarithm assumption.</p>
''')

c(56,'A PRF must withstand adaptively chosen oracle queries',r'''
<p>A <strong>pseudorandom function</strong> (PRF) is an efficiently computable keyed function \(F:\mathcal K\times\mathcal X\to\mathcal Y\). One uniform secret key \(K\) is chosen for the whole experiment. The resulting function \(F_K(x)\) is deterministic, so repeated inputs have repeated outputs.</p>
<p>Compare two experiments. In the real experiment, an adversary queries \(F_K\). In the random experiment, it queries one uniformly sampled function \(R:\mathcal X\to\mathcal Y\). The adversary can select inputs adaptively from all previous answers. It does not receive the secret key or a description of the random function.</p>
\[\operatorname{Adv}^{\mathrm{PRF}}_A(\lambda)=\left|
\Pr[A^{F_K}(1^\lambda)=1]-\Pr[A^R(1^\lambda)=1]\right|.\]
<p>The superscript denotes <em>oracle access</em>, not exponentiation. The probabilities include the key or random function and the adversary’s coins. PRF security requires this advantage to be negligible for every PPT oracle adversary. This is stronger than saying that one isolated output appears random: it concerns the entire adaptive conversation.</p>
'''+protocol('prf-game','The same query interface in both experiments','Adversary','Oracle','Chooses inputs using earlier replies.','Uses either one fixed secret key K or one fixed random function R.',[
('left',r"An input \(x_i\)",'A new query may depend on every preceding answer.'),
('right',r"\(F_K(x_i)\) or \(R(x_i)\)",'Both experiments return the same stored value if an input repeats.'),
('local-left','A final decision bit','The difference in output-1 probabilities is the PRF advantage.')]))

c(61,'Homomorphic encryption states correctness after decryption',r'''
<p>Fully homomorphic encryption (FHE) allows a server to evaluate a circuit on encrypted inputs. The client generates a secret key and any public evaluation material, encrypts a message \(m\), and sends its ciphertext \(c\). The server uses \(\operatorname{Eval}\) to obtain an encryption of the circuit’s output without decrypting \(c\).</p>
\[\operatorname{Dec}\bigl(sk,\operatorname{Eval}(evk,f,\operatorname{Enc}(pk,m))\bigr)=f(m).\]
<p>This is the correctness relation, up to the failure probability allowed by the scheme and its parameters. The evaluation key \(evk\) contains public material needed for the supported computation. The ciphertext may be randomized, so correctness does not require equality with the bytes of a fresh encryption of \(f(m)\).</p>
<p>For example, evaluating a circuit that maps \(m\) to \(m+1\) should yield a ciphertext decrypting to \(m+1\). There may be many ciphertexts with that same decryption. The homework asks you to distinguish this semantic guarantee from the stronger, generally unjustified claim that two ciphertext representations are identical.</p>
''')

c(64,'DDH compares a linked exponent with an independent one',r'''
<p>In a cyclic group of prime order \(q\) with generator \(g\), sample independent uniform \(\alpha,\beta,\gamma\in\mathbb Z_q\). The <strong>decisional Diffie–Hellman</strong> (DDH) problem asks us to distinguish these distributions:</p>
\[\text{real: }(g^\alpha,g^\beta,g^{\alpha\beta}),
\qquad\text{random: }(g^\alpha,g^\beta,g^\gamma).\]
<p>The attacker receives the group elements and public parameters, not the displayed exponents. In the real distribution the third exponent is the product of the first two. In the random distribution it is sampled independently. Multiplying the first two group elements only gives \(g^{\alpha+\beta}\), so it does not directly test the required product relation.</p>
\[\left|\Pr[A(g,g^\alpha,g^\beta,g^{\alpha\beta})=1]
-\Pr[A(g,g^\alpha,g^\beta,g^\gamma)=1]\right|
\le\mu_A(\lambda).\]
<p>The DDH assumption requires a negligible bound for every PPT \(A\) in the chosen group family; security parameters and group descriptions are implicit in this abbreviated formula. It is a separate assumption from discrete-logarithm hardness. Some groups permit an efficient product-relation test even though recovering exponents remains hard.</p>
''')

c(63,'A candidate PRF: hash to a group, then exponentiate',r'''
<p>Let \(H:\mathcal X\to G\) be a random oracle into a prime-order group, and choose a uniform secret key \(k\in\mathbb Z_q\). Define</p>
\[F_k(m)=H(m)^k.\]
<p>The same key is used for every input. A repeated input gives the same hash and therefore the same function value. The claim is that the function behaves like a random function to an efficient observer with access to both \(H\) and the function being tested, assuming DDH hardness.</p>
<p>The connection is visible for one input. If \(H(m)=g^\alpha\), then its real PRF output is \(g^{\alpha k}\). This resembles the linked DDH pair. A reduction must exploit that resemblance while still supplying independent random-oracle values at different inputs.</p>
<p>We first study the lecture’s restricted reduction with one PRF query. The homework then removes the loss from guessing its location and finally handles arbitrary polynomially many PRF queries. Those are different simulation tasks, so we will state the restriction at each step.</p>
''')

c(66,'Embed a DDH challenge at one oracle input',r'''
<p>The reduction receives \((g,X,Y,Z)=(g,g^\alpha,g^\beta,Z)\). Its task is to decide whether \(Z=g^{\alpha\beta}\) or an independent uniform group element. It runs a PRF adversary internally and answers its oracle queries without knowing \(\alpha\) or \(\beta\).</p>
<p>For the restricted lecture argument, first suppose the adversary’s sole PRF query will be at a designated input \(m_*\). Set \(H(m_*)=X\). At every other distinct input \(m_i\), sample uniform \(r_i\) and store \(H(m_i)=g^{r_i}\). These values have the required independent uniform distribution, and storing them preserves repeat consistency.</p>
'''+protocol('ddh-reduction','A challenge element becomes the adversary’s oracle answer','Reduction B','PRF adversary A','Holds X,Y,Z but does not know their exponents.','May query H and make one designated PRF query.',[
('right',r"Query \(H(m_*)\)",'The selected input is where B embeds its challenge.'),
('left',r"\(X\)",'X is a uniform group element, as a fresh hash answer must be.'),
('right',r"Query \(F(m_*)\)",'The same input now asks for its function value.'),
('left',r"\(Z\)",'Whether this is real or random follows from the DDH case analysed next.')]))

c(68,'Check both simulated worlds, then account for the guess',r'''
<p>In the real DDH case, \(Z=g^{\alpha\beta}=X^\beta\). Because the reduction set \(H(m_*)=X\), its response is exactly \(F_\beta(m_*)\). The hidden PRF key is \(\beta\), although the reduction never learns it.</p>
<p>In the random DDH case, \(Z\) is an independent uniform group element. Returning it for the one permitted PRF query gives the required random-function response, even when the adversary has already seen the hash answers. Thus a useful distinguishing gap transfers between these two experiments.</p>
<p>The real adversary may choose its PRF input after observing several oracle answers. In the lecture’s restricted setting, that input is among at most \(q_H\) distinct hash queries. The reduction guesses one query position uniformly before the run and embeds \(X\) there. Other hash replies are distributed identically, so the guess is hidden from the adversary.</p>
<p>It succeeds in selecting the later PRF input with probability \(1/q_H\); on other runs it aborts with a fixed unbiased output. If \(A\) has advantage \(\varepsilon\), this gives DDH advantage \(\varepsilon/q_H\) in the stipulated setting. A polynomial loss still preserves non-negligibility. The following homework improves this construction rather than reusing it outside its one-query restriction.</p>
''')

c(79,'A vector commitment binds values to their positions',r'''
<p>A <strong>vector commitment</strong> binds an ordered list \((m_1,\ldots,m_n)\) to one public commitment \(c\). An opening for index \(i\) supplies the claimed value \(m_i\) and a proof \(\pi\). The verification algorithm checks \(\operatorname{Verify}(c,i,m_i,\pi)\).</p>
<p><strong>Position binding</strong> requires that every PPT attacker has negligible probability of finding one \(c\), one valid index \(i\), and two distinct messages with accepted openings:</p>
\[m\ne m',\qquad
\operatorname{Verify}(c,i,m,\pi)=
\operatorname{Verify}(c,i,m',\pi')=1.\]
<p>The index is fixed in both claims. Opening different values at different positions is ordinary functionality, not an attack. This homework requires position binding but does not require hiding.</p>
<p>The next constructions compare two costs: the commitment sent once and the extra proof accompanying one opened entry. Publishing all entry hashes gives a long commitment and an empty extra proof. Hashing the entire vector gives a short commitment but a long opening. A Merkle tree will make both costs small.</p>
''')

c(83,'A Merkle opening reveals the missing inputs along one path',r'''
<p>A Merkle tree commits to a vector using a root hash. Hash each entry to obtain its leaf value, then hash ordered pairs of children until one root remains. Fix the tree shape and distinguish leaf encodings from internal-node encodings so the verifier interprets every hash input unambiguously.</p>
<p>To authenticate one entry, the verifier starts from its leaf hash. It cannot compute the parent without the sibling hash. Once that sibling is supplied, it can compute the parent, which becomes the known child at the next level. Supplying one sibling at each level is therefore enough to reconstruct the root.</p>
'''+path('Opening entry 4 in an eight-leaf tree',[
'Compute the leaf hash of m₄ and combine it with the supplied hash of leaf 3, placing leaf 3 on the left.',
'Combine the resulting hash of leaves 3–4 with the supplied hash of leaves 1–2, again on the left.',
'Combine the resulting hash of leaves 1–4 with the supplied hash of leaves 5–8, now on the right.',
'Accept only if the result equals the root published earlier. The index determines every left/right choice.'])+r'''
<p>A balanced tree has \(O(\log n)\) levels, so the sibling hashes use \(O(\lambda\log n)\) bits. This cost follows from what verification needs at each step; the root does not contain a recoverable copy of every entry.</p>
''')

z(1,'A proof protocol checks a public claim',r'''
<p>A <strong>prover</strong> \(P\) tries to convince a <strong>verifier</strong> \(V\) that a public statement \(x\) is true. We represent the true statements as a language \(L\), so the claim is \(x\in L\). In an NP relation, a witness \(w\) establishes this claim when an efficient check \(R(x,w)=1\) accepts.</p>
<p>For example, \(x\) can describe a Boolean circuit, while \(w\) is an assignment that makes its output 1. Sending \(w\) lets the verifier check the claim directly, but also discloses the assignment. This chapter develops protocols that can establish the claim while keeping the witness private.</p>
<p>In an <strong>interactive proof</strong>, the parties exchange messages before the verifier decides. The verifier may choose a random challenge after seeing a prover message. That timing limits the prover’s ability to manufacture a response tailored to a known check.</p>
'''+protocol('proof-conversation','A challenge depends on a message that has already been fixed','Prover','Verifier','Knows public x and, for our NP protocols, a witness w.','Knows public x and the verification rules.',[
('left','A first proof message','The prover must send this before learning the challenge.'),
('right','A fresh random challenge','The challenge determines which part of the claim will be checked.'),
('left','A response to that challenge','The verifier applies its prescribed test and accepts or rejects.')]))

z(2,'Completeness and soundness quantify over different provers',r'''
<p>Write \(\langle P,V\rangle(x)\) for the verifier’s output after running the interaction on statement \(x\). The lecture’s interactive-proof definition requires</p>
\[\begin{aligned}
\text{Completeness: }&\forall x\in L,
&&\Pr[\langle P,V\rangle(x)=1]\ge2/3,\\
\text{Soundness: }&\forall x\notin L\ \forall P^*,
&&\Pr[\langle P^*,V\rangle(x)=1]\le1/3.
\end{aligned}\]
<p>The first line uses the prescribed honest prover and verifier on a true statement. The second uses an arbitrary cheating prover \(P^*\), but keeps the verifier honest, on a false statement. The probabilities include the parties’ random choices.</p>
<p><strong>Perfect completeness</strong> replaces the lower bound by 1. More generally, the <strong>soundness error</strong> is the maximum permitted acceptance probability on false statements. The constants above are conventional starting points; repetition can reduce error.</p>
<p>A <strong>proof</strong> requires soundness even against an unbounded prover. An <strong>argument</strong> requires it only against PPT provers. This restriction concerns the cheating prover, not the honest verifier, which remains efficient in either case. We will later choose commitment assumptions that match the intended type of soundness.</p>
''')

z(4,'What interaction changes in the complexity picture',r'''
<p>NP describes claims with polynomial-size witnesses that a deterministic polynomial-time verifier can check. Interactive proofs allow a randomized polynomial-time verifier to exchange messages with a potentially unbounded prover. The class of languages admitting such protocols is called <strong>IP</strong>.</p>
<p>The lecture states the theorem \(\mathrm{IP}=\mathrm{PSPACE}\). Here <strong>PSPACE</strong> means decidability using polynomial working space; the running time need not be polynomial. Thus the theorem says that interaction and verifier randomness permit efficient verification of claims far beyond the ordinary NP-witness format, subject to the usual unresolved relationships between complexity classes.</p>
<p>We will also use <strong>BPP</strong>, bounded-error probabilistic polynomial time. A BPP algorithm decides membership using randomness and has error at most \(1/3\) on every input. It needs no prover. This class matters when we ask whether a proposed simulator would let a verifier decide the claim by itself.</p>
<p>These are statements about what a model can express. Our concrete goal is narrower: build understandable protocols for NP relations with completeness, soundness or knowledge, and a separate privacy guarantee.</p>
''')

z(7,'Zero knowledge protects the witness, not just the messages',r'''
<p>A protocol can be complete and sound while exposing its witness: the prover can simply send that witness for checking. <strong>Zero knowledge</strong> asks for an additional property. Whatever an allowed verifier learns from the interaction should already be reproducible from the public statement and its prior information, without the witness.</p>
<p>For a private transaction, the public claim might assert that hidden amounts satisfy balance and range constraints. The verifier should be convinced that those constraints hold without learning the amounts. For an exploit proof, the claim can establish that a program has a particular failure without disclosing the secret input that triggers it.</p>
<p>The claim itself may reveal information. If a public statement has only one possible witness, its truth can already determine that witness mathematically. Zero knowledge does not erase such consequences; it limits the additional information supplied by the conversation.</p>
<p>To make “no additional information” precise, we compare a real verifier view with the output of an algorithm that does not receive the witness. That algorithm is the simulator.</p>
''')

z(9,'A simulator reproduces the verifier’s complete view',r'''
<p>A <strong>transcript</strong> records the exchanged messages. A verifier’s <strong>view</strong> also contains its random coins, public input and any starting information relevant to its computation. Privacy must account for this whole view, because correlations between these values can reveal information even when individual messages appear harmless.</p>
<p>A <strong>simulator</strong> receives the public statement but no witness. Its output should have the same distribution as a real view, or be indistinguishable under the security notion being claimed. It does not need to reproduce a particular run word for word.</p>
'''+protocol('simulation-comparison','Compare two ways of producing the same type of observation','Real experiment','Simulation','Runs an honest prover with witness w against V*.','Receives x and the verifier’s prior information, but no w.',[
('local-left','Record the complete verifier view','The transcript comes from an actual interaction.'),
('local-right','Generate a candidate verifier view','The simulator uses only the capabilities granted in the proof model.')])+r'''
<p>An observer is then given one of those views. If every efficient observer has negligible distinguishing advantage, the interaction cannot give that observer a useful extra test that depends on receiving the real witness-based conversation. The next card states this guarantee with its quantifiers.</p>
''')

z(10,'The zero-knowledge definition: one simulator for each verifier',r'''
<p>Write \(\operatorname{Real}_{V^*}(x,w,z)\) for the complete view of verifier \(V^*\) when it interacts with the honest prover \(P(x,w)\). The verifier receives the public statement \(x\) and auxiliary information \(z\); the prover also receives witness \(w\). The view includes the verifier’s input, random coins and received messages.</p>
<p>For every PPT verifier \(V^*\), there must exist an efficient simulator \(S\) such that, for all valid statement–witness pairs \((x,w)\) and allowed auxiliary information \(z\),</p>
\[\operatorname{Real}_{V^*}(x,w,z)
\ \approx_c\ S(1^\lambda,x,z).\]
<p>The notation suppresses \(1^\lambda\) in the real interaction. We compare the resulting ensembles as \(\lambda\) grows, with polynomially bounded inputs. The subscript \(c\) means the exact computational-indistinguishability definition from Chapter 1: every PPT test has negligible difference in its output-1 probabilities.</p>
<p>The order is <strong>for every verifier, there exists a simulator, for every valid input</strong>. The simulator can be designed for that verifier, but it must work across inputs without being handed their witnesses. In the lecture’s black-box formulation, \(S^{V^*}\) indicates that the simulator can run the verifier as a subroutine, with the specified ability to reset its state.</p>
<p>Replacing \(\approx_c\) by statistical closeness gives statistical ZK; equality of the distributions gives perfect ZK. A theorem may permit expected polynomial-time simulation, which allows random retrying with a polynomial expected cost. That runtime condition must still be proved.</p>
''')

z(11,'Which participant must follow the protocol?',r'''
<p>The three guarantees protect different parties. Reading them correctly prevents mistakes such as expecting a malicious verifier to accept simply because completeness is perfect.</p>
<table><thead><tr><th>Guarantee</th><th>Honesty condition</th></tr></thead><tbody><tr><td>Completeness</td><td>The prover and verifier both follow the protocol on a true statement.</td></tr><tr><td>Soundness</td><td>The verifier follows its checking rule; the prover may cheat.</td></tr><tr><td>Zero knowledge</td><td>The prover follows its privacy-preserving algorithm; the verifier may use any strategy allowed by the definition.</td></tr></tbody></table>
<p>A malicious verifier can always ignore every message and reject. That does not contradict completeness. A malicious prover can deliberately send its witness in the clear. That does not contradict a privacy guarantee about the prescribed honest prover.</p>
<p>These are consequences of the quantifiers, not exceptions added to rescue a protocol. In each homework statement, first identify whose behaviour has changed, then ask whether the relevant definition covers it.</p>
''')

z(19,'Hamiltonian cycles: the statement and its witness',r'''
<p>A <strong>Hamiltonian cycle</strong> in a graph visits every vertex exactly once and then returns to its starting vertex, using graph edges throughout. The public statement is a graph \(G\); the secret witness is an ordered cycle through all its vertices. The verifier can check a supplied cycle efficiently, but finding one in an arbitrary graph can be hard.</p>
<figure class="learning graph-example"><figcaption>A cycle must include every vertex</figcaption><svg viewBox="0 0 280 170" role="img" aria-label="Vertices 1, 2, 3 and 4 form the cycle 1 to 2 to 3 to 4 to 1. A dashed edge from 1 to 3 is an extra graph edge, not part of this cycle."><path d="M55 35H225V130H55Z" fill="none" stroke="#487a5c" stroke-width="4"/><path d="M55 35L225 130" stroke="#89938b" stroke-dasharray="6 5"/><g fill="#f7faf5" stroke="#487a5c" stroke-width="2"><circle cx="55" cy="35" r="19"/><circle cx="225" cy="35" r="19"/><circle cx="225" cy="130" r="19"/><circle cx="55" cy="130" r="19"/></g><g text-anchor="middle" fill="#243c2b"><text x="55" y="41">1</text><text x="225" y="41">2</text><text x="225" y="136">3</text><text x="55" y="136">4</text></g></svg><p>The green edges describe 1 → 2 → 3 → 4 → 1. Extra graph edges are allowed; the witness selects one cycle.</p></figure>
<p>The Hamiltonicity problem is NP-complete: it is in NP, and every NP problem can be converted to it by a polynomial-time reduction. This is why the lecture uses it to illustrate a general route to zero-knowledge proofs for NP. We need its definition and verification rule here, rather than a derivation of NP-completeness.</p>
<p>The challenge is to convince the verifier that a cycle exists without revealing which cycle it is. The protocol will hide a renamed copy of the graph, then allow only one of two checks on that copy.</p>
''')

z(20,'Relabel the graph, then commit before the challenge',r'''
<p>A permutation \(\pi\) assigns a distinct new label to each vertex. Applying it to both endpoints of every edge produces the relabelled graph \(G'=\pi(G)\). The two graphs are <strong>isomorphic</strong>: the adjacency structure is unchanged, even though the vertex names differ. A cycle in \(G\) becomes a cycle in \(G'\) under the same relabelling.</p>
<p>The prover samples a fresh random \(\pi\) and commits separately to the adjacency entries of \(G'\). An entry records whether a particular pair is connected. Fresh randomness is used for each commitment. The first message contains the commitments, not the adjacency matrix or the permutation.</p>
<p>Hiding conceals which relabelling and graph entries were chosen. Binding prevents changing those entries after the verifier announces its check. The lecture uses perfectly binding, computationally hiding commitments: perfect binding supports soundness even against an unbounded prover, while computational hiding supports privacy against efficient verifiers.</p>
<p>One challenge will reveal the relabelling and the entire committed graph. The other will reveal only a Hamiltonian cycle in the renamed graph. Neither check by itself discloses a cycle in the original labelling.</p>
''')

z(21,'Two challenges test two parts of the same claim',r'''
<p>The prover has already committed to \(G'=\pi(G)\). The verifier now samples a uniform challenge bit \(b\). Its choice determines which opening the prover must provide.</p>
'''+protocol('hamiltonian','The graph protocol’s message exchange','Prover','Verifier','Knows a cycle C in G and chooses a fresh relabelling π.','Knows only the public graph G.',[
('left',r"Commitments to the adjacency entries of \(G'=\pi(G)\)",'These entries are fixed before the challenge.'),
('right',r"\(b\overset{\$}{\leftarrow}\{0,1\}\)",'A fresh fair challenge selects one check.'),
('left',r"If \(b=0\): \(\pi\) and all graph openings",'The verifier checks every commitment and verifies that the revealed graph is π(G).'),
('left',r"If \(b=1\): the renamed cycle and its edge openings",'The verifier checks a cycle through every vertex and verifies that all its edge commitments open to 1.')])+r'''
<p>The last two rows are alternatives, not two messages sent in one run. In the cycle branch, unopened adjacency entries and the relabelling stay hidden. Revealing both branches for the same first message would allow the verifier to map the cycle back into the public graph.</p>
''')

z(22,'Binding makes the two checks enforce soundness',r'''
<p>For a true graph, the honest prover can answer either challenge: relabelling preserves its cycle. Thus the protocol has perfect completeness.</p>
<p>Now suppose \(G\) has no Hamiltonian cycle. Perfect binding fixes the graph entries before the challenge. If the first message can be opened as \(\pi(G)\), that graph has no Hamiltonian cycle, so the cycle challenge cannot pass. If it can be opened to show a Hamiltonian cycle, it cannot also be a relabelling of this false public graph.</p>
<p>In other words, two accepting answers to the same fixed commitments would contradict the false statement. At most one of the two challenges can be answered successfully. A uniform challenge therefore gives</p>
\[\Pr[\text{accept}\mid G\text{ has no Hamiltonian cycle}]\le\frac12.\]
<p>The randomness must arrive after the commitments. If the prover knew which branch would be checked first, it could prepare an unrelated cycle for branch 1 or an arbitrary relabelling of \(G\) for branch 0. The protocol is secure because it fixes one object before choosing between these tests.</p>
''')

z(23,'Simulate the branch that will actually be revealed',r'''
<p>A simulator knows the public graph but no Hamiltonian cycle in it. It can nevertheless prepare to answer either <em>one</em> challenge. To answer 0, it commits to a random relabelling of \(G\), whose permutation it knows. To answer 1, it commits to a complete graph and chooses a uniformly random cycle through its vertices; all edges of that cycle exist.</p>
<p>The simulator chooses which branch to prepare by a fair guess \(\hat b\), sends the commitments to the verifier program, and observes the actual challenge. If the challenge matches, it reveals the prepared opening. Otherwise it restores the verifier’s saved state and tries again with fresh commitments.</p>
<p>In branch 0, the revealed relabelling has the genuine distribution. In branch 1, random relabelling makes an honest prover’s cycle uniformly labelled, matching the simulator’s chosen cycle. Both open only edges with value 1. The remaining committed entries may differ, but their computational hiding prevents an efficient verifier from distinguishing that difference.</p>
<p>This is a distributional argument, not merely a method for generating a transcript that passes. We must also show that retries remain efficient, which is the next step.</p>
''')

z(24,'Rewinding is a simulator capability with a runtime cost',r'''
<p>The simulator runs the verifier as a program. It can save the verifier’s state before the first message and restore that same state when an attempt fails. This is <strong>rewinding</strong>; an ordinary participant in a live protocol is not granted that capability.</p>
'''+protocol('graph-simulator','A failed guess returns to the saved verifier state','Simulator','Verifier program','Has G but no cycle witness; saves the verifier’s starting state.','May choose its challenge using the received commitments.',[
('left','Commitments prepared for a guessed branch b̂','The simulator knows one valid kind of opening for this attempt.'),
('right','The verifier’s actual challenge b','The simulator compares the challenge with its guess.'),
('local-left','If b ≠ b̂, restore the saved state and try again','Fresh commitment randomness prevents simply repeating the same failed attempt.'),
('left','If b = b̂, reveal the prepared opening','The simulator outputs the resulting verifier view.')])+r'''
<p>Against an honest verifier, the guess succeeds with probability exactly \(1/2\), giving two attempts on average. For an efficient malicious verifier, computational hiding makes the two preparation methods indistinguishable, so it cannot correlate its challenge with the hidden guess by a non-negligible amount. The standard simulation analysis therefore keeps the retry cost expected polynomial.</p>
<p>The resulting guarantee is computational ZK, with perfect completeness and soundness error at most \(1/2\), under the stated commitment assumptions. Running a simulator until it eventually succeeds would not be enough without this runtime argument.</p>
''')

z(26,'A true statement does not necessarily show knowledge',r'''
<p>Soundness prevents convincing the verifier of a false statement. It says much less when the public statement is automatically true. For example, if \(g\) generates \(G\), then every \(h\in G\) equals \(g^x\) for some \(x\). The existence claim is true whether or not the prover knows that exponent.</p>
<p>Authentication may require more: evidence that the prover actually possesses \(x\). A <strong>proof of knowledge</strong> formalizes this through an <strong>extractor</strong>, an algorithm that can recover a valid witness from a sufficiently successful prover using specified access to that prover.</p>
<p>This does not mean the normal verifier learns the witness. A normal execution supplies one conversation; an extractor may run, inspect oracle interactions, or rewind a prover according to the security definition. Those additional capabilities are exactly what can make extraction possible while preserving zero knowledge in ordinary runs.</p>
<p>We next state the success requirement, then see how two different challenge answers to the same first message can reveal a witness.</p>
''')

z(28,'Knowledge error is the part of success that need not yield a witness',r'''
<p>Let \(\varepsilon\) be the probability that an honest verifier accepts a possibly cheating prover \(P^*\) on public input \(x\). Let \(R(x,w)=1\) mean that \(w\) is a valid witness. The lecture expresses its extraction guarantee in the form</p>
\[\Pr[R(x,E^{P^*}(x))=1]\ \ge\
\Pr[\langle P^*,V\rangle(x)=1]-\kappa.\]
<p>The algorithm \(E\) is the extractor, and the superscript records its access to the prover. The quantity \(\kappa\) is the <strong>knowledge error</strong>: acceptance up to this threshold may come from guessing a challenge, without providing extractable knowledge. A meaningful success surplus must yield a valid witness under the theorem’s extraction and runtime conditions.</p>
<p>This is the lecture’s stated probability convention. More general knowledge definitions may formulate runtime in terms of the inverse surplus \(1/(\varepsilon-\kappa)\); those conditions cannot be dropped when applying an extraction theorem.</p>
<p>For a false statement, no valid witness exists. The left side is then zero, so acceptance is at most \(\kappa\). This is the direct reason a knowledge guarantee implies a corresponding soundness guarantee. For a true statement, it makes the additional claim that sufficiently successful proving permits witness recovery.</p>
''')

z(29,'Two graph openings let an extractor recover the cycle',r'''
<p>Suppose a prover can answer both challenges after one fixed first message. The extractor runs it until the commitments are sent and saves that state. It then obtains an accepting opening for each challenge from that same state.</p>
'''+protocol('graph-extraction','The two answers refer to the same committed graph','Extractor','Prover program','Retains the public graph G and both replies.','Has already sent one fixed set of commitments.',[
('left','Challenge b = 0','The extractor first asks for the relabelling check.'),
('right','Permutation π and all graph openings','Acceptance identifies the committed graph as π(G).'),
('local-left','Restore the prover state after its first message','The commitments remain fixed; the next challenge changes.'),
('left','Challenge b = 1','The extractor asks for the other check.'),
('right','A cycle C′ and its edge openings','Binding makes these edges belong to the same graph π(G).'),
('local-left','Return π⁻¹(C′)','Applying the inverse relabelling produces a Hamiltonian cycle in G.')])+r'''
<p>The two successful responses are the hypothesis of this extraction step. A full knowledge theorem also analyses how often an extractor can obtain them from a prover with a given success probability. The algebraic or combinatorial extraction rule alone does not supply that probability analysis.</p>
''')

z(31,'A Sigma protocol has three messages and three properties',r'''
<p>A <strong>Sigma protocol</strong> for relation \(R\) has a public statement \(x\), a prover witness \(w\), and the following message pattern. The first message is often called a commitment, but it need not be an instance of a commitment scheme.</p>
'''+protocol('sigma','The Sigma message pattern','Prover','Verifier','Has x,w with R(x,w) = 1.','Has x and challenge space C.',[
('left',r"First message \(u\)",'The prover retains the randomness used to construct u.'),
('right',r"Uniform challenge \(c\in\mathcal C\)",'The challenge is sampled after u is received.'),
('left',r"Response \(z\)",'The verifier checks the deterministic predicate V(x,u,c,z).')])+r'''
<p>Three messages are not sufficient to establish a Sigma protocol. The definition also requires <strong>perfect completeness</strong>, <strong>special soundness</strong>, and <strong>honest-verifier zero knowledge</strong>. These describe honest acceptance, witness extraction from two responses, and privacy for the prescribed challenge distribution, respectively.</p>
''')

z(32,'Special soundness extracts from a pair of transcripts',r'''
<p>Suppose \((u,c,z)\) and \((u,c',z')\) are both accepted for statement \(x\), with \(c\ne c'\). <strong>Special soundness</strong> requires an efficient algorithm \(\operatorname{Ext}\) such that</p>
\[R\bigl(x,\operatorname{Ext}(x,u,c,z,c',z')\bigr)=1.\]
<p>The first message must be identical. It ties the two responses to the same previously fixed prover state. In Schnorr, this will make the same unknown random exponent occur in both equations, so subtracting them removes it. If the first messages differed, that cancellation would be unjustified.</p>
<p>This property takes the two accepted transcripts as inputs. A separate rewinding analysis explains how an extractor obtains such transcripts from an interacting prover. The distinction prevents us from concluding that any one accepted proof immediately reveals a witness.</p>
''')

z(33,'Honest-verifier zero knowledge fixes the challenge distribution',r'''
<p><strong>Honest-verifier zero knowledge</strong> (HVZK) requires an efficient simulator for the view produced when the verifier follows the protocol, including its prescribed challenge sampling. For a Sigma protocol, this is commonly expressed as</p>
\[(u,c,z)_{\mathrm{real}}\ \approx_c\ S(1^\lambda,x),\]
<p>for every valid statement–witness pair, where the real challenge is uniform in \(\mathcal C\). Perfect HVZK uses equality of distributions instead. A simulator may generate the values in a different order; only the finished view’s distribution has to match.</p>
<p>This requirement does not cover a malicious verifier that computes its challenge from the first message in an arbitrary way. In particular, a simulator that samples a uniform challenge itself may fail to reproduce that malicious strategy.</p>
<p>When composing proofs in parallel, independent honest challenges make independent single-copy simulations useful. A malicious verifier can correlate all its challenges with all the first messages, which requires a stronger argument. The homework asks you to identify exactly where that difference matters.</p>
''')

z(34,'Special soundness bounds the number of successful challenges',r'''
<p>Fix a false statement \(x\notin L\) and one first message \(u\). If two distinct challenges could both receive accepted responses, special soundness would produce a witness for \(x\). That is impossible for a false statement.</p>
<p>Therefore at most one challenge can be answered successfully for this fixed \(u\). Since the honest verifier chooses uniformly after receiving \(u\),</p>
\[\Pr[\text{accept a false statement}]\le1/|\mathcal C|.\]
<p>The bound holds for every first message, so it also holds when the cheating prover chooses its first message randomly. It does not assume that the prover follows the honest strategy or knows how to answer all challenges.</p>
<p>This proof explains why the size of the challenge space matters. A binary challenge gives at most \(1/2\) soundness error; a large challenge space can make the bound negligible. The next practice question asks you to apply this reasoning directly.</p>
''')

z(38,'Repetition changes both soundness and the conversation',r'''
<p>To reduce soundness error, repeat a protocol with fresh verifier challenges and accept only if every copy passes. For sequential repetition of the graph protocol, even after conditioning on the entire preceding history, the next false-claim success probability is at most \(1/2\). Multiplying these conditional bounds gives \(2^{-k}\) for \(k\) rounds.</p>
<table><thead><tr><th>Sequential</th><th>Parallel</th></tr></thead><tbody><tr><td>Finish u₁,c₁,z₁ before starting u₂,c₂,z₂.</td><td>Send all first messages, then all challenges, then all responses.</td></tr><tr><td>The simulator can finish one conversation before carrying its resulting verifier state into the next.</td><td>A malicious verifier can choose the entire challenge vector from all first messages at once.</td></tr></tbody></table>
<p>For parallel Sigma copies on a false statement, special soundness leaves at most one acceptable challenge per fixed coordinate, hence at most one acceptable whole vector out of \(2^k\). This is a soundness argument about fixed messages and verifier randomness, not an assumption that a cheating prover behaves independently.</p>
<p>The privacy question is separate. A simulator that guesses one binary challenge succeeds about half the time; guessing a whole \(k\)-bit vector can require exponentially many retries. The following exercises compare sequential ZK, parallel ZK, and parallel HVZK using that difference.</p>
''')

z(43,'Schnorr: the response links a random exponent to the secret',r'''
<p>The public parameters are a prime-order group \(G\), its order \(q\), a generator \(g\), and \(h=g^x\). The prover knows the exponent \(x\in\mathbb Z_q\). Schnorr proves knowledge of that exponent using a fresh random \(r\) in each run.</p>
'''+protocol('schnorr','Follow the actual Schnorr messages','Prover','Verifier','Knows x; samples uniform r in Zq.','Knows g,h,q but not x or r.',[
('left',r"\(u=g^r\)",'The prover fixes its random contribution before the challenge.'),
('right',r"\(c\overset{\$}{\leftarrow}\mathbb Z_q\)",'The challenge decides how x will enter the response.'),
('left',r"\(z=r+cx\pmod q\)",'The response is an exponent in Zq, not a group element.'),
('local-right',r"Accept if \(g^z=u h^c\)",'The group equation checks the response without directly recovering x.')])+r'''
<p>The response contains the secret only through the challenge-weighted term \(cx\), combined with the unrevealed random \(r\). The next exercises establish the three properties separately: the honest equation always holds, an honest-verifier view can be simulated without \(x\), and two accepted responses with the same \(u\) and different challenges determine \(x\).</p>
''')

z(48,'Why plain-model non-interactive ZK is severely limited',r'''
<p>A <strong>non-interactive zero-knowledge proof</strong> (NIZK) consists of one prover message checked against the public statement. In the <strong>plain model</strong>, there is no specially generated reference string and no ideal oracle. Under the usual efficient-simulation, completeness and soundness conditions, such a proof would put its language in BPP.</p>
<p>To see the connection, consider the decision procedure “simulate a proof for \(x\), then verify it”. If \(x\) is true, zero knowledge makes the simulated proof behave like an honest accepted proof. If \(x\) is false, soundness prevents an efficiently generated proof from being accepted often. With the theorem’s runtime and error conditions, this yields an efficient randomized decider. Expected-time simulation needs the appropriate truncation and amplification argument.</p>
<p>This is an obstacle for hard languages, not a ban on all NIZKs. In a <strong>common reference string</strong> (CRS) model, setup publishes a string before proofs begin, and the simulator may generate a suitable simulated setup with secret information. In the random-oracle model, it may have carefully specified programming capabilities.</p>
<p>Those extra simulator capabilities are not granted to real cheating provers. “Standard model” means no random oracle; it may still include a CRS. Keeping these model distinctions explicit is essential for the conceptual homework questions.</p>
''')

z(49,'Fiat–Shamir replaces the challenge message with a hash',r'''
<p>For a suitable Sigma protocol, first generate the initial message \(u\) normally. Instead of waiting for a verifier challenge, compute \(c=H(x,u)\), produce the corresponding response \(z\), and send \(\pi=(u,z)\). The notation suppresses fixed public parameters and a protocol identifier, which must also be bound into the hash context.</p>
'''+protocol('fiat-shamir','The verifier reconstructs the missing middle message','Prover','Verifier','Knows x,w and the randomness used to produce u.','Knows x and the public hash context.',[
('local-left',r"\(c=H(x,u)\); compute response \(z\)",'The challenge is determined after the first message is fixed.'),
('left',r"Proof \(\pi=(u,z)\)",'No verifier challenge is sent during this proof.'),
('local-right',r"Recompute \(c=H(x,u)\), then check \(V(x,u,c,z)\)",'Both parties must hash the same complete context.')])+r'''
<p>Honest completeness follows from the original protocol’s ability to answer any allowed challenge. Soundness needs more work: the prover can try several first messages and keep one whose hash is favourable. The challenge space and repetition must make that search ineffective for polynomially many attempts.</p>
<p>The random-oracle model treats each fresh hash answer as unpredictable. A real concrete hash is an implementation choice; its replacement of that ideal interface does not automatically turn the ideal-model proof into a standard-model theorem.</p>
''')

z(51,'Simulation and extraction use different oracle capabilities',r'''
<p>For Fiat–Shamir simulation, the proof algorithm can first generate a valid-looking Sigma transcript \((u,c,z)\) without a witness, then arrange for the ideal oracle answer at \((x,u)\) to be \(c\). This is <strong>programming</strong> the random oracle. A complete theorem must handle prior queries and show that the programmed experiment remains indistinguishable.</p>
<p>An ordinary prover cannot set a published hash function’s output. That difference explains why the existence of a simulator does not itself give a public forgery algorithm.</p>
'''+protocol('fiat-shamir-extraction','Extraction forks at the same oracle query','Extractor','Prover program','Controls oracle replies in the extraction experiment.','Has reached the query H(x,u).',[
('left',r"Oracle answer \(c\)",'Continue this execution and retain an accepted response z.'),
('local-left','Restore the state at the same query','This keeps the public statement and first message fixed.'),
('left',r"A different oracle answer \(c'\)",'Continue again, seeking an accepted response z′.'),
('local-left',r"Apply special soundness to \((u,c,z),(u,c',z')\)",'If both responses accept, their common first message permits witness extraction.')])+r'''
<p>The diagram explains the extraction mechanism, not the probability of obtaining two successful branches. A Fiat–Shamir theorem must supply that analysis and its runtime, query and challenge-size conditions. In particular, an unamplified one-bit challenge is too easy to search over.</p>
''')

z(55,'Prove a circuit by connecting its committed wire values',r'''
<p>HW2 supplies Sigma protocols for XOR and AND relations between three committed bits: two inputs and one output. It also supplies a perfectly binding, computationally hiding commitment scheme. The task is to assemble these components into a proof that a circuit has an input making its final output 1.</p>
<p>The prover evaluates a satisfying assignment and publishes one commitment \(c_w=\operatorname{Com}(m_w;r_w)\) for each wire \(w\). The same commitment must be used wherever that wire occurs. Binding then prevents two adjacent gate proofs from silently using different values for their shared wire.</p>
'''+path('Why the shared wire matters',[
'For t = a XOR b, the first gate proof refers to commitments cₐ, cᵦ and cₜ.',
'For out = t AND a, the second gate proof refers to that same cₜ, together with cₐ and cₒᵤₜ.',
'After verifying both gate relations, the verifier also checks an opening of cₒᵤₜ to 1.'])+r'''
<p>The local relations and shared commitments together establish a consistent circuit evaluation. Checking only the final output would not establish the gates; checking isolated gates with unrelated wire commitments would not establish one computation. The next exercise specifies the full message exchange.</p>
''')

z(60,'A hybrid proof changes one justified component at a time',r'''
<p>When a verifier sees many commitments and proof transcripts, a single indistinguishability claim can be hard to prove directly. A <strong>hybrid argument</strong> inserts intermediate experiments \(H_0,H_1,\ldots,H_N\), changing one component at each step.</p>
\[\bigl|\Pr[D(H_0)=1]-\Pr[D(H_N)=1]\bigr|
\le\sum_{i=1}^{N}\bigl|\Pr[D(H_{i-1})=1]-\Pr[D(H_i)=1]\bigr|.\]
<p>If each neighbouring gap is negligible and \(N\) is polynomial, the total is negligible. For circuit proofs, one might first replace each real gate transcript by its simulation, then replace the committed wire values using hiding.</p>
<p>Every replacement must satisfy the security property’s input conditions. Ordinary HVZK guarantees simulation on true gate statements. If a changed wire assignment makes an XOR relation false, that guarantee cannot simply be invoked for it.</p>
<p>This is the missing link to examine in the supplied informal circuit-simulation solution. We can describe its intended construction while identifying the stronger simulator behaviour or alternative hybrid argument needed to justify that step.</p>
''')

ORDER={
 'commitment':[1,10,7,9,12,13,14,22,18,19,16,20,23,24,26,27,28,29,30,31,32,33,35,37,38,39,42,48,43,45,46,47,49,51,52,53,54,55,56,58,60,61,62,64,65,63,66,68,70,72,73,75,77,79,81,82,83,84],
 'zero-knowledge':[1,2,4,7,9,10,11,13,16,17,18,19,20,21,22,6,23,24,26,28,29,30,31,32,33,34,36,38,39,41,42,43,44,45,46,47,48,49,51,53,54,55,57,58,60,61]}
MERGED={
 'commitment':{2:10,3:29,4:29,5:30,6:43,8:7,11:7,15:13,17:16,21:22,25:26,34:35,36:39,40:48,41:46,44:43,50:51,57:56,59:60,67:66,69:68,71:72,74:77,76:77,78:77,80:79,85:84},
 'zero-knowledge':{3:1,5:38,8:7,12:2,14:9,15:11,25:24,27:29,35:38,37:38,40:38,50:49,52:51,56:55,59:58,62:61}}
PRIMER_TARGETS={
 'commitment':{'notation':1,'powers':10,'bits':27,'chance':29,'algorithms':10,'commit':23,'oracle':28,'group':38,'ddh':64,'linear':77},
 'zero-knowledge':{'notation':1,'powers':1,'bits':1,'chance':2,'algorithms':4,'proof':1,'circuit':1,'commit':20,'graph':19,'mod':43,'group':43}}
HW_ORDER={'hw1':[32,60,62,33,53,26,54,55,72,73,75,77,81,82,84],
          'hw2':[16,17,18,54,39,41,42,44,45,46,57,58,61]}
LEGACY_HW_ORDER={'hw1':[32,59,60,61,62,33,53,26,54,55,71,72,73,75,76,77,79,80,81,82,83,84],
                 'hw2':[15,16,17,18,54,37,38,39,41,42,43,44,45,46,55,56,57,58,60,61]}
HW_ALIASES={'hw1':{2:3,4:5,11:12,15:16,17:19,18:19,21:22},'hw2':{1:2,6:8,7:8,11:12,15:17,16:17,19:20}}
