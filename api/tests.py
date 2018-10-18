from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from web.models import Page, Report


def create_test_page(n):
    """
    Create page with the given `title`.
    """
    titles_list = ['Linux', 'Python', 'Django', 'Peon']

    for title in titles_list[:n]:
        Page.objects.create(title=title, content='')


def create_test_active_page(n):
    """
    Create page with the given `title` and active.
    """
    titles_list = ['Mari', 'Pycharm', 'Mezzo', 'Majid']

    for title in titles_list[:n]:
        Page.objects.create(title=title, content='', is_active=True)


class PageCreateApiTest(APITestCase):
    def test_with_no_required_field(self):
        """
        Check required fields.
        """
        url = reverse('v1:create-page')
        data = {}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Page.objects.count(), 0)

    def test_with_one_empty_required_field(self):
        """
        Check required fields and return error if one or more is empty.
        """
        url = reverse('v1:create-page')
        data = {'title': ''}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Page.objects.count(), 0)

    def test_with_one_filled_required_field(self):
        """
        Check required fields and return error if one or more is empty.
        """
        url = reverse('v1:create-page')
        data = {'title': 'test'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Page.objects.count(), 0)

    def test_with_empty_required_field(self):
        """
        Check required fields and return error if one or more is empty.
        """
        url = reverse('v1:create-page')
        data = {'title': '', 'content': ''}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Page.objects.count(), 0)

    def test_with_required_field(self):
        """
        Create a page if required field is filled.
        """
        url = reverse('v1:create-page')
        data = {'title': 'test', 'content': 'test content'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Page.objects.count(), 1)

    def test_with_required_field_and_email(self):
        """
        Validate email and send a mail to author.
        """
        url = reverse('v1:create-page')
        data = {'title': 'test', 'content': 'test content', 'email': 'go.mezzo@icloud.com'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Page.objects.count(), 1)

    def test_with_required_field_and_incorrect_email(self):
        """
        Validate email and return 400 Bad Request status if not valid.
        """
        url = reverse('v1:create-page')
        data = {'title': 'test', 'content': 'test content', 'author': 'go.mezzo'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Page.objects.count(), 0)


class ReportApiTest(APITestCase):
    def test_with_no_required_field(self):
        """
        Check required fields.
        """
        url = reverse('v1:create-report')
        data = {}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 0)

    def test_with_one_empty_required_field(self):
        """
        Check required fields and return error if one or more is empty.
        """
        url = reverse('v1:create-report')
        data = {'body': ''}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 0)

    def test_with_one_filled_required_field(self):
        """
        Check required fields and return error if one or more is empty.
        """
        url = reverse('v1:create-report')
        data = {'body': 'test'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 0)

    def test_with_empty_required_field(self):
        """
        Check required fields and return error if one or more is empty.
        """
        url = reverse('v1:create-report')
        data = {'body': '', 'reporter': ''}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 0)

    def test_with_required_field_and_email(self):
        """
        Validate email and send a mail to author.
        """
        create_test_active_page(1)

        page = Page.objects.get(id=1)

        url = reverse('v1:create-report')
        data = {'page': page.pid, 'body': 'test', 'reporter': 'go.mezzo@icloud.com'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Report.objects.count(), 1)

    def test_with_required_field_and_email_and_inactive_status(self):
        """
        Return 404 status when status is not active.
        """
        create_test_page(1)

        page = Page.objects.get(id=1)

        url = reverse('v1:create-report')
        data = {'page': page.pid, 'body': 'test', 'reporter': 'go.mezzo@icloud.com'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 0)

    def test_with_required_field_and_incorrect_email(self):
        """
        Create a page record if required field is filled.
        """
        url = reverse('v1:create-report')
        data = {'body': 'test', 'reporter': 'go.mezzo'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 0)

    def test_with_required_field_and_incorrect_pid(self):
        """
        Validate email and send a mail to author.
        """
        url = reverse('v1:create-report')
        data = {'page': '123', 'body': 'test', 'reporter': 'go.mezzo@icloud.com'}
        response = self.client.post(url, data, enforce_csrf_checks=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Report.objects.count(), 0)
