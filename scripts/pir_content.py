r"""Chapter 4: PIR followed by the connected HW4 midterm proof review."""
from hw4_content import HW,lab
from hw3_content import HW as HW3

CARDS=[]
def card(key,title,body,pages,requires=(),exercises=()):
 CARDS.append(dict(id=key,title=title,body=body,source=pages,requires=list(requires),kind='theory'))
 for ref in exercises:
  if ref.startswith('hw3:'):
   old=ref.split(':')[1]
   c=dict(HW3[old],id='hw3-'+old,requires=[key],kind='homework',origin='hw3:'+old)
  else:c=dict(HW[ref],origin='hw4:'+ref)
  CARDS.append(c)

card('pir-goal','Read a record without revealing which one',r'''
<p>A database server holds bits \(X_1,\ldots,X_n\). The client wants bit \(X_i\), but wants to hide the index \(i\) from the server. This is <strong>private information retrieval</strong>, or PIR. The index identifies the requested record; the database's contents are not assumed secret from the client.</p>
<p>For a DNS-style lookup, learning which record is requested can reveal which service the client intends to use. Encrypting the network connection protects against an outside eavesdropper, but the answering server still sees an ordinary query. PIR addresses that server-side visibility.</p>
<figure class="learning"><figcaption>The privacy goal</figcaption><div class="pir-flow"><span>Client knows index i</span><span>→ query that hides i from the server</span><span>Server holds database X; computes an answer</span><span>→ client reconstructs Xᵢ</span></div></figure>
<p>Downloading all \(n\) bits and choosing locally solves the privacy problem. The challenge is to communicate less than the whole database. We will follow two routes: split the query between non-colluding servers, or encrypt it for one server. These protocols retrieve an indexed item; converting an arbitrary search phrase into a suitable private database query is an additional problem.</p>
''','PIR pp. 1–2')

card('pir-contract','Separate correctness, privacy and cost',r'''
<p>A two-server protocol has three stages: \(\operatorname{Query}(i)\) produces queries \(q_0,q_1\); each server runs \(\operatorname{Answer}(X,q_b)\); the client reconstructs its bit from the answers and retained local information. The subscript \(b\in\{0,1\}\) labels a server.</p>
<table><thead><tr><th>Requirement</th><th>What to check</th></tr></thead><tbody><tr><td>Correctness</td><td>When the parties follow the protocol, reconstruction returns Xᵢ.</td></tr><tr><td>Query privacy</td><td>One server cannot distinguish which allowed index was requested from its view.</td></tr><tr><td>Communication</td><td>Count both uploaded queries and downloaded answers, in bits.</td></tr></tbody></table>
<p><strong>Sublinear</strong> means the communication divided by \(n\) tends to zero as \(n\) grows. This is written \(o(n)\). For example, \(\sqrt n/n=1/\sqrt n\) tends to zero, but \(n/n=1\) does not. The notation \(O(\sqrt n)\) is an upper growth bound, not an exact bit count.</p>
<p>Privacy does not promise correct answers from malicious servers, conceal the fact that a query happened, or limit the client to learning one record. Those are separate guarantees. In particular, the lecture's non-collusion condition concerns query privacy; a server that deliberately changes its answer can still spoil reconstruction.</p>
''','PIR p. 3',['pir-goal'])

card('bit-selection','An index can be represented by a vector',r'''
<p>A <strong>vector</strong> is an ordered list. The one-hot vector \(e_i\) has a 1 at position \(i\) and 0 everywhere else. For four positions, \(e_3=(0,0,1,0)\).</p>
<p>For now, arithmetic is in \(\mathbb F_2=\{0,1\}\). Addition keeps the remainder modulo 2: it is XOR, written \(\oplus\). Thus \(1\oplus1=0\). Multiplication of bits is AND: only \(1\cdot1\) gives 1.</p>
\[X\cdot q=\bigoplus_{k=1}^{n}X_kq_k.\]
<p>Read this <strong>inner product</strong> as “multiply corresponding entries, then XOR the products”. A query bit 1 includes a database bit in that XOR; a query bit 0 excludes it. Consequently \(X\cdot e_i=X_i\).</p>
<figure class="learning"><figcaption>Selection for X = (1, 0, 1, 1)</figcaption><div class="pir-flow"><span>e₃ = (0, 0, 1, 0)</span><span>Products: (0, 0, 1, 0)</span><span>XOR all products → 1 = X₃</span></div></figure>
<p>Sending \(e_i\) directly would reveal the index. We need to hide this vector while preserving a way to compute its inner product.</p>
''','PIR pp. 3–4',['pir-contract'])

