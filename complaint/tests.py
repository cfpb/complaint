from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase, Client

from .views import SubmitView, DataUseView, ProcessView

client = Client()


class SubmitViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_context_data_exist(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        response = SubmitView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('base_template' in response.context_data.keys())


class DataUseViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_context_data_exist(self):
        # Create an instance of a GET request.
        request = self.factory.get('/data-use')
        response = DataUseView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('base_template' in response.context_data.keys())


class ProcessViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_context_data_exist(self):
        # Create an instance of a GET request.
        request = self.factory.get('/process')
        response = ProcessView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('base_template' in response.context_data.keys())


class URLTest(TestCase):
    url_names = ['ccdb_submit', 'ccdb_data_use', 'ccdb_process']

    def test_complaint_urls(self):
        for url_name in self.url_names:
            response = client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
            self.assertTrue('base_template' in response.context_data.keys())
