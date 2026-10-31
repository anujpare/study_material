(() => {
  "use strict";
  const cards = [
    ["np","Why checking is different from finding","card-02.html"],
    ["interaction","The verifier asks a question","card-03.html"],
    ["guarantees","Completeness and soundness","card-04.html"],
    ["lecture-power","Why interaction expands what we can prove","lecture-power.html"],
    ["lecture-applications","When privacy is actually needed","lecture-applications.html"],
    ["zk","What zero knowledge means","card-05.html"],
    ["commitments","Hiding and binding","card-06.html"],
    ["hw1-security","HW1 · Hiding and binding","hw1-security.html"],
    ["hw1-pedersen","HW1 · Pedersen and ElGamal","hw1-pedersen.html"],
    ["witness","A claim and its witness","card-01.html"],
    ["permutation","Relabeling a Hamiltonian graph","card-07.html"],
    ["ham-protocol","The two Hamiltonicity challenges","card-08.html"],
    ["ham-proof","Proving the protocol works","card-09.html"],
    ["simulation","A simulator without the secret","card-10.html"],
    ["zk-proof","Why the simulator succeeds","card-11.html"],
    ["hw2-conceptual","HW2 · Conceptual security questions","hw2-conceptual.html"],
    ["repetition","Sequential versus parallel messages","card-12.html"],
    ["cost","Why parallel simulation is hard","card-13.html"],
    ["homework2","Homework: composition proof","card-14.html"],
    ["knowledge","Proof of knowledge: what must be extracted?","card-15.html"],
    ["knowledge-extraction","Extract a Hamiltonian cycle by rewinding","knowledge-extraction.html"],
    ["sigma","Sigma protocols and soundness","card-16.html"],
    ["schnorr","Schnorr’s protocol and completeness","card-17.html"],
    ["schnorr-zk","Schnorr’s zero-knowledge simulator","card-18.html"],
    ["schnorr-ext","Extracting Schnorr’s secret","card-19.html"],
    ["circuits","Circuit satisfiability","card-20.html"],
    ["nizk-limits","Why plain-model NIZK faces an obstacle","nizk-limits.html"],
    ["fiat-shamir","Construct a proof without interaction","card-21.html"],
    ["fiat-shamir-security","Prove privacy and extract knowledge in ROM","fiat-shamir-security.html"],
    ["hw3-fs-schnorr","HW3 · Noninteractive Schnorr","hw3-fs-schnorr.html"],
    ["hw3-fs-attacks","HW3 · Guessing and transfer","hw3-fs-attacks.html"],
    ["hw3-amplify","HW3 · Amplify before Fiat–Shamir","hw3-amplify.html"],
    ["hw1-vector","HW1 · Vector commitments","hw1-vector.html"],
    ["hw3-pcp","Optional · SNARG construction","hw3-pcp.html"],
    ["hw3-roots","Optional · Root bound over Z₆","hw3-roots.html"]
  ].map(a => ({id:a[0],title:a[1],file:a[2]}));

  const $=id=>document.getElementById(id);
  const content=$("lesson"),select=$("jump"),previous=$("previous"),next=$("next"),counter=$("counter"),slider=$("deck-slider"),position=$("position"),menu=$("chapter-menu"),headerTitle=$("header-title");
  let current=0,loading=0,lockedGuess=null,lockedChallenge=null,lockedBit=null,readingMode="guided";
  const coreIds=new Set([
    "witness","np","interaction","guarantees","lecture-power","lecture-applications",
    "zk","commitments","hw1-security","hw1-pedersen","permutation","ham-protocol","ham-proof","simulation","zk-proof","hw2-conceptual",
    "repetition","cost","homework2","knowledge","knowledge-extraction","sigma","schnorr","schnorr-zk","schnorr-ext",
    "circuits","nizk-limits","fiat-shamir","fiat-shamir-security","hw3-fs-schnorr","hw3-fs-attacks","hw3-amplify"
  ]);
  const exerciseOrigins={
    "hw1-security":"commitments",
    "hw1-pedersen":"commitments",
    "homework2":"cost",
    "hw3-fs-schnorr":"fiat-shamir",
    "hw3-fs-attacks":"fiat-shamir",
    "hw3-amplify":"fiat-shamir",
    "hw1-vector":"fiat-shamir",
    "hw3-pcp":"fiat-shamir",
    "hw3-roots":"fiat-shamir"
  };
  function routeCards(){return readingMode==="all"?cards:cards.filter(c=>coreIds.has(c.id));}
  function neighbor(delta){
    const list=routeCards();
    const index=list.findIndex(c=>c.id===cards[current].id);
    if(index>=0)return list[index+delta]||null;
    if(delta>0)return list.find(c=>cards.indexOf(c)>current)||null;
    return [...list].reverse().find(c=>cards.indexOf(c)<current)||null;
  }
  function updateFooter(){
    const card=cards[current],list=routeCards(),index=list.findIndex(c=>c.id===card.id);
    const label=index>=0?(index+1)+" / "+list.length:"Practice";
    counter.textContent=label;position.textContent=label;
    const thumb=index>=0?index+1:Math.max(1,list.filter(c=>cards.indexOf(c)<current).length);
    slider.min="1";slider.max=String(list.length);slider.value=String(thumb);
    slider.setAttribute("aria-valuetext",index>=0?"Lesson "+(index+1)+" of "+list.length+": "+card.title:"Optional exercise: "+card.title);
    previous.disabled=!neighbor(-1);next.disabled=!neighbor(1);
  }
  let soundnessSetup=null,soundnessChecked=false;
  function idxFromHash(){const i=cards.findIndex(c=>c.id===decodeURIComponent(location.hash.slice(1)));return i<0?0:i;}
  function setMenuOpen(open){
    const drawer=$("chapter-menu"),button=$("menu-toggle"),panel=$("chapter-panel");
    if(!drawer||!button||!panel)return;
    drawer.dataset.open=open?"true":"false";
    button.setAttribute("aria-expanded",open?"true":"false");
    panel.hidden=!open;
  }
  function closeMenu(){setMenuOpen(false)}
  function navigation(){
    current=idxFromHash();
    const card=cards[current];
    updateFooter();
    select.value=card.id;headerTitle.textContent=card.title;
    closeMenu();
  }
  async function render(){
    navigation();
    lockedGuess=null;lockedChallenge=null;lockedBit=null;
    soundnessSetup=null;soundnessChecked=false;
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
      if(!coreIds.has(card.id)){
        const source=cards.find(c=>c.id===exerciseOrigins[card.id]);
        if(source)content.insertAdjacentHTML("afterbegin",
          '<div class="practice-back"><a href="#'+source.id+'">← Back to '+source.title+'</a><span>Optional worked exercise</span></div>');
        const cont=neighbor(1);
        if(cont)content.insertAdjacentHTML("beforeend",
          '<div class="practice-forward"><a href="#'+cont.id+'">Continue the explanation: '+cont.title+' →</a></div>');
      }
      content.scrollTop=0;
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
  function go(delta){const target=neighbor(delta);if(target)location.hash=target.id;}
  previous.addEventListener("click",()=>go(-1));
  next.addEventListener("click",()=>go(1));
  $("menu-toggle").addEventListener("click",()=>setMenuOpen($("chapter-menu").dataset.open!=="true"));
  select.addEventListener("change",()=>{location.hash=select.value;closeMenu();});
  $("reading-mode").addEventListener("change",e=>{
    readingMode=e.target.value==="all"?"all":"guided";
    navigation();
  });
  slider.addEventListener("input",()=>{
    const n=Number(slider.value);
    position.textContent=n+" / "+routeCards().length;
  });
  slider.addEventListener("change",()=>{
    const target=routeCards()[Number(slider.value)-1];
    if(target)location.hash=target.id;
    else updateFooter();
  });
  document.addEventListener("pointerdown",event=>{
    if(menu?.dataset.open==="true"&&!menu.contains(event.target))closeMenu();
  });
  document.addEventListener("keydown",event=>{
    if(event.key==="Escape"&&menu?.dataset.open==="true")closeMenu();
  });
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
  function drawGraph(id,{permuted=false,route=null,mapping=permutation}={}){
    const container=$(id);if(!container)return;
    const map=x=>permuted?mapping[x]:x;
    const active=new Set((route||[]).slice(1).map((v,i)=>edgeKey(route[i],v)));
    const real=new Set(edges.map(([a,b])=>edgeKey(map(a),map(b))));
    const pos=v=>point[v];
    let markup='<svg class="graph-svg" viewBox="0 0 360 325" role="img" aria-label="Five-vertex graph; green segments represent existing edges of the candidate vertex sequence, gray segments other edges, and dashed red segments consecutive vertex pairs that are not edges">';
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
    const list=[];for(let i=0;i<route.length-1;i++)list.push(route[i]+"→"+route[i+1]+": "+(real.has(edgeKey(route[i],route[i+1]))?"edge exists in E":"not an edge of E"));
    const correct=route.length===6&&new Set(route.slice(0,-1)).size===5&&route[0]===route[route.length-1]&&route.slice(0,-1).every(v=>v>=1&&v<=5)&&route.slice(1).every((v,i)=>real.has(edgeKey(route[i],v)));
    feedback("route-result",(correct?"ACCEPT. ":"REJECT. ")+list.join("; ")+". "+(correct?"Each vertex occurs exactly once before returning to vertex 1.":"This candidate vertex sequence is not a Hamiltonian cycle because a required consecutive pair is not an edge."),correct?"good":"bad");
  }
  function npUpdate(){const node=$("np-n");if(!node)return;const n=Number(node.value);$("np-n-label").textContent=n;const f=factorial(n-1);$("np-candidates").textContent=f.toLocaleString("en-US");$("np-checks").textContent=n.toLocaleString("en-US");$("np-bound").textContent="For "+n+" vertices, an elementary exhaustive search may inspect up to "+f.toLocaleString("en-US")+" different orderings after fixing the start. Given one proposed cyclic ordering, checking its "+n+" consecutive vertex pairs requires "+n+" edge-membership tests, plus the distinctness and coverage checks. This comparison concerns the simple exhaustive algorithm; it does not prove that every algorithm needs factorial time.";}
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
  /* The lecture's Π maps NEW vertex labels back to OLD labels.
     "permutation" is explicitly the inverse Π^{-1}: OLD label -> NEW label.
     This choice makes the graph drawing operation a direct original-to-new mapping. */
  const alternateOriginalToNew={1:5,2:3,3:2,4:1,5:4};
  function permute(choice="one"){
    const originalToNew=choice==="two"?alternateOriginalToNew:permutation;
    const newToOriginal={};
    for(let original=1;original<=5;original++)newToOriginal[originalToNew[original]]=original;
    const route=fixedRoute.map(original=>originalToNew[original]);
    drawGraph("graph-original",{route:fixedRoute});
    drawGraph("graph-permuted",{permuted:true,route,mapping:originalToNew});
    const table=$("perm-table");
    if(table){
      let markup='<div class="table-wrap"><table class="matrix" aria-label="Two directions of the vertex permutation"><thead><tr><th>New label i in B</th>';
      for(let i=1;i<=5;i++)markup+='<th>'+i+'</th>';
      markup+='</tr></thead><tbody><tr><th>Original label Π(i) in G</th>';
      for(let i=1;i<=5;i++)markup+='<td>'+newToOriginal[i]+'</td>';
      markup+='</tr><tr><th>New label Π⁻¹(j) for original j</th>';
      for(let i=1;i<=5;i++)markup+='<td>'+originalToNew[i]+'</td>';
      markup+='</tr></tbody></table></div>';
      table.innerHTML=markup;
    }
    const info=$("perm-result");
    if(info)info.textContent="Original edge {1,2} becomes edge {"+originalToNew[1]+","+originalToNew[2]+"} in B. The full cycle 1→2→3→4→5→1 becomes "+route.join("→")+". Each edge and each distinct vertex is preserved, so the relabeled graph is isomorphic to G. The verifier does not learn these mappings in the c=1 branch.";
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
      "Challenge c=0: reveal Π and every B[i,j]. The verifier checks that B[i,j]=1 exactly when the corresponding original vertices Π(i), Π(j) are joined in G. The full permuted graph is disclosed.":
      "Challenge c=1: reveal only the five committed edges on the cycle 2→4→1→5→3→2. All five visible entries are 1. The verifier checks that the cycle visits every vertex once; Π and the other committed edges stay concealed.";
  }
  function drawFalseGraph(id,withCycle){
    const target=$(id);if(!target)return;
    if(withCycle===null){target.innerHTML='<p class="readout">No committed graph has been fixed yet.</p>';return;}
    const pathEdges=[[1,2],[2,3],[3,4],[4,5]];
    let h='<svg class="graph-svg" viewBox="0 0 360 325" role="img" aria-label="'+(withCycle?"Five-vertex cycle with an added closing edge between 5 and 1":"Five-vertex path, endpoints 1 and 5 have only one edge and cannot lie on a Hamiltonian cycle")+'">';
    for(const [a,b] of pathEdges){
      const u=point[a],v=point[b];
      h+='<line class="ordinary" x1="'+u[0]+'" y1="'+u[1]+'" x2="'+v[0]+'" y2="'+v[1]+'"/>';
    }
    const a=point[5],b=point[1];
    h+='<line class="'+(withCycle?"cycle":"invalid")+'" x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'"/>';
    for(let i=1;i<=5;i++){const p=point[i];h+='<circle class="node" cx="'+p[0]+'" cy="'+p[1]+'" r="22"/><text class="node-text" x="'+p[0]+'" y="'+p[1]+'">'+i+'</text>';}
    h+='</svg>';target.innerHTML=h;
  }
  function hamCase(which){
    soundnessSetup=which;soundnessChecked=false;
    drawFalseGraph("ham-false-public",false);
    drawFalseGraph("ham-false-hidden",which==="different");
    feedback("ham-false-result",which==="isomorphic"?
      "The prover fixed B as the same five-vertex PATH as G₀. The isomorphism check (c=0) can pass, but a cycle check (c=1) must fail because vertices 1 and 5 each have degree 1, so each has fewer than the two incident edges required by a Hamiltonian cycle. Choose one challenge.":
      "The prover fixed B as a five-vertex CYCLE. The additional edge {1,5} completes a Hamiltonian cycle, but means B is not isomorphic to the public path G₀. Choose one challenge.");
  }
  function hamFalseChallenge(c){
    if(soundnessSetup===null){feedback("ham-false-result","The prover must first choose and fix its committed graph B. A challenge cannot precede the commitments.","bad");return;}
    if(soundnessChecked){feedback("ham-false-result","This verifier has already challenged this committed first message. A fresh experimental run requires fixing a NEW first message; the prover cannot rewind the real verifier to change c.","bad");return;}
    soundnessChecked=true;
    const iso=soundnessSetup==="isomorphic",pass=(iso&&c===0)||(!iso&&c===1);
    const reason=iso?(c===0?
      "B is exactly a relabeling of G₀, so opening the graph and permutation passes the isomorphism check.":
      "B is a path. Its degree-one endpoints cannot belong to any Hamiltonian cycle, so the requested cycle opening is impossible.")
      :(c===0?
      "B contains the edge {1,5}, which is absent from the path graph G₀. Therefore B is not isomorphic to G₀. The isomorphism check fails.":
      "B contains the cycle 1→2→3→4→5→1, so the verifier can check opened cycle edges and accept that challenge.");
    feedback("ham-false-result",(pass?"ACCEPT on this ONE challenge. ":"REJECT on this challenge. ")+reason+
      " Because the first commitment was fixed before the random bit, the cheating prover can answer at most one of the two equally likely questions.",
      pass?"good":"bad");
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
    const mode=document.querySelector("[data-demo='schedule'][aria-pressed='true']")?.dataset.value||"sequential";
    const n=Number($("schedule-n")?.value||3);
    if($("schedule-n-label"))$("schedule-n-label").textContent=String(n);
    const messages=[];
    function add(sender,payload,action){
      const left=sender==="P"?"<b>P → V: "+payload+"</b>"+action:"<b>V → P: "+payload+"</b>Prover receives the challenge.";
      const right=sender==="V"?"<b>V → P: "+payload+"</b>Verifier chooses and sends the challenge.":"<b>P → V: "+payload+"</b>Verifier receives and "+(payload.startsWith("z")?"checks the response.":"keeps the first message.");
      messages.push('<div class="zk-exchange-row'+(sender==="V"?' zk-from-right':'')+'"><div>'+left+'</div><div>'+right+'</div></div>');
    }
    if(mode==="sequential"){
      for(let i=1;i<=n;i++){
        add("P","u"+i,"Prover prepares first message for run "+i+".");
        add("V","c"+i,"");
        add("P","z"+i,"Prover responds to challenge "+i+".");
      }
    }else{
      add("P","(u1,…,u"+n+")","Prover prepares ALL "+n+" first messages.");
      add("V","(c1,…,c"+n+")","");
      add("P","(z1,…,z"+n+")","Prover responds to the entire challenge vector.");
    }
    $("schedule-messages").innerHTML=messages.join("");
    $("schedule-explain").textContent=mode==="sequential"?
      "The first complete conversation finishes before the next begins. A simulator may retry that conversation without restarting later ones, because they have not begun.":
      "Every first message is fixed before the verifier reveals any challenge. The simple simulator that guesses each challenge must now prepare all "+n+" guesses together.";
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
    if(which==="c0"){result.textContent="From an accepting c=0 opening, the extractor learns the permutation Π and every edge in the committed graph B. It has not yet seen a cycle.";
    }else if(which==="c1"){result.textContent="From an accepting c=1 opening with the SAME first commitments, the extractor learns a Hamiltonian cycle of B: 2→4→1→5→3→2. It has not yet learned which original vertices the labels represent.";
    }else{result.textContent="Combine BOTH accepting responses to the SAME committed first message: inverse-permute the revealed cycle. Since Π⁻¹(2)=1, Π⁻¹(4)=2, Π⁻¹(1)=3, Π⁻¹(5)=4, and Π⁻¹(3)=5, we recover 1→2→3→4→5→1 in G. This is a valid witness, not merely a statement about the likelihood of cheating.";}
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
    if($("schnorr-msg-u-p")){
      $("schnorr-msg-u-p").textContent="Secret r="+r+". Compute u = 2^"+r+" mod 23 = "+u+". Send u="+u+".";
      $("schnorr-msg-u-v").textContent="Receive u="+u+". The verifier does not know r.";
      $("schnorr-msg-c-p").textContent="Receive c="+c+" after u was already sent.";
      $("schnorr-msg-c-v").textContent="Send challenge c="+c+" (selected from 0,…,10).";
      $("schnorr-msg-z-p").textContent="Compute z=("+r+"+"+c+"×"+x+") mod 11 = "+z+". Send z="+z+".";
      $("schnorr-msg-z-v").textContent="Check 2^"+z+" mod 23 = "+l+" and ("+u+"×"+h+"^"+c+") mod 23 = "+right+". They match: ACCEPT.";
    }
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
    const flow=$("fs-flow");
    if(!flow)return;
    const interactive=mode!=="noninteractive";
    const parts=interactive?[
      ["P","u","Prover computes u, then sends it.","Verifier receives the first message."],
      ["V","c","Prover receives c only after sending u.","Verifier samples and sends a uniformly random challenge c."],
      ["P","z","Prover computes the response z.","Verifier checks verif(x,u,c,z)."]
    ]:[
      ["P","π = (u,z)","Prover computes u, sets c=H(x,u), computes z and sends both u and z.","Verifier receives the proof, recomputes c=H(x,u), and checks verif(x,u,c,z)."]
    ];
    flow.innerHTML=parts.map(function(p){
      const label=(p[0]==="P"?"P → V":"V → P")+": "+p[1];
      return '<div class="zk-exchange-row'+(p[0]==="V"?' zk-from-right':'')+'"><div><b>'+label+'</b>'+p[2]+'</div><div><b>'+label+'</b>'+p[3]+'</div></div>';
    }).join("");
    feedback("fs-result",interactive?
      "Three transmitted messages. The verifier chooses c after seeing u; the prover can compute z only after receiving c.":
      "One transmitted proof with two values, u and z. Both parties calculate the challenge c independently using the same public hash rule.");
  }
  function pedersenUpdate(){
    const select=$("pedersen-new");if(!select)return;
    const q=11,p=23,g=2,h=8,t=3,m=4,r=2,mp=Number(select.value);
    const inv=invmod(t,q),rp=mod(r+(m-mp)*inv,q);
    const C=(powmod(g,m,p)*powmod(h,r,p))%p;
    const C2=(powmod(g,mp,p)*powmod(h,rp,p))%p;
    $("pedersen-new-label").textContent=String(mp);
    $("pedersen-alternative").textContent="m′="+mp+", r′="+rp;
    feedback("pedersen-result",
      "Original: 2^4 × 8^2 mod 23 = "+C+". Alternative: 2^"+mp+" × 8^"+rp+" mod 23 = "+C2+". "+
      (mp===m?"These are the same message with the same salt. Choose a different message to demonstrate loss of binding.":"The same fixed commitment "+C+" has two valid openings to DIFFERENT messages. Binding fails because the committer knows t=3 and can calculate t⁻¹=4 modulo 11."),
      mp===m?"":"bad");
  }
  function fsQueryUpdate(){
    const input=$("fs-query-q");if(!input)return;
    const Q=Number(input.value),q=11;
    $("fs-query-count").textContent=String(Q);
    $("fs-query-bound").textContent=Q+"/"+q+" = "+(100*Q/q).toFixed(1)+"%";
    $("fs-query-exact").textContent=(100*(1-Math.pow(1-1/q,Q))).toFixed(2)+"%";
    feedback("fs-query-result",
      "Each candidate fixes its response z and commitment u BEFORE the oracle reply. Its unique winning challenge is c=2. For Q="+Q+" distinct inputs, the union bound is Q/11; when the outputs are independent, exact success chance is 1−(10/11)^Q. A repeated query to one input would NOT count as another independent attempt.");
  }
  function fsQueryRun(){
    const inp=$("fs-query-q");if(!inp)return;
    const Q=Number(inp.value),q=11,p=23,h=8,winning=2;
    const inverseH=powmod(h,q-winning,p);
    const rows=[];
    let wins=0;
    // A new independent toy random oracle is sampled on each button click.
    // The Q first messages differ because z ranges from 0 to Q−1 in a prime-order group.
    for(let z=0;z<Q;z++){
      const u=(powmod(2,z,p)*inverseH)%p;
      const c=Math.floor(Math.random()*q),ok=c===winning;
      if(ok)wins++;
      rows.push("z="+z+", u="+u+": H(h,u)="+c+" → "+(ok?"ACCEPT":"reject"));
    }
    feedback("fs-query-result",
      "Fresh toy-oracle experiment: "+wins+"/"+Q+" guesses accepted. Each z fixes a different u BEFORE asking H, and each query has one winning answer c=2. "+rows.join(" | ")+
      ". A second run resets the simulated oracle; repeatedly querying the same input WITHOUT resetting would always return its previous value.",
      wins?"good":"");
  }
  function fsAmplifyUpdate(){
    const a=$("fs-lambda"),b=$("fs-budget");if(!a||!b)return;
    const n=Number(a.value),Q=Number(b.value),space=2**n,p=1/space;
    const union=Math.min(1,Q*p),exact=1-Math.pow(1-p,Q);
    $("fs-lambda-label").textContent=String(n);
    $("fs-budget-label").textContent=Q.toLocaleString("en-US");
    $("fs-one").textContent="1 / "+space.toLocaleString("en-US");
    $("fs-many").textContent=(100*union).toFixed(3)+"%";
    feedback("fs-amplify-result",
      "A fixed commitment vector for a false statement can pass at most one of "+space.toLocaleString("en-US")+
      " uniform challenge vectors. One attempt has probability at most "+(100*p).toPrecision(4)+
      "%. For Q="+Q+" fresh candidate hashes, the union bound is min(1,Q/2^λ)="+(100*union).toFixed(3)+
      "%. If all candidate hash outcomes are independent with one winning vector each, exact success probability is "+(100*exact).toFixed(3)+"%.");
  }
  function merkleUpdate(){
    const input=$("merkle-leaf");if(!input)return;
    const i=Number(input.value),chosen=i-1;
    const levels=[
      [{name:"c",x:340,y:35}],
      [{name:"c14",x:170,y:115},{name:"c58",x:510,y:115}],
      ["c12","c34","c56","c78"].map((name,j)=>({name,x:85+170*j,y:195})),
      ["c1","c2","c3","c4","c5","c6","c7","c8"].map((name,j)=>({name,x:42.5+85*j,y:280}))
    ];
    const path=[0,Math.floor(chosen/4),Math.floor(chosen/2),chosen];
    const siblings=[path[1]^1,path[2]^1,path[3]^1];
    const labels=["leaf", "pair", "half"];
    let svg='<svg viewBox="0 0 680 323" role="img" aria-label="Binary Merkle tree, selected leaf in green, ancestors in blue, required sibling hashes in amber">';
    for(let l=0;l<3;l++){
      for(let j=0;j<levels[l+1].length;j++){
        const parent=levels[l][Math.floor(j/2)],child=levels[l+1][j];
        const route=path[l+1]===j,required=siblings[l]===j;
        svg+='<line x1="'+parent.x+'" y1="'+parent.y+'" x2="'+child.x+'" y2="'+child.y+'" stroke="'+(route?"#1961a0":required?"#bf7d22":"#b9c7cd")+'" stroke-width="'+(route?6:required?4:2)+'"/>';
      }
    }
    for(let l=0;l<levels.length;l++){
      for(let j=0;j<levels[l].length;j++){
        const v=levels[l][j],onPath=path[l]===j,required=l>0&&siblings[l-1]===j,leafSelected=l===3&&j===chosen;
        const fill=leafSelected?"#a4dfc7":required?"#fee2ad":onPath?"#cfe7fb":"#f3f6f7";
        svg+='<circle cx="'+v.x+'" cy="'+v.y+'" r="'+(l===3?22:25)+'" fill="'+fill+'" stroke="'+(onPath?"#1961a0":required?"#b87313":"#a8b7c0")+'" stroke-width="'+(onPath||required?3:2)+'"/>';
        svg+='<text x="'+v.x+'" y="'+(v.y+6)+'" fill="#183a4d" font-size="20" font-weight="700" font-family="system-ui" text-anchor="middle">'+v.name+'</text>';
      }
    }
    svg+='</svg>';
    $("merkle-tree").innerHTML=svg;
    const steps=[
      {level:"leaf",value:levels[3][siblings[2]].name,side:chosen%2===0?"right":"left"},
      {level:"pair",value:levels[2][siblings[1]].name,side:Math.floor(chosen/2)%2===0?"right":"left"},
      {level:"half",value:levels[1][siblings[0]].name,side:Math.floor(chosen/4)%2===0?"right":"left"}
    ];
    feedback("merkle-path",
      "To open position "+i+", start from H(m"+i+") and send exactly three sibling hashes: "+
      steps.map(x=>x.value+" ("+x.side+" sibling at "+x.level+" level)").join(", ")+
      ". At each level combine the current value and the supplied sibling in the indicated left/right order. The final hash must equal the already-published root c. This is why proof size grows with the TREE HEIGHT, not with all eight messages.");
  }
  function pspaceUpdate(){
    const input=$("pspace-bits");if(!input)return;
    const n=Number(input.value),states=2**n;
    $("pspace-bits-label").textContent=String(n);
    $("pspace-memory").textContent=n+" bits";
    $("pspace-states").textContent=states.toLocaleString("en-US");
    feedback("pspace-result",
      "A binary counter using "+n+" bits has "+states.toLocaleString("en-US")+
      " distinct configurations, from 0 through "+(states-1).toLocaleString("en-US")+
      ". Visiting them all may require exponentially many steps, although the counter itself stores only "+n+
      " bits. This illustrates the difference between memory and time; it is NOT a proof that IP=PSPACE.");
  }
  function initializeLab(){
    drawFalseGraph("ham-false-public",false);drawFalseGraph("ham-false-hidden",null);
    drawGraph("witness-graph");npUpdate();permute("one");
    drawGraph("extract-b",{permuted:true});drawGraph("extract-g");
    scheduleUpdate();compareCost();fsUpdate("interactive");schnorrUpdate();schnorrExtract();gateUpdate();oddsUpdate();pedersenUpdate();fsQueryUpdate();fsAmplifyUpdate();merkleUpdate();pspaceUpdate();
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
      case"perm-view":permute("one");break;
      case"perm-select":permute(v);break;
      case"ham-challenge":matrixForChallenge(Number(v));break;
      case"ham-false":hamCase(v);break;
      case"ham-false-challenge":hamFalseChallenge(Number(v));break;
      case"ham-false-random":hamFalseChallenge(Math.random()<.5?0:1);break;
      case"sim-guess":simulator(v);break;
      case"sim-ask":simulator(v);break;
      case"schedule":scheduleUpdate();break;
      case"extract-graph":extractGraph(v);break;
      case"sigma":sigmaUpdate(Number(v));break;
      case"hvzk":zkSchnorr();break;
      case"fs":fsUpdate(v);break;
      case"fs-query-run":fsQueryRun();break;
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
      case"pedersen-slider":pedersenUpdate();break;
      case"fs-query-slider":fsQueryUpdate();break;
      case"fs-amplify-slider":fsAmplifyUpdate();break;
      case"merkle-leaf":merkleUpdate();break;
      case"pspace-slider":pspaceUpdate();break;
    }
  });
  document.addEventListener("change",e=>{if(content.contains(e.target)&&e.target.dataset.demo==="merkle-leaf")merkleUpdate();});
  select.innerHTML=cards.map((card,i)=>'<option value="'+card.id+'">'+String(i+1).padStart(2,"0")+" · "+card.title+"</option>").join("");
  render();
})();
