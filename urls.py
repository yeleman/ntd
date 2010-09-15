#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.defaults import *
urlpatterns = patterns("",

    # Example:
    # (r'^django_project/', include('django_project.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^rapidsms/', include("rapidsms.urls")),
)
