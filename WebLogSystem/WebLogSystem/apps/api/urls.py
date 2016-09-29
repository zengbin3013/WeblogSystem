from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from WebLogSystem.apps.api.views import Index,ApiLogin,GetSiteId,UploadLog

urlpatterns = patterns('',
    url(r'^$',Index.as_view(),name='index'),
    url(r'^apilogin/',ApiLogin.as_view(),name='apilogin'),
    url(r'^getsiteid/',csrf_exempt(GetSiteId.as_view()),name='getsiteid'),
    url(r'^uploadlog/',csrf_exempt(UploadLog.as_view()),name='uploadlog'),
    # Examples:
    # url(r'^$', 'WebLogSystem.views.home', name='home'),
    # url(r'^WebLogSystem/', include('WebLogSystem.WebLogSystem.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