card('query-shares','Hide the selector in two individually random shares',r'''
<p>Choose a uniform random bit vector \(q_0\), meaning all \(2^n\) vectors are equally likely. Define \(q_1=q_0\oplus e_i\), with XOR applied at each position. The pair satisfies \(q_0\oplus q_1=e_i\), since XORing any bit with itself cancels it.</p>
<p>This is <strong>additive secret sharing</strong> over \(\mathbb F_2\). Each server receives one share. For any fixed selector, XOR with it rearranges all possible random masks. Thus either share alone has the same uniform distribution for every index.</p>
''' + lab('shares','A sample pair versus the distribution seen by one server',
 '<p>With four positions, target 3 and mask q₀ = 1010 give q₁ = 1000. Together the shares reveal 0010, but either server alone sees a uniformly random four-bit vector.</p><div data-shares-sample class="pir-flow"><span>Server 0 sees 1010</span><span>Server 1 sees 1000</span><span>Client combines → 0010</span></div><div data-share-distribution></div>') + r'''
<p><strong>Non-collusion</strong> means the servers do not pool their views. If they do, combining the shares reveals the selector. For repeated queries, use a fresh random mask each time; reusing one mask would create relations between the observed queries.</p>
''','PIR pp. 3–4',['bit-selection'])

card('flat-pir','The first private protocol: XOR the two answers',r'''
<p>Both servers hold the same database \(X\). Server \(b\) returns the single bit \(a_b=X\cdot q_b\). The client XORs the replies. Distributing the inner product over XOR gives</p>
\[\begin{aligned}a_0\oplus a_1
 &=X\cdot(q_0\oplus q_1)\\
 &=X\cdot e_i=X_i.\end{aligned}\]
<p>Every random mask cancels, so honest reconstruction is always correct. Privacy follows from the single-share distributions established on the previous card; the answer is just a function of the server's database and that share.</p>
<p>Count the cost carefully: the client uploads two \(n\)-bit vectors and downloads two bits, for \(2n+2\) bits total. Hiding the index worked, but we have not achieved sublinear communication.</p>
<p>If each record instead contains \(B\) bits, apply the same selector to every bit position within a record. Upload remains \(2n\) bits and the two answers contain \(2B\) bits. This observation motivates arranging a bit database into fewer, longer records next.</p>
''','PIR p. 4',['query-shares'])

card('matrix-layout','Reshape the database into rows and columns',r'''
<p>Place the database bits into an \(R\)-row, \(C\)-column matrix, with \(RC\ge n\). Pad unused cells with known zeros. A matrix is simply a rectangular table; the entry \(X_{i,j}\) has row \(i\) and column \(j\).</p>
<p>To request \(X_{i,j}\), privately select its <em>column</em>. Use \(C\)-bit shares of \(e_j\). Each server computes \(a_b=Xq_b\), meaning one inner product per row, and returns an \(R\)-bit vector. Combining the answers reveals the whole column; the client reads row \(i\) locally.</p>
''' + lab('matrix','Follow a four-by-four query through both servers',
 '<p>The same table is stored at both servers. For target row 2, column 2, use q₀ = 1010 and q₁ = 1110.</p><div data-matrix-table><table><thead><tr><th>Row</th><th>C1</th><th>C2</th><th>C3</th><th>C4</th></tr></thead><tbody><tr><th>1</th><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><th>2</th><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><th>3</th><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><th>4</th><td>0</td><td>0</td><td>1</td><td>0</td></tr></tbody></table></div><div data-matrix-stage class="pir-flow"><span>a₀ = 0011</span><span>a₁ = 0101</span><span>a₀ XOR a₁ = 0110: column 2</span><span>Its row-2 bit is 1.</span></div>') + r'''
<p>The row number is never transmitted in this protocol. Changing the row while retaining the column changes only the client's final local selection. Ordinary PIR allows the client to learn the other bits in the reconstructed column.</p>
''','PIR pp. 4–5',['flat-pir'])

