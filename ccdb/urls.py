from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^complaint/', include('complaint.urls',
                                namespace='complaints')),
    url(r'^complaintdatabase/', include('complaintdatabase.urls',
                                        namespace='complaintdatabase')),
    url(r'^admin/', include(admin.site.urls)),
]
