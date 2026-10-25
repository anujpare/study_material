"""Targeted second-pass corrections; preserve original card IDs and SVG formulas."""
import re
from html import unescape

# These cards supply the full definition in their teaching prose. A glossary
# containing the same definition above that prose would repeat the explanation.
SELF_DEFINED = {
 ('commitment',7): {'witness'},
 ('commitment',34): {'modular'},
 ('commitment',47): {'homomorphic'},
 ('commitment',56): {'prf'},
 ('commitment',61): {'fhe'},
 ('commitment',79): {'vector'},
 ('zero-knowledge',33): {'hvzk'},
 ('zero-knowledge',49): {'fiat'},
}

EDITS = {
 ('commitment',7): [
  ('For example, a completed puzzle', 'For a cryptographic example, ask whether a secret key explains observed input/output pairs. A proposed key is a witness: evaluating the function at the listed inputs checks it efficiently. Finding such a key may still be difficult. NP does not mean “not polynomial.”'),
 ],
 ('zero-knowledge',13): [
  ('Suppose a verifier claims', 'Fix one public statement with two valid witnesses whose tested bits are 0 and 1. Choose either witness with equal probability, then produce its proof transcript. Suppose a verifier predicts the chosen bit with probability 1/2 plus a non-negligible advantage. Show how this would distinguish genuine transcripts from simulator transcripts.'),
  ('Feed the claimed extraction test', 'Feed the claimed bit-prediction test either a genuine or a simulated view and record its output.'),
  ('Since the simulator uses only the public statement', 'The public statement is the same for both chosen witnesses. The simulator receives that statement, but not the independently selected bit. Its output is therefore independent of which of the two witnesses was chosen.'),
  ('To construct that distinguisher,', 'The distinguishing experiment knows both witnesses and chooses one with a fair random bit. It obtains the corresponding real transcript or a simulated transcript and checks whether the prediction equals that bit. The simulated branch has success probability 1/2 because its transcript is independent of this balanced choice. The real branch has the claimed larger success probability.'),
 ],
 ('zero-knowledge',35): [
  ('Composing Sigma protocols:', 'Parallel composition batches the first messages, then the challenges, then the responses. For an honest verifier, independent single-copy simulations give the required joint transcript distribution. With computational HVZK, justify this by replacing one copy at a time; polynomially many indistinguishable changes remain indistinguishable.'),
  ('Against an honest verifier whose challenge vector', 'This simulation argument concerns the honest verifier’s challenge distribution. A malicious verifier may choose challenges jointly as a function of all first messages, which the component-wise argument does not reproduce.'),
  ('For arbitrary malicious verifiers,', ''),
 ],
 ('zero-knowledge',48): [
  ('Thus, for general hard NP problems,', 'For hard NP languages, this plain-model obstacle motivates additional resources. A common reference string (CRS) is public setup information generated before proofs begin. A random oracle is an ideal function available through queries. Either can change the model, but its security theorem must specify the simulator’s extra capabilities. “Standard model” excludes a random oracle; it does not necessarily exclude a CRS.'),
 ],
 ('zero-knowledge',40): [
  ('For sequential independent soundness challenges,', 'For sequential repetitions, condition on the complete preceding history. If every next round still has acceptance probability at most 1/2 on a false statement, multiplying those conditional bounds gives 2<sup>−λ</sup>. This reasoning does not assume the malicious prover uses independent strategies. Exponential decay is negligible because it eventually beats every inverse fixed power.'),
 ]
}
def plain(s): return ' '.join(unescape(re.sub('<[^>]*>',' ',s)).split())
def refine(deck, number, content):
 for prefix,replacement in EDITS.get((deck,number),[]):
  # New text no longer matches old prefix unless it is deliberately an idempotent rule.
  content=re.sub(r'<p\b[^>]*>.*?</p>',lambda m:('<p>'+replacement+'</p>' if replacement else '') if plain(m[0]).startswith(prefix) else m[0],content,flags=re.S)
 return content
