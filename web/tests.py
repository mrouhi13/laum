import datetime

from django.test import TestCase
from django.urls import reverse

from .forms import SearchForm
from .models import Page, generate_new_pid
from .templatetags.web_extras import convert_date_to_jalali as to_jalali, convert_digits_to_persian as to_persian


def create_test_page(n):
    """
    Create page with the given `title`.
    """
    titles_list = ['Linux', 'Python', 'Django', 'Mezzo']

    for title in titles_list[:n]:
        Page.objects.create(title=title, content='')


def create_test_active_page(n):
    """
    Create test page with the given `title` and active.
    """
    titles_list = ['Mari', 'Pycharm', 'Peon', 'Majid']

    for title in titles_list[:n]:
        Page.objects.create(title=title, content='', is_active=True)


class IndexViewTests(TestCase):
    def test_index(self):
        """
        Nothing to display.
        """
        response = self.client.get(reverse('web:index'))
        self.assertEqual(response.status_code, 200)


class PageListViewTests(TestCase):
    def test_search_without_query_string(self):
        """
        Redirect to index.
        """
        response = self.client.get(reverse('web:page-list'))

        self.assertEqual(response.status_code, 302)

    def test_search_with_empty_query_string(self):
        """
        Nothing to display.
        """
        create_test_page(4)
        create_test_active_page(4)

        response = self.client.get(reverse('web:page-list'), data={'q': ''})

        self.assertEqual(response.status_code, 302)

    def test_search_with_no_result(self):
        """
        If result found, show the result else an 404 message is displayed.
        """
        create_test_page(4)
        create_test_active_page(4)

        response = self.client.get(reverse('web:page-list'), data={'q': 'ubuntu'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 0)
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_search_with_result_with_exact_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_page(4)
        create_test_active_page(4)

        response = self.client.get(reverse('web:page-list'), data={'q': 'Majid'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertQuerysetEqual(response.context['object_list'], ['<Page: Majid>'])

    def test_search_with_result_with_partial_query_string(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_page(4)
        create_test_active_page(4)

        response = self.client.get(reverse('web:page-list'), data={'q': 'py'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertQuerysetEqual(response.context['object_list'], ['<Page: Pycharm>'])

    def test_search_with_no_include_inactive_pages(self):
        """
        If result found, show the result else an appropriate message is displayed.
        """
        create_test_page(4)
        create_test_active_page(4)

        response = self.client.get(reverse('web:page-list'), data={'q': 'm'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 3)
        self.assertQuerysetEqual(response.context['object_list'], ['<Page: Majid>', '<Page: Pycharm>', '<Page: Mari>'])


class PageDetailViewTests(TestCase):
    def test_page_with_id_exist(self):
        """
        If page found, show the content.
        """
        create_test_page(4)
        create_test_active_page(4)

        page = self.client.get(reverse('web:page-list'), data={'q': 'pycharm'}).context['object_list']
        response = self.client.get(reverse('web:page-detail', args=(page[0].pid,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pycharm')

    def test_page_with_id_exist_but_not_active(self):
        """
        Only show the active page.
        """
        create_test_page(4)
        create_test_active_page(4)

        page = Page.objects.get(title='Python')
        pid = page.pid

        response = self.client.get(reverse('web:page-detail', args=(pid,)))

        self.assertEqual(response.status_code, 404)

    def test_page_without_id_exist(self):
        """
        Return a 404 not found.
        """
        response = self.client.get(reverse('web:page-detail', args=(1,)))
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


class PageModelTests(TestCase):
    def test_random_pages_with_no_page(self):
        """
        Return empty queryset.
        """
        random_page = Page.objects.get_random_pages()

        self.assertIs(len(random_page), 0)

    def test_random_pages_with_less_than_three_page(self):
        """
        Return a queryset with 2 objects.
        """
        create_test_page(4)
        create_test_active_page(2)

        random_page = Page.objects.get_random_pages()

        self.assertIs(len(random_page), 2)

    def test_random_pages_with_exact_three_three_page(self):
        """
        Return a queryset with 3 objects.
        """
        create_test_page(4)
        create_test_active_page(3)

        random_page = Page.objects.get_random_pages()

        self.assertIs(len(random_page), 3)

    def test_random_pages_with_more_than_three_page(self):
        """
        Return a queryset with 3 objects.
        """
        create_test_page(4)
        create_test_active_page(4)

        random_page = Page.objects.get_random_pages()

        self.assertIs(len(random_page), 3)

    def test_random_pages_uniqueness(self):
        """
        Return a queryset with 3 unique objects.
        """
        create_test_page(4)
        create_test_active_page(4)

        random_page = Page.objects.get_random_pages()

        self.assertNotEqual(random_page[0].id, random_page[1].id)
        self.assertNotEqual(random_page[1].id, random_page[2].id)
        self.assertNotEqual(random_page[0].id, random_page[2].id)
        self.assertIs(len(random_page), 3)

    def test_a_new_pid(self):
        """
        Generate a new pid with 13 characters length.
        """
        new_pid = generate_new_pid()

        self.assertEqual(len(new_pid), 13)


class ToPersianFilterTests(TestCase):
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


class ToJalaliFilterTests(TestCase):
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

# class PageCreateApiTest(APITestCase):
#     def test_with_no_required_field(self):
#         """
#         Check required fields.
#         """
#         url = reverse('v1:create-page')
#         data = {}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Page.objects.count(), 0)
#
#     def test_with_one_empty_required_field(self):
#         """
#         Check required fields and return error if one or more is empty.
#         """
#         url = reverse('v1:create-page')
#         data = {'title': ''}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Page.objects.count(), 0)
#
#     def test_with_one_filled_required_field(self):
#         """
#         Check required fields and return error if one or more is empty.
#         """
#         url = reverse('v1:create-page')
#         data = {'title': 'test'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Page.objects.count(), 0)
#
#     def test_with_empty_required_field(self):
#         """
#         Check required fields and return error if one or more is empty.
#         """
#         url = reverse('v1:create-page')
#         data = {'title': '', 'content': ''}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Page.objects.count(), 0)
#
#     def test_with_required_field(self):
#         """
#         Create a page if required field is filled.
#         """
#         url = reverse('v1:create-page')
#         data = {'title': 'test', 'content': 'test content'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Page.objects.count(), 1)
#
#     def test_with_required_field_and_email(self):
#         """
#         Validate email and send a mail to author.
#         """
#         url = reverse('v1:create-page')
#         data = {'title': 'test', 'content': 'test content', 'email': 'go.mezzo@icloud.com'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Page.objects.count(), 1)
#
#     def test_with_required_field_and_incorrect_email(self):
#         """
#         Validate email and return 400 Bad Request status if not valid.
#         """
#         url = reverse('v1:create-page')
#         data = {'title': 'test', 'content': 'test content', 'author': 'go.mezzo'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Page.objects.count(), 0)
#
#
# class ReportApiTest(APITestCase):
#     def test_with_no_required_field(self):
#         """
#         Check required fields.
#         """
#         url = reverse('v1:create-report')
#         data = {}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Report.objects.count(), 0)
#
#     def test_with_one_empty_required_field(self):
#         """
#         Check required fields and return error if one or more is empty.
#         """
#         url = reverse('v1:create-report')
#         data = {'body': ''}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Report.objects.count(), 0)
#
#     def test_with_one_filled_required_field(self):
#         """
#         Check required fields and return error if one or more is empty.
#         """
#         url = reverse('v1:create-report')
#         data = {'body': 'test'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Report.objects.count(), 0)
#
#     def test_with_empty_required_field(self):
#         """
#         Check required fields and return error if one or more is empty.
#         """
#         url = reverse('v1:create-report')
#         data = {'body': '', 'reporter': ''}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Report.objects.count(), 0)
#
#     def test_with_required_field_and_email(self):
#         """
#         Validate email and send a mail to author.
#         """
#         create_test_active_page(1)
#
#         page = Page.objects.get(id=1)
#
#         url = reverse('v1:create-report')
#         data = {'page': page.pid, 'body': 'test', 'reporter': 'go.mezzo@icloud.com'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Report.objects.count(), 1)
#
#     def test_with_required_field_and_email_and_inactive_status(self):
#         """
#         Return 404 status when status is not active.
#         """
#         create_test_page(1)
#
#         page = Page.objects.get(id=1)
#
#         url = reverse('v1:create-report')
#         data = {'page': page.pid, 'body': 'test', 'reporter': 'go.mezzo@icloud.com'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Report.objects.count(), 0)
#
#     def test_with_required_field_and_incorrect_email(self):
#         """
#         Create a page record if required field is filled.
#         """
#         url = reverse('v1:create-report')
#         data = {'body': 'test', 'reporter': 'go.mezzo'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Report.objects.count(), 0)
#
#     def test_with_required_field_and_incorrect_pid(self):
#         """
#         Validate email and send a mail to author.
#         """
#         url = reverse('v1:create-report')
#         data = {'page': '123', 'body': 'test', 'reporter': 'go.mezzo@icloud.com'}
#         response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Report.objects.count(), 0)
