from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(text, search):
    if not text:
        return ""

    if not search:
        return text

    try:
        pattern = re.compile(re.escape(search), re.IGNORECASE)
        highlighted = pattern.sub(
            lambda m: f'<mark>{m.group(0)}</mark>',
            text
        )
        return mark_safe(highlighted)
    except:
        return text