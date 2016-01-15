import unittest
import collections
from requests.exceptions import ConnectionError

from mock import patch, Mock
import django
from django.test import RequestFactory, TestCase
from django.http import HttpResponse, HttpRequest
from django.test import Client
from django.core.urlresolvers import reverse
from datetime import datetime
from StringIO import StringIO
from .views import LandingView, DocsView, get_narratives_json, format_narratives, get_stats, get_count_info, get_now, is_data_not_updated

class LandingViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_context_data_exist(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        response = LandingView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('base_template' in response.context_data.keys())
        self.assertTrue('narratives' in response.context_data.keys())
        self.assertTrue('stats' in response.context_data.keys())
        self.assertTrue('total_complaints' in response.context_data.keys())
        self.assertTrue('timely_responses' in response.context_data.keys())


class NarrativeJsonTest(TestCase):
    @patch('requests.get')
    def test_get_narratives_json(self, mock_requests_get):
        # Using namedtuple to mock out the attribute text in response
        # not sure if this is the best way though
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text="narratives({});")
        res_json = get_narratives_json()
        self.assertEqual(res_json, {})

    @patch('requests.get')
    def test_request_exception_get_narratives_json(self, mock_requests_get):
        mock_requests_get.side_effect = ConnectionError(Mock(return_value={'status': 404}), 'not found')
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_json = get_narratives_json()
            self.assertEqual(res_json, {})
            self.assertIn('requests.exceptions.RequestException', fakeOutput.getvalue().strip())

    @patch('requests.get')
    def test_incorrect_text_get_narratives_json(self, mock_requests_get):
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text="This is not a correct set of narratives")
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_json = get_narratives_json()
            self.assertEqual(res_json, {})
            self.assertIn('ValueError', fakeOutput.getvalue().strip())


