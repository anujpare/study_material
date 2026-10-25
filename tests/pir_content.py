"""Assignment coverage, ordering, shared solutions and boundary-case arithmetic."""
from pathlib import Path
import re,sys,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from pir_content import CARDS
from hw4_content import HW
from deck_catalog import DECKS

assert len(CARDS)==45 and len(HW)==15
assert sum(c['kind']=='theory' for c in CARDS)==28
assert {c.get('origin') for c in CARDS if c['kind']=='homework'}=={'hw4:'+k for k in HW}|{'hw3:1a','hw3:1c'}
seen=set();last=None
for c in CARDS:
 assert c['id'] not in seen
 assert set(c['requires'])<=seen,(c['id'],'missing prerequisite')
 if c['kind']=='theory':last=c['id']
 else:assert last in c['requires'],(c['id'],'not immediately after preparation')
 seen.add(c['id'])

pages={}
for deck,(_,_,count) in DECKS.items():
 raw=(ROOT/'docs'/deck/'index.html').read_text()
 cards=re.findall(r'<section\b.*?</section>',raw,re.S)
 ids=[re.search(r'id="([^"]+)"',c)[1] for c in cards]
 assert len(ids)==count and len(set(ids))==count,(deck,'card count')
 menu=re.search(r'<nav aria-label="Chapters".*?</nav>',raw,re.S)[0]
 for target in DECKS:assert f'href="../{target}/"' in menu,(deck,target)
 assert menu.count('aria-current="page"')==1
 pages[deck]=dict(zip(ids,cards))
 if deck not in ['pir','hw4']:continue
 assert not re.search(r'\\\(|\\\[|data-mjx-error|data-mml-node="merror"|fill="red"',raw)
 assert not re.search(r'<script[^>]+src="https?',raw)
 assert '<mjx-container' in raw
 for i,c in enumerate(cards):
  nav=re.search(r'<nav aria-label="Card navigation".*?</nav>',c,re.S)[0]
  assert re.findall(r'href="#([^"]+)"',nav)==([ids[i-1]] if i else [])+([ids[i+1]] if i+1<len(ids) else [])
  assert 'data-source=' in c and 'data-requires=' in c
 for link in re.findall(r'href="#([^"]+)"',raw):assert link in ids,(deck,link)
solution=lambda card:re.search(r'<details class="solution">.*?</details>',card,re.S)[0]
for k in HW:assert solution(pages['pir']['hw4-'+k])==solution(pages['hw4']['hw4-'+k]),k
for k in ['1a','1c']:assert solution(pages['pir']['hw3-'+k])==solution(pages['hw3']['hw-'+k]),k
assert len(re.findall('data-exercise="hw4:',(ROOT/'docs/hw4/index.html').read_text()))==15

# Exhaustive small-model checks, independent of the browser's implementations.
X=[[1,0,1,1],[0,1,0,1],[1,1,0,0],[0,0,1,0]]
bits=lambda n:[(n>>(3-i))&1 for i in range(4)]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))%2
for j in range(4):
 seen_queries=set()
 for m in range(16):
  q0=bits(m);q1=[v^(i==j) for i,v in enumerate(q0)];seen_queries.add(tuple(q1))
  assert [dot(row,q0)^dot(row,q1) for row in X]==[row[j] for row in X]
 assert len(seen_queries)==16
assert min(2*c+2*(64//c) for c in [1,2,4,8,16,32,64])==32
assert {((a-1)*4+b-1)*4+c for a in range(1,5) for b in range(1,5) for c in range(1,5)}==set(range(1,65))
for n in range(2,33):
 ell=(n-1).bit_length();noise=2*n*8**ell
 assert n-1<2**ell
 if n&(n-1)==0:assert noise==2*n**4
 else:assert noise>2*n**4
for z in range(11):
 y=(z*z+2*z+4)%11;qalpha=(5+z)%11
 assert (qalpha*(3-z))%11==(8-y)%11
assert pow(2,4,23)*pow(8,2,23)*6%23==3
assert [sum([1,2,3][i]*[4,5,6][k-i] for i in range(3) if 0<=k-i<3) for k in range(5)]==[4,13,28,27,18]
readme=(ROOT/'README.md').read_text()
for d in DECKS:assert f'https://anujpare.github.io/study_material/{d}/' in readme
print('PASS Chapter 4/HW4 coverage, all 17 interleaved questions, canonical HW3 reuse, eight menus and boundary-case arithmetic')
