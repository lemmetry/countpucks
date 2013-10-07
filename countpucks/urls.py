from django.conf.urls import patterns, include, url
from countpucks.views import api, deleteEverything, playerOfTheDay, about


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^api$/', api, name='api'),
    # url(r'^wipe/$', deleteEverything, name='deleteEverything'),

    url(r'^$', playerOfTheDay, name='playerOfTheDay'),
    url(r'^about/$', about, name='about'),
    # url(r'^$', 'countpucks.views.home', name='home'),
    # url(r'^countpucks/', include('countpucks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)