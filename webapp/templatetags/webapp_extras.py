import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def topersian(value):
    persian_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    original_text = str(value)
    convertd_text = ''

    for char in original_text:
        if re.search('\d+', char):
            convertd_text += persian_nums[int(char)]
        else:
            convertd_text += char

    return convertd_text
