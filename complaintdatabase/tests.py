import collections
from datetime import datetime
from StringIO import StringIO
from unittest import skipIf

from mock import patch, Mock, MagicMock, mock_open

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from django.test import Client

from requests.exceptions import ConnectionError

from .views import (LandingView, DocsView, get_narratives_json, get_stats,
                    is_data_not_updated)


MOCK_404 = ConnectionError(Mock(return_value={'status': 404}), 'not found')
client = Client()


class LandingViewTest(TestCase):
    def setUp(self):
        """Every test needs access to the request factory."""
        self.factory = RequestFactory()

    def test_get_context_data_exist(self):
        """Create an instance of a GET request."""
        request = self.factory.get('/')
        response = LandingView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('base_template' in response.context_data.keys())
        self.assertTrue('stats' in response.context_data.keys())

    @skipIf(True, "not running with feature flags")
    def test_demo_json(self):
        """Test demo version of landing page"""
        response = client.get(reverse("ccdb-demo",
                                      kwargs={'demo_json': 'demo.json'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('base_template' in response.context_data.keys())
        self.assertTrue('stats' in response.context_data.keys())


class NarrativeJsonTest(TestCase):

    @patch('complaintdatabase.views.requests.get')
    def test_get_narratives_json(self, mock_get):
        mock_return = MagicMock()
        mock_return.json.return_value = {}
        mock_get.return_value = mock_return
        res_json = get_narratives_json()
        self.assertEqual(res_json, {})
        self.assertTrue(mock_get.call_count == 1)

    @patch('complaintdatabase.views.requests.get')
    def test_get_demo_narratives_json(self, mock_get):
        mock_return = MagicMock()
        mock_return.json.return_value = {}
        mock_get.return_value = mock_return
        m = mock_open(read_data='{"mock_data": ""}')
        with patch("__builtin__.open", m, create=True):
            res_json = get_narratives_json(demo_json='/fake/path')
        self.assertEqual(res_json, {"mock_data": ""})

    @patch('complaintdatabase.views.requests.get')
    def test_request_exception_get_narratives_json(self, mock_requests_get):
        mock_requests_get.side_effect = MOCK_404
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_json = get_narratives_json()
            self.assertEqual(res_json, {})
            self.assertIn('requests.exceptions.RequestException',
                          fakeOutput.getvalue().strip())

    @patch('complaintdatabase.views.requests.get')
    def test_incorrect_text_get_narratives_json(self, mock_get):
        mock_return = MagicMock()
        mock_return.json.return_value = {}
        mock_get.return_value = mock_return
        with patch('sys.stdout', new=StringIO('ValueError')) as fakeOutput:
            res_json = get_narratives_json()
            self.assertEqual(res_json, {})
            self.assertIn('ValueError', fakeOutput.getvalue())
            self.assertTrue(mock_get.call_count == 1)


class GetStatsTest(TestCase):
    def test_get_stats(self):
        input_json = {'stats': {'test': 1}}
        res = get_stats(input_json)
        self.assertEqual({'test': 1}, res)

    def test_no_key_get_stats(self):
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res = get_stats({})
            self.assertEqual({}, res)
            self.assertIn('KeyError', fakeOutput.getvalue().strip())



class DataUpdatedTest(TestCase):

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_monday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 21, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-14",
                      'last_updated_narratives': "2015-12-14"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_monday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 21, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-15",
                      'last_updated_narratives': "2015-12-15"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_monday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 21, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-15",
                      'last_updated_narratives': "2015-12-14"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_tuesday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 22, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-15",
                                'last_updated_narratives': "2015-12-15"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_tuesday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 22, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-16",
                                'last_updated_narratives': "2015-12-16"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_tuesday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 22, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-16",
                                'last_updated_narratives': "2015-12-15"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_wednesday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 23, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-16",
                                'last_updated_narratives': "2015-12-16"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_wednesday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 23, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-17",
                                'last_updated_narratives': "2015-12-17"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_wednesday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 23, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-17",
                                'last_updated_narratives': "2015-12-16"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_thursday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 24, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-17",
                                'last_updated_narratives': "2015-12-17"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_thursday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 24, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18",
                                'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_thursday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 24, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18",
                                'last_updated_narratives': "2015-12-17"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_friday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 25, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18",
                                'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_friday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 25, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21",
                                'last_updated_narratives': "2015-12-21"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_friday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 25, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21",
                                'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 27, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18",
                                'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 27, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21",
                                'last_updated_narratives': "2015-12-21"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 27, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21",
                                'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_incorrect_json_data_not_updated_saturday(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 27, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated_narratives': "2015-12-21"}}
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            data_down, narratives_down = is_data_not_updated(input_json)
            self.assertFalse(data_down)
            self.assertFalse(narratives_down)
            self.assertIn('KeyError', fakeOutput.getvalue().strip())


class DocsViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_context_data_exist(self):
        # Create an instance of a GET request.
        request = self.factory.get('/technical-documentation')
        response = DocsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('base_template' in response.context_data.keys())
