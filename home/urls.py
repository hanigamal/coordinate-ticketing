from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('home.views',
    url(r'^jobs$',
        'jobs',
        name='home_display'),
    url(r'^$',
        'home',
        name='home_display'),
    )