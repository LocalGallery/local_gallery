from django.template import Library
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def u(instance):
    s = conditional_escape(instance)
    return mark_safe(f'<a href="{instance.get_absolute_url()}">{s}</a>')
