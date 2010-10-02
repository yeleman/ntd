#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

import os

urlpatterns = patterns('',

    # admin
    (r'^admin/', include(admin.site.urls)),
    
    # rapidsms
    (r'^account/', include('rapidsms.urls.login_logout')),
    (r'^ajax/', include('rapidsms.contrib.ajax.urls')),
    (r'^export/', include('rapidsms.contrib.export.urls')),
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    (r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messagelog/', include('logger_ng.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^registration/', include('auth.urls')),
    (r'^scheduler/', include('rapidsms.contrib.scheduler.urls')),
    
    url(r'^rapidsms-dashboard/$', 
        'rapidsms.views.dashboard', 
        name='rapidsms-dashboard'),
        
)


if settings.DEBUG:

    urlpatterns += patterns("", url("%s/who_base/(?P<path>.*)$" % settings.MEDIA_URL.strip('/'),
                                "django.views.static.serve", 
                                {"document_root": 
                                  os.path.join(settings.PROJECT_DIR, 
                                                'who_base', 'static'), 
                                  'show_indexes': True}))

    urlpatterns += patterns('',
        # helper URLs file that automatically serves the 'static' folder in
        # INSTALLED_APPS via the Django static media server (NOT for use in
        # production)
        (r'^', include('rapidsms.urls.static_media')),
    )


urlpatterns += patterns("",
                        url(r'^', include('who_base.urls'), 
                                  name='who-dashboard'),)

                                                    
    
