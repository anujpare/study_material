"""Build the MPC reader and HW6 from canonical teaching sources, with offline math.

No uploaded PDFs are published. Source page labels and pedagogical corrections live
in sources.html and source-map.json. Interactive lab defaults render without JS.
"""
from pathlib import Path
import html, json, re, subprocess
from mpc_core import CARDS as CORE, SOURCE_ISSUES as CORE_ISSUES
from mpc_exercises import CARDS as EXERCISES, SOURCE_ISSUES as EXERCISE_ISSUES
from mpc_shamir import CARDS as SHAMIR, SOURCE_ISSUES as SHAMIR_ISSUES

ROOT=Path(__file__).resolve().parents[1]
ALL={c['id']:c for c in CORE+EXERCISES+SHAMIR}
ORDER=[
'mpc-goal','mpc-models','simulation-definition','simulation-test','hw6-1b',
'additive-sharing','additive-privacy','hw6-1ai','input-sharing','shared-circuit','local-addition','hw6-1aii','public-constants','multiplication-obstacle',
'beaver-triple','beaver-identity','beaver-opening','beaver-combine','mask-privacy','mask-reuse','remove-dealer','mpc-cost','hw6-3a','hw6-3b','hw6-3c',
'malicious-guarantees','hw6-2a','commitments-channel','hw6-2b','hw6-2c','authenticated-shares','hw6-2d','mac-security','hw6-2e',
* [c['id'] for c in SHAMIR]
]
assert len(ALL)==len(CORE)+len(EXERCISES)+len(SHAMIR),'Duplicate card ID'
assert set(ORDER)==set(ALL),'Missing or extra sequenced card'
assert len(ORDER)==len(set(ORDER)),'Duplicate route card'
CARDS=[ALL[id] for id in ORDER]
for pos,c in enumerate(CARDS,1):
 c['section']=('I · What MPC protects' if pos<=5 else 'II · Computing on shares' if pos<=13 else 'III · Private multiplication' if pos<=25 else 'IV · Malicious parties and authentication' if pos<=34 else 'V · Threshold secret sharing' if pos<=42 else 'VI · Threshold signatures')
HW_ORDER=['hw6-1ai','hw6-1aii','hw6-1b','hw6-1c','hw6-2a','hw6-2b','hw6-2c','hw6-2d','hw6-2e','hw6-3a','hw6-3b','hw6-3c','hw6-4a','hw6-4b','hw6-4c','hw6-4d']
for i,c in enumerate(CARDS):
 assert all(k in ORDER[:i] for k in c['requires']),(c['id'],c['requires'])
 assert c.get('check',{}).get('solution'),f'No worked check: {c["id"]}'
assert {c['id'] for c in CARDS if c['kind']=='homework'}==set(HW_ORDER)
MATH=re.compile(r'\\\((.*?)\\\)|\\\[(.*?)\\\]',re.S)
LAB=re.compile(r'\{\{lab:([a-z-]+)\}\}')

def texts(value):
 if isinstance(value,str):yield value
 elif isinstance(value,list):
  for x in value:yield from texts(x)
 elif isinstance(value,dict):
  for x in value.values():yield from texts(x)
tex=sorted({m[1] or m[2] for c in CARDS for text in texts(c) for m in MATH.finditer(text)})
compiled=subprocess.run(['node',str(ROOT/'scripts/render-mpc-math.cjs')],input=json.dumps(tex),capture_output=True,text=True,check=True)
math_result=json.loads(compiled.stdout)
rendered=math_result['rendered']
glyphs='<svg aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden" xmlns="http://www.w3.org/2000/svg">'+math_result['defs']+'</svg>'
lab_proc=subprocess.run(['node','-e',"const x=require('./docs/mpc-workbench/labs.js'); process.stdout.write(JSON.stringify(Object.fromEntries(x.labNames.map(n=>[n,x.renderLab(n)]))));"],cwd=ROOT,capture_output=True,text=True,check=True)
LABS=json.loads(lab_proc.stdout)

