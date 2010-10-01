#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.list_detail import object_list

from .models import Campaign

urlpatterns = patterns("",

    url(r'campaigns/$',  object_list, {'queryset': Campaign.objects.all(),
                                       'template_name': 'campaigns-list.html', 
                                       'template_object_name': 'campaigns'}, 
        name="campaigns-list"),
    url(r'campaign/create/$',  "who_base.views.create_campaign", 
        name="create-campaign"),
    url(r'campaign/edit/(?P<pk>\d+)/$',  "who_base.views.edit_campaign", 
        name="edit-campaign"),
    url(r'$',  "who_base.views.dashboard"),
    
)