card('matrix-proof','Why the reshaped protocol still works',r'''
<p>Now \(q_0,q_1\) each have \(C\) entries and \(a_0,a_1\) each have \(R\). The same cancellation works simultaneously in every row:</p>
\[\begin{aligned}a_0\oplus a_1
 &=Xq_0\oplus X(q_0\oplus e_j)\\
 &=Xq_0\oplus Xq_0\oplus Xe_j\\
 &=Xe_j=X_{:,j}.\end{aligned}\]
<p>The notation \(X_{:,j}\) means “all rows in column j”. Taking entry \(i\) of this vector yields \(X_{i,j}\), the desired bit. Each equality uses distributivity or cancellation over \(\mathbb F_2\).</p>
<p>For privacy, each individual query is uniform among all \(C\)-bit strings, regardless of \(j\). The query also contains no row index. Thus the view of either non-colluding server is independent of both coordinates. This proves information-theoretic query privacy, rather than relying on an attacker being unable to solve a difficult computation.</p>
''','PIR p. 5',['matrix-layout'])

card('communication-balance','Balance uploads against downloads',r'''
<p>The two queries cost \(2C\) bits and the two replies cost \(2R\) bits. With \(RC=n\), the total is</p>
\[T(C)=2C+2n/C.\]
<p>Making more columns lengthens queries but shortens replies. The smallest sum occurs at \(R=C=\sqrt n\): from \((R-C)^2\ge0\), we get \((R+C)^2\ge4RC=4n\), so \(R+C\ge2\sqrt n\).</p>
''' + lab('balance','See which rectangular shape communicates least',
 '<p>For 64 bits, an 8×8 layout sends 16 query bits and 16 answer bits: 32 bits total. A 1×64 layout sends 130 bits. Whole-database download sends 64 bits.</p><div data-balance-plot></div>') + r'''
<p>For nonsquare \(n\), choose \(C=\lceil\sqrt n\rceil\) and \(R=\lceil n/C\rceil\); the ceiling symbol means round up to an integer. Padding preserves the \(O(\sqrt n)\) bound. Growth rates do not guarantee a saving on tiny inputs: \(4\sqrt n<n\) only when \(n>16\).</p>
''','PIR pp. 4–5',['matrix-proof'])

card('pir-assumptions','Which assumption pays for privacy?',r'''
<p>Two-server PIR relies on separation of the servers' views. Its uniform-share proof survives even unlimited computation, but not collusion. Single-server PIR cannot obtain sublinear communication with information-theoretic privacy in the standard setting of the lecture; it needs computational assumptions.</p>
<table><thead><tr><th>Route</th><th>What privacy relies on</th></tr></thead><tbody><tr><td>Two replicated servers</td><td>Each server sees only its own share.</td></tr><tr><td>One server</td><td>The server cannot efficiently distinguish encrypted queries.</td></tr></tbody></table>
<p>For the homework's hypothetical world, recall the complexity classes: <strong>P</strong> contains yes/no questions decidable in polynomial time, while <strong>NP</strong> contains questions with proposed yes-witnesses checkable in polynomial time. For instance, a proposed key can be checked against a list of function inputs and outputs.</p>
<p>Assuming \(\mathrm P=\mathrm{NP}\) would collapse the distinction between efficient verification of such a witness and efficient decision of its existence. It would defeat the hardness needed by the cryptographic route. It would not change the fact that two distributions are mathematically identical. Apply that distinction to the two-server scheme now.</p>
''','PIR pp. 2–5; HW4 1',['communication-balance'],['1c'])

card('homomorphic-operations','Compute on an encryption without decrypting it',r'''
<p>An encryption algorithm turns a plaintext \(m\) into a ciphertext \(c=\operatorname{Enc}(pk,m;r)\), using public key \(pk\) and fresh randomness \(r\). Only the client holds the decryption key \(sk\). Fresh randomness prevents identifying a secret bit by comparing it with one fixed encryption of 0 or 1.</p>
<p><strong>Linearly homomorphic encryption</strong> (LHE) lets the server combine ciphertexts so that decryption gives a sum of plaintexts, and multiply a plaintext by a known scalar. Write \(\boxplus\) for encrypted addition and \(a\odot c\) for multiplication by known scalar \(a\). Then</p>
\[\operatorname{Dec}(sk,c_1\boxplus c_2)=m_1+m_2,\qquad
\operatorname{Dec}(sk,a\odot c_1)=a m_1.\]
<p>These operations use the encryption scheme's plaintext arithmetic. The equalities concern <em>decrypted values</em>; evaluated ciphertext bytes need not equal a fresh encryption's bytes. The server does not learn the plaintext sum.</p>
<p>LHE does not generally multiply two unknown encrypted plaintexts. <strong>Fully homomorphic encryption</strong> (FHE), used later, supports evaluation of whole circuits including such multiplications. Both need an appropriate encryption-security assumption to hide the inputs.</p>
''','PIR p. 5',['pir-assumptions'])

