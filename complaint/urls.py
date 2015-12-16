from django.conf.urls import url
from complaint.views import SubmitView, ProcessView

urlpatterns = [
    url(r'^$', SubmitView.as_view()),
    url(r'^process/', ProcessView.as_view()),
]
