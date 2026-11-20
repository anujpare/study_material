"""Source-authored Shamir and threshold-signature lessons for the MPC lab."""

CARDS = [
    {
        'id': 'threshold-definition',
        'title': 'How many shares should reconstruction require?',
        'section': 'V · Threshold secret sharing',
        'kind': 'lesson',
        'source': 'Lecture 17–19, p. 9, Definition 3; handwritten notes, pp. 13–14',
        'source_ref': 'lecture',
        'requires': ['additive-privacy'],
        'body': r'''<p>Additive sharing has a strong privacy guarantee: any \(n-1\) of the \(n\) parties learn nothing about the secret. Its reconstruction requirement is equally strong: all \(n\) shares are needed. If one share is lost, the others do not determine the secret.</p>
<p>A <strong>\(t\)-out-of-\(n\) secret-sharing scheme</strong> lets any \(t\) parties reconstruct, while any \(t-1\) parties learn nothing. Here \(t\) counts the shares needed for reconstruction; it is not a count of corrupted parties that an MPC protocol tolerates.</p>
<blockquote class="definition"><p>Let \(\mathcal Z\) be the set of possible secrets, and let \(1\le t\le n\). An efficient randomized algorithm \(\mathrm{Gen}(n,t,\alpha)\) creates shares \((s_1,\ldots,s_n)\) of a secret \(\alpha\in\mathcal Z\). An efficient algorithm \(\mathrm{Recons}\) receives \(t\) indexed shares and returns \(\alpha\).</p></blockquote>
<p><strong>Correctness</strong> must hold for every secret, every possible set of shares output by \(\mathrm{Gen}\), and every set \(I\subseteq\{1,\ldots,n\}\) of \(t\) indices:</p>
<div class="math">\[\mathrm{Recons}\bigl((s_i)_{i\in I}\bigr)=\alpha.\]</div>
<p><strong>Perfect privacy</strong> requires that, for every pair of secrets \(\alpha,\beta\in\mathcal Z\) and every set \(S\) of \(t-1\) indices,</p>
<div class="math">\[\mathrm{Gen}(n,t,\alpha)[S]\equiv\mathrm{Gen}(n,t,\beta)[S].\]</div>
<p>The notation \([S]\) means “keep only the shares at these indices.” The symbol \(\equiv\) means identical probability distributions: every possible observed collection of shares has the same probability for both secrets. It does not mean the two independent runs literally produce equal shares. Smaller groups also learn nothing, because their observations are obtained by discarding some of a \(t-1\)-share view.</p>
{{lab:threshold}}
<p>Replacing identical distributions by computational indistinguishability gives a weaker computational privacy notion. Shamir’s scheme below achieves the perfect version. Reconstruction assumes genuine shares; this definition alone does not detect altered shares or force an absent party to participate.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> In a \(3\)-out-of-\(5\) scheme, two parties are offline. The remaining three have genuine shares. Can they reconstruct, and would a coalition holding only two shares learn the secret?</p>',
            'choices': ['The three can reconstruct; two shares reveal nothing.', 'The three cannot reconstruct; all five are needed.', 'The three can reconstruct, so two shares must reveal part of the secret.'],
            'answer': 0,
            'feedback': [
                r'<p>Yes. Three meets the reconstruction threshold. Perfect privacy separately says that any two-share view has a distribution independent of the secret.</p>',
                r'<p>That is the reconstruction requirement of \(5\)-out-of-\(5\) additive sharing. A \(3\)-out-of-\(5\) scheme guarantees reconstruction from any three genuine shares.</p>',
                r'<p>Reconstruction begins at the threshold; there need not be partial leakage below it. Perfect privacy requires identical two-share distributions for every secret.</p>'
            ],
            'hint': r'<p>Apply correctness to three shares, then apply privacy to \(t-1=2\) shares.</p>',
            'solution': r'<p>The three available parties reconstruct because correctness holds for every set of \(t=3\) genuine shares. A coalition of two parties learns nothing because its view is covered by perfect privacy.</p>'
        }
    },
    {
        'id': 'shamir-generation',
        'title': 'Put the secret at a polynomial’s value at zero',
        'section': 'V · Threshold secret sharing',
        'kind': 'lesson',
        'source': 'Lecture 17–19, p. 10, Definition 4; handwritten notes, pp. 14–15',
        'source_ref': 'lecture',
        'requires': ['threshold-definition'],
        'body': r'''<p>Shamir sharing uses the fact that enough values determine a polynomial. Choose a prime \(p>n\), and work in \(\mathbb F_p\), the numbers \(0,\ldots,p-1\) with arithmetic modulo \(p\). The inequality ensures that the party indices \(1,\ldots,n\) are distinct and nonzero in this field.</p>
<p>To share \(\alpha\in\mathbb F_p\) with threshold \(t\), independently choose \(t-1\) coefficients \(a_1,\ldots,a_{t-1}\), each uniformly from \(\mathbb F_p\). Uniformly means that each of the \(p\) values has probability \(1/p\). Define</p>
<div class="math">\[f(X)=\alpha+a_1X+\cdots+a_{t-1}X^{t-1}.\]</div>
<p>The capital \(X\) is the polynomial’s variable. Every term after \(\alpha\) contains a positive power of \(X\), so evaluating at zero gives \(f(0)=\alpha\). Party \(P_i\) receives the <strong>indexed share</strong> \(s_i=(i,f(i))\). The index tells reconstruction where the value belongs; it is not itself secret.</p>
<p>Our running example uses \(p=17\), \(t=3\), \(n=5\), secret \(\alpha=6\), and sampled coefficients \(a_1=4,a_2=2\). Thus</p>
<div class="math">\[f(X)=6+4X+2X^2\pmod {17}.\]</div>
<table><caption>One possible sharing of the secret \(6\)</caption><thead><tr><th scope="col">Party index \(i\)</th><th scope="col">Private value \(f(i)\)</th></tr></thead><tbody><tr><th scope="row">1</th><td>12</td></tr><tr><th scope="row">2</th><td>5</td></tr><tr><th scope="row">3</th><td>2</td></tr><tr><th scope="row">4</th><td>3</td></tr><tr><th scope="row">5</th><td>8</td></tr></tbody></table>
<p>For example, \(f(2)=6+8+8=22\equiv5\pmod {17}\). A fresh sharing of the same secret normally uses different random coefficients and produces different shares.</p>
{{lab:shamir}}
<p>The degree is <strong>at most</strong> \(t-1\). We allow a sampled leading coefficient to equal zero. Forcing it to be nonzero would change the distribution used by the privacy proof. With \(t=1\), no random coefficients are needed: every share directly contains \(\alpha\).</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> For \(f(X)=6+4X+2X^2\) over \(\mathbb F_{17}\), what private value does party \(P_4\) receive? Enter its representative from \(0\) to \(16\).</p>',
            'answer': 3,
            'hint': r'<p>Substitute \(X=4\), then subtract a multiple of \(17\).</p>',
            'solution': r'<p>\(f(4)=6+4\cdot4+2\cdot4^2=6+16+32=54\). Since \(54=3\cdot17+3\), the private value is \(3\); the full indexed share is \((4,3)\).</p>'
        }
    },
    {
        'id': 'interpolation-lemma',
        'title': 'What makes a polynomial reconstructible?',
        'section': 'V · Threshold secret sharing',
        'kind': 'lesson',
        'source': 'Lecture 17–19, p. 10, Lemma 2; handwritten notes, pp. 15–16',
        'source_ref': 'lecture',
        'requires': ['shamir-generation'],
        'body': r'''<p><strong>Interpolation</strong> means finding a polynomial from specified evaluations. The lecture uses the following exact statement.</p>
<blockquote class="definition"><p>For every collection of \(d\) points \((x_1,y_1),\ldots,(x_d,y_d)\in\mathbb F_p^2\) whose first coordinates are pairwise distinct, there is exactly one polynomial \(f\in\mathbb F_p[X]\) of degree at most \(d-1\) satisfying \(f(x_i)=y_i\) for every \(i\).</p></blockquote>
<p>Here \(d\) counts points, rather than the degree. In Shamir sharing we will take \(d=t\). A polynomial of degree at most \(d-1\) has \(d\) coefficient positions, including its constant coefficient. Each observed point supplies one equation about those coefficients.</p>
<p>The requirements matter. Two records at the same position do not supply two independent evaluations. If both say \(f(1)=4\), they repeat one equation. If one says \(f(1)=4\) and another says \(f(1)=7\), no polynomial can satisfy both. Distinct \(x\)-coordinates exclude both failures.</p>
<p>The phrase “degree at most” also matters. Three points \((1,4),(2,4),(3,4)\) have the constant interpolant \(f(X)=4\), whose degree is zero. They do not require a degree-two term.</p>
<p>We can already see why there is <em>at most</em> one interpolant. If two degree-at-most-\(d-1\) polynomials fit all the points, their difference is zero at each of the \(d\) distinct positions. A nonzero polynomial of degree at most \(d-1\) cannot have \(d\) distinct roots over a field: each distinct root contributes a different linear factor, and the product of \(d\) such factors has degree \(d\). Therefore the difference is the zero polynomial.</p>
<p>Existence also follows by counting. There are \(p^d\) coefficient lists: \(p\) choices for each of the \(d\) coefficients. There are also \(p^d\) possible lists of \(d\) output values. Uniqueness says that different coefficient lists give different output lists at the fixed positions. With equal numbers of possibilities on both sides, every output list must occur. Thus every specified list has an interpolant. The next teaching card expresses this result in the lecture’s matrix notation; HW6 4(a) gives a constructive formula.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> Over \(\mathbb F_{17}\), the observations are \((1,4),(2,4),(3,4)\). Which statement follows from the interpolation lemma?</p>',
            'choices': [r'There is one polynomial of degree exactly \(2\).', r'There is one polynomial of degree at most \(2\), namely \(f(X)=4\).', r'Three equal values violate the distinct-coordinate requirement.'],
            'answer': 1,
            'feedback': [
                r'<p>The lemma bounds the degree from above; it does not force the leading coefficients to be nonzero. The constant polynomial already fits all three observations.</p>',
                r'<p>Correct. The positions \(1,2,3\) are distinct, and \(f(X)=4\) fits them. Uniqueness applies within all polynomials of degree at most \(2\).</p>',
                r'<p>The requirement concerns the first coordinates \(x_i\), not the values \(y_i\). Different positions may have equal values.</p>'
            ],
            'hint': r'<p>Check which coordinates must differ and whether “at most” requires a nonzero quadratic coefficient.</p>',
            'solution': r'<p>The first coordinates \(1,2,3\) are distinct in \(\mathbb F_{17}\). The constant polynomial \(4\) is an allowed polynomial of degree at most \(2\) and fits all observations, so the lemma makes it the unique allowed interpolant.</p>'
        }
    },
    {
        'id': 'hw6-1c',
        'title': 'HW6 1(c) · Find the missing interpolation conditions',
        'section': 'V · Threshold secret sharing',
        'kind': 'homework',
        'exercise': 'HW6 1(c)',
        'source': 'HW6, p. 1, Problem 1(c)',
        'source_ref': 'hw6',
        'requires': ['interpolation-lemma'],
        'body': r'''<p>Use the field \(\mathbb Z_p=\mathbb F_p\), where \(p\) is prime. In this question \(d\) denotes the proposed degree, so there are \(d+1\) supplied points. The homework asks for TRUE or FALSE with a one-sentence justification.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p>“A set of \(d+1\) points \((x_0,y_0),\ldots,(x_d,y_d)\in\mathbb Z_p^2\) determines a unique polynomial \(f\in\mathbb Z_p[X]\) of degree \(d\) such that \(f(x_i)=y_i\) for every \(i=0,1,\ldots,d\).” Is this statement true or false? Give one concrete obstruction.</p>',
            'hint': r'<p>Can two distinct points have the same first coordinate but different second coordinates?</p>',
            'solution': r'''<p><strong>False.</strong> The statement does not require distinct first coordinates. For example, over \(\mathbb F_{17}\), the two distinct points \((1,0)\) and \((1,1)\) would require both \(f(1)=0\) and \(f(1)=1\). No function, and therefore no polynomial, can do this.</p>
<p>There is also an independent degree issue. Distinct first coordinates guarantee an interpolant of degree <em>at most</em> \(d\), not necessarily exactly \(d\). For \(d=1\), the points \((1,4),(2,4)\) have a constant interpolant.</p>
<p><strong>Exam-length answer:</strong> False: the first coordinates need not be distinct, so, for example, \((1,0)\) and \((1,1)\) cannot both lie on a polynomial.</p>''',
            'rubric': ['States FALSE.', 'Gives incompatible values at the same position, or explains the missing distinct-coordinate condition.', 'If discussing degree, distinguishes degree at most d from degree exactly d.']
        }
    },
    {
        'id': 'vandermonde',
        'title': 'Read the Vandermonde matrix as simultaneous equations',
        'section': 'V · Threshold secret sharing',
        'kind': 'lesson',
        'source': 'Lecture 17–19, p. 10, proof of Lemma 2; handwritten notes, pp. 16–17',
        'source_ref': 'lecture',
        'requires': ['interpolation-lemma'],
        'body': r'''<p>The lecture writes the interpolation equations as a matrix equation. A <strong>matrix</strong> is a rectangular table of coefficients; a <strong>column vector</strong> is a list written vertically. These objects package familiar simultaneous equations.</p>
<p>For a quadratic \(f(X)=a_0+a_1X+a_2X^2\) with \(f(1)=12,f(2)=5,f(3)=2\) in \(\mathbb F_{17}\), the equations are</p>
<div class="math">\[\begin{aligned}a_0+a_1+a_2&=12,\\a_0+2a_1+4a_2&=5,\\a_0+3a_1+9a_2&=2.\end{aligned}\]</div>
<p>Write \(\mathbf a=(a_0,a_1,a_2)^{\mathsf T}\) and \(\mathbf y=(12,5,2)^{\mathsf T}\), where \({\mathsf T}\) turns a horizontal list into a column. The same equations become</p>
<div class="math">\[\underbrace{\begin{pmatrix}1&1&1\\1&2&4\\1&3&9\end{pmatrix}}_{\mathbf V}\underbrace{\begin{pmatrix}a_0\\a_1\\a_2\end{pmatrix}}_{\mathbf a}=\underbrace{\begin{pmatrix}12\\5\\2\end{pmatrix}}_{\mathbf y}.\]</div>
<p>Multiplying a row by the column means multiplying matching entries and adding them. Thus the second row gives exactly \(a_0+2a_1+4a_2=5\).</p>
<p>For \(d\) points, row \(i\) of the <strong>Vandermonde matrix</strong> \(\mathbf V\) is \((1,x_i,\ldots,x_i^{d-1})\). A square matrix has an <strong>inverse</strong> precisely when its determinant is nonzero; the inverse reverses the equation, giving the unique solution \(\mathbf a=\mathbf V^{-1}\mathbf y\). The determinant is a scalar calculated from the matrix. The specific algebraic identity used by the lecture is</p>
<div class="math">\[\det(\mathbf V)=\prod_{1\le i<j\le d}(x_j-x_i).\]</div>
<p>The product includes one factor for each pair of positions. Distinct positions make every factor nonzero. In a field, a product of nonzero factors is nonzero, so the inverse exists for every choice of \(\mathbf y\). This proves the existence and uniqueness claimed by the lemma. For positions \(1,2,3\), the determinant is \((2-1)(3-1)(3-2)=2\ne0\).</p>
<p>The matrix depends on the positions, not the secret values. With the same chosen parties, reconstruction can reuse the same inverse.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> Over \(\mathbb F_{17}\), a Vandermonde matrix uses positions \(1,2,4\). What is its determinant, represented from \(0\) to \(16\)?</p>',
            'answer': 6,
            'hint': r'<p>There are three pairwise differences: \(2-1\), \(4-1\), and \(4-2\).</p>',
            'solution': r'<p>The determinant is \((2-1)(4-1)(4-2)=1\cdot3\cdot2=6\pmod {17}\). Since it is nonzero, these three positions determine a unique polynomial of degree at most \(2\), whatever the three supplied values are.</p>'
        }
    },
    {
        'id': 'shamir-reconstruction',
        'title': 'Reconstruct the secret without guessing the polynomial',
        'section': 'V · Threshold secret sharing',
        'kind': 'lesson',
        'source': 'Lecture 17–19, pp. 10–11, reconstruction and Lemma 3 correctness; handwritten notes, pp. 15–17',
        'source_ref': 'lecture',
        'requires': ['vandermonde'],
        'body': r'''<p>Shamir’s reconstruction algorithm takes any \(t\) genuine shares, interpolates the unique polynomial of degree at most \(t-1\), and returns its value at zero. The dealer’s original polynomial is one polynomial that fits these shares. Uniqueness therefore forces the reconstructed polynomial to be that original polynomial, so its value at zero is the secret \(\alpha\). This proves correctness for <em>every</em> subset of \(t\) parties.</p>
<p>Often we can calculate the value at zero directly. For a quadratic \(f(X)=a_0+a_1X+a_2X^2\), consider shares at positions \(1,2,3\). Multiplying their values by \(3,-3,1\) cancels both nonconstant coefficients:</p>
<div class="math">\[\begin{aligned}3f(1)-3f(2)+f(3)&=(3-3+1)a_0\\&\quad +(3-6+3)a_1\\&\quad +(3-12+9)a_2\\&=a_0=f(0).\end{aligned}\]</div>
<p>These weights depend on the positions \(1,2,3\); they are not a universal formula for every choice of parties. In \(\mathbb F_{17}\), the weight \(-3\) is also represented by \(14\).</p>
<p>For the running example, the three values are \(12,5,2\). Hence</p>
<div class="math">\[\alpha=3\cdot12-3\cdot5+2=23\equiv6\pmod {17}.\]</div>
<p>Different sets of three shares give the same secret with their own weights. The experiment computes those weights by interpolation; HW6 4(a) will derive their general formula.</p>
{{lab:interpolate}}
<p>Having three genuine shares guarantees reconstruction. Having three arbitrary numbers does not guarantee that they came from the dealer’s polynomial. An attacker’s altered share can change the reconstructed answer unless another mechanism checks integrity.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> A different \(3\)-out-of-\(5\) sharing over \(\mathbb F_{17}\) supplies \((1,2),(2,5),(3,10)\). What secret do these three shares reconstruct?</p>',
            'answer': 1,
            'hint': r'<p>The positions are still \(1,2,3\), so the weights remain \(3,-3,1\).</p>',
            'solution': r'<p>The secret is \(3\cdot2-3\cdot5+10=6-15+10=1\pmod {17}\). Indeed, \(f(X)=1+X^2\) fits these three values and has constant coefficient \(1\).</p>'
        }
    },
    {
        'id': 'shamir-privacy',
        'title': 'Prove privacy by counting equally likely coefficient choices',
        'section': 'V · Threshold secret sharing',
        'kind': 'lesson',
        'source': 'Lecture 17–19, p. 11, Lemma 3 privacy; handwritten notes, p. 17',
        'source_ref': 'lecture',
        'requires': ['shamir-reconstruction'],
        'body': r'''<p>Failure to reconstruct does not by itself prove privacy. An incomplete view might still favour some secrets. We must show that every possible view has the same probability for every candidate secret.</p>
<p>Fix a secret \(\alpha\), and fix a coalition \(S\) of \(t-1\) parties at distinct nonzero positions \(x_1,\ldots,x_{t-1}\). Let \(\mathbf z=(z_1,\ldots,z_{t-1})\) be any proposed list of the values they see. Consider the \(t\) points</p>
<div class="math">\[(0,\alpha),(x_1,z_1),\ldots,(x_{t-1},z_{t-1}).\]</div>
<p>Their positions are distinct because no party’s position is zero. The interpolation lemma gives exactly one polynomial of degree at most \(t-1\) through these points. Its constant coefficient is already fixed to \(\alpha\). Therefore <strong>exactly one</strong> choice of the random coefficients \((a_1,\ldots,a_{t-1})\) produces the proposed view \(\mathbf z\).</p>
<p>The dealer samples these \(t-1\) coefficients independently and uniformly. There are \(p^{t-1}\) equally likely coefficient lists: \(p\) choices for each position. Consequently, writing \(\mathrm{View}_S(\alpha)\) for the coalition’s list of share values,</p>
<div class="math">\[\Pr[\mathrm{View}_S(\alpha)=\mathbf z]=\frac{1}{p^{t-1}}.\]</div>
<p>The probability is over the dealer’s random coefficients. It contains no \(\alpha\), so it is identical for every secret. This is precisely the distribution equality in the privacy definition.</p>
<p>For the running example, fix visible shares \((1,12),(2,5)\). Secret \(6\) is compatible with \(6+4X+2X^2\). Secret \(7\) is compatible with \(7+11X+11X^2\), which has the same values at \(1\) and \(2\). Each candidate gives those two visible values with probability \(1/17^2=1/289\). The view does not change an observer’s prior beliefs about the secret.</p>
<p>This counting proof includes the case \(t=1\): the coalition is empty, there is one empty coefficient list, and the empty view occurs with probability \(1\).</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> Change to a \(4\)-out-of-\(6\) Shamir scheme over \(\mathbb F_{17}\). Fix the secret \(\alpha\) and only two observed values, \(f(1)=12,f(2)=5\). What is the probability of this exact two-value view?</p>',
            'choices': [r'\(1/17\)', r'\(1/289\)', r'\(1/4913\)'],
            'answer': 1,
            'feedback': [
                r'<p>Two observed values impose two constraints on the three random coefficients. There are \(17\) compatible coefficient triples out of \(17^3\) equally likely triples, so the probability is \(1/17^2\), not \(1/17\).</p>',
                r'<p>Correct. The fixed secret and two observed values leave \(17\) possible coefficient triples. Their total probability is \(17/17^3=1/289\).</p>',
                r'<p>\(1/4913\) is the probability of one particular coefficient triple. This two-value view does not determine all three random coefficients; \(17\) different triples produce it.</p>'
            ],
            'hint': r'<p>A threshold of \(4\) allows degree at most \(3\). Imagine also choosing \(f(3)\): each choice supplies a fourth distinct point and determines one polynomial.</p>',
            'solution': r'<p>The dealer samples three coefficients, giving \(17^3=4913\) equally likely triples. We have fixed only the three points \((0,\alpha),(1,12),(2,5)\). For each of the \(17\) choices of an additional value \(z=f(3)\), four distinct positions determine exactly one polynomial of degree at most \(3\). Different \(z\) values give different polynomials, and every polynomial fitting the original three points has one such \(z\). Thus exactly \(17\) coefficient triples produce the two-value view, whose probability is \(17/17^3=1/289\), independently of \(\alpha\).</p>'
        }
    },
    {
        'id': 'shamir-linearity',
        'title': 'Which computations preserve the Shamir degree bound?',
        'section': 'V · Threshold secret sharing',
        'kind': 'lesson',
        'source': 'Handwritten notes, p. 17, linearity observation; derived examples using Lecture 17–19, Definition 4',
        'source_ref': 'notes',
        'requires': ['shamir-privacy'],
        'body': r'''<p>The handwritten notes finish with an important observation: interpolation is <strong>linear</strong> in the supplied values. Here linear means that adding value lists adds their reconstructed secrets, and multiplying all values by a public scalar multiplies the secret by that scalar.</p>
<p>Suppose \(f(0)=\alpha\) and \(g(0)=\beta\), with both polynomials of degree at most \(t-1\), and each party \(P_i\) holds \(f(i)\) and \(g(i)\). If each party adds its two values, the new value is</p>
<div class="math">\[f(i)+g(i)=(f+g)(i).\]</div>
<p>The sum polynomial still has degree at most \(t-1\), and \((f+g)(0)=\alpha+\beta\). Thus any \(t\) parties can reconstruct the sum. Similarly, multiplying each share by a public scalar \(k\) gives evaluations of \(kf\), whose value at zero is \(k\alpha\). Independent randomness for the original sharings gives the usual privacy of the sum sharing.</p>
<p>Adding a public constant \(k\) has a different local rule from additive sharing: <strong>every</strong> party adds \(k\) to its Shamir value, because \(f(i)+k\) evaluates the polynomial \(f(X)+k\). In additive sharing, the shares are summed, so only one party adds the public constant. The representation determines the rule.</p>
<p>For multiplication, local products do have the correct value at zero, but the degree changes:</p>
<div class="math">\[f(i)g(i)=(fg)(i),\qquad (fg)(0)=\alpha\beta,\qquad \deg(fg)\le2(t-1).\]</div>
<p>That larger bound requires \(2t-1\) distinct evaluations for ordinary interpolation, rather than \(t\). A protocol that continues with threshold \(t\) therefore needs an additional multiplication procedure to restore the required sharing form. The notes’ linearity observation does not supply that procedure.</p>''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> Two degree-at-most-\(2\) Shamir polynomials share two secrets. Parties locally multiply their share values. How many distinct resulting evaluations suffice to interpolate the product polynomial in the worst case?</p>',
            'answer': 5,
            'hint': r'<p>The degrees can add when polynomials multiply. Then apply the degree-plus-one interpolation requirement.</p>',
            'solution': r'<p>The product can have degree \(2+2=4\). Five distinct points determine a degree-at-most-\(4\) polynomial. Three shares were enough for either input polynomial, but do not generally determine the product polynomial.</p>'
        }
    },
    {
        'id': 'hw6-4a',
        'title': 'HW6 4(a) · Build the interpolation formula',
        'section': 'VI · Threshold signatures',
        'kind': 'homework',
        'exercise': 'HW6 4(a)',
        'source': 'HW6, p. 4, Problem 4(a)',
        'source_ref': 'hw6',
        'requires': ['shamir-linearity'],
        'body': r'''<p>Let \(g\) be a polynomial of degree \(d\) over \(\mathbb F_p\), and let \(I\) contain \(d+1\) distinct field elements. Here \(I\) is a set of evaluation positions. For each \(i\in I\), define the polynomial</p>
<div class="math">\[\lambda_i(X)=\prod_{j\in I\setminus\{i\}}\frac{X-j}{i-j}.\]</div>
<p>A product symbol means multiply one factor for every listed \(j\). Each denominator \(i-j\) is nonzero because the positions differ. Division means multiplication by its inverse in \(\mathbb F_p\); a nonzero field element has exactly one inverse. These \(\lambda_i\) are the Lagrange interpolation polynomials; their evaluations will be our reconstruction weights.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p>Show that \(g\) can be written as</p><div class="math">\[g(X)=\sum_{i\in I}g(i)\lambda_i(X).\]</div><p>Your argument should check both the degree bound and the value at every position in \(I\).</p>',
            'hint': r'<p>Evaluate \(\lambda_i\) at \(X=i\), then at a different \(X=j\in I\). In the second case, one numerator is zero.</p>',
            'solution': r'''<p>Call the right-hand polynomial \(q(X)=\sum_{i\in I}g(i)\lambda_i(X)\). Every \(\lambda_i\) multiplies \(d\) linear factors with nonzero constant denominators, so its degree is \(d\). Multiplying by a constant \(g(i)\) and adding these terms cannot increase the bound. Hence \(\deg(q)\le d\).</p>
<p>At \(X=i\), each ratio in \(\lambda_i(i)\) is \((i-j)/(i-j)=1\), so \(\lambda_i(i)=1\). At a different position \(k\in I\), the factor with \(j=k\) has numerator \(k-k=0\), so \(\lambda_i(k)=0\). Thus, at any \(k\in I\), all terms in \(q(k)\) vanish except the term indexed by \(k\), leaving \(q(k)=g(k)\).</p>
<p>Both \(q\) and \(g\) have degree at most \(d\), and they agree at \(d+1\) distinct positions. The interpolation uniqueness lemma gives \(q=g\), proving the formula.</p>
<p>For positions \(I=\{1,2,3\}\), evaluating at zero gives \(\lambda_1(0)=3\), \(\lambda_2(0)=-3\), and \(\lambda_3(0)=1\), recovering our earlier direct reconstruction. For example, \(\lambda_1(0)=\frac{0-2}{1-2}\frac{0-3}{1-3}=2\cdot\frac32=3\), with divisions interpreted in the field. If \(d=0\), the product has no factors and by convention equals \(1\), so the same argument covers a constant polynomial.</p>
<p><strong>Exam-length proof:</strong> The right side has degree at most \(d\) and agrees with \(g\) at every \(k\in I\), because \(\lambda_i(k)\) is \(1\) for \(i=k\) and \(0\) otherwise; uniqueness of interpolation gives equality.</p>''',
            'rubric': ['Shows that the proposed right-hand polynomial has degree at most d.', 'Explains why each basis polynomial is 1 at its own position and 0 at the other positions.', 'Uses agreement at d+1 distinct positions and the degree bound to conclude equality.']
        }
    },
    {
        'id': 'exponent-interpolation',
        'title': 'Apply known weights while values remain in exponents',
        'section': 'VI · Threshold signatures',
        'kind': 'lesson',
        'source': 'Prerequisite bridge for HW6, pp. 5–6, Problems 4(b–d)',
        'source_ref': 'hw6',
        'requires': ['hw6-4a'],
        'body': r'''<p>A <strong>group</strong> is a set with a combination operation, an identity element, and an inverse for each element. Here we write its operation as multiplication. A cyclic group \(G\) of prime order \(p\) has \(p\) elements generated by powers of one element. The exponent arithmetic takes place modulo \(p\).</p>
<p>For any fixed group element \(h\in G\), and known scalars \(a,b\in\mathbb F_p\), the exponent rules are</p>
<div class="math">\[h^a h^b=h^{a+b},\qquad (h^a)^b=h^{ab}.\]</div>
<p>The sums and products in the exponents are modulo \(p\). The operation outside the exponents is the group operation; a group element is not a field scalar. Knowing the encoded value \(h^a\) need not reveal \(a\): recovering such an exponent is the discrete-logarithm problem, assumed difficult in the groups used for cryptography.</p>
<p>Suppose you receive \(h^{a_1},h^{a_2},h^{a_3}\), and you know scalar weights \(\ell_1,\ell_2,\ell_3\). You can exponentiate each received element by its known weight and multiply:</p>
<div class="math">\[(h^{a_1})^{\ell_1}(h^{a_2})^{\ell_2}(h^{a_3})^{\ell_3}=h^{\ell_1a_1+\ell_2a_2+\ell_3a_3}.\]</div>
<p>This computes an <em>encoding of the weighted sum</em>. It does not recover any hidden exponent, or their weighted sum as a field value.</p>
<p>For our Shamir example, take a group of order \(17\), and suppose the received elements are \(h^{12},h^5,h^2\). The known reconstruction weights are \(3,14,1\). Their product is \(h^{3\cdot12+14\cdot5+2}=h^{108}=h^6\), because \(108\equiv6\pmod {17}\). The small order and visible exponents here serve only to show the algebra.</p>
{{lab:exponent}}''',
        'check': {
            'type': 'number',
            'prompt': r'<p><strong>Practice.</strong> In a group of order \(17\), you combine \(h^8\) and \(h^4\) using public weights \(2\) and \(3\). For this teaching calculation, what exponent from \(0\) to \(16\) describes \((h^8)^2(h^4)^3\)?</p>',
            'answer': 11,
            'hint': r'<p>Multiply each exponent by its weight, add, then reduce modulo the group order.</p>',
            'solution': r'<p>The exponent is \(2\cdot8+3\cdot4=28\equiv11\pmod {17}\), so the computed group element is \(h^{11}\). In a real cryptographic execution, computing that element does not require learning the hidden exponents.</p>'
        }
    },
    {
        'id': 'hw6-4b',
        'title': 'HW6 4(b) · Interpolate without taking discrete logarithms',
        'section': 'VI · Threshold signatures',
        'kind': 'homework',
        'exercise': 'HW6 4(b)',
        'source': 'HW6, p. 5, Problem 4(b)',
        'source_ref': 'hw6',
        'requires': ['exponent-interpolation'],
        'body': r'''<p>Let \(G\) be a group of prime order \(p\). Let \(I\subseteq\mathbb F_p\) contain \(t\) distinct positions, and let \(i^{\ast}\in\mathbb F_p\) be a target position. A polynomial \(\omega\in\mathbb F_p[X]\) has degree at most \(t-1\). You know \(I,i^{\ast}\) and the group elements \(\{h^{\omega(i)}:i\in I\}\), for some \(h\in G\), but you need not know the field values \(\omega(i)\).</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p>Show how to compute \(h^{\omega(i^{\ast})}\) efficiently using only the supplied group elements and the public positions.</p>',
            'hint': r'<p>Express \(\omega(i^{\ast})\) as a weighted sum using Lagrange interpolation. Then apply exponent rules to the group elements you actually have.</p>',
            'solution': r'''<p>Compute the scalar weights</p>
<div class="math">\[\ell_i=\lambda_i(i^{\ast})=\prod_{j\in I\setminus\{i\}}\frac{i^{\ast}-j}{i-j}\quad\text{in }\mathbb F_p.\]</div>
<p>Every denominator is nonzero because the positions in \(I\) are distinct. These weights use only \(I\) and \(i^{\ast}\), which are public. Since \(\omega\) has degree at most \(t-1\), interpolation gives \(\omega(i^{\ast})=\sum_{i\in I}\ell_i\omega(i)\). Therefore compute</p>
<div class="math">\[\prod_{i\in I}\bigl(h^{\omega(i)}\bigr)^{\ell_i}=h^{\sum_{i\in I}\ell_i\omega(i)}=h^{\omega(i^{\ast})}.\]</div>
<p>Each operation is exponentiation of a known group element by a known scalar, followed by group multiplication. No discrete logarithm is needed. If the target is already in \(I\), its weight is \(1\) and the other weights are \(0\), so the formula simply returns the corresponding supplied element.</p>''',
            'rubric': ['Computes the Lagrange weights from the public positions, with nonzero denominators.', 'Returns the product of supplied group elements raised to those weights.', 'Uses interpolation and exponent rules to establish the result without recovering hidden exponents.']
        }
    },
    {
        'id': 'bls-interface',
        'title': 'Understand the signature that the parties will share',
        'section': 'VI · Threshold signatures',
        'kind': 'lesson',
        'source': 'HW6, p. 5, Definition 1, BLS signature scheme',
        'source_ref': 'hw6',
        'requires': ['hw6-4b'],
        'body': r'''<p>A digital signature allows a secret-key holder to authenticate a message, while anyone with its public key can verify the result. The homework supplies the following BLS interface; it does not require implementing pairings.</p>
<p>Let \(G\) have prime order \(p\) and generator \(g\). A hash function \(H\) maps a message \(m\) to a group element \(H(m)\in G\). The secret key is a uniformly chosen exponent \(\alpha\in\mathbb F_p\), and the public key is \(u=g^{\alpha}\).</p>
<blockquote class="definition"><p><strong>KeyGen:</strong> sample \(\alpha\), and output secret key \(sk=\alpha\) and public key \(pk=g^{\alpha}\).</p><p><strong>Sign:</strong> on message \(m\), output \(\sigma=H(m)^{\alpha}\).</p><p><strong>Verify:</strong> output \(O_{\rm DDH}(pk,H(m),\sigma)\), using the oracle described below.</p></blockquote>
<p>The <strong>DDH oracle</strong> is an assumed checking algorithm: on group elements \(g^a,g^b,g^c\), it returns \(1\) exactly when \(c=ab\pmod p\). DDH stands for decisional Diffie–Hellman. The checker tests a relation between hidden exponents without requiring the verifier to recover them.</p>
<p>To see why a genuine signature passes, write \(H(m)=g^b\) for its exponent \(b\), even though the verifier need not know \(b\). Then \(\sigma=(g^b)^{\alpha}=g^{\alpha b}\). The triple \((g^{\alpha},g^b,g^{\alpha b})\) satisfies the oracle’s product relation. In the special groups used by BLS, a pairing implements this check; its construction is outside this homework.</p>
<p>The threshold goal is now precise: different parties will hold Shamir shares of \(\alpha\). They should jointly produce the one ordinary signature \(H(m)^{\alpha}\), while keeping \(\alpha\) unreconstructed.</p>''',
        'check': {
            'type': 'choice',
            'prompt': r'<p><strong>Practice.</strong> In a teaching group of order \(17\), let \(pk=g^6\) and \(H(m)=g^5\). Which proposed signature satisfies the supplied DDH verification rule?</p>',
            'choices': [r'\(g^{11}\)', r'\(g^{13}\)', r'\(g^{30}\) is invalid because the exponent exceeds \(16\).'],
            'answer': 1,
            'feedback': [
                r'<p>Adding the exponents gives \(11\), but verification requires their product. The signature exponent is \(6\cdot5=30\equiv13\pmod {17}\).</p>',
                r'<p>Correct. \(6\cdot5=30\equiv13\pmod {17}\), so \((g^6,g^5,g^{13})\) satisfies the DDH relation.</p>',
                r'<p>Exponents are interpreted modulo the group order. \(g^{30}=g^{13}\) is the same valid group element, not an invalid encoding merely because the displayed exponent is large.</p>'
            ],
            'hint': r'<p>The oracle checks multiplication of exponents, modulo the order of the group.</p>',
            'solution': r'<p>The verifier accepts \(g^{13}\), since the required exponent is \(6\cdot5\equiv13\pmod {17}\). Writing the same element as \(g^{30}\) would also be valid.</p>'
        }
    },
    {
        'id': 'hw6-4c',
        'title': 'HW6 4(c) · Construct a threshold BLS signature',
        'section': 'VI · Threshold signatures',
        'kind': 'homework',
        'exercise': 'HW6 4(c)',
        'source': 'HW6, pp. 5–6, Problem 4(c)',
        'source_ref': 'hw6',
        'requires': ['bls-interface'],
        'body': r'''<p>Use the BLS scheme just defined: \(pk=g^{\alpha}\), \(\sigma=H(m)^{\alpha}\), and verification by the supplied DDH oracle. The homework writes \(N\) for the number of signers. Let \(1\le t\le N<p\), so signer positions \(1,\ldots,N\) are distinct and nonzero in \(\mathbb F_p\).</p>
<p>The setup algorithm may act as a trusted dealer. Distributed key generation, where no dealer ever knows the full key, is a separate problem not requested here. A public key share \(pk_i\) identifies the key corresponding to signer \(i\)’s secret share \(sk_i\).</p>''',
        'check': {
            'type': 'written',
            'prompt': r'''<p>Define a \(t\)-out-of-\(N\) threshold version with algorithms \(\mathrm{KeyGen}(N,t)\), \(\mathrm{Sign}(m,sk_i)\), \(\mathrm{Combine}(m,I,\{(pk_i,\sigma_i)\}_{i\in I})\), and \(\mathrm{Verify}(m,pk,\sigma)\), where \(I\) contains \(t\) signers.</p><p>The public key \(pk\) and final signature \(\sigma\) must each contain one group element, regardless of \(t,N\). Show correctness and give an informal security argument.</p>''',
            'hint': r'<p>Share the BLS secret exponent using a degree-at-most-\(t-1\) polynomial. Let each signer apply its exponent share to \(H(m)\), then interpolate at zero in the exponent.</p>',
            'solution': r'''<p><strong>KeyGen.</strong> Sample the BLS secret \(\alpha\in\mathbb F_p\) uniformly. Sample independent uniform coefficients \(a_1,\ldots,a_{t-1}\), and define the Shamir polynomial \(\varphi(X)=\alpha+\sum_{j=1}^{t-1}a_jX^j\). Set \(\alpha_i=\varphi(i)\), and output</p>
<div class="math">\[pk=g^{\alpha},\qquad sk_i=\alpha_i,\qquad pk_i=g^{\alpha_i}\quad(i=1,\ldots,N).\]</div>
<p><strong>Sign.</strong> Signer \(i\) computes its signature share \(\sigma_i=H(m)^{\alpha_i}\). It sends the group element \(\sigma_i\), not its scalar secret share \(\alpha_i\).</p>
<p><strong>Combine.</strong> For \(t\) valid shares indexed by \(I\), compute the scalar Lagrange weights at zero, \(\ell_i=\prod_{j\in I\setminus\{i\}}\frac{-j}{i-j}\), and output</p>
<div class="math">\[\sigma=\prod_{i\in I}\sigma_i^{\ell_i}.\]</div>
<p><strong>Verify.</strong> Use ordinary BLS verification: return \(O_{\rm DDH}(pk,H(m),\sigma)\). The next subquestion shows how to check each signature share before combining.</p>
<p><strong>Correctness.</strong> Since \(\varphi\) has degree at most \(t-1\), the weights satisfy \(\sum_{i\in I}\ell_i\alpha_i=\varphi(0)=\alpha\). Therefore</p>
<div class="math">\[\sigma=\prod_{i\in I}(H(m)^{\alpha_i})^{\ell_i}=H(m)^{\sum_{i\in I}\ell_i\alpha_i}=H(m)^{\alpha}.\]</div>
<p>This is exactly the ordinary BLS signature, so the unchanged verification algorithm accepts. Both \(pk\) and \(\sigma\) are one group element. The list of public key shares and the communication during signing can still grow with \(N\) or \(t\).</p>
<p><strong>Informal security argument.</strong> Fewer than \(t\) scalar Shamir shares reveal no information about \(\alpha\) by themselves. Public key shares and signature shares expose group encodings, so the entire public transcript is not information-theoretically private. Under the cryptographic assumptions supporting the intended threshold BLS construction, an efficient coalition below threshold cannot turn those encodings into a new signature without enough authorised signature shares. Shamir privacy explains the sharing component; it is not, alone, a complete unforgeability proof. We assume correctly generated keys and the underlying BLS security model, as the homework intends.</p>''',
            'rubric': ['Shares the secret exponent with a degree-at-most-(t−1) Shamir polynomial and publishes the corresponding public key shares.', 'Makes each partial signature H(m) raised to its signer’s secret share.', 'Combines with Lagrange weights at zero and derives H(m) raised to the original secret.', 'Uses ordinary BLS verification and checks the one-element size requirements.', 'Separates perfect privacy of scalar shares from the cryptographic assumptions needed for signature unforgeability.']
        }
    },
    {
        'id': 'hw6-4d',
        'title': 'HW6 4(d) · Reject a bad signature share before combining',
        'section': 'VI · Threshold signatures',
        'kind': 'homework',
        'exercise': 'HW6 4(d)',
        'source': 'HW6, p. 6, Problem 4(d)',
        'source_ref': 'hw6',
        'requires': ['hw6-4c'],
        'body': r'''<p>Signer \(i\)’s established public key share is \(pk_i=g^{\alpha_i}\). Its correct signature share on message \(m\) is \(\sigma_i=H(m)^{\alpha_i}\). The combiner knows \(pk_i\), \(m\), and the received \(\sigma_i\), but not \(\alpha_i\). Assume that the public key shares were generated and associated with signers correctly during setup.</p>''',
        'check': {
            'type': 'written',
            'prompt': r'<p>Show how the combine algorithm can detect that a malicious signer supplied an incorrect signature share \(\sigma_i\).</p>',
            'hint': r'<p>A signature share has the same algebraic form as an ordinary BLS signature, with \(pk_i\) replacing the overall public key.</p>',
            'solution': r'''<p>For every received share, run ordinary BLS verification using the corresponding public key share:</p>
<div class="math">\[O_{\rm DDH}(pk_i,H(m),\sigma_i).\]</div>
<p>Writing \(H(m)=g^b\) for the proof, the checker accepts exactly when \(\sigma_i=g^{\alpha_i b}=H(m)^{\alpha_i}\). The combiner does not calculate \(b\) or \(\alpha_i\); the supplied DDH-checking operation tests this relation directly.</p>
<p>Reject any share for which the check returns \(0\). Combine only a set of at least \(t\) valid, correctly indexed shares for the same message, using the Lagrange weights for the chosen indices. Detecting a bad share does not force its signer to send a valid replacement; availability of enough valid shares is a separate requirement.</p>
{{lab:signature}}
<p><strong>Exam-length answer:</strong> Verify each \(\sigma_i\) as an ordinary BLS signature under \(pk_i\), by checking \(O_{\rm DDH}(pk_i,H(m),\sigma_i)=1\), and reject it before interpolation if the check fails.</p>''',
            'rubric': ['Uses the signer’s public key share pk_i, not the overall public key pk.', 'Checks the received share on the same message m using the BLS/DDH verification operation.', 'Rejects invalid shares before interpolation and recognises that detection alone does not ensure enough shares arrive.']
        }
    }
]

