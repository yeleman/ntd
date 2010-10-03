#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.list_detail import object_list
from django.views.generic.simple import redirect_to

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
    url(r'campaign/delete/(?P<pk>\d+)/$',  "who_base.views.delete_campaign", 
        name="delete-campaign"),
    
    url(r'switch-language/$',  "who_base.views.switch_lang", name='switch-lang'),    
    
    url(r'dashboard/$',  "who_base.views.dashboard", name='who-dashboard'),
    url(r'$',  redirect_to, { 'url': "/dashboard/" }),
)


