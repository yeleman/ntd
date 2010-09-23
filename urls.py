#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('')

if settings.DEBUG:

    urlpatterns += patterns("", url("%s/who_base/(?P<path>.*)$" % settings.MEDIA_URL.strip('/'),
                                    "django.views.static.serve", 
                                    {"document_root": 
                                      os.path.join(settings.PROJECT_DIR, 
                                                    'who_base', 'static'), 
                                      'show_indexes': True}))

urlpatterns += patterns("",

    url(r'^admin/', include(admin.site.urls)),
    url(r'^',  include("rapidsms.urls"), name='rapidsms-ui'),
)


                                                    
    
