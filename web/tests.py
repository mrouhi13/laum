import datetime

from django.test import TestCase
from django.urls import reverse

from .forms import SearchForm
from .models import Data, Tag, generate_new_pid
from .templatetags.web_extras import to_persian, to_jalali


def create_test_data(n):
    """
    Create data with the given `title`.
    """
    titles_list = ['Linux', 'Python', 'Django', 'Peon']

    for title in titles_list[:n]:
        Data.objects.create(title=title, content='')


def create_test_active_data(n):
    """
    Create test data with the given `title` and active.
    """
    titles_list = ['Mari', 'Pycharm', 'Mezzo', 'Majid']

    for title in titles_list[:n]:
        Data.objects.create(title=title, content='', is_active=True)


class IndexViewTests(TestCase):
    def test_index(self):
        """
        Nothing to display.
        """
        response = self.client.get(reverse('web:index'))
        self.assertEqual(response.status_code, 200)


class DataListViewTests(TestCase):
    def test_search_without_query_string(self):
        """
        Nothing to display.
        """
        response = self.client.get(reverse('web:list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 0)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_empty_query_string(self):
        """
        An appropriate message is displayed.
        """
        create_test_data(4)
        create_test_active_data(4)

        response = self.client.get(reverse('web:list'), data={'q': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 0)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_no_result(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data(4)
        create_test_active_data(4)

        response = self.client.get(reverse('web:list'), data={'q': 'ubuntu'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 0)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_result_with_exact_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data(4)
        create_test_active_data(4)

        response = self.client.get(reverse('web:list'), data={'q': 'Majid'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 1)
        self.assertQuerysetEqual(response.context['data_list'], ['<Data: Majid>'])

    def test_search_with_result_with_partial_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data(4)
        create_test_active_data(4)

        response = self.client.get(reverse('web:list'), data={'q': 'py'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 1)
        self.assertQuerysetEqual(response.context['data_list'], ['<Data: Pycharm>'])

    def test_search_with_not_active_pages_include(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data(4)
        create_test_active_data(4)

        response = self.client.get(reverse('web:list'), data={'q': 'ma'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 2)
        self.assertQuerysetEqual(response.context['data_list'], ['<Data: Mari>', '<Data: Majid>'])


class DataDetailViewTests(TestCase):
    def test_data_with_id_exist(self):
        """
        If data found, show the content.
        """
        create_test_data(4)
        create_test_active_data(4)

        data = self.client.get(reverse('web:list'), data={'q': 'pycharm'})
        response = self.client.get(reverse('web:detail', args=(data.context['data_list'][0].pid,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pycharm')

    def test_data_with_id_exist_but_not_active(self):
        """
        If data found, show only active the content.
        """
        create_test_data(4)
        create_test_active_data(4)

        data = self.client.get(reverse('web:list'), data={'q': 'python'}).context['data_list']

        pid = '0'

        if data:
            pid = data[0].pid

        response = self.client.get(reverse('web:detail', args=(pid,)))

        self.assertEqual(response.status_code, 404)

    def test_data_without_id_exist(self):
        """
        Return a 404 not found.
        """
        response = self.client.get(reverse('web:detail', args=(1,)))
        self.assertEqual(response.status_code, 404)


class SearchFormTest(TestCase):
    def test_without_data(self):
        """
        Return empty dict.
        """
        form = SearchForm()

        self.assertEqual(form.data, {})
        self.assertFalse(form.is_valid())

    def test_with_empty_string(self):
        """
        Return q with empty string.
        """
        form = SearchForm(data={'q': ''})

        self.assertEqual(form.data, {'q': ''})
        self.assertFalse(form.is_valid())

    def test_with_string(self):
        """
        Return q with it's data.
        """
        form = SearchForm(data={'q': 'django'})

        self.assertEqual(form.data, {'q': 'django'})
        self.assertTrue(form.is_valid())


class DataModelTests(TestCase):
    def test_random_pages_with_no_data(self):
        """
        Return empty queryset.
        """
        random_data = Data.objects.get_random_data()

        self.assertIs(len(random_data), 0)

    def test_random_pages_with_less_than_three_data(self):
        """
        Return a queryset with 2 objects.
        """
        create_test_data(4)
        create_test_active_data(2)

        random_data = Data.objects.get_random_data()

        self.assertIs(len(random_data), 2)

    def test_random_pages_with_exact_three_three_data(self):
        """
        Return a queryset with 3 objects.
        """
        create_test_data(4)
        create_test_active_data(3)

        random_data = Data.objects.get_random_data()

        self.assertIs(len(random_data), 3)

    def test_random_pages_with_more_than_three_data(self):
        """
        Return a queryset with 3 objects.
        """
        create_test_data(4)
        create_test_active_data(4)

        random_data = Data.objects.get_random_data()

        self.assertIs(len(random_data), 3)

    def test_random_pages_uniqueness(self):
        """
        Return a queryset with 3 unique objects.
        """
        create_test_data(4)
        create_test_active_data(4)

        random_data = Data.objects.get_random_data()

        self.assertNotEqual(random_data[0].id, random_data[1].id)
        self.assertNotEqual(random_data[1].id, random_data[2].id)
        self.assertNotEqual(random_data[0].id, random_data[2].id)
        self.assertIs(len(random_data), 3)

    def test_a_new_pid(self):
        """
        Generate a new pid with 13 characters length.
        """
        new_pid = generate_new_pid()

        self.assertEqual(len(new_pid), 13)


class TagModelTests(TestCase):
    def test_single_word_tag_name(self):
        """
        The single-word names keyword are one.
        """
        new_tag = Tag.objects.create(name='test')

        new_tag.save()

        self.assertEqual(new_tag.keyword, 'test')

    def test_with_two_word_tag_name_with_space(self):
        """
        The space of two word names convert to underscore (_).
        """
        new_tag = Tag.objects.create(name='test tag')

        new_tag.save()

        self.assertEqual(new_tag.keyword, 'test_tag')

    def test_with_two_word_tag_name_with_underscore(self):
        """
        The more than two word names with underscore is same.
        """
        new_tag = Tag.objects.create(name='new test_tag')

        new_tag.save()

        self.assertEqual(new_tag.keyword, 'new_test_tag')


class to_persianFilterTests(TestCase):
    def test_with_english_text_and_no_digits(self):
        """
        No change.
        """
        original_text = 'Text with no digits.'
        converted_text = 'Text with no digits.'
        result = to_persian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_english_text_and_digits(self):
        """
        Convert digits to persian.
        """
        original_text = 'Text with digit: 1234567890'
        converted_text = 'Text with digit: ۱۲۳۴۵۶۷۸۹۰'
        result = to_persian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_english_text_and_persian_digits(self):
        """
        No change
        """
        original_text = 'Text with digit: ۱۲۳۴۵۶۷۸۹۰'
        converted_text = 'Text with digit: ۱۲۳۴۵۶۷۸۹۰'
        result = to_persian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_persian_text_and_no_digits(self):
        """
        No change.
        """
        original_text = 'متن آزمایشی بدون عدد.'
        converted_text = 'متن آزمایشی بدون عدد.'
        result = to_persian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_persian_text_and_digits(self):
        """
        No change.
        """
        original_text = 'متن آزمایشی با عدد: ۱۲۳۴۵۶۷۸۹۰'
        converted_text = 'متن آزمایشی با عدد: ۱۲۳۴۵۶۷۸۹۰'
        result = to_persian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_persian_text_and_english_digits(self):
        """
        Convert digits to persian.
        """
        original_text = 'متن آزمایشی با عدد: 1234567890'
        converted_text = 'متن آزمایشی با عدد: ۱۲۳۴۵۶۷۸۹۰'
        result = to_persian(original_text)

        self.assertEqual(result, converted_text)


class to_jalaliFilterTests(TestCase):
    def test_with_empty_date(self):
        """
        Return none.
        """
        date = ''
        jalali_date = to_jalali(date)
        self.assertEqual(jalali_date, None)

    def test_with_none_date(self):
        """
        Return none.
        """
        date = None
        jalali_date = to_jalali(date)
        self.assertEqual(jalali_date, None)

    def test_with_incorrect_date_format(self):
        """
        Return none.
        """
        date = '201822'
        jalali_date = to_jalali(date)
        self.assertEqual(jalali_date, None)

    def test_with_correct_date_format(self):
        """
        Return date in Jalali format.
        """
        date = datetime.date(2019, 2, 2)
        jalali_date = to_jalali(date)
        self.assertEqual(jalali_date, '13 بهمن، 1397')