card('single-server','Encrypt the column selector for one server',r'''
<p>The client encrypts every component of \(e_j\), using fresh encryption randomness, and sends the \(C\) ciphertexts. For each row \(i\), the server forms an encrypted linear combination using its known database bits as scalars:</p>
\[a_i=\mathop{\boxplus}_{k=1}^{C}\bigl(X_{i,k}\odot\operatorname{Enc}(pk,(e_j)_k)\bigr).\]
<p>The large \(\boxplus\) means combine all these terms with encrypted addition. Since only position \(j\) of the plaintext selector is 1, decrypting \(a_i\) gives \(X_{i,j}\). The server returns one ciphertext per row; the client decrypts its desired row.</p>
<figure class="learning"><figcaption>One server's view</figcaption><div class="pir-flow"><span>C encrypted selector entries</span><span>↓ use each database row as known coefficients</span><span>R encrypted column entries</span><span>↓ client decrypts the desired entry</span></div></figure>
<p>Upload and download total \(C+R\) ciphertexts. If each has \(L_{\mathrm{ct}}\) bits, communication is \((C+R)L_{\mathrm{ct}}\), or \(O(\lambda\sqrt n)\) under the lecture's \(L_{\mathrm{ct}}=O(\lambda)\) simplification and square layout. Here \(\lambda\) is the security parameter. Public setup/key material is accounted for separately when reused.</p>
<p>The encrypted query vectors for different indices must be computationally indistinguishable: efficient tests should not identify which was sent. This is a guarantee about the joint encrypted vector, not about whether one displayed ciphertext looks random.</p>
''','PIR pp. 5–6',['homomorphic-operations'],['1b'])

card('recursive-selection','Retrieve privately from the intermediate answer too',r'''
<p>The matrix scheme returns a whole encrypted column even though the client needs one entry. Recursion applies private selection again to that intermediate data. For a simple example, let \(n=L^3\) and label a target by three coordinates \((a,b,c)\), each from 1 to \(L\).</p>
<p>Arrange the original database in \(L^2\) rows and \(L\) columns. Selecting column \(c\) produces \(L^2\) inner ciphertexts, indexed by \((a,b)\). Reshape them as an \(L\)-by-\(L\) table and privately select column \(b\). The client receives \(L\) outer-encrypted records and locally chooses row \(a\).</p>
''' + lab('recursion','Follow the target through two selections',
 '<p>With n = 64 and L = 4, first select one column from a 16×4 table. Reshape its 16 encrypted entries into 4×4, then select another column. Four outer records remain.</p><div data-recursion-stage class="pir-flow"><span>64 bits → 16 inner ciphertexts → 4 outer-encrypted records → one selected bit</span></div>') + r'''
<p>Why can LHE handle the second layer? The server treats the <em>encoding of an inner ciphertext</em> as known data to select, just as it previously treated a database bit as known data. It encrypts that representation under the outer selection; it is not multiplying two hidden plaintexts. Ciphertext encodings may need suitable plaintext blocks. The client removes the outer layer to obtain an inner ciphertext, then decrypts that ciphertext.</p>
''','PIR pp. 6–7',['single-server'])

card('recursive-size','Count the size of an encrypted record, not only its number',r'''
<p>In the two-selection example, queries contain two length-\(L\) selector vectors, and the reply contains \(L\) outer-encrypted records. This suggests \(O(n^{1/3})\) objects. It is not yet an \(O(n^{1/3})\)-bit claim, because an outer object contains an encoded inner ciphertext.</p>
<p>Let \(B_t\) be the number of bits representing an object after \(t\) encryption layers. If every layer doubles the length, then \(B_t=2^tB_0\). A useful low-expansion scheme can have much milder growth; the illustration compares that with an additive-overhead model \(B_t=B_0+t\lambda\).</p>
''' + lab('expansion','Track the hidden cost of another encryption layer',
 '<p>Starting from 128 bits, four layers give 2,048 bits under doubling, versus 640 bits when each layer adds 128 bits. These are size models for the diagram, not measured cryptosystem costs.</p><div data-expansion-plot></div>') + r'''
<p>The lecture's polylogarithmic-communication result uses suitable low-expansion linearly homomorphic encryption and the full recursive encoding. “Polylogarithmic” means bounded by a fixed power of \(\log n\), with security-parameter factors retained. It does not follow for an arbitrary LHE scheme merely by repeating selection and ignoring ciphertext lengths.</p>
''','PIR pp. 6–7',['recursive-selection'])

