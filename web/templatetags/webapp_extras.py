import re

from django import template
from django.template.defaultfilters import stringfilter

from web import jalali

register = template.Library()


@register.filter
@stringfilter
def to_persian(value):
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
def to_jalali(date):
    if date is None or date == '':
        return None
    else:
        try:
            jalali_string = jalali.Gregorian(date).persian_tuple()
            month_name = get_jalali_month_name(jalali_string[1])
        except ValueError:
            return None

        return '{0} {1}، {2}'.format(jalali_string[2], month_name, jalali_string[0])


def get_jalali_month_name(month_number):
    persian_names = (
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')

    return persian_names[month_number - 1]
