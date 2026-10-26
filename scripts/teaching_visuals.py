"""Static-first protocol diagrams. Enhancements only highlight the current step."""
from html import escape

def protocol(key,title,left,right,known_left,known_right,steps):
    """Each step is (sender: left/right/local-left/local-right, message, explanation)."""
    rows=[]
    for i,(direction,message,explanation) in enumerate(steps,1):
        local=direction.startswith('local-')
        sender=left if direction.endswith('left') else right
        receiver=right if sender==left else left
        label=f'{sender} computes locally' if local else f'{sender} sends to {receiver}'
        arrow='' if local else '<span class="protocol-arrow" aria-hidden="true">'+('⟶' if direction=='left' else '⟵')+'</span>'
        rows.append(f'<li class="protocol-step {direction}" data-step="{i}"><div class="protocol-action"><strong>{escape(label)}</strong><div class="protocol-message">{message}</div>{arrow}</div><p>{explanation}</p></li>')
    return f'<figure class="learning protocol" data-protocol="{key}"><figcaption>{title}</figcaption><div class="protocol-parties"><div><span class="protocol-person" aria-hidden="true">{escape(left[0])}</span><strong>{escape(left)}</strong><p>{known_left}</p></div><div><span class="protocol-person" aria-hidden="true">{escape(right[0])}</span><strong>{escape(right)}</strong><p>{known_right}</p></div></div><ol class="protocol-steps">'+''.join(rows)+'</ol></figure>'

def path(title,items):
    return '<figure class="learning concept-path"><figcaption>'+title+'</figcaption><ol>'+''.join('<li>'+x+'</li>' for x in items)+'</ol></figure>'
