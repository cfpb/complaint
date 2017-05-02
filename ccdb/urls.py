from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^complaint/', include('complaint.urls')),
    url(r'^complaintdatabase/', include('complaintdatabase.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