def math(text):
 # Author-supplied tables may be wider than a phone. Keep them locally scrollable.
 text=re.sub(r'<table\b.*?</table>', lambda m:'<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable mathematical table">'+m[0]+'</div>', text, flags=re.S)
 def repl(m):
  t=m[1] or m[2];tag='span' if m[1] is not None else 'div';cls='mi' if tag=='span' else 'math'
  svg=rendered[t].replace('<mjx-container ','<mjx-container aria-hidden="true" ')
  return f'<{tag} class="{cls}" role="math" aria-label="{html.escape(t,quote=True)}">{svg}</{tag}>'
 # Authors can use a display wrapper. Remove it first to avoid nested scroll boxes.
 text=re.sub(r'<div class="math">\s*(\\\[.*?\\\])\s*</div>',r'\1',text,flags=re.S)
 return MATH.sub(repl,LAB.sub(lambda m:LABS[m[1]],text))

def jscript(data):return json.dumps(data,ensure_ascii=False).replace('</','<\\/')

def checkpoint(c):
 q=c['check'];id=c['id'];kind=q['type'];prompt=math(q['prompt']);hint=math(q.get('hint',''))
 data={k:v for k,v in q.items() if k in ['type','answer']}
 if 'feedback' in q:
  data['feedback']=[math(t) for t in q['feedback']]
  if kind=='number' and q['feedback']:data['correctFeedback']=math(q['feedback'][0])
 choices=''
 if kind=='choice':
  choices='<div class="choice-list interactive-only">'+''.join(f'<button type="button" data-choice="{i}" aria-pressed="false"><span class="choice-letter">{chr(65+i)}</span><span>{math(t)}</span></button>' for i,t in enumerate(q['choices']))+'</div><noscript><ol type="A">'+''.join(f'<li>{math(t)}</li>' for t in q['choices'])+'</ol></noscript>'
 elif kind=='number':
  choices=f'<form class="number-answer interactive-only"><label class="answer-label" for="answer-{id}">Your value</label><input id="answer-{id}" inputmode="numeric" type="number" step="any" required autocomplete="off"><div class="control-row"><button type="submit">Check my value</button></div></form>'
 else:
  choices=f'<div class="interactive-only"><label class="answer-label" for="answer-{id}">Write a short argument</label><textarea id="answer-{id}" placeholder="State the relation or assumption, show the step, then explain what follows." spellcheck="false"></textarea></div>'
 rubric=''
 if kind=='written':
  rubric='<div class="rubric interactive-only"><strong>Check your written reasoning</strong>'+''.join(f'<label><input type="checkbox"><span>{math(t)}</span></label>' for t in q.get('rubric',[]))+'</div>'
 selfcheck='<div class="control-row self-check interactive-only"><button type="button" data-self="practice">Try again later</button>'+(('<button type="button" data-self="ready">I can justify each point</button>') if kind=='written' else '')+'</div>'
 return f'''<section class="checkpoint" data-check-type="{kind}" aria-labelledby="check-{id}"><h2 id="check-{id}">{'Your written attempt' if kind=='written' else 'Your turn'}</h2><div class="question">{prompt}</div>{choices}<div class="answer-feedback feedback" role="status" hidden></div>{'<details class="hint"><summary>Give me a hint</summary><div class="hint-content">'+hint+'</div></details>' if hint else ''}<details class="solution"><summary>Compare with the worked solution</summary><div class="solution-content">{math(q['solution'])}{rubric}{selfcheck}</div></details><p class="check-state" aria-live="polite"></p><script type="application/json" class="check-data">{jscript(data)}</script></section>'''

