"""Build the undergraduate Chapter 1/2 paths and canonical HW1/2 copies.
Existing HTML supplies unchanged exercise statements and legacy SVG math. Full
teaching replacements live in undergraduate_content.py; no glossary is injected.
"""
from pathlib import Path
import html,json,re,subprocess
from undergraduate_content import REVISIONS,ORDER,MERGED,PRIMER_TARGETS,HW_ORDER,LEGACY_HW_ORDER,HW_ALIASES
from beginner_solutions import SOLUTIONS
from deck_catalog import ROOT,DECKS,links,refresh_menus
from homework_visuals import EARLIER_VISUALS
MATH=re.compile(r'\\\((.*?)\\\)|\\\[(.*?)\\\]',re.S)
texts=[body for revisions in REVISIONS.values() for _,body in revisions.values()]
texts += [v for d in EARLIER_VISUALS.values() for v in d.values()]
tex=sorted({m[1] or m[2] for text in texts for m in MATH.finditer(text)})
proc=subprocess.run(['node',str(ROOT/'scripts/render-math.cjs')],input=json.dumps(tex),text=True,capture_output=True,check=True)
rendered=json.loads(proc.stdout)
def math(text):
 def sub(m):
  t=m[1] or m[2];tag='span' if m[1] is not None else 'div';cls='mi mathnew' if tag=='span' else 'math mathnew'
  return f'<{tag} class="{cls}" role="math" aria-label="{html.escape(t,quote=True)}">'+rendered[t].replace('<mjx-container ','<mjx-container aria-hidden="true" ')+f'</{tag}>'
 return MATH.sub(sub,text)
def nav(ids,i):
 def a(n,label,d):return f'<a class="navbtn" href="#{ids[n]}" aria-label="{label} card"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="{d}"/></svg></a>'
 return '<nav aria-label="Card navigation" class="nav">'+(a(i-1,'Previous','m14.5 6.5-5.5 5.5 5.5 5.5') if i else '<span class="navbtn" aria-disabled="true" aria-label="Previous card">‹</span>')+(a(i+1,'Next','m9.5 6.5 5.5 5.5-5.5 5.5') if i+1<len(ids) else '')+'</nav>'
def split(raw):
 cards=list(re.finditer(r'<section\b.*?</section>',raw,re.S))
 return raw[:cards[0].start()],{int(m[1]):c[0] for c in cards if (m:=re.search(r'id="lesson-(\d+)"',c[0]))},raw[cards[-1].end():]
def clean(c):
 c=re.sub(r'<aside class="beginner-context".*?</aside>','',c,flags=re.S)
 c=re.sub(r'<div class="(?:guide|reasoning-link)">.*?</div>','',c,flags=re.S)
 c=re.sub(r'<span class="card-alias"[^>]*></span>','',c)
 return c
def aliases(mapping,n):return ''.join(f'<span class="card-alias" id="{k}"></span>' for k,v in mapping.items() if v==n)
SHORTCUTS={
 'commitment':[(10,'PPT and the security parameter'),(22,'Indistinguishability'),(23,'Commitment messages'),(38,'Prime-order groups'),(51,'The Pedersen reduction'),(56,'The PRF security game')],
 'zero-knowledge':[(10,'The zero-knowledge definition'),(19,'Hamiltonian cycles'),(21,'The graph protocol'),(29,'Extraction'),(43,'Schnorr'),(49,'Fiat–Shamir')]}
def write(deck,prefix,body,suffix):
 count=len(body);ids=[re.search(r'id="([^"]+)"',c)[1] for c in body]
 for i,c in enumerate(body):body[i]=re.sub(r'<nav aria-label="Card navigation".*?</nav>',lambda _:nav(ids,i),c,flags=re.S)
 if '../teaching.css' not in prefix:prefix=prefix.replace('</head>','<link rel="stylesheet" href="../teaching.css"/></head>')
 if '../teaching.js' not in suffix:suffix=suffix.replace('</body>','<script src="../teaching.js" defer></script></body>')
 shortcuts=SHORTCUTS.get(deck,[])
 menu='<nav aria-label="Chapters" class="chapter-panel"><span class="menu-brand">PETS</span>'+links(deck)+f'<a href="#{ids[0]}">Start from the beginning</a><div class="menu-experiments"><span class="menu-brand">Explore</span>'+''.join(f'<a href="#lesson-{n}">{title}</a>' for n,title in shortcuts)+'</div><a href="../" class="all-chapters">Deck overview</a></nav>'
 prefix=re.sub(r'<nav aria-label="Chapters" class="chapter-panel">.*?</nav>',lambda _:menu,prefix,count=1,flags=re.S)
 suffix=re.sub(r'1 / \d+',f'1 / {count}',suffix);suffix=re.sub(r'Card 1 of \d+',f'Card 1 of {count}',suffix);suffix=re.sub(r'max="\d+"',f'max="{count}"',suffix)
 (ROOT/'docs'/deck/'index.html').write_text(prefix+''.join(body)+suffix)
 assert count==DECKS[deck][2],(deck,count)
 print(deck,count,'cards')
 return ids