card('replication-limit','Why the same recursion cannot simply reuse two-server PIR',r'''
<p>The two-server primitive assumed both servers hold the <em>same</em> database. After a private matrix query, server 0 has computed \(a_0=Xq_0\), while server 1 has computed \(a_1=Xq_1\). These are different shares of the selected column, not two copies of that column.</p>
<figure class="learning"><figcaption>Check the precondition before reusing a protocol</figcaption><div class="pir-flow"><span>Initial state: server 0 has X; server 1 has X ✓</span><span>After answering: server 0 has a₀; server 1 has a₁</span><span>Only the client can combine them to obtain the column</span></div></figure>
<details class="solution"><summary>Try the lecture question: what goes wrong?</summary><div class="solution-content"><p>Calling the same replicated-database PIR protocol on these intermediate answers would violate its input assumption. Giving both answers to a server could expose the reconstructed column and hence information about the target. The single-server encrypted scheme instead leaves the server with a complete table of encrypted intermediate records that it can select from again.</p><p>This explains why the <em>naive reuse</em> fails; it is not an impossibility theorem against all more sophisticated multi-server PIR constructions.</p></div></details>
''','PIR p. 7',['recursive-size','matrix-proof'])

card('binary-gates','Before FHE: describe an address and a Boolean circuit',r'''
<p>A one-hot vector for \(n\) records needs \(n\) bits. A binary address needs only \(\ell=\lceil\log_2 n\rceil\) bits. For eight records, use 000 through 111. We keep record numbers 1 through 8 for reading, and encode record number minus one as its address.</p>
<p>A Boolean circuit connects gates with bit-valued wires. NOT flips a bit, AND outputs 1 only if both inputs are 1, and OR outputs 1 if at least one input is 1.</p>
<table><thead><tr><th>a,b</th><th>AND</th><th>OR</th><th>Equal?</th></tr></thead><tbody><tr><td>0,0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0,1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1,0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1,1</td><td>1</td><td>1</td><td>1</td></tr></tbody></table>
<p>To select by an encrypted binary address, the server will need to test equality with each record's public address. Start with the ordinary, unencrypted equality circuit in the next exercise. Build the one-bit test from its two accepting cases, then require it to hold at every position.</p>
''','HW4 4(a–b), prerequisite to PIR from FHE',['single-server'],['4a'])

card('fhe-selection','Turn a binary address into selection bits inside a circuit',r'''
<p>For each record \(j\), compare its public address \(j-1\) with the requested address \(i-1\). Call the equality result \(s_j\). Exactly one \(s_j\) is 1 for a valid request. Combine these selectors with the database:</p>
\[X_i=\bigvee_{j=1}^{n}\left(s_j\land X_j\right).\]
<p>The large \(\bigvee\) means OR all terms. Each unwanted record is masked to 0; the desired record contributes its own bit. OR is appropriate here because at most one selector is 1. It should not be read as ordinary integer addition in general.</p>
<p>FHE evaluates this Boolean circuit on encrypted inputs without revealing its intermediate bits. Unlike LHE, it supports AND between values whose plaintexts are both hidden. For the homework's <em>secret-key</em> scheme, the server also needs encrypted constants supplied by the client; it does not receive the key.</p>
<p><strong>Compactness</strong> is the guarantee that the final ciphertext does not grow with the entire evaluated circuit. Parameter choices must also support the circuit's computation correctly. These are the properties needed to make the next exercise's “one returned ciphertext” useful.</p>
''','HW4 4(b); PIR p. 5 encryption background',['binary-gates'],['4b'])

card('noise-model','Track the quantity that a gate changes',r'''
<p>Many homomorphic schemes carry an error quantity often called <strong>noise</strong>. Decryption works only while the error stays within the scheme's permitted range. For HW4 we use its stated numerical rules, rather than deriving a particular cryptosystem's error analysis.</p>
<table><thead><tr><th>Operation</th><th>Noise rule in HW4</th></tr></thead><tbody><tr><td>Fresh encryption</td><td>2</td></tr><tr><td>NOT</td><td>Keep the input magnitude</td></tr><tr><td>AND</td><td>Multiply the two magnitudes</td></tr><tr><td>OR</td><td>Add the two magnitudes</td></tr></tbody></table>
<p>Work from input wires toward output wires and label each intermediate result. These magnitudes are not the encrypted bits themselves: a plaintext AND result of 0 does not imply noise 0.</p>
<p>To simplify the final count, remember \(2^\ell=n\) when \(n\) is a power of two. Thus \((2^3)^\ell=(2^\ell)^3=n^3\). For other database sizes, retain \(\ell=\lceil\log_2 n\rceil\). The next exercise follows the actual gates built in 4(a–b), including their encrypted constants.</p>
''','HW4 4(c)',['fhe-selection'],['4c'])

