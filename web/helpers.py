import random
import string

from django.conf import settings
from django.utils.translation import get_language


def get_jalali_month_name(month_number):
    try:
        if month_number is not None:
            month_number = int(month_number)

            if month_number > 12:
                month_number = 12

            if month_number < 1:
                month_number = 1

            persian_names = (
                'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')
            return persian_names[month_number - 1]
    except ValueError:
        pass

    return None


def swap_prefix(string_, new, delimiter='_'):
    new_string_exploded = string_.split(delimiter)
    new_string_exploded[0] = new
    new_string = delimiter.join(new_string_exploded)
    return new_string


def id_generator(n=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def get_active_lang():
    language = get_language()
    if not language:
        language = settings.LANGUAGE_CODE
    return language.split('-')[0]


def switch_lang_code(path_, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    if path_ == '':
        raise Exception('URL path for language switch is empty')
    elif path_[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)

    parts = path_.split('/')
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = '/' + language
    return '/'.join(parts)
