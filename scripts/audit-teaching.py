"""A review disposition for every current card, with explicit source limits."""
from pathlib import Path
import json,re,sys
from undergraduate_content import REVISIONS,MERGED
from later_teaching import NEW,EDITS
from deck_catalog import ROOT,DECKS
notes={
'snarks':{
'proof-properties':'Keep soundness, knowledge error and privacy distinct; the recap supports HW3 1(a).',
'setup-models':'Retain the simulator capability difference between plain, CRS and random-oracle models.',
'fiat-shamir':'Keep the challenge timing, whole-context hash and privacy limitation before the three assigned questions.',
 'transferability':'Explain why a simulated recording does not attest live challenge timing, while NIZK has public verification.',
 'challenge-search':'Retain the nonidentity h condition and count tested challenges rather than invoking unexplained hardness.',
 'parallel-amplification':'Retain the fixed-first-message argument; no independence assumption on malicious prover strategies.',
 'merkle-oracle':'Explain how each missing sibling lets verification advance one level; authentication does not establish the PCP predicate.',
 'pcp-cost':'Retain message-by-message bit costs and distinguish succinct communication from fast verification.',
 'pcp-fiat-shamir':'Retain derivation of queries from fixed root, domain separation and the scope of the compiled guarantee.',
 'finite-fields':'Retain the inverse/cancellation property needed by the root proof, including the composite-modulus counterexample.',
 'root-bound':'Retain the factorization proof; show explicitly where field cancellation is needed.',
 'polynomial-equality':'Retain the difference-polynomial argument, degree limit and fix-before-challenge condition.',
 'schwartz-zippel':'Teach total degree and independent sampling from a common finite subset without elementary polynomial vocabulary.',
 'interpolation':'Retain the Lagrange-basis existence and root-bound uniqueness argument; remove explanations of sum/product symbols.',
 'vanishing-polynomial':'Keep the equivalence between zeros on a set and a polynomial quotient, with a concrete factorization.',
 'fibonacci-iop':'Retain the seven queried values, same-polynomial consistency, indexing correction and verifier-work limitation.',
 'arithmetic-circuit':'Retain the actual circuit diagram and distinguish the displayed output 56 from zero-normalized relation.',
 'execution-trace':'Retain the repeated-wire example that motivates constraints beyond local gate arithmetic.',
 'roots-of-unity':'Retain primitivity, twelve distinct addresses and the counterexample omega=1.',
 'trace-polynomial':'Retain the address/value distinction and explain why interpolation alone accepts dishonest tables too.',
 'four-obligations':'Retain independently failing scenarios; each illustrates why one of the four checks is necessary.',
 'boundary-conditions':'Retain public/private-input separation and authentication of any auxiliary difference polynomial.',
 'gate-selector':'Retain the derivation of the residual in each selector case and interactive numerical counterfactual.',
 'gate-polynomial':'Retain how shifted evaluations access one gate, the vanishing domain and increased product degree.',
 'wire-permutation':'Retain the concrete wire cycles and formal equality; explain the scope of the unproved permutation argument.',
 'fast-vanishing':'Retain the monic-polynomial argument, repeated-squaring cost and warning that subset domains differ.',
 'construction-map':'Retain the connected construction and distinguish universal setup, preprocessing, proving and additional privacy/knowledge proofs.'},
'pir':{
'pir-goal':'Retain indexed retrieval, DNS motivation and whole-download baseline; the database is not assumed secret from the client.',
'matrix-layout':'Retain the reason to select a column and reconstruct a row locally; remove the definition of a matrix.',
'matrix-proof':'Retain cancellation in every row and the privacy argument for both coordinates.',
'communication-balance':'Retain the upload/download tradeoff and minimum derivation; remove a definition of ceiling notation.',
'pir-assumptions':'Retain information-theoretic versus computational assumptions in the P=NP question.',
'homomorphic-operations':'Retain decryption-level correctness and the distinction between known scalar and hidden-plaintext multiplication.',
'single-server':'Retain encrypted linear selection, ciphertext/bit costs and security of the joint encrypted vector.',
'recursive-selection':'Retain the two-dimensional re-encoding step and explanation that known ciphertext encodings become outer plaintext data.',
'recursive-size':'Retain expansion models and explain why counting objects does not establish the claimed bit complexity.',
'replication-limit':'Retain the missing replicated-database precondition and distinguish naive reuse from a general impossibility claim.',
'fhe-selection':'Retain equality selectors, masked OR, encrypted constants and compactness before HW4 4(b).',
'noise-model':'Retain the stipulated gate model and distinguish ciphertext noise from plaintext values.',
'server-work':'Retain the comparison of communication and database-wide computation; delimit the raw-data scan argument.',
'offline-online':'Retain amortized, offline, online and batching distinctions, with source-scoped performance claims.',
'field-review':'Retain the field/cancellation recap needed for the HW3 counterexample; remove elementary polynomial definitions.',
'coefficient-shift':'Retain the ideal bounded-degree oracle condition and its relation to coefficient positions.',
'coefficient-split':'Retain the disjoint degree-range argument and endpoint zero-polynomial cases.',
'product-coefficient':'Retain why reversed coefficient lists form the middle coefficient and why two identities must be checked.',
'proof-models':'Retain the information-theoretic ideal test versus computational compiler distinction before conceptual exercises.',
'succinctness-review':'Retain the verifier-time limitation of the empty-proof argument.',
'exponent-product':'Retain why exponent multiplication needs the supplied interface and is distinct from discrete-log recovery.'}}
records=[]
for deck,(_,_,expected) in DECKS.items():
 raw=(ROOT/'docs'/deck/'index.html').read_text()
 for section in re.findall(r'<section\b.*?</section>',raw,re.S):
  id=re.search(r'id="([^"]+)"',section)[1]
  title=re.search(r'<div class="section">(.*?)</div>',section,re.S)[1]
  n=int(id[7:]) if id.startswith('lesson-') else None
  assigned='HW' in title and 'class="solution"' in section or bool(re.search(r'data-exercise="hw',section)) or deck.startswith('hw')
  if assigned:
   action='canonical worked exercise reviewed';note='Keep the actual task, local assumptions, justified solution steps and initially closed solution. Chapter/homework copies share their source.'
  elif deck in REVISIONS and n in REVISIONS[deck]:
   action='rewritten';note='Rebuilt the course-specific explanation in connected prose; local notation and formal scope are stated before use.'
  elif deck in NEW and id in NEW[deck]:
   action='rewritten';note='Rebuilt the definition or mechanism and its missing inferential links; diagrams show the relevant message order where applicable.'
  elif deck in notes:
   action='reviewed and refined' if id in EDITS.get(deck,{}) else 'reviewed and retained'
   assert id in notes[deck],(deck,id)
   note=notes[deck][id]
  else:
   action='reviewed practice retained';note='Retain the mathematical exercise and worked inference; elementary or duplicate practice was merged into its related homework.'
  records.append({'deck':deck,'id':id,'title':title,'action':action,'review':note,'protocol_diagrams':len(re.findall('data-protocol=',section))})
 assert sum(r['deck']==deck for r in records)==expected
assert len(records)==251
(ROOT/'scripts/teaching-audit.json').write_text(json.dumps({'source_limits':'Chapters 1/2 use the existing repository transcription; the source PDFs available for page comparison are Chapters 3/4 and HW3/4.','cards':records},indent=2,ensure_ascii=False)+'\n')
print('PASS editorial disposition recorded for all 251 cards')
