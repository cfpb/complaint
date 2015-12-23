from django.conf.urls import url
from complaintdatabase.views import LandingView, DocsView

urlpatterns = [
    url(r'^$', LandingView.as_view()),
    url(r'^technical-documentation/', DocsView.as_view()),
]
