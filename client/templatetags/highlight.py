import logging
import re
from django import template
from django.utils.html import escape

logger = logging.getLogger(__name__)

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
        return escape(highlighted)
    except Exception as e:
        logger.error(f"Highlight error: {e}")
        return text