class FormatNarrativesTest(TestCase):
    def test_format_narratives(self):
        input_json = {
            'bank_accounts': {'date_received': '2015-04-08T20:32:15', 'tags': ['Older American', 'Servicemember']},
            'credit_cards': {'date_received': '2015-04-08T20:32:16', 'tags': ['Older American', 'Servicemember']},
            'credit_reporting': {'date_received': '2015-04-08T20:32:17', 'tags': ['Older American', 'Servicemember']},
            'debt_collection': {'date_received': '2015-04-08T20:32:18', 'tags': ['Older American', 'Servicemember']},
            'money_transfers': {'date_received': '2015-04-08T20:32:19', 'tags': ['Older American', 'Servicemember']},
            'mortgages': {'date_received': '2015-04-08T21:32:15', 'tags': ['Older American', 'Servicemember']},
            'other_financial_services': {'date_received': '2015-04-09T20:32:15'},
            'payday_loans': {'date_received': '2015-04-10T20:32:15'},
            'prepaid_cards': {'date_received': '2015-04-11T20:32:15'},
            'student_loans': {'date_received': '2015-04-12T20:32:15'},
            'other_consumer_loans': {'date_received': '2015-04-13T20:32:15'}
        }
        exp_res = [
                    {
                    'date_received': '2015-04-08T20:32:15', 
                    'title': 'Bank account', 'css': 'bank-account', 'icon':'bank-account',
                    'tags': ['Older American', 'Servicemember'],
                    'date': datetime(2015, 4, 8, 20, 32, 15),
                    'next': {'key':'credit_cards', 'title':'Credit card', 'css':'credit-card', 'icon':'credit-card'}
                    },
                    {
                    'date_received': '2015-04-08T20:32:16',
                    'title':'Credit card', 'css':'credit-card', 'icon':'credit-card',
                    'tags': ['Older American', 'Servicemember'],
                    'date': datetime(2015, 4, 8, 20, 32, 16),
                    'next': {'key':'credit_reporting', 'title':'Credit Reporting', 'css':'credit-reporting', 'icon':'loan'}
                    },
                    {
                    'date_received': '2015-04-08T20:32:17',
                    'title':'Credit Reporting', 'css':'credit-reporting', 'icon':'loan',
                    'tags': ['Older American', 'Servicemember'],
                    'date': datetime(2015, 4, 8, 20, 32, 17),
                    'next': {'key':'debt_collection', 'title':'Debt Collection', 'css':'debt-collection', 'icon': 'debt-collection'}
                    },
                    {
                    'date_received': '2015-04-08T20:32:18',
                    'title':'Debt Collection', 'css':'debt-collection', 'icon': 'debt-collection',
                    'tags': ['Older American', 'Servicemember'],
                    'date': datetime(2015, 4, 8, 20, 32, 18),
                    'next': {'key':'money_transfers', 'title':'Money Transfer', 'css':'money-transfer', 'icon': 'money-transfer'}
                    },
                    {
                    'date_received': '2015-04-08T20:32:19',
                    'title':'Money Transfer', 'css':'money-transfer', 'icon': 'money-transfer',
                    'tags': ['Older American', 'Servicemember'],
                    'date': datetime(2015, 4, 8, 20, 32, 19),
                    'next': {'key':'mortgages', 'title':'Mortgage', 'css':'mortgage', 'icon': 'owning-home'}
                    },
                    {
                    'date_received': '2015-04-08T21:32:15',
                    'title':'Mortgage', 'css':'mortgage', 'icon': 'owning-home',
                    'tags': ['Older American', 'Servicemember'],
                    'date': datetime(2015, 4, 8, 21, 32, 15),
                    'next': {'key':'other_financial_services', 'title':'Other financial service', 'css':'other', 'icon': 'money'}
                    },
                    {
                    'date_received': '2015-04-09T20:32:15',
                    'title':'Other financial service', 'css':'other', 'icon': 'money',
                    'date': datetime(2015, 4, 9, 20, 32, 15),
                    'next': {'key':'payday_loans', 'title':'Payday Loan', 'css':'payday-loan', 'icon': 'payday-loan'}
                    },
                    {
                    'date_received': '2015-04-10T20:32:15',
                    'title':'Payday Loan','css':'payday-loan','icon': 'payday-loan',
                    'date': datetime(2015, 4, 10, 20, 32, 15),
                    'next': {'key':'prepaid_cards', 'title':'Prepaid Card', 'css':'prepaid-card', 'icon': 'prepaid-cards'}
                    },
                    {
                    'date_received': '2015-04-11T20:32:15',
                    'title':'Prepaid Card', 'css':'prepaid-card', 'icon': 'prepaid-cards',
                    'date': datetime(2015, 4, 11, 20, 32, 15),
                    'next': {'key':'student_loans', 'title':'Student Loan', 'css':'student-loan', 'icon': 'paying-college'}
                    },
                    {
                    'date_received': '2015-04-12T20:32:15',
                    'title':'Student Loan', 'css':'student-loan', 'icon': 'paying-college',
                    'date': datetime(2015, 4, 12, 20, 32, 15),
                    'next': {'key':'other_consumer_loans', 'title':'Vehicle / consumer loan', 'css':'consumer-loan', 'icon': 'buying-car'}
                    },
                    {
                    'date_received': '2015-04-13T20:32:15',
                    'title':'Vehicle / consumer loan', 'css':'consumer-loan', 'icon': 'buying-car',
                    'date': datetime(2015, 4, 13, 20, 32, 15),
                    'next': {'key': 'bank_accounts', 'title': 'Bank account', 'css': 'bank-account', 'icon':'bank-account'}
                    }]
        res = format_narratives(input_json)
        self.assertEqual(res, exp_res)

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
    @patch('requests.get')
    def test_get_count_info(self, mock_requests_get):
        # Using namedtuple to mock out the attribute text in response
        # not sure if this is the best way though
        Response = collections.namedtuple('Response', 'text')
        input_text = "[{\"company_response\": \"Untimely response\", \"count_complaint_id\": \"4\"}, \
                        {\"company_response\": \"Ok\", \"count_complaint_id\":\"5\"}, \
                        {\"company_response\": \"Yes\", \"count_complaint_id\": \"6\"}]"
        mock_requests_get.return_value = Response(text=input_text)
        res_complaints, res_timely = get_count_info()
        self.assertEqual(res_complaints, 15)
        self.assertEqual(res_timely, 11)

    @patch('requests.get')
    def test_request_exception_get_count_info(self, mock_requests_get):
        mock_requests_get.side_effect = ConnectionError(Mock(return_value={'status': 404}), 'not found')
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_complaints, res_timely = get_count_info()
            self.assertEqual(res_complaints, 0)
            self.assertEqual(res_timely, 0)
            self.assertIn('requests.exceptions.RequestException', fakeOutput.getvalue().strip())

    @patch('requests.get')
    def test_incorrect_text_get_count_info(self, mock_requests_get):
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text="This is not a correct set of info")
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_complaints, res_timely = get_count_info()
            self.assertEqual(res_complaints, 0)
            self.assertEqual(res_timely, 0)
            self.assertIn('ValueError', fakeOutput.getvalue().strip())

    @patch('requests.get')
    def test_no_key_get_count_info(self, mock_requests_get):
        Response = collections.namedtuple('Response', 'text')
        mock_requests_get.return_value = Response(text="[ {\"count\": \"1\"}, {\"count\": \"2\"} ]")
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            res_complaints, res_timely = get_count_info()
            self.assertEqual(res_complaints, 0)
            self.assertEqual(res_timely, 0)
            self.assertIn('KeyError', fakeOutput.getvalue().strip())

