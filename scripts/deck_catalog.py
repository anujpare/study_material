"""Public deck names and navigation shared by both generators."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DECKS = {
 'commitment': ('Chapter 1', 'Commitment', 58),
 'zero-knowledge': ('Chapter 2', 'Zero Knowledge', 46),
 'snarks': ('Chapter 3', 'SNARKs', 48),
 'pir': ('Chapter 4', 'PIR', 44),
 'hw1': ('Homework 1', 'HW1', 15),
 'hw2': ('Homework 2', 'HW2', 13),
 'hw3': ('Homework 3', 'HW3', 12),
 'hw4': ('Homework 4', 'HW4', 15),
}
def links(current):
 return ''.join(f'<a href="../{key}/"'+(' aria-current="page"' if key==current else '')+f'><small>{kind} · {count} cards</small>{title}</a>' for key,(kind,title,count) in DECKS.items())

def refresh_menus():
 for deck in DECKS:
  f=ROOT/'docs'/deck/'index.html'
  if not f.exists(): continue
  text=f.read_text()
  # Preserve each deck's local shortcuts, replacing only cross-deck links.
  text=re.sub(r'(<span class="menu-brand">PETS</span>)(?:<a href="\.\./[^/]+/"[^>]*>.*?</a>)+',lambda m:m[1]+links(deck),text,count=1,flags=re.S)
  f.write_text(text)

