from urllib.parse import urlencode

from django import template
from django.template.defaultfilters import stringfilter

from web.persian_editors import PersianEditors

register = template.Library()


@register.filter(name='to_persian')
@stringfilter
def convert_digits_to_persian(value):
    editor = PersianEditors(['number'])
    editor.escape_return = False
    return editor.run(value)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
