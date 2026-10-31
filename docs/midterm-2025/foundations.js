/* Beginner prerequisites for the PETS 2025 midterm. */
window.MIDTERM_FOUNDATIONS = {
  "1a": [
    [
      "What a security proof actually says",
      "A security proof starts with an assumption and shows that an attacker cannot achieve some forbidden goal while the assumption holds. If the assumption changes, the same argument may stop working; this does not automatically mean the goal becomes achievable."
    ],
    [
      "Two very different hash guarantees",
      "An ideal random oracle gives a fresh unpredictable answer for a previously unseen input, then repeats that answer on later queries. Collision resistance only makes finding different inputs with the same hash difficult. It does not promise unpredictability or independence."
    ],
    [
      "How to judge this TRUE/FALSE statement",
      "The exam asks whether a missing proof guarantees an attack. It does not. To call a real implementation insecure, we would need an actual attack or another reason establishing insecurity."
    ]
  ],
  "1b": [
    [
      "Claim, witness, and verifier",
      "A <b>claim</b> is something to be proved. For example, “15 has a nontrivial factor.” A <b>witness</b> is 3, because 15 = 3 × 5. The <b>verifier</b> checks the witness efficiently without searching for it."
    ],
    [
      "What extraction adds",
      "A proof of knowledge requires an <b>extractor</b>: a special algorithm that can recover a valid witness from a prover that convinces the verifier often enough. This is a property of the prover, not a privacy guarantee."
    ],
    [
      "What simulation adds",
      "Zero knowledge asks whether the verifier could have seen an equally plausible conversation without receiving the witness. Its <b>simulator</b> produces that view. If the prover simply sends 3, extraction is easy but the secret is exposed."
    ],
    [
      "Why the knowledge-error qualifier matters",
      "Knowledge error κ is a threshold: when a prover convinces the verifier with probability greater than κ, the proof-of-knowledge property requires an efficient extractor to obtain a witness. Negligible κ makes this exceptional threshold tiny as the security parameter λ grows; it says nothing about hiding the witness."
    ]
  ],
  "1c": [
    [
      "First, a commitment",
      "A commitment is a fixed value published now that binds the sender to some hidden data. An <b>opening</b> later proves a claimed value. For a polynomial commitment, the data is a polynomial and an opening can prove the value at one chosen input."
    ],
    [
      "A vector can be represented by polynomial values",
      "Take the two-entry vector <code><b>v</b> = [2,5]</code> over arithmetic modulo 7. The degree-one polynomial <code>f(X) = 3X − 1</code> gives <code>f(1) = 2</code> and <code>f(2) = 5</code> after taking remainders modulo 7."
    ],
    [
      "Why d entries need degree at most d − 1",
      "A line (degree 1) can match two specified values; a quadratic (degree 2) can match three. More generally, d distinct input positions determine one polynomial of degree at most d − 1 over a field. We can therefore commit to the vector by committing to that polynomial."
    ]
  ],
  "1d": [
    [
      "An encrypted value and its location are separate",
      "Imagine a server stores ciphertext at addresses 1, 2, 3, and 4. Encryption hides the value stored at address 4, but a request saying “read address 4” still exposes which location was read."
    ],
    [
      "Why two programs remain distinguishable",
      "One program requests <code>4 → 4 → 2</code>; another requests <code>1 → 3 → 1</code>. Even with perfectly hidden contents, the server sees the different address sequences. ORAM aims to prevent this kind of distinction."
    ]
  ],
  "1e": [
    [
      "Reconstruction is only half of secret sharing",
      "A correct secret-sharing scheme must rebuild the secret from sufficient shares. A private scheme must also keep an unauthorized subset from learning anything about the secret. These are separate requirements."
    ],
    [
      "Look at the digits of 11",
      "In base 4, <code>11 = 3 + 2 × 4</code>. If party 1 receives digit 3, it learns that the secret is among <code>{3,7,11,15}</code>, even before speaking to party 2. That is already information leakage."
    ],
    [
      "Contrast with properly randomized shares",
      "For a secret α = 7 modulo 11, choose the first share uniformly at random, say <code>s₀ = 4</code>, and set <code>s₁ = (7 − 4) mod 11 = 3</code>. Their sum restores 7; the first share alone is uniformly random regardless of α."
    ]
  ],
  "2a": [
    [
      "What set intersection means",
      "A set is a collection with no duplicates. If <code>A = {1,3}</code> and <code>B = {3,4}</code>, the intersection <code>A ∩ B = {3}</code> contains only the elements present in both sets."
    ],
    [
      "The protocol sees sets, not YES/NO answers",
      "PSI accepts sets from both participants and reveals their intersection. We therefore choose the sets so their intersection reveals exactly the desired result. A shared marker <code>1</code> means YES; an empty set means NO."
    ],
    [
      "Check all four cases",
      "YES/YES gives <code>{1} ∩ {1} = {1}</code>. YES/NO, NO/YES, and NO/NO all give the empty intersection. Thus nothing in the output distinguishes those three NO cases."
    ]
  ],
  "2b": [
    [
      "Define the universe X",
      "The universe <code>X</code> is the list of every allowed element. For example, <code>X = {a,b,c,d}</code>. Any legal input set is a subset of X."
    ],
    [
      "What the upper bound permits",
      "If the maximum permitted size is <code>N = |X| = 4</code>, Alice is allowed to supply all four elements, <code>A = X</code>. With Bob's set <code>B = {b,d}</code>, their intersection is exactly <code>{b,d}</code>."
    ],
    [
      "Why this is not a broken encryption scheme",
      "PSI intentionally reveals the intersection. When Alice chooses the whole universe, that authorized output equals Bob's input. Privacy guarantees cannot hide information that the prescribed output itself reveals."
    ]
  ],
  "2c1": [
    [
      "Why matching the same input is easy",
      "A hash function always gives the same output on the same input. If both parties contain an element a, Bob sends H(a) and Alice computes exactly H(a), so the shared element is included."
    ],
    [
      "What could cause a false match",
      "Different elements may have an identical hash; that is a <b>collision</b>. If a random hash has λ output bits, there are 2<sup>λ</sup> possible outputs, so two particular distinct inputs collide with probability 1/2<sup>λ</sup>."
    ],
    [
      "From one pair to any pair",
      "The <b>union bound</b> says: the probability that any bad event occurs is at most the sum of the individual event probabilities. There are at most <code>|X|(|X|−1)/2</code> unordered pairs of different elements, giving the bound in the solution. Polynomially many pairs cannot offset the exponentially small probability."
    ]
  ],
  "2c2": [
    [
      "The meaning of semi-honest",
      "A semi-honest participant sends the prescribed messages but may make any additional efficient computation using everything it has received. Alice can hash other elements locally because H is public."
    ],
    [
      "Compare two worlds with the same legitimate output",
      "Let <code>A = {a,d}</code>. Bob may hold <code>B₀ = {a,b}</code> or <code>B₁ = {a,c}</code>. In either world, Alice should learn only <code>A ∩ B = {a}</code>. The set sizes are also identical."
    ],
    [
      "Why Alice can nevertheless tell",
      "Alice evaluates H(b) and checks if it appears in Bob's sent hash set. Except for a collision, the answer is YES with B₀ and NO with B₁. An ideal simulator given only Alice's set and the intersection cannot tell these worlds apart, so Bob's privacy fails."
    ],
    [
      "Why Bob does not learn Alice's other elements",
      "Bob receives Alice's final intersection, plus messages he generated himself. A simulator that knows Bob's input and that intersection can reproduce his view without knowing the rest of A. That establishes Alice's semi-honest privacy."
    ]
  ],
  "2d1": [
    [
      "The vulnerability we must repair",
      "With a public hash, Alice can evaluate H(z) for any unsubmitted z, which allows her to test Bob's hidden elements. We need values that she cannot calculate freely."
    ],
    [
      "A PRF is a keyed function",
      "A pseudorandom function is written <code>F(k,x)</code>: the server chooses secret key k, and someone who does not know k cannot predict the value at an unqueried input. The output looks like a random function's output to an efficient observer."
    ],
    [
      "The extra service an OPRF provides",
      "An oblivious PRF lets Alice learn <code>F(k,a)</code> for her own a without showing a to Bob, while Bob keeps k secret. Alice still obtains exactly the PRF values required to check whether an element belongs to the intersection."
    ],
    [
      "Read the repaired protocol as four actions",
      "Bob chooses k; Bob sends the keyed values of B; Alice makes one OPRF evaluation per element of A; Alice returns the elements whose keyed values match. The rest of the solution just proves these actions work."
    ]
  ],
  "2d2": [
    [
      "A participant's view is more than its received messages",
      "For Bob, the view contains his own input B, his secret key k and random coins, outgoing messages, server-side OPRF transcripts, and the final intersection I. We must simulate all these pieces."
    ],
    [
      "What the simulator is allowed to know",
      "To prove Alice's privacy, the simulator gets <code>(N, B, I)</code> and no other part of A. This forces the proof to show that Bob's real messages did not secretly depend on Alice's nonintersection elements."
    ],
    [
      "Why the OPRF simulator is the crucial piece",
      "The OPRF client-privacy definition already guarantees simulated server transcripts using only the server key k and the number of client queries q. Here the fixed-size condition gives exactly <code>q = N</code>, so we can simulate those N interactions without Alice's elements."
    ]
  ],
  "2e": [
    [
      "What the group notation means",
      "A <b>cyclic group</b> has a generator g: every element can be written as g raised to some exponent. <b>Order p</b> means the group has p elements. The exponent rule <code>(g^r)^k = g^(rk)</code> makes blinding reversible, and exponents are reduced modulo p. The exam lets us assume the PRF is secure, so we do not need to prove the DDH assumption implies it."
    ],
    [
      "Why a modular inverse exists",
      "For nonzero r modulo prime p, there is a number r<sup>−1</sup> satisfying <code>r × r<sup>−1</sup> ≡ 1 (mod p)</code>. Example: with p = 11 and r = 3, the inverse is 4 because <code>3 × 4 = 12 ≡ 1 (mod 11)</code>."
    ],
    [
      "Walk through the blinding algebra",
      "Alice sends <code>U = H(x)^r</code>. Bob returns <code>V = U^k = H(x)^(rk)</code>. Alice raises V to r<sup>−1</sup>, obtaining <code>H(x)^(rk r<sup>−1</sup>) = H(x)^k</code> because <code>r r<sup>−1</sup> ≡ 1</code>."
    ],
    [
      "What privacy simulation must recreate",
      "Bob should see no clue about x: raising a nonidentity group element to uniform nonzero r distributes U uniformly among nonidentity elements. Alice should learn only her permitted PRF output; the client-view simulator can choose a dummy key and rebuild a consistent transcript backwards."
    ],
    [
      "How programming the random oracle helps",
      "In the Random Oracle Model, a simulator may select the oracle answer at an input that has not already been fixed, allowing it to build a consistent transcript backwards. There is one rare special case for <b>client-input privacy</b>: H(x) might be the group's identity element, in which case blinding does not hide it. This event has probability 1/p per new hash value."
    ]
  ],
  "3a": [
    [
      "Represent the tally as a vector",
      "With three candidates, <code><b>v</b> = [0,0,0]</code> means nobody has voted. A vote for candidate 2 adds <code><b>e</b>₂ = [0,1,0]</code>, resulting in <code>[0,1,0]</code>. Multiple voters add their contribution coordinate by coordinate."
    ],
    [
      "How two servers hold one hidden tally",
      "Let p = 11 and the tally be <code>[0,1,0]</code>. Server S₀ could hold <code>[4,8,2]</code> and S₁ hold <code>[7,4,9]</code>. Add corresponding entries modulo 11: <code>[0,1,0]</code>. Neither individual vector reveals which candidate was chosen."
    ],
    [
      "Read the question as a private write",
      "The voter must modify exactly one candidate's count, but must not tell either server which position to change. PIR is designed for private reading; a SNARG checks a claim. We still need a way to write a secret one-position update."
    ]
  ],
  "3b1": [
    [
      "The point function we want to split",
      "For candidate 2 among three candidates, the function should output zero at positions 1 and 3 and one at position 2. Evaluating it everywhere produces the vector <code>[0,1,0]</code>."
    ],
    [
      "What the DPF keys represent",
      "The voter runs <code>Gen(2,1)</code> and sends one short key to each server. Each server evaluates its own key for every candidate j. The two results add to the required point-function value, although either key alone hides the chosen candidate."
    ],
    [
      "A numerical example of the evaluation outputs",
      "Over arithmetic modulo 11, servers might reconstruct <code>[3,8,1] + [8,4,10] = [0,1,0]</code>. This only illustrates how the evaluated shares add; real DPF keys are shorter encodings, not these entire arrays."
    ],
    [
      "Why the communication is small",
      "If each key has ℓ bits, the voter sends <code>ℓ + ℓ = 2ℓ</code> bits. Every N-entry vector is built locally by a server. This is the difference between sending a short function key and sending an N-entry vector."
    ],
    [
      "Privacy by simulation",
      "A DPF key seen by one server looks computationally indistinguishable from a key simulated without the target index. Repeat the one-key simulator for every voter; reveal the final public tally separately as the voting definition allows."
    ]
  ],
  "3b2": [
    [
      "What an honest vote should encode",
      "For one vote, the point function is zero at every candidate except one position, where its value must be exactly 1. Correctness of the DPF guarantees the result matches whatever value was passed into Gen."
    ],
    [
      "What an attacker changes",
      "A malicious voter can call <code>Gen(i,M)</code> rather than <code>Gen(i,1)</code>. If M exceeds the maximum possible number of honest votes and is small enough to avoid wraparound modulo p, that single update dominates every other candidate."
    ]
  ],
  "3c1": [
    [
      "Learn the dot product with numbers",
      "For vectors <code><b>x</b> = [1,0]</code> and <code><b>r</b> = [2,5]</code>, their inner product means multiply matching coordinates and add: <code>〈<b>x</b>,<b>r</b>〉 = 1×2 + 0×5 = 2</code>. Squaring the result gives 4."
    ],
    [
      "A valid vote always passes the test",
      "For <code><b>x</b> = [1,0]</code>, the left side is <code>2² = 4</code>. The right side is <code>1×2² + 0×5² = 4</code>. The same calculation works for any chosen random vector because exactly one coordinate of x is 1."
    ],
    [
      "An invalid vector can fail",
      "Try <code><b>x</b> = [1,1]</code>, <code><b>r</b> = [2,5]</code>, and p = 11. The left side is <code>(2+5)² mod 11 = 5</code>; the right side is <code>(2²+5²) mod 11 = 7</code>. Since 5 ≠ 7, this random challenge rejects the cheating vector."
    ],
    [
      "Why randomness turns this into a proof",
      "For a fixed invalid x, subtract the right side from the left: this is a polynomial f in the random coordinates. <b>Nonzero polynomial</b> means at least one coefficient is nonzero; it may still evaluate to zero on some inputs. The <b>Schwartz–Zippel lemma</b> says that a nonzero polynomial of total degree at most d, evaluated at independent uniform field values, equals zero with probability at most d/p. Here d = 2."
    ],
    [
      "Why the field characteristic matters",
      "The proof uses the coefficient <code>2xᵢxⱼ</code> when two vote coordinates are nonzero. It is nonzero for odd prime p. In characteristic 2, this coefficient vanishes and the stated test does not have the claimed soundness guarantee."
    ]
  ],
  "3c2": [
    [
      "What a 'language' means here",
      "In proof systems, a <b>language L</b> is simply the collection of allowed inputs. Here L consists of the N possible vectors with exactly one 1 and all other coordinates 0, such as <code>[0,1,0]</code>. The all-zero vector is <b>not</b> allowed for this final voting check."
    ],
    [
      "What changes from the previous exercise",
      "Question (c.1) checked a simple equation but did not hide the vote. Now the vote vector x and the proof vector π are shared across two servers, and the verifier must work without reconstructing either secret vector."
    ],
    [
      "Concatenating vectors",
      "The notation <code><b>x</b> ∥ <b>π</b></code> means putting the entries of x immediately before the entries of π. If x has N entries and π has M, their concatenation has N + M entries. Every linear query q has exactly this length."
    ],
    [
      "Linearity is the trick",
      "With p = 11, take the hidden combined vector <code>[0,1,2]</code> split into <code>[4,3,7]</code> and <code>[7,9,6]</code>. For query <code><b>q</b> = [1,3,2]</code>, the servers get local inner products 5 and 2 modulo 11. Their sum 7 equals the direct inner product <code>0×1 + 1×3 + 2×2 = 7</code>."
    ],
    [
      "The privacy simulator in ordinary arithmetic",
      "Suppose the simulated full answer to a linear query is 7 modulo 11, while server S₀'s own answer is 5. A simulator can invent the other server's answer as <code>(7 − 5) mod 11 = 2</code>. The pair of answers is consistent, yet the simulator never needed the hidden vote or proof."
    ],
    [
      "Why a common seed is enough",
      "The IOP verifier's deterministic query algorithm Q accepts one randomly selected λ-bit seed r and produces k query vectors. The servers agree on r, independently compute the same queries, and exchange only k field values each, not all N + M hidden coordinates."
    ],
    [
      "Exactly what the final proof must establish",
      "Completeness: every honest one-hot vote is accepted. Soundness: an invalid vote cannot be accepted except with negligible probability. Zero knowledge: the validation transcript can be simulated without revealing which one-hot vector was submitted. The correction is crucial: the verifier makes <b>k</b> queries, not necessarily three."
    ]
  ]
};
