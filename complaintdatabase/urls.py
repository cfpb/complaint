from django.conf.urls import url
from complaintdatabase.views import LandingView

urlpatterns = [
    url(r'^$', LandingView.as_view()),
]
