def get_jalali_month_name(month_number):
    persian_names = (
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')

    return persian_names[month_number - 1]