def article(c,index,cards,homework=False):
 id=c['id'];e=html.escape;exercise=c.get('exercise');meta=f'<span class="pill exercise-label">{e(exercise)}</span>' if exercise else '<span class="pill">Lesson + practice</span>'
 req=''
 if homework and c['requires']:
  req='<p>Review the preparation: '+', '.join(f'<a href="../mpc-workbench/#{k}">{e(ALL[k]["title"])}</a>' for k in c['requires'])+'.</p>'
 prev=f'<a href="#{cards[index-1]["id"]}">← Previous card</a>' if index else '<span></span>'
 nxt=f'<a href="#{cards[index+1]["id"]}">Next card →</a>' if index+1<len(cards) else '<a href="../">PETS chapters →</a>'
 return f'''<article class="lesson" id="{id}" data-title="{e(c['title'],quote=True)}" data-kind="{c['kind']}" data-homework-order="{HW_ORDER.index(id) if id in HW_ORDER else -1}" data-requires="{' '.join(c['requires'])}" aria-labelledby="title-{id}"><p class="eyebrow">{e(c['section'])}</p><h1 id="title-{id}">{e(c['title'])}</h1><div class="lesson-meta">{meta}</div>{math(c['body'])}{checkpoint(c)}<footer class="source"><p>Source: {e(c['source'].rstrip('.'))}. <a href="../mpc-workbench/sources.html">Coverage and clarifications</a>.</p>{req}</footer><nav class="static-nav" aria-label="Card navigation">{prev}{nxt}</nav></article>'''

def build(cards,target,homework=False):
 title='HW6 · MPC exercises' if homework else 'Secure MPC · Learning Lab';assets='../mpc-workbench/' if homework else './';n=len(cards)
 sections=''.join(article(c,i,cards,homework) for i,c in enumerate(cards))
 options=''.join(f'<option value="{c["id"]}">{i+1}. {html.escape(c["title"])}</option>' for i,c in enumerate(cards))
 modes=f'<option value="guided">{"HW6 in assignment order" if homework else "Lecture + homework"} · {n} cards</option>'+('' if homework else '<option value="homework">HW6 in assignment order · 16 questions</option>')+'<option value="review">Try again · my marked questions</option>'
 text=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f3f3f2"><title>PETS · {title}</title><meta name="description" content="Learn secure multiparty computation from the official PETS lectures. Interactive shares, Beaver multiplication, malicious security, Shamir sharing, and all 16 HW6 subquestions."><link rel="stylesheet" href="../typography.css"><link rel="stylesheet" href="{assets}style.css?v=1"><script defer src="{assets}labs.js?v=1"></script><script defer src="{assets}app.js?v=1"></script></head>
