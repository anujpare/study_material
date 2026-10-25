"""Apply the reviewed beginner explanations and prerequisite order to all four decks.
Existing lesson-N URLs stay attached to the same original cards.
"""
from pathlib import Path
from html.parser import HTMLParser
import html,json,re,subprocess,sys
from beginner_content import TERMS,PATTERNS,PRIMERS,AIMS
from beginner_solutions import SOLUTIONS
ROOT=Path(__file__).resolve().parents[1]
class Prose(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag=='svg':self.skip+=1
  if not self.skip:
   a=dict(attrs)
   if a.get('role')=='math' and 'aria-label' in a:self.parts.append(a['aria-label'])
 def handle_endtag(self,tag):
  if tag=='svg':self.skip-=1
 def handle_data(self,text):
  if not self.skip:self.parts.append(text)
def prose(s):p=Prose();p.feed(s);return ' '.join(' '.join(p.parts).split())
def terms(s):return {k for k,pattern in PATTERNS.items() if re.search(pattern,prose(s),re.I)}
def nav(previous,next):
 def link(id,label,d):return f'<a aria-label="{label} card" class="navbtn" href="#{id}"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="{d}"/></svg></a>'
 return '<nav aria-label="Card navigation" class="nav">'+(link(previous,'Previous','m14.5 6.5-5.5 5.5 5.5 5.5') if previous else '<span class="navbtn" aria-disabled="true" aria-label="Previous card">‹</span>')+(link(next,'Next','m9.5 6.5 5.5 5.5-5.5 5.5') if next else '')+'</nav>'
def primer(key):
 title,body=PRIMERS[key]
 return f'<section class="slide theory beginner-lesson" id="start-{key}" data-prerequisite="{key}" aria-label="Start here · {title}"><header class="head"><div class="section">Start here · {title}</div></header><article class="reading">{body}</article>{nav(None,None)}</section>'
# Before-card insertions use stable original lesson IDs, not displayed position numbers.
INSERT={
 'commitment':{1:['notation','powers','bits','chance'],7:['algorithms'],20:['commit'],27:['oracle'],36:['group'],63:['ddh'],77:['linear']},
 'zero-knowledge':{1:['notation','powers','bits','chance','algorithms','proof'],3:['circuit'],19:['commit','graph'],26:['mod','group']},
 'hw1':{1:['notation','powers','bits','chance','algorithms','commit','oracle'],7:['mod','group'],11:['ddh'],16:['linear']},
 'hw2':{1:['notation','powers','bits','chance','algorithms','proof','circuit'],8:['commit','graph'],11:['mod','group']}}
PROSE_EDITS={
 'commitment':{
  1:[("You'll repeatedly see",'The letters are names for values. We will explain what each letter stands for when it is needed, so you do not have to memorize a list of cryptographic symbols before starting.')],
  2:[('Why is a truly random function','Suppose we store the output of a function in a table, with one row for every possible input. For n-bit inputs there are 2<sup>n</sup> rows. If each output needs k bits, the table needs k·2<sup>n</sup> bits. This is another example of an exponential cost.'),('This is the exact reason the random-oracle model','Counting the rows explains the storage cost: adding one input bit doubles the number of rows, even though the rule “add one bit” sounds like a small change.')],
  3:[('A distribution describes','A <strong>distribution</strong> lists the possible values and their probabilities. For a fair coin, the values are heads and tails, each with probability 1/2.')],
  4:[('This lets us prove statements like','For example, suppose an attacker makes Q guesses and each fixed guess has success probability at most 1/2<sup>n</sup>. Adding these Q probabilities gives an upper bound of Q/2<sup>n</sup> for any guess succeeding. A probability cannot exceed 1, so use 1 if that expression is larger.')],
  6:[('In cryptography, we often want','For example, consider the claim “if n² is even, then n is even.” Its contrapositive is “if n is odd, then n² is odd.” Proving the second statement proves the first, because an odd n could never produce an even square.')],
  7:[('Example: “Does this Boolean circuit','For example, a completed puzzle can be checked by testing its rules. That may be much easier than searching for a solution from scratch. The supplied solution is the witness. NP does not mean “not polynomial.”')]
 },
 'zero-knowledge':{
  5:[('Caution for later:','')],
  15:[('HW2 moves beyond the uploaded commitment lecture','The first homework questions ask which party must follow the protocol for each guarantee to apply. Keep the prover’s role separate from the verifier’s role as you read them.')]
 }
}
AUDIT=[]
def revise(deck):
 f=ROOT/'docs'/deck/'index.html';raw=f.read_text();allcards=list(re.finditer(r'<section\b.*?</section>',raw,re.S))
 original={int(m[1]):c[0] for c in allcards if (m:=re.search(r'id="lesson-(\d+)"',c[0]))}
 order=sorted(original)
 if deck=='zero-knowledge':
  # This exercise needs the graph protocol and its two challenges first.
  order.remove(6);order.insert(order.index(22)+1,6)
 seen=set();cards=[]
 for n in order:
  for key in INSERT[deck].get(n,[]):
   card=primer(key);cards.append(card);seen.update(terms(card))
  c=original[n]
  c=re.sub(r'<aside class="beginner-context".*?</aside>','',c,flags=re.S)
  # These older add-on boxes repeated the main explanation and sometimes named
  # advanced concepts before their lessons. Keep one continuous teaching path.
  c=re.sub(r'<div class="(?:guide|reasoning-link)">.*?</div>','',c,flags=re.S)
  for needle,replacement in PROSE_EDITS.get(deck,{}).get(n,[]):
   c=re.sub(r'<p\b[^>]*>.*?</p>',lambda m:('<p>'+replacement+'</p>' if replacement else '') if needle in prose(m[0]) else m[0],c,flags=re.S)
  source=deck if deck in AIMS else ('commitment' if deck=='hw1' else 'zero-knowledge')
  source_id=n if deck in AIMS else int(re.search(r'data-source-card="(\d+)"',c)[1])
  assert source_id in AIMS[source],(deck,n)
  if deck in SOLUTIONS and n in SOLUTIONS[deck]:
   heading,steps=SOLUTIONS[deck][n]
   solution='<div class="solution-content"><p><strong>'+heading+'</strong></p><ol>'+''.join('<li><p>'+step+'</p></li>' for step in steps)+'</ol></div></details>'
   c,count=re.subn(r'<div class="solution-content">.*?</div></details>',lambda _:solution,c,count=1,flags=re.S)
   assert count==1,(deck,n)
  # Use one name consistently after teaching it. Do not change mathematical SVGs.
  c=re.sub(r'(?<=>)[^<>]+(?=<)',lambda m:re.sub(r'\bsalts?\b',lambda t:'randomizers' if t[0].endswith('s') else 'randomizer',m[0],flags=re.I),c)
  used=terms(re.search(r'<article\b.*?</article>',c,re.S)[0]);new=used-seen
  definitions=''.join('<dt>'+html.escape(TERMS[t][0])+'</dt><dd>'+html.escape(TERMS[t][1])+'</dd>' for t in TERMS if t in new)
  context='<aside class="beginner-context" data-source="'+source+'-'+str(source_id)+'"'+('' if definitions else ' hidden')+'>'
  if definitions:context+='<div class="new-terms"><h3>New words for this lesson</h3><dl>'+definitions+'</dl></div>'
  context+='</aside>'
  c=c.replace('<article class="reading">','<article class="reading">'+context,1)
  cards.append(c);seen.update(used)
  AUDIT.append({'deck':deck,'id':'lesson-'+str(n),'source':source_id,'new_terms':sorted(new),'available_terms':sorted(used),'worked_solution_rewritten':source_id in SOLUTIONS.get(source,{})})
 ids=[re.search(r'id="([^"]+)"',c)[1] for c in cards]
 assert len(ids)==len(set(ids))
 for i,c in enumerate(cards):cards[i]=re.sub(r'<nav aria-label="Card navigation".*?</nav>',lambda _:nav(ids[i-1] if i else None,ids[i+1] if i+1<len(ids) else None),c,flags=re.S)
 prefix=raw[:allcards[0].start()];suffix=raw[allcards[-1].end():]
 suffix=re.sub(r'1 / \d+',f'1 / {len(cards)}',suffix);suffix=re.sub(r'Card 1 of \d+',f'Card 1 of {len(cards)}',suffix);suffix=re.sub(r'max="\d+"',f'max="{len(cards)}"',suffix)
 f.write_text(prefix+''.join(cards)+suffix)
 return len(cards)
counts={deck:revise(deck) for deck in ['commitment','zero-knowledge']}
subprocess.run([sys.executable,str(ROOT/'scripts/build-homework.py')],check=True)
counts.update({deck:revise(deck) for deck in ['hw1','hw2']})
for deck in counts:
 f=ROOT/'docs'/deck/'index.html';s=f.read_text()
 for key,total in counts.items():
  s=re.sub(r'(<a href="../'+key+r'/"[^>]*><small>[^<]*?· )\d+( cards)',rf'\g<1>{total}\2',s)
 # Label shortcuts by stable lesson reference; visual position now includes prerequisite lessons.
 s=re.sub(r'<small>Card (\d+)</small>',r'<small>Lesson \1</small>',s)
 s=s.replace('<div class="menu-experiments">','<a href="#start-notation" class="beginner-start">Start from the basics</a><div class="menu-experiments">') if 'class="beginner-start"' not in s else s
 f.write_text(s)
landing=ROOT/'docs/index.html';s=landing.read_text()
for deck,total in counts.items():
 pattern=r'(<a class="card" href="./'+deck+r'/">.*?<div class="meta">)\d+( cards)'
 s=re.sub(pattern,rf'\g<1>{total}\2',s,flags=re.S)
s=s.replace('Follow the explanations, try the interactive visualizations, and reveal each solution step by step.','Each deck starts from the basics and introduces new concepts before using them. Try the interactive visualizations and follow each worked solution step by step.')
landing.write_text(s)
(ROOT/'scripts/beginner-audit.json').write_text(json.dumps({'counts':counts,'original_cards_reviewed':len(AUDIT),'cards':AUDIT},indent=2)+'\n')
print('Beginner decks:',counts,'; original cards revised:',len(AUDIT))
