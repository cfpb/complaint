from django.conf.urls import patterns, include, url
from complaint.views import SubmitView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ccdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^complaintdatabase/', include('complaintdatabase.urls')),
    url(r'^complaint/', SubmitView.as_view()),
    # url(r'^$', SubmitView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
