import requests
import json
from datetime import datetime
from django.shortcuts import render
from django.views.generic import View, TemplateView
from datetime import datetime
from django.conf import settings

try:
    STANDALONE = settings.STANDALONE
except:  # pragma: no cover
    STANDALONE = False

if STANDALONE:
    BASE_TEMPLATE = "standalone/base_update.html"
else:  # pragma: no cover
    BASE_TEMPLATE = "front/base_update.html"


class SubmitView(TemplateView):
    template_name = "submit-a-complaint.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context


class DataUseView(TemplateView):
    template_name = "data-use.html"

    def get_context_data(self, **kwargs):
        context = super(DataUseView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context


class ProcessView(TemplateView):
    template_name = "process.html"

    def get_context_data(self, **kwargs):
        context = super(ProcessView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context
