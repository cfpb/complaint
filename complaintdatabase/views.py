import requests
import json
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.conf import settings

try:
    STANDALONE = settings.STANDALONE
except:  # pragma: no cover
    STANDALONE = False

if STANDALONE:
    BASE_TEMPLATE = "standalone/base_update.html"
else:  # pragma: no cover
    BASE_TEMPLATE = "front/base_update.html"


class LandingView(TemplateView):
    """
    Main page view.

    To run as a standalone demo with local data, put your demo json
    in the 'demo.json' file at the project root and use this standalone url:
    'http://127.0.0.1:8000/complaintdatabase/demo/demo.json/'
    You can use a different file name; just specify it in the last URL field.
    """

    @property
    def template_name(self):
        return "landing-page.html"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        if 'demo_json' in kwargs:
            res_json = get_narratives_json(demo_json=kwargs['demo_json'])
        else:
            res_json = get_narratives_json()
        context['narratives'] = format_narratives(res_json)
        context['stats'] = get_stats(res_json)
        (context['total_complaints'],
         context['timely_responses']) = get_count_info()
        (context['data_down'],
         context['narratives_down']) = is_data_not_updated(res_json)
        return context


class DocsView(TemplateView):
    template_name = "technical-documentation.html"

    def get_context_data(self, **kwargs):
        context = super(DocsView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context


def get_narratives_json(demo_json=None):
    """
    Main handler to deliver sample narratives to the landing page.

    To demo a local json file, pass in a file path via the 'demo_json' kwarg
    """

    if demo_json:
        with open(demo_json, 'r') as f:
            res_json = json.loads(f.read())
        return res_json

    s3json = "http://files.consumerfinance.gov/ccdb/narratives.json"
    try:
        res_json = requests.get(s3json).json()
    except requests.exceptions.RequestException as e:
        print("get_narratives_json:requests.exceptions.RequestException")
        print("There is a problem with getting data from the URL")
        print(e)
        res_json = {}
    except ValueError as e:
        print("get_narratives_json:ValueError")
        print("The text from the response doesn't follow "
              "the correct format to be parse as json")
        print(e)
        res_json = {}
    return res_json


def format_narratives(res_json):
    """Set up label and css values for page."""
    narratives = []

    # Additional data needed to output the narratives on the page
    # title, css, and icon are required
    # optional 'tooltip' determines text that displays on section button hover
    # 'tooltip' defaults to title
    narrative_types = [
        {'key': 'bank_accounts',
         'title': 'Bank account',
         'css': 'bank-account',
         'icon': 'bank-account'},
        {'key': 'credit_cards',
         'title': 'Credit card',
         'css': 'credit-card',
         'icon': 'credit-card'},
        {'key': 'credit_reporting',
         'title': 'Credit reporting',
         'css': 'credit-reporting',
         'icon': 'loan'},
        {'key': 'debt_collection',
         'title': 'Debt collection',
         'css': 'debt-collection',
         'icon': 'debt-collection'},
        {'key': 'money_transfers',
         'title': 'Money transfer or virtual currency',
         'css': 'money-transfer',
         'icon': 'money-transfer',
         'tooltip': 'Money transfer/virtual currency'},
        {'key': 'mortgages',
         'title': 'Mortgage',
         'css': 'mortgage',
         'icon': 'owning-home'},
        {'key': 'other_financial_services',
         'title': 'Other financial service',
         'css': 'other',
         'icon': 'money'},
        {'key': 'payday_loans',
         'title': 'Payday loan',
         'css': 'payday-loan',
         'icon': 'payday-loan'},
        {'key': 'prepaid_cards',
         'title': 'Prepaid card',
         'css': 'prepaid-card',
         'icon': 'prepaid-cards'},
        {'key': 'student_loans',
         'title': 'Student loan',
         'css': 'student-loan',
         'icon': 'paying-college'},
        {'key': 'other_consumer_loans',
         'title': 'Vehicle / consumer loan',
         'css': 'consumer-loan',
         'icon': 'buying-car'}
    ]

    try:

        for index, item in enumerate(narrative_types):
            # get json data for this type
            narrative = res_json[item['key']]

            # extend it with the additional title/css/icon/tooltip data
            narrative.update(item)

            # format date
            narrative['date'] = datetime.strptime(narrative['date_received'],
                                                  "%Y-%m-%dT%H:%M:%S")

            # add data for next item
            narrative['next'] = narrative_types[(index + 1) %
                                                len(narrative_types)]

            narratives.append(narrative)

    except KeyError as e:
        print("format_narratives:KeyError")
        print("There is problem accessing with the given key, "
              "which probably means the json has missing data")
        print(e)

    return narratives


def get_stats(res_json):
    res_stat = {}
    try:
        res_stat = res_json['stats']
    except KeyError as e:
        print("get_stats:KeyError")
        print("There is problem accessing with the given key, "
              "which probably means the json has missing data")
        print(e)

    return res_stat


def get_count_info():
    total_complaints = 0
    timely_responses = 0
    try:
        count_response = requests.get('https://data.consumerfinance.gov/'
                                      'resource/u473-64qt.json')
        count_json = json.loads(count_response.text)

        for item in count_json:
            item_count = int(item['count_complaint_id'])
            total_complaints += item_count
            if item['company_response'] != 'Untimely response':
                timely_responses += item_count

    except requests.exceptions.RequestException as e:
        print("get_count_info:requests.exceptions.RequestException")
        print("There is a problem with getting data from the URL")
        print(e)

    except ValueError as e:
        print("get_count_info:ValueError")
        print("The text from the response doesn't follow "
              "the correct format to be parsed as json.")
        print(e)

    except KeyError as e:
        print("get_count_info:KeyError")
        print("There is problem accessing with the given key, "
              "which probably means the json has missing data")
        print(e)
        total_complaints = 0
        timely_responses = 0

    return (total_complaints, timely_responses)


def get_now():
    return datetime.now()


def is_data_not_updated(res_json):
    data_down = False
    narratives_down = False
    # show notification starting fifth business day data has not been updated
    # M-Th, data needs to have been updated 6 days ago; F-S, preceding Monday
    weekday = datetime.weekday(get_now())
    delta = weekday if weekday > 3 else 6
    four_business_days_ago = (get_now() -
                              timedelta(delta)).strftime("%Y-%m-%d")

    try:

        if res_json['stats']['last_updated'] < four_business_days_ago:
            data_down = True
        elif (res_json['stats']['last_updated_narratives'] <
                four_business_days_ago):
            narratives_down = True
    except KeyError as e:
        print("is_data_not_updated:KeyError")
        print("There is problem accessing with the given key, "
              "which probably means the json has missing data")
        print(e)

    return (data_down, narratives_down)
