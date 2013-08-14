from django.conf.urls import patterns, include, url
from countpucks.views import homepage, api


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^homepage/$', homepage, name='homepage'),
    url(r'^api$', api, name='api'),
    # url(r'^$', 'countpucks.views.home', name='home'),
    # url(r'^countpucks/', include('countpucks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
