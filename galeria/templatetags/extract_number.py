# app/templatetags/extract_number.py
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def extract_number(context):
    path = context['request'].path
    parts = path.strip('/').split('/')
    # Asume que el número siempre está después de 'imgs'
    if len(parts) > 1 and parts[0] == 'imgs':
        return parts[1]
    return 'default_value'
