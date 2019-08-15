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


def swap_prefix(string, new, delimiter='_'):
    new_string_exploded = string.split(delimiter)
    new_string_exploded[0] = new
    new_string = delimiter.join(new_string_exploded)
    return new_string
