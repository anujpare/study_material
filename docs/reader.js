(function(){
'use strict';
const root=document.getElementById('lessons');
const slider=document.getElementById('pet-card-slider');
const position=document.getElementById('pet-card-position');
if(!root||!slider||!position)return;
const slides=Array.from(root.querySelectorAll('section.slide'));
const count=slides.length;
if(!count)return;
// The chapter decks have different lengths; derive all bounds from their cards.
slider.min="1";
slider.max=String(count);
slider.step="1";
let current=1;

// Materialize SVG paths for all cards, including unopened solutions.
// Result: mathematical glyphs no longer reference a different, hidden SVG.
// This is essential for consistent Safari/WebKit and embedded-site display.
function resolveGlyphs(){
  const source=new Map();
  for(const p of root.querySelectorAll('#pet-math-glyph-sprite path[id]')) source.set(p.id,p.getAttribute('d'));
  const all=root.querySelectorAll('section.slide svg use[href^="#pet-math-glyph-"]');
  for(const use of all){
    const d=source.get(use.getAttribute('href').substring(1));
    if(!d)continue;
    const path=document.createElementNS('http://www.w3.org/2000/svg','path');
    path.setAttribute('d',d);
    for(const attr of Array.from(use.attributes)){
      if(attr.name!=='href'&&attr.name!=='xlink:href')path.setAttribute(attr.name,attr.value);
    }
    use.replaceWith(path);
  }
  // The sprite is no longer needed, and hidden shared glyphs cannot affect rendering.
  const sprite=document.getElementById('pet-math-glyph-sprite');if(sprite)sprite.remove();
}
resolveGlyphs();

function clamp(value){let n=Number(value);return Number.isFinite(n)?Math.max(1,Math.min(count,Math.round(n))):1;}
function fromHash(){
  const index=slides.findIndex(slide=>'#'+slide.id===location.hash);
  if(index>=0)return index+1;
  const alias=document.getElementById(location.hash.slice(1));
  const owner=alias?.classList.contains('card-alias')?alias.closest('section.slide'):null;
  if(owner)return slides.indexOf(owner)+1;
  // Retain the previous numeric out-of-range fallback for old links.
  const match=/^#lesson-(\d+)$/.exec(location.hash);
  return match?clamp(match[1]):1;
}

// Inspect actual rendered formula width. When a formula is wider than its text
// column, put it on a full-width line and resize the vector proportionately.
// This preserves the entire expression instead of silently clipping its right half.
function fitMath(slide){
  const reader=slide.querySelector('.reading');if(!reader)return;
  // Reset first so orientation changes also work.
  for(const el of slide.querySelectorAll('.pet-math-fit'))el.classList.remove('pet-math-fit');
  for(const mjx of slide.querySelectorAll('mjx-container')){
    const svg=mjx.querySelector(':scope > svg');if(!svg)continue;
    const holder=mjx.closest('.eq-inline, .mi.mathnew, .math.mathnew, .math');
    if(!holder)continue;
    const ancestor=mjx.closest('p, li, blockquote, .guide, .math, .reading');
    if(!ancestor)continue;
    let target=ancestor.getBoundingClientRect().width;
    const sty=getComputedStyle(ancestor);
    target-=parseFloat(sty.paddingLeft||0)+parseFloat(sty.paddingRight||0);
    if(ancestor.classList.contains('math'))target-=18;
    target=Math.max(100,target-4);
    const fullWidth=svg.getBoundingClientRect().width;
    if(fullWidth>target+3){holder.classList.add('pet-math-fit');}
  }
}
function render(n){
  const next=clamp(n);
  const changed=next!==current;
  current=next;
  slides.forEach((slide,i)=>{
    const active=i===current-1;
    slide.classList.toggle('pet-active',active);
    slide.setAttribute('aria-hidden',active?'false':'true');
    if(active&&changed){const reading=slide.querySelector('.reading');if(reading)reading.scrollTop=0;}
  });
  root.classList.add('pet-js-ready');
  slider.value=String(current);
  slider.setAttribute('aria-valuetext','Card '+current+' of '+count);
  position.textContent=current+' / '+count;
  fitMath(slides[current-1]);
}
function go(value,replace){
  let n=clamp(value);let hash='#'+slides[n-1].id;
  if(location.hash!==hash){if(replace)history.replaceState(null,'',hash);else history.pushState(null,'',hash);}
  render(n);
}
document.addEventListener('click',event=>{
  const node=event.target;if(!(node instanceof Element))return;
  const link=node.closest('#lessons .navbtn[href^="#"]');if(!link)return;
  const index=slides.findIndex(slide=>'#'+slide.id===link.getAttribute('href'));if(index<0)return;
  event.preventDefault();event.stopImmediatePropagation();go(index+1,false);
},true);
slider.addEventListener('input',()=>go(slider.value,true));
slider.addEventListener('change',()=>go(slider.value,true));
window.addEventListener('hashchange',()=>render(fromHash()));
window.addEventListener('popstate',()=>render(fromHash()));
window.addEventListener('resize',()=>fitMath(slides[current-1]));
window.addEventListener('pageshow',()=>render(fromHash()));
root.addEventListener('toggle',ev=>{
  if(ev.target.matches('details'))requestAnimationFrame(()=>fitMath(slides[current-1]));
},true);
render(fromHash());
})();
