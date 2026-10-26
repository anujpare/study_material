"""Course-specific prerequisites, source retention and merged-card bookmarks."""
from pathlib import Path
import re,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from undergraduate_content import ORDER,MERGED,REVISIONS,HW_ORDER,LEGACY_HW_ORDER
from deck_catalog import DECKS
from beginner_solutions import SOLUTIONS
for deck in ['commitment','zero-knowledge','hw1','hw2']:
 raw=(ROOT/'docs'/deck/'index.html').read_text();cards=re.findall(r'<section\b.*?</section>',raw,re.S)
 ids=[re.search(r'id="([^"]+)"',c)[1] for c in cards]
 allids=re.findall(r'\bid="([^"]+)"',raw)
 assert len(ids)==DECKS[deck][2] and len(ids)==len(set(ids))
 assert len(allids)==len(set(allids)),(deck,'duplicate ID')
 assert 'class="beginner-context"' not in raw and 'Start here ·' not in raw
 original=85 if deck=='commitment' else 62 if deck=='zero-knowledge' else len(LEGACY_HW_ORDER[deck])
 assert {f'lesson-{n}' for n in range(1,original+1)}<=set(allids),(deck,'lost bookmark')
 for i,c in enumerate(cards):
  nav=re.search(r'<nav aria-label="Card navigation".*?</nav>',c,re.S)[0]
  assert re.findall(r'href="#([^"]+)"',nav)==([ids[i-1]] if i else [])+([ids[i+1]] if i+1<len(ids) else [])
 for ref in re.findall(r'<a[^>]*href="#([^"]+)"',raw):assert ref in allids,(deck,ref)
 if deck in ORDER:
  assert ids==['lesson-'+str(n) for n in ORDER[deck]]
  for n,(_,steps) in SOLUTIONS[deck].items():
   assert n in ORDER[deck]
   c=cards[ids.index('lesson-'+str(n))];assert all(step in c for step in steps),(deck,n)
 else:
  assert len(re.findall('class="solution"',raw))==len(HW_ORDER[deck])
  assert all('class="solution"' in c for c in cards)
 assert not re.search(r'fill="red"|data-mjx-error|\\parallelr',raw)
 print(f'PASS {deck}: {len(cards)} cards, all legacy bookmarks and worked solutions')
# Core course concepts precede the constructions that rely on them.
for deck,pairs in {'commitment':[(10,12),(12,22),(22,23),(35,38),(39,48),(48,51),(64,63)],'zero-knowledge':[(10,13),(19,21),(22,6),(28,29),(31,43),(49,53)]}.items():
 for a,b in pairs:assert ORDER[deck].index(a)<ORDER[deck].index(b)
# These requirements check actual formal content, not an auto-added glossary.
body=REVISIONS['commitment'][22][1]
for fragment in ['probabilit','\\forall','PPT','1^\\lambda','\\mu_D','own random choices','oracle access']:assert fragment in body
assert 'prime order' in REVISIONS['commitment'][38][0]
assert 'every vertex exactly once' in REVISIONS['zero-knowledge'][19][1]
assert 'for every verifier, there exists a simulator, for every valid input' in REVISIONS['zero-knowledge'][10][1]
assert not any('fraction a/b' in b or 'A <strong>bit</strong> is' in b for d in REVISIONS.values() for _,b in d.values())
print('PASS undergraduate prerequisite boundary, formal definitions and dependency order')
