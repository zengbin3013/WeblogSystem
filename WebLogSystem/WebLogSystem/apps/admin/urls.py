from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from WebLogSystem.apps.admin.views import LoginView,IndexView,GetcodedataView,AjaxLoginView

urlpatterns = patterns('',
    url(r'^login$',LoginView.as_view(),name='login'),
    url(r'^ajaxlogin$',AjaxLoginView.as_view(),name='ajaxlogin'),
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^index$',IndexView.as_view(),name='index'),
    url(r'^getcodedata/',GetcodedataView.as_view(),name='getcodedata'),
    #url(r'^getsiteid/',csrf_exempt(GetSiteId.as_view()),name='getsiteid'),
    # Examples:
    # url(r'^$', 'WebLogSystem.views.home', name='home'),
    # url(r'^WebLogSystem/', include('WebLogSystem.WebLogSystem.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
