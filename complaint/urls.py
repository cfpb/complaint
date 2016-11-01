from django.conf.urls import url
from complaint.views import SubmitView, DataUseView, ProcessView

urlpatterns = [
    url(r'^$', SubmitView.as_view(), name='ccdb_submit'),
    url(r'^data-use/', DataUseView.as_view(), name='ccdb_data_use'),
    url(r'^process/', ProcessView.as_view(), name='ccdb_process'),
]
