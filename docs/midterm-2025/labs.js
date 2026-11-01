window.PETS_MIDTERM_LABS={"1c":"<figure class=\"midterm-lab\" data-midterm-lab=\"poly\"><figcaption>Open one coordinate</figcaption><p>For \\(\\mathbf v=[2,5]\\), the polynomial \\(f(X)=3X-1\\pmod 7\\) matches both vector entries.</p><label>Vector index <select data-index><option value=\"1\">1</option><option value=\"2\">2</option></select></label><div class=\"mini-circuit\"><span>v = [2,5]</span><span>→</span><span>f(X) = 3X − 1</span></div><output class=\"lab-result\" aria-live=\"polite\"></output></figure>","2a":"<figure class=\"midterm-lab\" data-midterm-lab=\"love\"><figcaption>Try all four cases</figcaption><p>Pick whether each person loves the other and examine only the public set intersection.</p><label>Alice <select data-alice><option value=\"1\">YES</option><option value=\"0\">NO</option></select></label><label>Bob <select data-bob><option value=\"1\">YES</option><option value=\"0\">NO</option></select></label><div class=\"mini-circuit\"><span data-a-set>A = {1}</span><span>∩</span><span data-b-set>B = {1}</span></div><output class=\"lab-result\" aria-live=\"polite\"></output></figure>","2c2":"<figure class=\"midterm-lab\" data-midterm-lab=\"hash\"><figcaption>Discover the privacy leak</figcaption><p>Alice has A = {a,d}. Bob secretly has {a,b} or {a,c}. In both cases the intersection is {a}.</p><label>Bob's secret <select data-bset><option value=\"b\">B₀ = {a,b}</option><option value=\"c\">B₁ = {a,c}</option></select></label><div class=\"mini-circuit\"><span>A ∩ B = {a}</span><span>·</span><span>Alice checks H(b)</span></div><output class=\"lab-result\" aria-live=\"polite\"></output></figure>","2e":"<figure class=\"midterm-lab\" data-midterm-lab=\"oprf\"><figcaption>Watch the blinding cancel</figcaption><p>Toy cyclic group G = {1,3,4,5,9} of order p = 5, with multiplication mod 11. Take H(x) = 3. These are not secure parameters.</p><label>Client mask r <input data-r type=\"range\" min=\"1\" max=\"4\" value=\"2\"><output data-r-out>2</output></label><label>Server key k <input data-k type=\"range\" min=\"1\" max=\"4\" value=\"3\"><output data-k-out>3</output></label><div class=\"mini-circuit\"><span data-u></span><span>→</span><span data-v></span><span>→</span><span data-y></span></div><output class=\"lab-result\" aria-live=\"polite\"></output></figure>","3b1":"<figure class=\"midterm-lab\" data-midterm-lab=\"dpf\"><figcaption>Expand two additive shares</figcaption><p>Toy evaluated vectors modulo 11. The DPF <em>keys</em> are shorter; only their evaluated values are shown here.</p><label>Vote for candidate <select data-candidate><option value=\"0\">1</option><option value=\"1\" selected>2</option><option value=\"2\">3</option></select></label><div class=\"mini-circuit\"><span>S₀ share</span><span>+</span><span>S₁ share</span><span>=</span><span>vote</span></div><output class=\"lab-result\" aria-live=\"polite\"></output></figure>","3c1":"<figure class=\"midterm-lab\" data-midterm-lab=\"sz\"><figcaption>Explore the random algebraic check</figcaption><p>All calculations are modulo 11. Valid vectors must pass every challenge; invalid ones may occasionally pass.</p><label>Vector \\(\\mathbf x\\) <select data-x><option value=\"valid\">[1,0] (valid)</option><option value=\"bad\" selected>[1,1] (invalid)</option></select></label><label>r₁ <input type=\"range\" data-r1 min=\"0\" max=\"10\" value=\"2\"><output data-r1-out>2</output></label><label>r₂ <input type=\"range\" data-r2 min=\"0\" max=\"10\" value=\"5\"><output data-r2-out>5</output></label><output class=\"lab-result\" aria-live=\"polite\"></output></figure>","3c2":"<figure class=\"midterm-lab\" data-midterm-lab=\"linear\"><figcaption>How shared linear answers reconstruct</figcaption><p>One tiny query, modulo 11: \\(\\mathbf q=[1,3,2]\\), local vector shares [4,3,7] and [7,9,6], whose sum is the hidden combined vector [0,1,2].</p><label>Number of IOP queries k <input type=\"range\" data-query-count min=\"1\" max=\"6\" value=\"4\"><output data-query-out>4</output></label><div class=\"mini-circuit\"><span>5</span><span>+</span><span>2</span><span>=</span><span>7</span></div><output class=\"lab-result\" aria-live=\"polite\"></output></figure>"};
window.addEventListener('DOMContentLoaded',function(){

(() => {
'use strict';
const root=document.getElementById('lessons');if(!root)return;
const mod=(a,p)=>((a%p)+p)%p;
const pow=(a,b,p)=>{let r=1;for(let j=0;j<b;j++)r=mod(r*a,p);return r;};
const inv=(a,p)=>{for(let j=1;j<p;j++)if(mod(a*j,p)===1)return j;return 0;};
for(const panel of root.querySelectorAll('[data-midterm-lab]')){
 const type=panel.dataset.midtermLab,out=panel.querySelector('.lab-result');
 const draw=()=>{
  if(type==='poly'){
    const i=Number(panel.querySelector('[data-index]').value);out.textContent='Open at position '+i+': f('+i+') = (3 × '+i+' − 1) mod 7 = '+mod(3*i-1,7)+'.';
  }else if(type==='love'){
    const a=Number(panel.querySelector('[data-alice]').value),b=Number(panel.querySelector('[data-bob]').value);
    panel.querySelector('[data-a-set]').textContent='A = '+(a?'{1}':'∅');
    panel.querySelector('[data-b-set]').textContent='B = '+(b?'{1}':'∅');
    out.textContent='Intersection = '+(a&&b?'{1}. Both output YES.':'∅. Both output NO.');
  }else if(type==='hash'){
    const b=panel.querySelector('[data-bset]').value;out.textContent='The true intersection is always {a}; checking H(b) in Bob’s sent hashes returns '+(b==='b'?'YES':'NO')+' (except for collisions). That leaks which Bob set was used.';
  }else if(type==='oprf'){
    const r=Number(panel.querySelector('[data-r]').value),k=Number(panel.querySelector('[data-k]').value);
    const u=pow(3,r,11),v=pow(u,k,11),ri=inv(r,5),y=pow(v,ri,11);
    for(const [key,val] of [['r-out',r],['k-out',k],['u','U = '+u],['v','V = '+v],['y','result = '+y]])panel.querySelector('[data-'+key+']').textContent=val;
    out.textContent='r⁻¹ mod 5 = '+ri+'. Unblind: '+v+'^'+ri+' mod 11 = '+y+'. Direct PRF: 3^'+k+' mod 11 = '+pow(3,k,11)+'. They match.';
  }else if(type==='dpf'){
    const i=Number(panel.querySelector('[data-candidate]').value),s0=[3,8,1],goal=[0,0,0];goal[i]=1;
    const s1=s0.map((x,j)=>mod(goal[j]-x,11));
    out.textContent='['+s0.join(',')+'] + ['+s1.join(',')+'] = ['+goal.join(',')+'] (mod 11).';
  }else if(type==='sz'){
    const x=panel.querySelector('[data-x]').value==='bad'?[1,1]:[1,0],a=Number(panel.querySelector('[data-r1]').value),b=Number(panel.querySelector('[data-r2]').value);
    panel.querySelector('[data-r1-out]').textContent=a;panel.querySelector('[data-r2-out]').textContent=b;
    const l=mod((x[0]*a+x[1]*b)**2,11),r=mod(x[0]*a*a+x[1]*b*b,11);
    out.textContent='Left = ('+x[0]+'×'+a+' + '+x[1]+'×'+b+')² mod 11 = '+l+'. Right = '+x[0]+'×'+a+'² + '+x[1]+'×'+b+'² mod 11 = '+r+'. '+(l===r?'ACCEPT':'REJECT')+'.';
  }else if(type==='linear'){
    const k=Number(panel.querySelector('[data-query-count]').value);panel.querySelector('[data-query-out]').textContent=k;
    out.textContent='One query: 〈q, share₀〉 = 5, 〈q, share₁〉 = 2; 5 + 2 = 7 = 〈q, hidden vector〉. With '+k+' queries, the same computation is repeated '+k+' times; each server sends '+k+' field values.';
  }
 };
 panel.addEventListener('input',draw);panel.addEventListener('change',draw);draw();
}
})();
});