SOURCE_ISSUES = [
    'Shamir generation at positions 1,...,n needs p>n (or any n distinct nonzero field positions). The lecture omits this explicit size condition.',
    'The interpolation and Shamir degree bounds are at most d-1 and at most t-1. Sampled leading coefficients may equal zero; excluding zero changes the privacy distribution.',
    'Handwritten p. 15 draws a smooth real curve as intuition. The lab uses discrete finite-field evaluations and labels the field.',
    'Handwritten p. 17 writes the inverse/coefficient relationship informally. The lesson uses column vectors and the correct orientation a=V^{-1}y.',
    'HW6 1(c) has two independent problems: repeated first coordinates may be incompatible, and distinct coordinates guarantee degree at most d rather than exactly d.',
    'The Shamir privacy proof concerns the full joint view of t-1 shares. It counts one coefficient list for each fixed secret and view, yielding probability p^{-(t-1)}; insufficient reconstruction alone is not a privacy proof.',
    'Threshold t counts required shares here. Ordinary Shamir sharing neither authenticates malformed shares nor guarantees availability or fairness.',
    'The handwritten final-page linearity observation supports addition and public scaling. Local products have degree at most 2(t-1), so their direct reconstruction generally needs 2t-1 points; the supplied notes do not develop a degree-reduction MPC protocol.',
    'HW6 4(c) uses trusted-dealer key generation, not distributed key generation. Perfect secrecy of scalar Shamir shares does not imply perfect secrecy of published group encodings or by itself prove threshold-signature unforgeability; security remains conditional on the intended BLS assumptions.',
    'HW6 4(d) checks each partial signature against its own established public key share and the same message. Rejecting a faulty share does not guarantee that t valid shares arrive.'
]