class DataUpdatedTest(TestCase):

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_monday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 21, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-14", 'last_updated_narratives': "2015-12-14"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_monday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 21, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-15", 'last_updated_narratives': "2015-12-15"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_monday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 21, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-15", 'last_updated_narratives': "2015-12-14"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_tuesday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 22, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-15", 'last_updated_narratives': "2015-12-15"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)    

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_tuesday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 22, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-16", 'last_updated_narratives': "2015-12-16"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down) 

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_tuesday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 22, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-16", 'last_updated_narratives': "2015-12-15"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down) 

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_wednesday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 23, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-16", 'last_updated_narratives': "2015-12-16"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)    

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_wednesday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 23, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-17", 'last_updated_narratives': "2015-12-17"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down) 

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_wednesday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 23, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-17", 'last_updated_narratives': "2015-12-16"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_thursday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 24, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-17", 'last_updated_narratives': "2015-12-17"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)    

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_thursday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 24, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18", 'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down) 

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_thursday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 24, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18", 'last_updated_narratives': "2015-12-17"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_friday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 25, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18", 'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)    

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_friday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 25, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21", 'last_updated_narratives': "2015-12-21"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down) 

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_friday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 25, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21", 'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 26, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18", 'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)    

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 26, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21", 'last_updated_narratives': "2015-12-21"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down) 

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 26, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21", 'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertTrue(narratives_down)

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 27, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-18", 'last_updated_narratives': "2015-12-18"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertTrue(data_down)
        self.assertFalse(narratives_down)    

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_up(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 27, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21", 'last_updated_narratives': "2015-12-21"}}
        data_down, narratives_down = is_data_not_updated(input_json)
        self.assertFalse(data_down)
        self.assertFalse(narratives_down) 

    @patch('complaintdatabase.views.get_now')
    def test_data_not_updated_saturday_narratives_down(self, mock_get_now):
        mock_get_now.return_value = datetime(2015, 12, 27, 19, 20, 10, 975427)
        input_json = {'stats': {'last_updated': "2015-12-21", 'last_updated_narratives': "2015-12-18"}}
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
