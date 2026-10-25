// A complete static conversation stays visible. Controls only highlight its steps.
document.addEventListener('DOMContentLoaded',()=>{
  for(const figure of document.querySelectorAll('[data-protocol]')){
    const steps=[...figure.querySelectorAll('.protocol-step')];
    const controls=document.createElement('div');controls.className='protocol-controls';
    controls.setAttribute('role','group');controls.setAttribute('aria-label','Follow the conversation');
    controls.innerHTML='<button type="button" data-previous disabled>Previous</button><button type="button" data-next>Follow steps</button><button type="button" data-reset disabled>Clear</button>';
    const status=document.createElement('output');status.className='protocol-status';status.setAttribute('aria-live','polite');
    let current=-1;
    const render=()=>{
      steps.forEach((step,i)=>{step.classList.toggle('is-current',i===current);if(i===current)step.setAttribute('aria-current','step');else step.removeAttribute('aria-current');});
      controls.querySelector('[data-previous]').disabled=current<=0;
      controls.querySelector('[data-next]').disabled=current===steps.length-1;
      controls.querySelector('[data-next]').textContent=current<0?'Follow steps':'Next';
      controls.querySelector('[data-reset]').disabled=current<0;
      status.textContent=current<0?'':`Step ${current+1} of ${steps.length}: ${steps[current].querySelector('strong').textContent}.`;
    };
    controls.addEventListener('click',e=>{
      if(e.target.closest('[data-next]'))current=Math.min(current+1,steps.length-1);
      if(e.target.closest('[data-previous]'))current=Math.max(0,current-1);
      if(e.target.closest('[data-reset]'))current=-1;
      render();
      if(current>=0)steps[current].scrollIntoView({block:'nearest',behavior:'instant'});
    });
    figure.querySelector('.protocol-steps').before(controls,status);render();
  }
});
