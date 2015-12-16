from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ccdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^complaintdatabase/', include('complaintdatabase.urls')),
    url(r'^complaint/', include('complaint.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