card('server-work','A short query can still require a full database scan',r'''
<p>The constructions above reduce communication while leaving substantial server work. A matrix answer uses the entire table in its row-wise combinations. The FHE construction compares the address with every record and combines every result. With the unsimplified equality circuit, its Boolean gate count is \(O(n\log n)\), before the cost of homomorphic gate evaluation.</p>
''' + lab('work','Compare three different quantities',
 '<p>For n = 256, matrix two-server PIR transmits 64 bits total but each server processes the 256-bit table. The FHE construction uploads 10 ciphertexts and returns 1, while computing 256 address comparisons of 8 bits each.</p><div data-work-table></div>') + r'''
<p>Why not read only the requested entry? That memory access would reveal the index to the server. For an arbitrary unprocessed database, an algorithm that never examines a particular bit cannot in general return it correctly for both possible values. This is the intuition behind the linear-work obstacle in the basic model.</p>
<p>That intuition is not a lower bound for every possible PIR model. Preprocessing can store derived information, and batching can share work across requests. Those change what “work for this query” means.</p>
''','PIR p. 7',['noise-model'])

card('offline-online','Move or share work without pretending it disappears',r'''
<p><strong>Batching</strong> answers several queries together so they can share database processing. The notes cite a bound of \(O((\lambda\log k)n)\) work for a batch of \(k\ge2\) queries. This describes a specialized construction; simply running the original protocol \(k\) times still costs about \(k\) scans.</p>
<p><strong>Preprocessing</strong> performs work before the individual queries arrive. The <strong>offline</strong> phase prepares a data structure; the <strong>online</strong> phase answers each later request. To compare schemes, count the setup once and the online cost once per query. An amortized cost divides that total by the number of served queries.</p>
<figure class="learning"><figcaption>Where the work goes</figcaption><div class="pir-flow"><span>Without preprocessing: q queries × one database scan each</span><span>With preprocessing: initial setup + q × online answer cost</span><span>Database changes may require maintenance or rebuilding</span></div></figure>
<p>The notes describe a two-server result with linear offline preprocessing and roughly \(O(\sqrt n\,\operatorname{polylog}n)\) online communication/work, and a later single-server theoretical result with near-linear encoding and polylogarithmic online complexity. These are separate constructions with their own assumptions, not automatic upgrades to the simple protocols we derived. The next sequence revisits polynomial proofs and commitments because HW4 also tests those midterm topics.</p>
''','PIR pp. 7–8',['server-work'])

card('field-review','Midterm bridge: prove claims about polynomials',r'''
<p>PIR hides a requested index. The remaining HW4 questions return to a different task from Chapter 3: verifying a claim about a polynomial. We now prepare that algebra explicitly, before working through the proof constructions.</p>
<p>Over a prime field \(\mathbb F_p\), calculate modulo prime \(p\). Every nonzero element has a multiplicative inverse, so it can be cancelled. A polynomial \(f(X)=a_0+a_1X+\cdots+a_dX^d\) has coefficients \(a_j\); its degree is the largest index of a nonzero coefficient. A root is an input \(r\) for which \(f(r)=0\).</p>
<p>A nonzero degree-\(d\) polynomial has at most \(d\) distinct roots over a field. The reason is that a root \(a\) gives a factor \(X-a\). Any different root must belong to the remaining factor, since \(b-a\ne0\) can be cancelled. Each new root therefore consumes another degree.</p>
<p>The zero polynomial, whose coefficients are all zero, is the exception: it is zero everywhere. Also, arithmetic modulo a composite number need not permit cancellation. Use the earlier homework question next to check that condition before using the theorem.</p>
''','Chapter 3 prerequisite; HW3 1(c); HW4 2',['offline-online'],['hw3:1c'])

