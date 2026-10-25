"""Protocol diagrams placed inside worked solutions, never before the attempt."""
from teaching_visuals import protocol,path
EARLIER_VISUALS={'commitment':{},'zero-knowledge':{}}
EARLIER_VISUALS['commitment'][26]=protocol('hw-xor','One published value, two accepted openings','Sender','Receiver','Publishes c = 1001.','Retains that same c for both checks.',[
 ('left','m = 0011, r = 1010','The XOR is 1001, so this opening passes.'),
 ('left','Alternatively: m′ = 1100, r′ = 0101','This XOR is also 1001. The sender can compute a valid randomizer for either message.')])
EARLIER_VISUALS['commitment'][75]=protocol('hw-ddh-single','The table makes both interfaces consistent','Reduction B','PRF adversary A','Receives X,Y,Z and stores one fresh shift per input.','Can ask many hash queries and one PRF query.',[
 ('right','A new hash input mᵢ','B samples a fresh rᵢ only when the input is new.'),
 ('left','H(mᵢ) = Xgʳⁱ','B returns this stored answer on every repetition.'),
 ('right','The single PRF query mⱼ','B retrieves the shift associated with this same input.'),
 ('left','ZYʳʲ','In the real case this equals H(mⱼ)ᵝ; in the random case the one response is uniform.')])
EARLIER_VISUALS['zero-knowledge'][45]=path('Compare the generation order, not only the final equation',[
 'Real run: sample r, send u = gʳ, receive uniform c, and compute z = r + cx.',
 'Simulator: sample independent uniform c,z, then calculate u = gᶻh⁻ᶜ from the public equation.',
 'For fixed c, uniform r makes the real z uniform. Thus both methods give the same pair distribution for c,z.',
 'The equation uniquely determines u from that pair, so the whole transcript distribution agrees.'])
EARLIER_VISUALS['zero-knowledge'][46]=protocol('hw-schnorr-extract','Rewind after u so the unknown r is shared','Extractor','Prover program','Keeps both accepted responses.','Has sent u = gʳ and saved its state.',[
 ('left','Challenge c = 2','The first branch produces response z = 0 in the example.'),
 ('right','Response z = 0','The verifier’s equation accepts.'),
 ('local-left','Restore the state after u','The next response must use that same first message.'),
 ('left','Challenge c′ = 5','The second branch produces z′ = 1.'),
 ('right','Response z′ = 1','Subtracting cancels r: −1 = −3x modulo 11.'),
 ('local-left','x = 10 · 8⁻¹ = 10 · 7 = 4 mod 11','The inverse exists because the challenges differ modulo prime 11.')])
EARLIER_VISUALS['zero-knowledge'][57]=protocol('hw-circuit','The composed circuit proof has three message batches','Prover','Verifier','Knows a satisfying wire assignment and commitment openings.','Knows the circuit and the supplied gate-proof protocols.',[
 ('left','All wire commitments and first gate-proof messages','One commitment is reused wherever the same wire occurs.'),
 ('right','Independent random challenges for every gate proof','All gate challenges arrive in one batch.'),
 ('left','All gate responses and the final output opening','The final commitment is opened to 1.'),
 ('local-right','Check every gate proof and the output opening','Acceptance requires all checks, with the same wire commitments throughout.')])

LATER_VISUALS={'hw3':{},'hw4':{}}
LATER_VISUALS['hw3']['2a']=protocol('hw3-schnorr-fs','The proof omits the reproducible challenge','Prover','Verifier','Knows x with h = gˣ and chooses fresh r.','Knows h and the public parameters.',[
 ('local-left','u = gʳ; c = H(h,u); z = r + cx','The first message is fixed before its hash challenge is evaluated.'),
 ('left','π = (u,z)','These two values are the transmitted proof.'),
 ('local-right','Recompute c, then test gᶻ = uhᶜ','The verifier does not choose a new challenge or receive x.')])
LATER_VISUALS['hw3']['4a']=protocol('hw3-pcp','Commit before the verifier selects positions','Prover','Verifier','Retains the encoded PCP string and Merkle tree.','Knows the PCP test for the public statement.',[
 ('left','One Merkle root','The proof bits are now bound to their positions.'),
 ('right','All positions for λ independent tests','The requested positions are chosen before their bits are seen.'),
 ('left','Requested bits with their Merkle paths','Each answer must authenticate to the previously sent root.'),
 ('local-right','Verify paths and apply every PCP predicate','Both authenticity and the logical tests are necessary.')])
LATER_VISUALS['hw4']['2b']=protocol('hw4-coefficient','The random point comes after all degree-bounded oracles','Prover','Verifier','Has f and proposes the lower and upper pieces.','Knows the claimed coefficient β and its position i.',[
 ('left','Fix f, fL, fR in the ideal oracle','Their degree limits prevent the side pieces from changing coefficient i.'),
 ('local-right','Sample uniform r and query the three values','The fixed-polynomial promise rules out adapting the pieces to r.'),
 ('local-right','Test f(r) = fL(r) + βrⁱ + rⁱ⁺¹fR(r)','If the claim is false, this equality can hold at only a degree-bounded number of field points.')])
LATER_VISUALS['hw4']['3d']=protocol('hw4-pcs-opening','The verifier handles encoded exponents','Prover','Verifier','Retains f and forms q = (f − y)/(X − z).','Knows c_f, z, y and the public setup powers.',[
 ('left',r'\(\pi=g^{q(\alpha)}\)','The prover computes this encoding from q’s coefficients and the public powers.'),
 ('local-right','A = π; B = g^α / g^z; C = c_f / g^y','The verifier obtains three group elements without recovering their exponents.'),
 ('local-right','Check that the exponent of C is the product of those of A and B','The supplied product interface and its identity-element cases implement this check.')])
LATER_VISUALS['hw4']['4b']=protocol('hw4-fhe-pir','Only the client decrypts the chosen database bit','Client','Server','Knows the requested index and keeps the secret key.','Holds X and the public evaluation material.',[
 ('left','Encryptions of the address bits, 0 and 1','Fresh randomness hides the joint collection of encrypted inputs.'),
 ('local-right','Evaluate equality, masking and the final OR','The server computes on ciphertexts for every record.'),
 ('right','One ciphertext encrypting Xᵢ','Compactness keeps the response size independent of the entire circuit.'),
 ('local-left','Decrypt with the retained key','Correct homomorphic evaluation yields the requested bit.')])
