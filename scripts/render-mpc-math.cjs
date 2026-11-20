// Share glyph definitions within each static reader to keep mobile downloads small.
const fs=require('node:fs');
const {mathjax}=require('mathjax-full/js/mathjax.js');
const {TeX}=require('mathjax-full/js/input/tex.js');
const {SVG}=require('mathjax-full/js/output/svg.js');
const {liteAdaptor}=require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler}=require('mathjax-full/js/handlers/html.js');
const {AllPackages}=require('mathjax-full/js/input/tex/AllPackages.js');
const adaptor=liteAdaptor();RegisterHTMLHandler(adaptor);
const output=new SVG({fontCache:'global'});
const doc=mathjax.document('',{InputJax:new TeX({packages:AllPackages}),OutputJax:output});
const expressions=JSON.parse(fs.readFileSync(0,'utf8')),rendered={};
for(const tex of expressions){const svg=adaptor.outerHTML(doc.convert(tex,{display:false}));if(/data-mjx-error|merror|fill="red"/.test(svg))throw new Error('Invalid mathematics: '+tex);rendered[tex]=svg;}
const defs=adaptor.outerHTML(output.fontCache.getCache());
process.stdout.write(JSON.stringify({rendered,defs}));
