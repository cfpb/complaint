from django.conf.urls import url
from complaint.views import SubmitView, DataUseView, ProcessView

urlpatterns = [
    url(r'^$', SubmitView.as_view()),
    url(r'^data-use/', DataUseView.as_view()),
    url(r'^process/', ProcessView.as_view()),
]
