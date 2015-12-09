import requests
import json
from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.
#BASE_TEMPLATE = "base.html"

BASE_TEMPLATE = "standalone/base_update.html"

class LandingView(TemplateView):
    template_name = "landing-page.html"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        response = requests.get("http://files.consumerfinance.gov/ccdb/narratives.json")
        res_json = json.loads(response.text[11:-2])  # This is to parse out the narratives(); wrap around the json
        context['narratives'] = res_json
        return context

class DataUseView(TemplateView):
    template_name = "data-use-content.html"

    def get_context_data(self, **kwargs):
        context = super(DataUseView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context

class DocsView(TemplateView):
    template_name = "technical-documentation.html"

    def get_context_data(self, **kwargs):
        context = super(DocsView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context
