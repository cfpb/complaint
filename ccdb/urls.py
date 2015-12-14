from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ccdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ccdb_content/', include('ccdb_content.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
