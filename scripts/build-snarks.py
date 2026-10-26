"""Build both new decks from one reviewed source; MathJax runs only at build time."""
from pathlib import Path
import html,json,re,subprocess
from snarks_content import CARDS
from hw3_content import HW
from deck_catalog import ROOT,links,refresh_menus

MATH = re.compile(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', re.S)
def body(c):
 if c['kind']=='theory': return c['body']
 return c['question']+'<details class="solution"><summary>Show step-by-step solution</summary><div class="solution-content"><ol>'+''.join('<li><p>'+s+'</p></li>' for s in c['steps'])+'</ol>'+c['visual']+'</div></details>'

tex = sorted({m[1] or m[2] for c in CARDS for m in MATH.finditer(body(c))})
proc=subprocess.run(['node',str(ROOT/'scripts/render-math.cjs')],input=json.dumps(tex),text=True,capture_output=True,check=True)
rendered=json.loads(proc.stdout)
def math(text):
 def replace(m):
  t=m[1] or m[2]; tag='span' if m[1] is not None else 'div'; cls='mi mathnew' if tag=='span' else 'math mathnew'
  svg=rendered[t].replace('<mjx-container ', '<mjx-container aria-hidden="true" ')
  return f'<{tag} class="{cls}" role="math" aria-label="{html.escape(t,quote=True)}">{svg}</{tag}>'
 return MATH.sub(replace,text)

template=(ROOT/'docs/commitment/index.html').read_text()
head=template[:template.index('</head>')]
head=re.sub(r'<title>.*?</title>','<title>PETS — {title}</title>',head)
head=re.sub(r'<meta content="[^"]*" name="description"/>','<meta content="PETS: SNARKs, connected explanations, interactive diagrams and all HW3 solutions." name="description"/>',head)
head=head.replace('<script src="../concepts.js" defer></script>','')
head+='<link rel="stylesheet" href="../snarks.css"/></head>'

def nav(ids,i):
 def link(n,label,path): return f'<a class="navbtn" href="#{ids[n]}" aria-label="{label} card"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="{path}"/></svg></a>'
 return '<nav aria-label="Card navigation" class="nav">'+(link(i-1,'Previous','m14.5 6.5-5.5 5.5 5.5 5.5') if i else '<span class="navbtn" aria-disabled="true" aria-label="Previous card">‹</span>')+(link(i+1,'Next','m9.5 6.5 5.5 5.5-5.5 5.5') if i+1<len(ids) else '')+'</nav>'

for deck,cards,title in [('snarks',CARDS,'SNARKs'),('hw3',[dict(HW[k],kind='homework') for k in ['1a','1b','1c','1d','2a','2b','2c','2d','3a','3b','4a','4b']],'HW3')]:
 ids=[c['id'] for c in cards]; count=len(cards)
 shortcuts=[('two-routes','Two routes to succinct proofs'),('interpolation','Polynomial interpolation'),('four-obligations','Check a circuit trace'),('construction-map','Construction map')] if deck=='snarks' else [(c['id'],c['title']) for c in cards]
 menu='<details class="chapter-menu"><summary aria-label="Choose chapter" title="Choose chapter"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M5 6h14M5 12h14M5 18h14"/></svg></summary><nav aria-label="Chapters" class="chapter-panel"><span class="menu-brand">PETS</span>'+links(deck)+f'<a href="#{ids[0]}">Start from the beginning</a><div class="menu-experiments"><span class="menu-brand">Explore</span>'+''.join(f'<a href="#{id}">{label}</a>' for id,label in shortcuts)+'</div><a href="../" class="all-chapters">Deck overview</a></nav></details>'
 sections=[]
 for i,c in enumerate(cards):
  title_escaped=html.escape(c['title'],quote=True)
  content=math(body(c))
  aliases=''.join(f'<span class="card-alias" id="{a}"></span>' for a in c.get('aliases',[]))
  if deck=='hw3':
   prerequisites=' · '.join(f'<a href="../snarks/#{key}">{next(x["title"] for x in CARDS if x["id"]==key)}</a>' for key in c['requires'])
   content+='<p class="prerequisite-link">Review the preparation: '+prerequisites+'</p>'
  sections.append(f'<section class="slide {c["kind"]}" id="{c["id"]}" data-source="{html.escape(c["source"],quote=True)}" data-requires="{" ".join(c["requires"])}" aria-label="{title_escaped}"><header class="head"><div class="section">{title_escaped}</div></header><article class="reading">{aliases}{content}</article>{nav(ids,i)}</section>')
 footer=f'<div aria-label="Card navigation slider" class="deck-jump" role="group"><output class="deck-position" for="pet-card-slider" id="pet-card-position">1 / {count}</output><input aria-label="Jump to card" aria-valuetext="Card 1 of {count}" class="deck-slider" id="pet-card-slider" max="{count}" min="1" step="1" type="range" value="1"/></div></main><script src="../teaching.js" defer></script><script src="../reader.js" defer></script><script src="../learning.js" defer></script><script src="../snarks.js" defer></script></body></html>'
 target=ROOT/'docs'/deck;target.mkdir(exist_ok=True)
 (target/'index.html').write_text(head.replace('{title}',title)+f'<body><main id="lessons" data-chapter="{deck}">'+menu+''.join(sections)+footer)
 print(deck,count,'cards')
refresh_menus()
(ROOT/'scripts/snarks-audit.json').write_text(json.dumps([{'position':i+1,**{k:c[k] for k in ('id','kind','source','requires')}} for i,c in enumerate(CARDS)],indent=2)+'\n')

