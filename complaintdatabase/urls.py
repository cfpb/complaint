from django.conf import settings
from django.conf.urls import url
from complaintdatabase.views import LandingView

try:
    STANDALONE = settings.STANDALONE
except AttributeError:  # pragma: no cover
    STANDALONE = False

urlpatterns = [
    url(r'^$', LandingView.as_view(),
        name='ccdb-landing-page')
]

if STANDALONE:
    urlpatterns += [
        url(r'^demo/(?P<demo_json>[^/]+)/$', LandingView.as_view(),
            name='ccdb-demo')
    ]
