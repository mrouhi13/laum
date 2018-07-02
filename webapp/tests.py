from django.test import TestCase
from django.urls import reverse

from .forms import SearchForm
from .models import Data
from .templatetags.webapp_extras import topersian


def create_test_data(n):
    """
    Create a data with the given `title`.
    """
    titles_list = ['Linux', 'Python', 'Django', 'Pycharm', 'Majid']

    for title in titles_list[:n]:
        Data.objects.create(title=title, content='')


class IndexViewTests(TestCase):
    def test_index(self):
        """
        Nothing to display.
        """
        response = self.client.get(reverse('webapp:index'))
        self.assertEqual(response.status_code, 200)


class DataListViewTests(TestCase):
    def test_search_without_query_string(self):
        """
        Nothing to display.
        """
        response = self.client.get(reverse('webapp:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 0)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_empty_query_string(self):
        """
        An appropriate message is displayed.
        """
        create_test_data(5)
        response = self.client.get(reverse('webapp:list'), data={'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 0)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_no_result(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data(5)
        response = self.client.get(reverse('webapp:list'), data={'q': 'Mari'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 0)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_result_with_exact_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data(5)
        response = self.client.get(reverse('webapp:list'), data={'q': 'Majid'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 1)
        self.assertQuerysetEqual(response.context['data_list'], ['<Data: Majid>'])

    def test_search_with_result_with_partial_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data(5)
        response = self.client.get(reverse('webapp:list'), data={'q': 'py'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 2)
        self.assertQuerysetEqual(response.context['data_list'], ['<Data: Python>', '<Data: Pycharm>'])


class DataDetailViewTests(TestCase):
    def test_data_with_id_exist(self):
        """
        If data found, show the content.
        """
        create_test_data(5)
        data = self.client.get(reverse('webapp:list'), data={'q': 'python'})
        response = self.client.get(reverse('webapp:detail', args=(data.context['data_list'][0].pid,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')

    def test_data_without_id_exist(self):
        """
        Return a 404 not found.
        """
        response = self.client.get(reverse('webapp:detail', args=(1,)))
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
        create_test_data(2)

        random_data = Data.objects.get_random_data()

        self.assertIs(len(random_data), 2)

    def test_random_pages_with_exact_three_three_data(self):
        """
        Return a queryset with 3 objects.
        """
        create_test_data(3)

        random_data = Data.objects.get_random_data()

        self.assertIs(len(random_data), 3)

    def test_random_pages_with_more_than_three_data(self):
        """
        Return a queryset with 3 objects.
        """
        create_test_data(5)

        random_data = Data.objects.get_random_data()

        self.assertIs(len(random_data), 3)


class ToPersianFilterTests(TestCase):
    def test_with_english_text_and_no_digits(self):
        """
        No change.
        """
        original_text = 'Text with no digits.'
        converted_text = 'Text with no digits.'
        result = topersian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_english_text_and_digits(self):
        """
        Convert digits to persian.
        """
        original_text = 'Text with digit: 1234567890'
        converted_text = 'Text with digit: ۱۲۳۴۵۶۷۸۹۰'
        result = topersian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_english_text_and_persian_digits(self):
        """
        No change
        """
        original_text = 'Text with digit: ۱۲۳۴۵۶۷۸۹۰'
        converted_text = 'Text with digit: ۱۲۳۴۵۶۷۸۹۰'
        result = topersian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_persian_text_and_no_digits(self):
        """
        No cange.
        """
        original_text = 'متن آزمایشی بدون عدد.'
        converted_text = 'متن آزمایشی بدون عدد.'
        result = topersian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_persian_text_and_digits(self):
        """
        No change.
        """
        original_text = 'متن آزمایشی با عدد: ۱۲۳۴۵۶۷۸۹۰'
        converted_text = 'متن آزمایشی با عدد: ۱۲۳۴۵۶۷۸۹۰'
        result = topersian(original_text)

        self.assertEqual(result, converted_text)

    def test_with_persian_text_and_english_digits(self):
        """
        Convert digits to persian.
        """
        original_text = 'متن آزمایشی با عدد: 1234567890'
        converted_text = 'متن آزمایشی با عدد: ۱۲۳۴۵۶۷۸۹۰'
        result = topersian(original_text)

        self.assertEqual(result, converted_text)
