from django import template
from django.template.defaultfilters import stringfilter

from laum.urls import switch_lang_code

register = template.Library()


@register.filter
@stringfilter
def switch_i18n_prefix(path, language):
    """
    Takes in a string path.
    """
    return switch_lang_code(path, language)


@register.filter
def switch_i18n(request, language):
    """
    Takes in a request object and gets the path from it.
    """
    return switch_lang_code(request.get_full_path(), language)
