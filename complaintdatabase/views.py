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
    template_name = "landing-page.html"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE

        res_json = get_narratives_json()

        context['narratives'] = format_narratives(res_json)
        context['stats'] = res_json['stats']
        context['total_complaints'], context['timely_responses'] = get_count_info()

        context['data_down'], context['narratives_down'] = is_data_not_updated(res_json)

        
        return context


class DocsView(TemplateView):
    template_name = "technical-documentation.html"

    def get_context_data(self, **kwargs):
        context = super(DocsView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context

def get_narratives_json():
    response = requests.get("http://files.consumerfinance.gov/ccdb/narratives.json")
    return json.loads(response.text[11:-2])  # This is to parse out the 'narratives();' that wrapped around the json

def format_narratives(res_json):
    
    narratives = []
    narrative_types = [
        {'key': 'bank_accounts', 'title': 'Bank account', 'css': 'bank-account', 'icon':'bank-account'},
        {'key':'credit_cards', 'title':'Credit card', 'css':'credit-card', 'icon':'credit-card'},
        {'key':'credit_reporting', 'title':'Credit Reporting', 'css':'credit-reporting', 'icon':'loan'},
        {'key':'debt_collection', 'title':'Debt Collection', 'css':'debt-collection', 'icon': 'debt-collection'},
        {'key':'money_transfers', 'title':'Money Transfer', 'css':'money-transfer', 'icon': 'money-transfer'},
        {'key':'mortgages', 'title':'Mortgage', 'css':'mortgage', 'icon': 'owning-home'},
        {'key':'other_financial_services', 'title':'Other financial service', 'css':'other', 'icon': 'money'},
        {'key':'payday_loans', 'title':'Payday Loan', 'css':'payday-loan', 'icon': 'payday-loan'},
        {'key':'prepaid_cards', 'title':'Prepaid Card', 'css':'prepaid-card', 'icon': 'prepaid-cards'},
        {'key':'student_loans', 'title':'Student Loan', 'css':'student-loan', 'icon': 'paying-college'},
        {'key':'other_consumer_loans', 'title':'Vehicle / consumer loan', 'css':'consumer-loan', 'icon': 'buying-car'}
    ]

    for index, item in enumerate(narrative_types):
        # get json data for this type
        narrative = res_json[item['key']]

        for attr in ['title', 'css', 'icon']:
            narrative[attr] = item[attr]

        # format date
        narrative['date'] = datetime.strptime(narrative['date_received'], "%Y-%m-%dT%H:%M:%S")

        # add data for next item
        narrative['next'] = narrative_types[(index + 1) % len(narrative_types)]

        narratives.append(narrative)

    return narratives

def get_count_info():
    count_response = requests.get('https://data.consumerfinance.gov/resource/u473-64qt.json')
    count_json = json.loads(count_response.text)     
    total_complaints = 0
    timely_responses = 0
    for item in count_json:
        item_count = int(item['count_complaint_id'])
        total_complaints += item_count
        if item['company_response'] != 'Untimely response':
            timely_responses += item_count

    return (total_complaints, timely_responses)

def is_data_not_updated(res_json):
    data_down = False
    narratives_down = False
    # show notification starting fifth business day data has not been updated
    # M-Th, data needs to have been updated 6 days ago; F-S, preceding Monday
    weekday = datetime.weekday(datetime.now())
    delta = weekday if weekday > 3 else 6
    four_business_days_ago = (datetime.now() - timedelta(delta)).strftime("%Y-%m-%d")
    
    if res_json['stats']['last_updated'] < four_business_days_ago: 
        data_down = True
    elif res_json['stats']['last_updated_narratives'] < four_business_days_ago: 
        narratives_down = True

    return (data_down, narratives_down)
