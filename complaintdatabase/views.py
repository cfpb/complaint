import requests
import json
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
        response = requests.get("http://files.consumerfinance.gov/ccdb/narratives.json")
        res_json = json.loads(response.text[11:-2])  # This is to parse out the 'narratives();' that wrapped around the json
        context['narratives'] = res_json
        context['pipeline_down'] = True
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

class SubmitView(TemplateView):
    template_name = "submit-a-complaint.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context

class ProcessView(TemplateView):
    template_name = "process.html"

    def get_context_data(self, **kwargs):
        context = super(ProcessView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context