AUDIT=[]
for deck in ORDER:
 path=ROOT/'docs'/deck/'index.html';prefix,original,suffix=split(path.read_text());cards=[]
 redirect={f'lesson-{k}':v for k,v in MERGED[deck].items()}
 redirect.update({'start-'+k:v for k,v in PRIMER_TARGETS[deck].items()})
 for n in ORDER[deck]:
  c=clean(original[n])
  if n in REVISIONS[deck]:
   title,body=REVISIONS[deck][n]
   c=re.sub(r'aria-label="[^"]*"',lambda _:f'aria-label="{html.escape(title,quote=True)}"',c,count=1)
   c=re.sub(r'<div class="section">.*?</div>',lambda _:'<div class="section">'+title+'</div>',c,count=1,flags=re.S)
   c=re.sub(r'<article\b[^>]*>.*?</article>',lambda _:'<article class="reading">'+math(body)+'</article>',c,count=1,flags=re.S)
  elif n in SOLUTIONS.get(deck,{}):
   conclusion,steps=SOLUTIONS[deck][n]
   solution='<div class="solution-content"><p><strong>'+conclusion+'</strong></p><ol>'+''.join('<li><p>'+step+'</p></li>' for step in steps)+'</ol>'+math(EARLIER_VISUALS.get(deck,{}).get(n,''))+'</div></details>'
   c,nmatch=re.subn(r'<div class="solution-content">.*?</div></details>',lambda _:solution,c,count=1,flags=re.S)
   assert nmatch==1,(deck,n)
  c=c.replace('<article class="reading">','<article class="reading">'+aliases(redirect,n),1)
  cards.append(c)
  AUDIT.append({'deck':deck,'id':'lesson-'+str(n),'action':'rewritten explanation' if n in REVISIONS[deck] else 'reviewed worked solution','aliases':[k for k,v in redirect.items() if v==n]})
 write(deck,prefix,cards,suffix)
 for old,target in MERGED[deck].items():AUDIT.append({'deck':deck,'id':'lesson-'+str(old),'action':'merged; repeated or elementary explanation removed','target':'lesson-'+str(target)})
for deck,order in HW_ORDER.items():
 source='commitment' if deck=='hw1' else 'zero-knowledge'
 prefix,_,suffix=split((ROOT/'docs'/deck/'index.html').read_text())
 _,sourcecards,_=split((ROOT/'docs'/source/'index.html').read_text())
 cards=[]
 for old in order:
  n=LEGACY_HW_ORDER[deck].index(old)+1
  c=clean(sourcecards[old])
  c=c.replace(f'id="lesson-{old}"',f'id="lesson-{n}" data-source-card="{old}" data-source-chapter="{source}"',1)
  redirect={f'lesson-{k}':v for k,v in HW_ALIASES[deck].items()}
  # Old prerequisite bookmarks point into the first appropriate worked exercise.
  primer_ids=['notation','powers','bits','chance','algorithms','commit','oracle','mod','group','ddh','linear'] if deck=='hw1' else ['notation','powers','bits','chance','algorithms','proof','circuit','commit','graph','mod','group']
  redirect.update({'start-'+k:LEGACY_HW_ORDER[deck].index(order[0])+1 for k in primer_ids})
  c=c.replace('<article class="reading">','<article class="reading">'+aliases(redirect,n),1)
  cards.append(c)
  AUDIT.append({'deck':deck,'id':'lesson-'+str(n),'action':'shared reviewed solution','source':source+'/lesson-'+str(old),'aliases':[k for k,v in redirect.items() if v==n]})
 write(deck,prefix,cards,suffix)
refresh_menus()
landing=ROOT/'docs/index.html';s=landing.read_text()
for deck,(_,_,total) in DECKS.items():s=re.sub(r'(<a class="card" href="./'+deck+r'/">.*?<div class="meta">)\d+( cards)',rf'\g<1>{total}\2',s,flags=re.S)
s=s.replace('Each deck starts from the basics and introduces new concepts before using them. Try the interactive visualizations and follow each worked solution step by step.','Learn the cryptographic definitions, follow the protocol diagrams, and practise with worked homework solutions. Ordinary undergraduate mathematics is assumed.')
landing.write_text(s)
(ROOT/'scripts/beginner-audit.json').write_text(json.dumps({'counts':{d:DECKS[d][2] for d in ['commitment','zero-knowledge','hw1','hw2']},'cards':AUDIT},indent=2)+'\n')
