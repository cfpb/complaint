from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.
#BASE_TEMPLATE = "base.html"
BASE_TEMPLATE = "base_update.html"

class LandingView(TemplateView):
    template_name = "landing-page.html"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context

class DataUseView(TemplateView):
    template_name = "data-use-content.html"

    def get_context_data(self, **kwargs):
        context = super(DataUseView, self).get_context_data(**kwargs)
        context['base_template'] = BASE_TEMPLATE
        return context
