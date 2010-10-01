#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4

import csv

from itertools import groupby
from operator import attrgetter

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from .models import Campaign, Results

from simple_locations.models import Area

from .forms import CampaignForm

@login_required
def dashboard(request):

    return render_to_response('who_base/index.html',  {},
                              context_instance=RequestContext(request))
                              
@login_required                          
def create_campaign(request):

    locations = Area.objects.filter(as_data_source__isnull=False)
    
    if request.method == 'POST':
        campaign_form = CampaignForm(request.POST)
        if campaign_form.is_valid():
           campaign_form.save() 
           return redirect('campaigns-list')
    else:
        campaign_form = CampaignForm()

    ctx = locals()
    return render_to_response('create_campaign.html',  ctx,
                              context_instance=RequestContext(request))
