"""Coverage, dependency, synchronization and numerical assertions for Chapter 3."""
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from snarks_content import CARDS
from hw3_content import HW
from deck_catalog import DECKS

assert len(CARDS)==48 and len(HW)==12
seen=set()
for card in CARDS:
 assert set(card['requires'])<=seen,(card['id'],'prerequisite comes later')
 assert card['id'] not in seen
 seen.add(card['id'])
assert {c['id'] for c in CARDS if c['kind']=='homework'}=={'hw-'+k for k in HW}
# Each exercise appears immediately after its preparation or a sibling exercise.
last_theory=None
for c in CARDS:
 if c['kind']=='theory':last_theory=c['id']
 else:assert last_theory in c['requires'],c['id']

decks={}
for deck,(_,_,count) in DECKS.items():
 raw=(ROOT/'docs'/deck/'index.html').read_text()
 sections=re.findall(r'<section\b.*?</section>',raw,re.S)
 ids=[re.search(r'id="([^"]+)"',s)[1] for s in sections]
 assert len(ids)==count and len(set(ids))==count
 menu=re.search(r'<nav aria-label="Chapters".*?</nav>',raw,re.S)[0]
 for target in DECKS:assert f'href="../{target}/"' in menu,(deck,target)
 assert menu.count('aria-current="page"')==1
 if deck not in ['snarks','hw3']:continue
 assert not re.search(r'\\\(|\\\[|data-mjx-error|data-mml-node="merror"|fill="red"',raw)
 assert not re.search(r'<script[^>]+src="https?',raw)
 assert raw.count('<details class="solution">')==12
 assert '<mjx-container' in raw
 for i,s in enumerate(sections):
  nav=re.search(r'<nav aria-label="Card navigation".*?</nav>',s,re.S)[0]
  assert re.findall(r'href="#([^"]+)"',nav)==([ids[i-1]] if i else [])+([ids[i+1]] if i+1<len(ids) else [])
  # Inline math has an accessible label independent of the SVG paths.
  for math in re.findall(r'<(?:span|div) class="(?:mi )?mathnew"[^>]*>',s):assert 'aria-label=' in math
 decks[deck]=dict(zip(ids,sections))
for k in HW:
 pattern=r'<details class="solution">.*?</details>'
 assert re.search(pattern,decks['snarks']['hw-'+k],re.S)[0]==re.search(pattern,decks['hw3']['hw-'+k],re.S)[0],k
assert [x['id'] for x in CARDS]==list(decks['snarks'])

# Independently verify the small numerical examples used in the explanation.
assert [x for x in range(6) if (2*x*x+4*x)%6==0]==[0,1,3,4]
assert [x for x in range(7) if (2*x*x+4*x)%7==0]==[0,5]
assert [(5*x*x+3)%7 for x in range(3)]==[3,1,2]
assert len({pow(6,i,97) for i in range(12)})==12 and pow(6,12,97)==1
assert pow(2,10,23)==16*pow(8,2,23)%23==12
a,b=0,1
for _ in range(100):a,b=b,a+b
assert a==354224848179261915075
readme=(ROOT/'README.md').read_text()
for deck in DECKS:assert f'https://anujpare.github.io/study_material/{deck}/' in readme
guide=(ROOT/'TEACHING_GUIDE.md').read_text()
assert len(re.findall(r'^## ',guide,re.M))==5
print('PASS 48-card dependency order, all 12 interleaved/shared solutions, six menus, math generation and numerical examples')

