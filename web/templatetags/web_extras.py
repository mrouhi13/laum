import re

from django import template
from django.template.defaultfilters import stringfilter

from web import jalali

register = template.Library()


@register.filter(name='to_persian')
@stringfilter
def convert_digits_to_persian(value):
    persian_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    original_text = str(value)
    converted_text = ''

    for char in original_text:
        if re.search('\d+', char):
            converted_text += persian_nums[int(char)]
        else:
            converted_text += char

    return converted_text


@register.filter(name='to_jalali')
def convert_date_to_jalali(date):
    if date is None or date == '':
        return None
    else:
        try:
            y, m, d = jalali.Gregorian(date).persian_tuple()
            month_name = get_jalali_month_name(m)
        except ValueError:
            return None

        return '{0} {1}، {2}'.format(d, month_name, y)


def get_jalali_month_name(month_number):
    persian_names = (
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')

    return persian_names[month_number - 1]