card('coefficient-shift','A degree bound turns a random check into evidence',r'''
<p>Fix two polynomials of degree at most \(d\) before choosing a uniform random field point \(r\). If the polynomials differ, their difference is nonzero and has at most \(d\) roots. Thus checking equality at \(r\) misses a false identity with probability at most \(d/|\mathbb F|\), capped at 1.</p>
<p>HW4 supplies an <strong>ideal polynomial oracle</strong>: once a polynomial and degree bound are fixed, every query returns an evaluation of that same bounded-degree polynomial. Without that promise, a prover could invent a convenient value after seeing \(r\). A large field compared with \(d\) makes the error small; the two-element field used in bit PIR would generally be too small for this test.</p>
<figure class="learning"><figcaption>A multiplication that shifts positions</figcaption><div class="pir-flow"><span>g(X) = b₀ + b₁X + b₂X²</span><span>Multiply by Xⁱ</span><span>Xⁱg(X) = b₀Xⁱ + b₁Xⁱ⁺¹ + b₂Xⁱ⁺²</span></div></figure>
<p>Each coefficient moves up by exactly \(i\) positions. No term below position \(i\) remains. This will let the prover express “these low coefficients are zero” as an identity that the verifier can test.</p>
''','HW4 2(a); Chapter 3 random identity test',['field-review'],['2a'])

card('coefficient-split','Give the target coefficient a position nobody else can occupy',r'''
<p>To certify one coefficient, reserve its degree position and constrain the remaining pieces to lie on either side. The indices count powers, starting with the constant term at position 0.</p>
<figure class="learning"><figcaption>Three disjoint degree ranges</figcaption><div class="pir-flow"><span>Lower part: positions 0 through i − 1</span><span>Claimed coefficient β: position i</span><span>Upper part: positions i + 1 through d</span></div></figure>
<p>A polynomial with degree at most \(i-1\) cannot change position \(i\). A polynomial multiplied by \(X^{i+1}\) cannot change any lower position. These restrictions make a false claim at the reserved position impossible to conceal in the side pieces.</p>
<p>The next exercise asks you to specify those side polynomials, their degree bounds and the random evaluation check. For an endpoint coefficient, one side is empty and is represented by the zero polynomial.</p>
''','HW4 2(b)',['coefficient-shift'],['2b'])

card('product-coefficient','Multiplication groups terms by the sum of their degrees',r'''
<p>When multiplying polynomials, multiply every term of the first by every term of the second, then collect equal powers. A product \((a_jX^j)(b_kX^k)\) becomes \(a_jb_kX^{j+k}\).</p>
<p>To obtain coefficient \(d\), select exactly the pairs whose indices sum to \(d\): \((0,d),(1,d-1),\ldots,(d,0)\). Their contribution is</p>
\[a_0b_d+a_1b_{d-1}+\cdots+a_db_0.\]
<p>This is the inner product of the first coefficient list with the <em>reversed</em> second list. The largest possible exponent in the whole product is \(d+d=2d\).</p>
<p>To prove a claim about that middle coefficient, an auxiliary polynomial must satisfy two requirements: it really is the product, and its middle coefficient really is the claimed value. A coefficient check on an unrelated polynomial would establish neither fact about the original pair.</p>
''','HW4 2(c)',['coefficient-split'],['2c'])

card('proof-models','Midterm check: identify the guarantee and the model',r'''
<p>The preceding tests work because a false polynomial identity has few roots. That conclusion holds even against unlimited computation, as long as the polynomials were fixed with the enforced degree limits. Cryptographic commitments are a separate mechanism for implementing that ideal interface.</p>
<table><thead><tr><th>Property</th><th>Meaning</th></tr></thead><tbody><tr><td>Completeness</td><td>Honest proofs of true claims pass.</td></tr><tr><td>Soundness</td><td>False claims pass only with bounded probability.</td></tr><tr><td>Knowledge</td><td>A sufficiently successful prover permits extraction of a valid witness.</td></tr><tr><td>Zero knowledge</td><td>The verifier's view can be simulated without the witness.</td></tr></tbody></table>
<p>A relation \(R(x,w)=1\) says that witness \(w\) establishes public statement \(x\). Knowledge error is the success threshold above which an efficient extractor must recover such a witness, using its prescribed interaction with the prover. A false statement has no valid witness to extract.</p>
<p>First use HW3 1(a) to distinguish knowledge from soundness. Then apply the separation between ideal oracles and computational implementations to HW4 1(a). Neither exercise claims that every sound proof automatically hides its witness.</p>
''','Chapter 3 prerequisite; HW3 1(a); HW4 1(a)',['product-coefficient'],['hw3:1a','1a'])

