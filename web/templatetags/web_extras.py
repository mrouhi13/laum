from urllib.parse import urlencode

from django import template
from django.template.defaultfilters import stringfilter

from web import jalali
from web.helpers import get_jalali_month_name
from web.persian_editors import PersianEditors

register = template.Library()


@register.filter(name='to_persian')
@stringfilter
def convert_digits_to_persian(value):
    editor = PersianEditors(['number'])
    editor.escape_return = False
    return editor.run(value)


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
        return f'{d} {month_name}، {y}'


@register.filter(name='to_list')
def convert_queryset_values_to_list(queryset, field):
    item_list = []
    if queryset:
        for item in queryset:
            if field in item:
                item_list.append(item[field])
    return item_list


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
