(() => {
  "use strict";
  const cards = [
    ["witness", "A claim and its witness"],
    ["np", "Why checking is different from finding"],
    ["interaction", "The verifier asks a question"],
    ["guarantees", "Completeness and soundness"],
    ["zk", "What zero knowledge means"],
    ["commitments", "Hiding and binding"],
    ["permutation", "Relabeling a Hamiltonian graph"],
    ["ham-protocol", "The two Hamiltonicity challenges"],
    ["ham-proof", "Proving the protocol works"],
    ["simulation", "A simulator without the secret"],
    ["zk-proof", "Why the simulator succeeds"],
    ["repetition", "Sequential versus parallel messages"],
    ["cost", "Why parallel simulation is hard"],
    ["homework2", "Homework: composition proof"],
    ["knowledge", "Proof of knowledge and rewinding"],
    ["sigma", "Sigma protocols and soundness"],
    ["schnorr", "Schnorr’s protocol and completeness"],
    ["schnorr-zk", "Schnorr’s zero-knowledge simulator"],
    ["schnorr-ext", "Extracting Schnorr’s secret"],
    ["circuits", "Circuit satisfiability"],
    ["fiat-shamir", "Making the proof non-interactive"]
  ].map((a,i) => ({id:a[0],title:a[1],file:"card-"+String(i+1).padStart(2,"0")+".html"}));

  const $=id=>document.getElementById(id);
  const content=$("lesson"),select=$("jump"),previous=$("previous"),next=$("next"),counter=$("counter"),progress=$("progress"),label=$("current-label");
  let current=0,loading=0,lockedGuess=null,lockedChallenge=null,lockedBit=null;
  function idxFromHash(){const i=cards.findIndex(c=>c.id===decodeURIComponent(location.hash.slice(1)));return i<0?0:i;}
  function navigation(){
    current=idxFromHash();
    counter.textContent=String(current+1).padStart(2,"0")+" / "+String(cards.length).padStart(2,"0");
    progress.style.width=String(100*(current+1)/cards.length)+"%";
    previous.disabled=current===0;next.disabled=current===cards.length-1;
    select.value=cards[current].id;label.textContent=cards[current].title;
  }
  async function render(){
    navigation();
    lockedGuess=null;lockedChallenge=null;lockedBit=null;
    const request=++loading, card=cards[current];
    if(window.MathJax?.typesetClear){try{window.MathJax.typesetClear([content]);}catch(e){console.warn(e);}}
    content.innerHTML='<p class="loader">Loading the lesson…</p>';
    try{
      const res=await fetch(card.file,{cache:"no-store"});
      if(!res.ok)throw Error("HTTP "+res.status);
      const html=await res.text();
      if(request!==loading)return;
      const node=new DOMParser().parseFromString(html,"text/html").querySelector("article.lesson");
      if(!node)throw Error("Lesson article missing");
      content.innerHTML=node.outerHTML;
      window.scrollTo(0,0);
      document.title="PETS · "+card.title;
      initializeLab();
      typeset();
    }catch(e){
      if(request===loading)content.innerHTML='<p class="loader">Could not load this lesson. <a href="'+card.file+'">Open its source page</a>.</p>';
      console.error(e);
    }
  }
  async function typeset(){
    try{
      if(window.MathJax?.typesetPromise){await window.MathJax.typesetPromise([content]);}
    }catch(err){console.warn("Math rendering failed:",err);}
  }
  function go(delta){
    const n=current+delta;
    if(n<0||n>=cards.length)return;
    location.hash=cards[n].id;
  }
  previous.addEventListener("click",()=>go(-1));
  next.addEventListener("click",()=>go(1));
  select.addEventListener("change",()=>{location.hash=select.value;});
  window.addEventListener("hashchange",render);
  window.addEventListener("mathjax-ready",typeset);
  window.addEventListener("keydown",e=>{
    if(e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;
    if(e.target.closest("button,select,input,textarea,summary,[contenteditable]"))return;
    if(e.key==="ArrowRight"){e.preventDefault();go(1);}
    if(e.key==="ArrowLeft"){e.preventDefault();go(-1);}
  });
  function feedback(id,message,kind){
    const node=$(id);if(!node)return;
    node.className="feedback"+(kind?" "+kind:"");node.textContent=message;
  }
  function toggleGroup(button){const group=button.closest(".control-row");if(group)group.querySelectorAll("button[data-demo='"+button.dataset.demo+"']").forEach(b=>b.setAttribute("aria-pressed",String(b===button)));}
  function factorial(n){let k=1;for(let i=2;i<=n;i++)k*=i;return k;}
  function mod(n,m){return (n%m+m)%m;}
  function powmod(a,e,m){let result=1;for(let i=0;i<e;i++)result=(result*a)%m;return result;}
  function invmod(a,q){for(let i=1;i<q;i++)if(mod(a*i,q)===1)return i;return null;}
  const edges=[[1,2],[2,3],[3,4],[4,5],[5,1],[1,3],[2,4]];
  const cycle=[[1,2],[2,3],[3,4],[4,5],[5,1]];
  const permutation={1:2,2:4,3:1,4:5,5:3};
  const fixedRoute=[1,2,3,4,5,1];
  const fixedPermRoute=fixedRoute.map(v=>permutation[v]);
  const point={1:[180,27],2:[325,135],3:[270,285],4:[90,285],5:[35,135]};
  const edgeKey=(a,b)=>[Number(a),Number(b)].sort((x,y)=>x-y).join("-");
  function drawGraph(id,{permuted=false,route=null}={}){
    const container=$(id);if(!container)return;
    const map=x=>permuted?permutation[x]:x;
    const active=new Set((route||[]).slice(1).map((v,i)=>edgeKey(route[i],v)));
    const real=new Set(edges.map(([a,b])=>edgeKey(map(a),map(b))));
    const pos=v=>point[v];
    let markup='<svg class="graph-svg" viewBox="0 0 360 325" role="img" aria-label="Five-vertex graph; green edges show an indicated Hamiltonian cycle, gray edges are additional roads, and dashed red lines are missing roads">';
    for(const [a,b] of edges){
      const u=map(a),v=map(b),xy=pos(u),zw=pos(v);
      markup+='<line class="ordinary" x1="'+xy[0]+'" y1="'+xy[1]+'" x2="'+zw[0]+'" y2="'+zw[1]+'"/>';
    }
    if(route){
      for(let i=0;i<route.length-1;i++){
        const a=route[i],b=route[i+1],xy=pos(a),zw=pos(b),ok=real.has(edgeKey(a,b));
        markup+='<line class="'+(ok?"cycle":"invalid")+'" x1="'+xy[0]+'" y1="'+xy[1]+'" x2="'+zw[0]+'" y2="'+zw[1]+'"/>';
      }
    }
    for(let i=1;i<=5;i++){const xy=pos(i);markup+='<circle class="node" cx="'+xy[0]+'" cy="'+xy[1]+'" r="22"/><text class="node-text" x="'+xy[0]+'" y="'+xy[1]+'">'+i+'</text>';}
    markup+='</svg>';container.innerHTML=markup;
  }
  function graphRoute(which){
    const route=which==="valid"?fixedRoute:[1,2,4,3,5,1];
    drawGraph("witness-graph",{route});
    const real=new Set(edges.map(([a,b])=>edgeKey(a,b)));
    const list=[];for(let i=0;i<route.length-1;i++)list.push(route[i]+"→"+route[i+1]+": "+(real.has(edgeKey(route[i],route[i+1]))?"road exists":"NO ROAD"));
    const correct=route.length===6&&new Set(route.slice(0,-1)).size===5&&route[0]===route[route.length-1]&&route.slice(0,-1).every(v=>v>=1&&v<=5)&&route.slice(1).every((v,i)=>real.has(edgeKey(route[i],v)));
    feedback("route-result",(correct?"ACCEPT. ":"REJECT. ")+list.join("; ")+". "+(correct?"Every city occurs once before returning to city 1.":"A proposed list of cities is not a valid witness if even one required road is missing."),correct?"good":"bad");
  }
  function npUpdate(){const node=$("np-n");if(!node)return;const n=Number(node.value);$("np-n-label").textContent=n;const f=factorial(n-1);$("np-candidates").textContent=f.toLocaleString("en-US");$("np-checks").textContent=n.toLocaleString("en-US");$("np-bound").textContent="For "+n+" vertices, an elementary exhaustive search may inspect up to "+f.toLocaleString("en-US")+" different orderings after fixing the start. Given one proposed ordering, checking its "+n+" edges requires only "+n+" road tests. This comparison concerns the simple exhaustive algorithm; it does not prove that every algorithm needs factorial time.";}
  function toyTrial(){const chosen=document.querySelector("[data-demo='toy-prepare'][aria-pressed='true']");if(!chosen){feedback("toy-result","Choose the challenge your hypothetical cheater prepared an answer for before drawing the verifier’s challenge.","bad");return;}
    const prepared=Number(chosen.dataset.value),c=Math.random()<.5?0:1;
    feedback("toy-result","The prover prepared for c="+prepared+". The verifier now independently drew c="+c+". "+(c===prepared?"The prepared answer matched, so the cheater got lucky.":"The challenge differed, so this cheater cannot answer.")+" This toy illustrates why the order of messages matters; it is not itself a proof system.",c===prepared?"good":"bad");}
  function securityCase(which){
    const explanations={
      honest:"True statement, honest P and honest V: completeness applies. The course definition guarantees Pr[accept] ≥ 2/3; it does not claim certainty unless completeness is perfect.",
      cheat:"False statement, malicious P* and honest V: soundness applies. Regardless of the cheating strategy, Pr[accept] ≤ 1/3.",
      malicious:"True statement and malicious V*: neither honest-verifier completeness nor soundness forces V* to accept. A malicious verifier could always reject. Zero knowledge is instead a privacy guarantee concerning what V* learns."
    };
    feedback("security-result",explanations[which]||"",which==="cheat"?"bad":"");
  }
  function commitment(action){
    if(action==="zero"||action==="one"){
      lockedBit=action==="zero"?0:1;
      $("sealed-readout").textContent="Commitment: SEALED · original bit is hidden from the verifier.";
      feedback("commit-result","A fresh commitment to a bit has been made. The verifier sees only a sealed value. In a real commitment scheme, computational hiding prevents efficiently distinguishing 0 from 1.","");
    }else if(lockedBit===null){feedback("commit-result","First commit to 0 or 1. The opening must correspond to an already fixed commitment.","bad");
    }else if(action==="open"){
      $("sealed-readout").textContent="Opened bit: "+lockedBit+" · accepted as the original bit.";
      feedback("commit-result","Opening reveals the originally committed bit "+lockedBit+" and its opening randomness. Binding ensures the prover cannot make the same commitment open as the other bit.","good");
    }else if(action==="switch"){
      feedback("commit-result","REJECT. The prover tries to open the same commitment as "+(1-lockedBit)+", but it was fixed to "+lockedBit+". Perfect binding forbids two valid openings of one commitment to different values.","bad");
    }
  }
  function permute(reveal){
    drawGraph("graph-original",{route:fixedRoute});
    drawGraph("graph-permuted",{permuted:true,route:fixedPermRoute});
    const info=$("perm-result");
    if(info)info.textContent=reveal?"The fixed relabeling is π(1)=2, π(2)=4, π(3)=1, π(4)=5, π(5)=3. Applying π to the original cycle 1→2→3→4→5→1 yields 2→4→1→5→3→2. Every mapped pair remains an edge, so the two graphs are isomorphic.":"The two green cycles show the same road structure after renaming. Choose “Explain each relabeling” to trace exactly which old vertex becomes which new vertex.";
  }
  function matrixForChallenge(c){
    const permEdges=new Set(edges.map(([a,b])=>edgeKey(permutation[a],permutation[b])));
    const permCycle=new Set(cycle.map(([a,b])=>edgeKey(permutation[a],permutation[b])));
    let out='<div class="table-wrap"><table class="matrix" aria-label="Committed adjacency matrix for B"><thead><tr><th>B</th>';
    for(let i=1;i<=5;i++)out+='<th>'+i+'</th>';out+='</tr></thead><tbody>';
    for(let i=1;i<=5;i++){out+='<tr><th>'+i+'</th>';
      for(let j=1;j<=5;j++){const edge=edgeKey(i,j),visible=c===0||permCycle.has(edge);
        out+='<td class="'+(visible?"open":"sealed")+'">'+(visible?(permEdges.has(edge)?"1":"0"):"🔒")+'</td>';}
      out+='</tr>';}
    out+='</tbody></table></div>';
    $("ham-matrix").innerHTML=out;
    $("ham-openings").textContent=c===0?
      "Challenge c=0: reveal π and every B[i,j]. The verifier checks that B[i,j]=1 exactly when the corresponding original vertices π⁻¹(i), π⁻¹(j) are joined in G. The full permuted graph is disclosed.":
      "Challenge c=1: reveal only the five committed edges on the cycle 2→4→1→5→3→2. All five visible entries are 1. The verifier checks that the cycle visits every vertex once; π and the other committed edges stay concealed.";
  }
  function hamCase(which){
    const isomorphic=which==="isomorphic";
    feedback("ham-false-result",isomorphic?
      "The commitments correctly encode a graph isomorphic to G. Challenge 0 can pass, but because G has no Hamiltonian cycle, its isomorphic copy cannot contain one. Challenge 1 must fail.":
      "The committed graph is not isomorphic to G. Challenge 0 must fail, even if the prover deliberately committed to a graph containing an easy Hamiltonian cycle that could pass challenge 1.",
    "bad");
  }
  function simPreview(guess,challenge){
    const box=$("sim-preview");if(!box)return;
    const premEdges=new Set(edges.map(([a,b])=>edgeKey(permutation[a],permutation[b])));
    const cycleEdges=new Set(cycle.map(([a,b])=>edgeKey(permutation[a],permutation[b])));
    let h='<div class="table-wrap"><table class="matrix" aria-label="What the verifier may see after opening commitments"><thead><tr><th>B</th>';
    for(let j=1;j<=5;j++)h+='<th>'+j+'</th>';h+='</tr></thead><tbody>';
    for(let i=1;i<=5;i++){
      h+='<tr><th>'+i+'</th>';
      for(let j=1;j<=5;j++){
        const e=edgeKey(i,j),revealed=guess!==null&&challenge===guess&&(challenge===0||cycleEdges.has(e));
        const bit=guess===0?Number(premEdges.has(e)):Number(i!==j);
        h+='<td class="'+(revealed?"open":"sealed")+'">'+(revealed?bit:"🔒")+'</td>';
      }
      h+='</tr>';
    }
    box.innerHTML=h+'</tbody></table></div>';
  }
  function simulator(action){
    if(action==="zero"||action==="one"){
      lockedGuess=Number(action==="one");lockedChallenge=null;
      simPreview(lockedGuess,null);
      $("sim-prep").textContent="Prepared for ĉ="+lockedGuess+". Sealed commitments were sent. The verifier does not see whether the simulator prepared a relabeled G (ĉ=0) or a graph containing a known cycle (ĉ=1).";
      feedback("sim-result","Now let the verifier ask c=0 or c=1. A simulator must choose its preparation before receiving that challenge.","");
    }else if(lockedGuess===null){feedback("sim-result","The simulator must prepare and send commitments before the verifier chooses the challenge.","bad");}
    else if(lockedChallenge!==null){feedback("sim-result","The verifier already asked its challenge. To try a different preparation, start a NEW attempt; you cannot change sealed commitments mid-run.","bad");}
    else{lockedChallenge=Number(action==="ask-one");
      const ok=lockedChallenge===lockedGuess;
      simPreview(lockedGuess,lockedChallenge);
      feedback("sim-result","Simulator guessed ĉ="+lockedGuess+"; verifier asked c="+lockedChallenge+". "+(ok?
        "MATCH: simulator opens the prepared commitments in the requested manner and outputs an accepting-looking transcript. It never used a Hamiltonian cycle of G.":
        "MISMATCH: simulator cannot produce the requested consistent opening from this preparation. It aborts and rewinds/restarts the verifier from its saved state before attempting another commitment."),ok?"good":"bad");
    }
  }
  function oddsUpdate(){
    const inp=$("trials-k");if(!inp)return;const t=Number(inp.value);
    $("trials-n").textContent=t;
    $("trials-prob").textContent=(Math.pow(.5,t)*100).toFixed(t<=5?3:5).replace(/0+$/,"").replace(/\.$/,"")+"%";
    $("trials-words").textContent="Under independent, fair challenges the probability of requiring more than "+t+" attempts is (1/2)^"+t+". The expected number of attempts is 2, since a geometric random variable with success probability 1/2 has expectation 1/(1/2). This empirical panel is not a substitute for the hiding argument against a malicious verifier.";
  }
  function scheduleUpdate(){
    if(!$("schedule-messages"))return;
    const mode=document.querySelector("[data-demo='schedule'][aria-pressed='true']")?.dataset.value||"sequential",n=Number($("schedule-n")?.value||3);
    if($("schedule-n-label"))$("schedule-n-label").textContent=n;
    let msg=[];
    if(mode==="sequential"){
      for(let k=1;k<=n;k++){msg.push(["prover","P","Commitment u"+k]);msg.push(["verifier","V","Challenge c"+k+" (after seeing u"+k+")"]);msg.push(["prover","P","Response z"+k+"; round "+k+" completes"]);}
    }else{
      msg=[["prover","P","ALL commitments u1, …, u"+n+" sent together"],["verifier","V","ONE challenge vector (c1, …, c"+n+") after seeing ALL commitments"],["prover","P","ALL responses z1, …, z"+n+" sent together"]];
    }
    $("schedule-messages").innerHTML=msg.map(([kind,who,message])=>'<div class="message '+(kind==="prover"?"prover":"")+'"><span class="who">'+who+'</span><span>'+message+'</span></div>').join("");
    $("schedule-explain").textContent=mode==="sequential"?
      "There are "+(3*n)+" messages across "+n+" completed rounds. After the simulator finishes round 1, it can prepare round 2. It has to guess only one challenge at a time.":
      "There are still "+n+" internal instances, but only three batches of messages. The prover must commit to all "+n+" instances before learning any challenge, so the usual simulator must guess an entire "+n+"-bit challenge vector before the verifier responds.";
  }
  function compareCost(){
    const n=Number($("cost-n")?.value||4);if(!$("cost-n"))return;
    $("cost-label").textContent=n;
    $("cost-seq").textContent=String(2*n);
    $("cost-par").textContent=String(2**n);
    $("cost-sound").textContent="1 / "+String(2**n);
    $("cost-explain").textContent="At λ="+n+", each honest-verifier repetition has two possible challenges. Sequential simulation needs about 2 attempts per round, hence about 2λ="+(2*n)+" single-round attempts overall. The straightforward parallel simulator guesses one "+n+"-bit vector, succeeds with probability 1/"+(2**n)+", and requires about "+(2**n)+" whole-protocol attempts. This demonstrates why that simulator is inefficient for large λ; it does not prove parallel repetition is never zero knowledge.";
  }
  function extractGraph(which){
    const result=$("extract-result");if(!result)return;
    drawGraph("extract-b",{permuted:true,route:which==="c0"?null:fixedPermRoute});
    drawGraph("extract-g",{route:which==="combine"?fixedRoute:null});
    if(which==="c0"){result.textContent="From an accepting c=0 opening, the extractor learns the permutation π and every edge in the committed graph B. It has not yet seen a cycle.";
    }else if(which==="c1"){result.textContent="From an accepting c=1 opening with the SAME first commitments, the extractor learns a Hamiltonian cycle of B: 2→4→1→5→3→2. It has not yet learned which original vertices the labels represent.";
    }else{result.textContent="Combine BOTH accepting responses to the SAME committed first message: inverse-permute the revealed cycle. Since π⁻¹(2)=1, π⁻¹(4)=2, π⁻¹(1)=3, π⁻¹(5)=4, and π⁻¹(3)=5, we recover 1→2→3→4→5→1 in G. This is a valid witness, not merely a statement about the likelihood of cheating.";}
  }
  function sigmaUpdate(n){
    feedback("sigma-result","For a false statement and a fixed commitment u, special soundness forbids two distinct accepting challenges: otherwise extraction would yield an impossible witness. So at most one of "+n+" uniformly chosen challenges may pass, which gives soundness error ≤ 1/"+n+".","good");
  }
  function schnorrUpdate(){
    const x=Number($("schnorr-x")?.value||0),r=Number($("schnorr-r")?.value||0),c=Number($("schnorr-c")?.value||0);
    if(!$("schnorr-x"))return;
    const h=powmod(2,x,23),u=powmod(2,r,23),z=mod(r+c*x,11);
    const l=powmod(2,z,23),right=(u*powmod(h,c,23))%23;
    $("sx").textContent=x;$("sr").textContent=r;$("sc").textContent=c;
    $("schnorr-public").textContent="Public h = 2^"+x+" mod 23 = "+h+"; commitment u = 2^"+r+" mod 23 = "+u+"; response z = ("+r+" + "+c+"×"+x+") mod 11 = "+z+".";
    feedback("schnorr-result","Verifier computes g^z mod 23 = "+l+" and (u × h^c) mod 23 = "+right+". They are equal, so the honest response is ACCEPTED. This is one numerical instance of the algebraic proof below.","good");
  }
  function zkSchnorr(){
    const c=Math.floor(Math.random()*11),z=Math.floor(Math.random()*11),h=8,q=11,u=(powmod(2,z,23)*powmod(h,mod(q-c,q),23))%23;
    const lhs=powmod(2,z,23),rhs=(u*powmod(h,c,23))%23;
    feedback("hvzk-result","Simulator chooses c="+c+" and z="+z+" uniformly in {0,…,10}, then computes u=g^z·h^(−c) mod 23="+u+". Verification: g^z="+lhs+"; u·h^c="+rhs+" (mod 23). Both agree. The simulator used only public h=8, not secret x=3.",lhs===rhs?"good":"bad");
  }
  function schnorrExtract(){
    const cprime=Number($("extract-cprime")?.value||0);
    if(!$("extract-cprime"))return;
    $("extract-cprime-label").textContent=cprime;
    const c=2,z=10,zprime=mod(4+cprime*3,11),dif=mod(c-cprime,11),numerator=mod(z-zprime,11);
    if(cprime===c){feedback("schnorr-extraction","c′=c=2, so the two challenges are identical. The difference c−c′ is 0 modulo 11 and cannot be divided by. The extractor fails on this choice. Two independent random challenges collide with probability 1/11.","bad");return;}
    const inverse=invmod(dif,11),x=mod(numerator*inverse,11);
    feedback("schnorr-extraction","The first accepting transcript has c=2, z=10. The second has c′="+cprime+", z′="+zprime+". Thus (z−z′) mod 11="+numerator+", (c−c′) mod 11="+dif+", and its inverse is "+inverse+". The extracted x = "+numerator+"×"+inverse+" mod 11 = "+x+". Indeed the public h=8 equals 2^"+x+" mod 23.","good");
  }
  function gateUpdate(){
    if(!$("gate-result"))return;
    const gate=document.querySelector("[data-demo='gate'][aria-pressed='true']")?.dataset.value||"XOR";
    const a=Number($("gate-a")?.value||0),b=Number($("gate-b")?.value||0);
    const out=gate==="XOR"?(a^b):(a&b);
    $("gate-result").textContent="Gate "+gate+": input bits "+a+" and "+b+" determine output bit "+out+". A gate-level proof must establish that the commitments to its two inputs and its output satisfy this exact relation. Reusing the SAME wire commitment in neighboring gates prevents inconsistent claims about a shared wire.";
    $("gate-a-label").textContent=a;$("gate-b-label").textContent=b;
  }
  function fsUpdate(mode){
    const text=mode==="interactive"?
      "Interactive Σ protocol: P sends u → V chooses a random challenge c → P sends z → V checks verif(x,u,c,z). The verifier is an active participant and supplies fresh unpredictability.":
      "Fiat–Shamir: P computes c=H(x,u) locally and sends only (u,z). V independently computes the same H(x,u) and checks verif(x,u,H(x,u),z). The hash plays the role of the challenge; security arguments here use the random-oracle model.";
    feedback("fs-result",text);
  }
  function initializeLab(){
    drawGraph("witness-graph");npUpdate();drawGraph("graph-original",{route:fixedRoute});drawGraph("graph-permuted",{permuted:true,route:fixedPermRoute});
    drawGraph("extract-b",{permuted:true});drawGraph("extract-g");
    scheduleUpdate();compareCost();schnorrUpdate();schnorrExtract();gateUpdate();oddsUpdate();
  }
  document.addEventListener("click",e=>{
    const b=e.target.closest("button[data-demo]");if(!b||!content.contains(b))return;
    const d=b.dataset.demo,v=b.dataset.value;
    if(!["toy-trial","commit","sim-ask"].includes(d))toggleGroup(b);
    switch(d){
      case"path":graphRoute(v);break;
      case"toy-prepare":feedback("toy-result","The dishonest prover has prepared an answer only for c="+v+". Now the verifier may choose its bit. The prover cannot modify that earlier preparation.","");break;
      case"toy-trial":toyTrial();break;
      case"security":securityCase(v);break;
      case"commit":commitment(v);break;
      case"perm-view":permute(true);break;
      case"ham-challenge":matrixForChallenge(Number(v));break;
      case"ham-false":hamCase(v);break;
      case"sim-guess":simulator(v);break;
      case"sim-ask":simulator(v);break;
      case"schedule":scheduleUpdate();break;
      case"extract-graph":extractGraph(v);break;
      case"sigma":sigmaUpdate(Number(v));break;
      case"hvzk":zkSchnorr();break;
      case"fs":fsUpdate(v);break;
    }
  });
  document.addEventListener("input",e=>{
    if(!content.contains(e.target))return;
    switch(e.target.dataset.demo){
      case"np-slider":npUpdate();break;
      case"odds-slider":oddsUpdate();break;
      case"schedule-slider":scheduleUpdate();break;
      case"cost-slider":compareCost();break;
      case"schnorr-slider":schnorrUpdate();break;
      case"extract-slider":schnorrExtract();break;
      case"gate-slider":gateUpdate();break;
    }
  });
  select.innerHTML=cards.map((card,i)=>'<option value="'+card.id+'">'+String(i+1).padStart(2,"0")+" · "+card.title+"</option>").join("");
  render();
})();