<body>{glyphs}<div class="shell"><header class="head"><span class="brand">PETS · {'HW6' if homework else 'Secure MPC'}</span><div class="head-right"><span class="count" id="counter" aria-live="polite">1 / {n}</span><button class="menu-toggle" id="menu-toggle" type="button" aria-expanded="false" aria-controls="chapter-panel" aria-label="Choose chapter or lesson"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M5 6h14M5 12h14M5 18h14"/></svg></button></div></header>
<nav class="chapter-panel" id="chapter-panel" hidden aria-label="PETS chapters and learning path"><h2>Secure MPC</h2><label for="mode">Learning path</label><select id="mode">{modes}</select><label for="lesson-select">Jump to a card</label><select id="lesson-select">{options}</select><p id="saved-progress">Your progress stays in this browser.</p><div class="menu-group"><a href="../mpc-workbench/">Secure MPC · complete learning lab</a><a href="../hw6/">HW6 · all 16 assigned questions</a><a href="../zk-workbench/">Zero Knowledge · learning lab</a><a href="../snarg-workbench/">SNARGs → PLONK · learning lab</a><a href="../pir/">PIR</a><a href="../">All PETS chapters</a><a href="../mpc-workbench/sources.html">Sources and teaching scope</a></div></nav>
<main class="reading" id="lesson" tabindex="-1" aria-label="Learning card"><noscript><p class="no-js-note">The complete lesson text, equations, static experiments and worked solutions remain readable here. Enable JavaScript for one-card navigation and live experiments.</p></noscript>{sections}<section class="empty-state" id="empty-state" hidden><h1>No questions marked for another attempt</h1><p>Use “Try again later” after a solution, or revisit a question you answered incorrectly. Those questions appear here.</p><button id="return-guided" type="button">Return to the learning path</button></section></main>
<footer class="reader-footer interactive-only"><div class="row"><div class="deck-jump"><output class="deck-position" id="position" for="deck-slider">1 / {n}</output><input class="deck-slider" id="deck-slider" type="range" min="1" max="{n}" value="1" step="1" aria-label="Jump to card"></div></div><nav class="nav" aria-label="Previous or next card"><button type="button" id="previous" class="navbtn" aria-label="Previous card"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="m14.5 6.5-5.5 5.5 5.5 5.5"/></svg></button><span class="route-status" id="route-status">0 / {n} checked</span><button type="button" id="next" class="navbtn" aria-label="Next card"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="m9.5 6.5 5.5 5.5-5.5 5.5"/></svg></button></nav></footer></div></body></html>'''
 target.mkdir(exist_ok=True);(target/'index.html').write_text(text)
 print(target.relative_to(ROOT),n,'cards',len(text.encode()),'bytes')

build(CARDS,ROOT/'docs/mpc-workbench')
build([ALL[k] for k in HW_ORDER],ROOT/'docs/hw6',True)
source_map=[{'position':i+1,**{k:c[k] for k in ['id','title','kind','section','source','source_ref','requires']},'exercise':c.get('exercise'),'check_type':c['check']['type'],'labs':sorted(set(LAB.findall(c['body']+c['check']['solution'])))} for i,c in enumerate(CARDS)]
(ROOT/'docs/mpc-workbench/source-map.json').write_text(json.dumps(source_map,ensure_ascii=False,indent=2)+'\n')
issues=CORE_ISSUES+EXERCISE_ISSUES+SHAMIR_ISSUES
rows=''.join(f'<tr><th scope="row"><a href="./#{c["id"]}">{html.escape(c["title"])}</a></th><td>{html.escape(c["source"])}</td></tr>' for c in CARDS)
issues_html=''.join(f'<li>{html.escape(x)}</li>' for x in issues)
sources=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PETS · MPC sources and scope</title><link rel="stylesheet" href="../typography.css"><link rel="stylesheet" href="./style.css?v=1"></head><body><main class="shell reading sources-screen"><p><a href="./">← Return to the MPC lab</a></p><h1>Sources and teaching scope</h1><p>The learning path follows the printed lecture’s order, with homework inserted after its prerequisites. Each card contains a bounded question. New practice questions are authored for this lab; they are not presented as past MPC exam questions.</p><h2>Supplied course materials</h2><ul class="source-list"><li><strong>lecture17-18-19_mpc.pdf</strong>: 11 pages, Privacy Enhancing Technologies FS2026, Florian Tramèr. Defines MPC and develops additive sharing, GMW-style arithmetic evaluation, Beaver triples, malicious security and Shamir sharing.</li><li><strong>lecture17-18-19_notes.pdf</strong>: 17 handwritten pages. Reviewed alongside the printed notes, including the marked difficulty with Beaver’s algebra and the interpolation derivation.</li><li><strong>hw6_sol.pdf</strong>: 6 pages, Exercise Sheet 6, version 1, FS2025. All 16 subquestions appear with their assignment labels and worked reasoning.</li><li><strong>Privacy Enhancing Technologies HS 2025 Endterm (Solution).pdf</strong>: 8 supplied pages. This paper concerns differential privacy. It calibrates the scope of one-sentence counterexamples, short derivations and staged proofs; it contains no MPC exam questions.</li></ul><h2>What the experiments establish</h2><p>Small finite-field examples expose the mechanics and errors. They are not cryptographic software, empirical security estimates or substitutes for the general proofs. A full malicious MPC implementation, pairing implementation, and security proof of distributed preprocessing are outside the supplied lectures.</p><p>Written solutions use self-check criteria. Numerical and choice questions are checked automatically. Progress and draft answers are stored only in this browser’s local storage; the site sends no answers to a server.</p><h2>Clarifications to terse source arguments</h2><ul class="source-list">{issues_html}</ul><h2>Card-by-card source map</h2><div class="table-scroll"><table><thead><tr><th scope="col">Card</th><th scope="col">Source</th></tr></thead><tbody>{rows}</tbody></table></div><p><a href="./">Return to the learning path →</a></p></main></body></html>'''
(ROOT/'docs/mpc-workbench/sources.html').write_text(sources)
