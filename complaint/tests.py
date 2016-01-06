import unittest

import django
from django.test import RequestFactory, TestCase
from django.http import HttpResponse, HttpRequest
from django.test import Client
from django.core.urlresolvers import reverse
from .views import SubmitView, DataUseView, ProcessView

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
