from django.conf.urls import url
from landing_pages.views import DataUseView, LandingView, DocsView

urlpatterns = [
    url(r'^data-use-content/', DataUseView.as_view()),
    url(r'^landing-page/', LandingView.as_view()),
    url(r'^technical-documentation/', DocsView.as_view()),
]