import re

from django import template
from django.template.defaultfilters import stringfilter

from webapp import jalali

register = template.Library()


@register.filter
@stringfilter
def topersian(value):
    persian_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    original_text = str(value)
    converted_text = ''

    for char in original_text:
        if re.search('\d+', char):
            converted_text += persian_nums[int(char)]
        else:
            converted_text += char

    return converted_text


@register.filter
@stringfilter
def tojalali(date):
    jalali_string = jalali.Gregorian(date).persian_tuple()
    month_name = getjalalimonthname(jalali_string[1])

    return '{0} {1}، {2}'.format(jalali_string[2], month_name, jalali_string[0])


def getjalalimonthname(month_number):
    persian_names = (
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')

    return persian_names[month_number - 1]
