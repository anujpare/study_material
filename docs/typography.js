// SVG viewBoxes resize their labels as well as their shapes. Keep diagram text
// at the shared box size while allowing the surrounding drawing to resize.
document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('lessons');
  if (!root) return;
  let scheduled = false;
  const schedule = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      for (const svg of root.querySelectorAll('.pet-active svg.lab-diagram')) {
        const matrix = svg.getScreenCTM();
        if (!matrix || !svg.getBoundingClientRect().width) continue;
        const scale = Math.hypot(matrix.a, matrix.b);
        if (!scale) continue;
        for (const text of svg.querySelectorAll('text')) {
          const x = Number(text.getAttribute('x') || 0);
          const y = Number(text.getAttribute('y') || 0);
          text.setAttribute('transform', `translate(${x} ${y}) scale(${1 / scale}) translate(${-x} ${-y})`);
        }
      }
    });
  };
  new ResizeObserver(schedule).observe(root);
  new MutationObserver(schedule).observe(root, {subtree: true, childList: true, attributes: true, attributeFilter: ['class']});
  schedule();
});
