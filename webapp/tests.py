from django.test import TestCase
from django.urls import reverse

from .models import Data


def create_test_data():
    """
    Create a data with the given `title`.
    """
    titles_list = ['Linux', 'Python', 'Django', 'Pycharm', 'Majid']

    for title in titles_list:
        Data.objects.create(title=title, content='', tags='', pid=title)


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
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_empty_query_string(self):
        """
        An appropriate message is displayed.
        """
        create_test_data()
        response = self.client.get(reverse('webapp:list'), data={'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_no_result(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data()
        response = self.client.get(reverse('webapp:list'), data={'q': 'Mari'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['data_list'], [])

    def test_search_with_result_with_exact_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data()
        response = self.client.get(reverse('webapp:list'), data={'q': 'Majid'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['data_list'], ['<Data: Majid>'])

    def test_search_with_result_with_partial_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_data()
        response = self.client.get(reverse('webapp:list'), data={'q': 'py'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['data_list'], ['<Data: Python>', '<Data: Pycharm>'])


class DataDetailViewTests(TestCase):
    def test_data_with_id_exist(self):
        """
        If data found, show the content.
        """
        create_test_data()
        data = self.client.get(reverse('webapp:list'), data={'q': 'python'})
        response = self.client.get(reverse('webapp:detail', args=(data.context['data_list'][0].id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')

    def test_data_without_id_exist(self):
        """
        Return a 404 not found.
        """
        response = self.client.get(reverse('webapp:detail', args=(1,)))
        self.assertEqual(response.status_code, 404)
