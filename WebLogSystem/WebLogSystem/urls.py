"""
Definition of urls for WebLogSystem.
"""

from django.conf.urls import patterns, include, url
from WebLogSystem.apps.admin.views import LoginView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'api/',include('WebLogSystem.apps.api.urls')),
    url(r'admin/',include('WebLogSystem.apps.admin.urls')),
    url(r'^$',LoginView.as_view(),name='login'),
    # Examples:
    # url(r'^$', 'WebLogSystem.views.home', name='home'),
    # url(r'^WebLogSystem/', include('WebLogSystem.WebLogSystem.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
