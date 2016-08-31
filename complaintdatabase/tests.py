import collections
from mock import patch, Mock

from requests.exceptions import ConnectionError
from django.test import RequestFactory, TestCase
from datetime import datetime
from StringIO import StringIO
from .views import (LandingView, DocsView, get_narratives_json,
                    format_narratives, get_stats, get_count_info,
                    is_data_not_updated)

MOCK_404 = ConnectionError(Mock(return_value={'status': 404}), 'not found')


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
        self.assertTrue('narratives' in response.context_data.keys())
        self.assertTrue('stats' in response.context_data.keys())
        self.assertTrue('total_complaints' in response.context_data.keys())
        self.assertTrue('timely_responses' in response.context_data.keys())


class NarrativeJsonTest(TestCase):

    @patch('complaintdatabase.views.requests.get')
    def test_get_narratives_json(self, mock_requests_get):
        # Using namedtuple to mock out the attribute text in response
        # not sure if this is the best way though
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text="narratives({});")
        res_json = get_narratives_json()
        self.assertEqual(res_json, {})

    @patch('complaintdatabase.views.requests.get')
    def test_request_exception_get_narratives_json(self, mock_requests_get):
        mock_requests_get.side_effect = MOCK_404
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_json = get_narratives_json()
            self.assertEqual(res_json, {})
            self.assertIn('requests.exceptions.RequestException',
                          fakeOutput.getvalue().strip())

    @patch('complaintdatabase.views.requests.get')
    def test_incorrect_text_get_narratives_json(self, mock_requests_get):
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text=("This is not a correct"
                                                        " set of narratives"))
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_json = get_narratives_json()
            self.assertEqual(res_json, {})
            self.assertIn('ValueError', fakeOutput.getvalue().strip())


class FormatNarrativesTest(TestCase):
    def test_format_narratives(self):
        input_json = {
            'bank_accounts': {'date_received': '2015-04-08T20:32:15',
                              'tags': ['Older American', 'Servicemember']},
            'credit_cards': {'date_received': '2015-04-08T20:32:16',
                             'tags': ['Older American', 'Servicemember']},
            'credit_reporting': {'date_received': '2015-04-08T20:32:17',
                                 'tags': ['Older American', 'Servicemember']},
            'debt_collection': {'date_received': '2015-04-08T20:32:18',
                                'tags': ['Older American', 'Servicemember']},
            'money_transfers': {'date_received': '2015-04-08T20:32:19',
                                'tags': ['Older American', 'Servicemember']},
            'mortgages': {'date_received': '2015-04-08T21:32:15',
                          'tags': ['Older American', 'Servicemember']},
            'other_financial_services': {'date_received':
                                         '2015-04-09T20:32:15'},
            'payday_loans': {'date_received': '2015-04-10T20:32:15'},
            'prepaid_cards': {'date_received': '2015-04-11T20:32:15'},
            'student_loans': {'date_received': '2015-04-12T20:32:15'},
            'other_consumer_loans': {'date_received': '2015-04-13T20:32:15'}
        }
        sorted_titles = ['Bank account', 'Credit card',
                         'Credit reporting', 'Debt collection',
                         'Money transfer or virtual currency', 'Mortgage',
                         'Other financial service', 'Payday loan',
                         'Prepaid card', 'Student loan',
                         'Vehicle / consumer loan']
        res = format_narratives(input_json)
        self.assertEqual(len(res), 11)
        res_titles = sorted([entry['title'] for entry in res])
        self.assertEqual(res_titles, sorted_titles)
        for date in [entry['date'] for entry in res]:
            self.assertEqual(type(date), datetime)

    def test_invalid_json_format_narratives(self):
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res = format_narratives({})
            self.assertEqual(res, [])
            self.assertIn('KeyError', fakeOutput.getvalue().strip())


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


class CountInfoTest(TestCase):
    @patch('complaintdatabase.views.requests.get')
    def test_get_count_info(self, mock_requests_get):
        # Using namedtuple to mock out the attribute text in response
        # not sure if this is the best way though
        Response = collections.namedtuple('Response', 'text')
        input_text = ("[{\"company_response\": \"Untimely response\", "
                      "\"count_complaint_id\": \"4\"}, "
                      "{\"company_response\": \"Ok\", "
                      "\"count_complaint_id\": \"5\"}, "
                      "{\"company_response\": \"Yes\", "
                      "\"count_complaint_id\": \"6\"}]")
        mock_requests_get.return_value = Response(text=input_text)
        res_complaints, res_timely = get_count_info()
        self.assertEqual(res_complaints, 15)
        self.assertEqual(res_timely, 11)

    @patch('complaintdatabase.views.requests.get')
    def test_request_exception_get_count_info(self, mock_requests_get):
        mock_requests_get.side_effect = MOCK_404
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_complaints, res_timely = get_count_info()
            self.assertEqual(res_complaints, 0)
            self.assertEqual(res_timely, 0)
            self.assertIn('requests.exceptions.RequestException',
                          fakeOutput.getvalue().strip())

    @patch('complaintdatabase.views.requests.get')
    def test_incorrect_text_get_count_info(self, mock_requests_get):
        error = "This is not a correct set of info"
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text=error)
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_complaints, res_timely = get_count_info()
            self.assertEqual(res_complaints, 0)
            self.assertEqual(res_timely, 0)
            self.assertIn('ValueError', fakeOutput.getvalue().strip())

    @patch('complaintdatabase.views.requests.get')
    def test_no_key_get_count_info(self, mock_requests_get):
        response_text = "[ {\"count\": \"1\"}, {\"count\": \"2\"} ]"
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text=response_text)
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_complaints, res_timely = get_count_info()
            self.assertEqual(res_complaints, 0)
            self.assertEqual(res_timely, 0)
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

    # @patch('complaintdatabase.views.get_now')
    # def test_data_not_updated_saturday_down(self, mock_get_now):
    #     mock_get_now.return_value = datetime(2015, 12, 26, 19, 20, 10, 975427)
    #     input_json = {'stats': {'last_updated': "2015-12-18",
    #                             'last_updated_narratives': "2015-12-18"}}
    #     data_down, narratives_down = is_data_not_updated(input_json)
    #     self.assertTrue(data_down)
    #     self.assertFalse(narratives_down)

    # @patch('complaintdatabase.views.get_now')
    # def test_data_not_updated_saturday_up(self, mock_get_now):
    #     mock_get_now.return_value = datetime(2015, 12, 26, 19, 20, 10, 975427)
    #     input_json = {'stats': {'last_updated': "2015-12-21",
    #                             'last_updated_narratives': "2015-12-21"}}
    #     data_down, narratives_down = is_data_not_updated(input_json)
    #     self.assertFalse(data_down)
    #     self.assertFalse(narratives_down)

    # @patch('complaintdatabase.views.get_now')
    # def test_data_not_updated_saturday_narratives_down(self, mock_get_now):
    #     mock_get_now.return_value = datetime(2015, 12, 26, 19, 20, 10, 975427)
    #     input_json = {'stats': {'last_updated': "2015-12-21",
    #                             'last_updated_narratives': "2015-12-18"}}
    #     data_down, narratives_down = is_data_not_updated(input_json)
    #     self.assertFalse(data_down)
    #     self.assertTrue(narratives_down)

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