card('succinctness-review','Midterm check: proof length and verifier time are different',r'''
<p>A SNARG is a succinct non-interactive argument. The lecture asks for a short proof <em>and</em> fast verification, allowing the verifier to read the public input:</p>
\[T_V=O(|x|)+\operatorname{poly}(\lambda,\log|w|).\]
<p>Vertical bars mean the bit length of a string. The notation “poly” allows fixed powers of its arguments. The bound is more specific than “some polynomial in the statement length”. A cubic-time decider is efficient in the complexity-class sense, but is not thereby a nearly linear-time verifier.</p>
<p>If \(\mathrm P=\mathrm{NP}\), an NP statement can be decided without a prover's message. That supplies an empty proof. Before calling it a SNARG under this definition, ask how much work the verifier's decision algorithm performs. This is the distinction the next conceptual question is testing.</p>
''','Chapter 3 succinctness; HW4 1(d)',['proof-models'],['1d'])

card('powers-setup','Public powers let us encode a polynomial evaluation',r'''
<p>A group \(G\) of prime order \(p\) contains \(p\) elements. A generator \(g\) reaches them all as \(g^0,\ldots,g^{p-1}\). Group multiplication adds exponents; raising a group element to a known scalar multiplies its exponent:</p>
\[g^a g^b=g^{a+b},\qquad (g^a)^t=g^{at}.\]
<p>Exponents are calculated modulo \(p\). The identity element is \(g^0=1\), and a negative exponent means a group inverse. Finding \(a\) from \(g^a\) is the discrete-logarithm problem. An efficiently computable group operation does not imply this inverse problem is easy.</p>
<p>The setup in HW4 chooses a hidden nonzero field element \(\alpha\) and publishes</p>
\[g,\ g^\alpha,\ g^{\alpha^2},\ldots,g^{\alpha^d}.\]
<p>Each item is a group element, not the exponent written above it. The prover knows its polynomial coefficients and can use the two power rules to combine these items. Parts 3(a–b) ask what this allows it to compute, and what security can—and cannot—follow from that encoding.</p>
''','HW4 3(a–b); Chapter 1 group prerequisites',['succinctness-review'],['3a','3b'])

card('point-quotient','An evaluation claim becomes divisibility by X − z',r'''
<p>In this part of HW4, \(z\) names the point to open and \(y\) the claimed value. This changes the role of \(z\) from the earlier inner-product exercise, where it named a claimed scalar result.</p>
<p>Polynomial division gives</p>
\[f(X)-y=(X-z)q(X)+r_0,\]
<p>where the remainder \(r_0\) is a constant because the divisor has degree 1. Substituting \(X=z\) cancels the product term and yields \(r_0=f(z)-y\). Thus the opening is valid exactly when this remainder is zero.</p>
<figure class="learning"><figcaption>The link to the earlier ZeroTest</figcaption><div class="pir-flow"><span>Claim f(z) = y</span><span>↓ f − y vanishes on the one-point set {z}</span><span>Vanishing polynomial is X − z</span><span>↓ f − y is divisible by X − z with no remainder</span></div></figure>
<p>The quotient identity connects the opening claim to a multiplication relation that can later be checked in the exponent. It is an identity between polynomials, so evaluating the written fraction at its root is unnecessary.</p>
''','HW4 3(c); Chapter 3 ZeroTest',['powers-setup'],['3c'])

card('exponent-product','A product check needs a stronger group interface',r'''
<p>From \(g^a\) and \(g^b\), ordinary group multiplication gives \(g^{a+b}\), not \(g^{ab}\). HW4 therefore supplies an extra operation: \(\operatorname{VerifProd}(g^a,g^b,g^c)\) decides whether \(c=ab\). It checks the relation without revealing the three exponents.</p>
<p>This makes the <strong>decisional Diffie–Hellman</strong> (DDH) relation easy to test in that group. Recovering an exponent is still a different problem. The exercise invokes groups where this product test is efficient while appropriate computational hardness assumptions remain plausible; its footnote connects them to pairings, specialized group operations that can test such exponent relations. No pairing formula is needed to use the supplied interface.</p>
<figure class="learning"><figcaption>What the opening verifier will connect</figcaption><div class="pir-flow"><span>Commitment encodes f(α)</span><span>Opening proof encodes q(α)</span><span>Setup and public z give an encoding of α − z</span><span>Public y lets us subtract y in the exponent</span></div></figure>
<p>The next two exercises turn that diagram into a verification algorithm, then show how a hypothetical exponent-division capability would defeat it. Keep public group elements separate from their hidden exponents throughout the derivation.</p>
''','HW4 3(d–e)',['point-quotient'],['3d','3e'])

assert sum(c['kind']=='theory' for c in CARDS)==28
assert len(CARDS)==45
