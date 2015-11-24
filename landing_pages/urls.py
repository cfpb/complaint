from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^data-use-content/', TemplateView.as_view(template_name="data-use-content.html")),
    url(r'^landing-page/', TemplateView.as_view(template_name="landing-page.html")),
    url(r'^technical-documentation/', TemplateView.as_view(template_name="technical-documentation.html")),
]
