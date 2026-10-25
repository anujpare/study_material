"""Content and navigation regressions for the beginner paths (no third-party dependencies)."""
from pathlib import Path
import re,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from beginner_solutions import SOLUTIONS
expected={'commitment':(95,85),'zero-knowledge':(73,62),'hw1':(33,22),'hw2':(31,20)}
prereqs={
 'commitment':[('start-notation','lesson-1'),('start-algorithms','lesson-7'),('start-commit','lesson-20'),('start-oracle','lesson-27'),('start-group','lesson-46'),('start-ddh','lesson-63'),('start-linear','lesson-77')],
 'zero-knowledge':[('start-proof','lesson-1'),('lesson-22','lesson-6'),('start-commit','lesson-19'),('start-graph','lesson-19'),('start-mod','lesson-26'),('start-group','lesson-26'),('start-circuit','lesson-3')],
 'hw1':[('start-commit','lesson-1'),('start-oracle','lesson-1'),('start-group','lesson-7'),('start-ddh','lesson-12'),('start-linear','lesson-16')],
 'hw2':[('start-proof','lesson-1'),('start-graph','lesson-8'),('start-mod','lesson-11'),('start-group','lesson-11'),('start-circuit','lesson-1')]}
for deck,(total,original) in expected.items():
 source=(ROOT/'docs'/deck/'index.html').read_text()
 cards=re.findall(r'<section\b.*?</section>',source,re.S)
 ids=[re.search(r'id="([^"]+)"',c)[1] for c in cards]
 assert len(ids)==total and len(set(ids))==total,(deck,'count/unique IDs')
 assert ids[0]=='start-notation'
 assert {f'lesson-{n}' for n in range(1,original+1)} <= set(ids),(deck,'legacy links lost')
 assert source.count('class="beginner-context"')==original,(deck,'missing card review')
 for first,second in prereqs[deck]:assert ids.index(first)<ids.index(second),(deck,first,second)
 for i,c in enumerate(cards):
  nav=re.search(r'<nav aria-label="Card navigation".*?</nav>',c,re.S)[0]
  links=re.findall(r'href="#([^"]+)"',nav)
  assert links==([ids[i-1]] if i else [])+([ids[i+1]] if i+1<len(ids) else []),(deck,ids[i],links)
  if ids[i].startswith('lesson-'):
   assert c.count('class="beginner-context"')==1
   assert 'Read the symbols.' not in c and 'In plain language.' not in c
   body=re.sub(r'<aside class="beginner-context".*?</aside>','',c,flags=re.S)
   assert not re.search(r'\bsalt\b',re.sub(r'<[^>]*>',' ',body),re.I),(deck,ids[i],'unintroduced salt terminology')
 for ref in re.findall(r'<a[^>]*href="#([^"]+)"',source):assert ref in ids,(deck,'broken link',ref)
 if deck in SOLUTIONS:
  for n,(_,steps) in SOLUTIONS[deck].items():
   c=cards[ids.index(f'lesson-{n}')]
   assert all(step in c for step in steps),(deck,n,'worked explanation not applied')
 assert 'fill="red"' not in source and '\\parallelr' not in source
 print(f'PASS {deck}: prerequisite order, {original} reviewed cards, {total} linked cards, worked solutions')
audit=json.loads((ROOT/'scripts/beginner-audit.json').read_text())
assert audit['original_cards_reviewed']==189
readme=(ROOT/'README.md').read_text()
for suffix in ['', 'commitment/', 'zero-knowledge/', 'hw1/', 'hw2/']:
 assert f'https://anujpare.github.io/study_material/{suffix}' in readme
print('PASS original-card audit coverage and README links for all decks')
