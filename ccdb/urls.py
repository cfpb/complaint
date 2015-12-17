from django.conf.urls import patterns, include, url
from complaintdatabase.views import SubmitView, ProcessView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ccdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^complaintdatabase/', include('complaintdatabase.urls')),
    url(r'^complaint/process', ProcessView.as_view()),
    url(r'^complaint/', SubmitView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
