#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4

from itertools import groupby
from operator import attrgetter

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage


from .models import Campaign


@login_required
def dashboard(request):

    paginator = Paginator(Campaign.objects.all(), 1)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    campaign = None
    try:
        campaign = paginator.page(page).object_list[0]
    except (EmptyPage, InvalidPage, IndexError):
        campaigns = paginator.page(paginator.num_pages).object_list
        if campaigns:
            campaign = campaigns[0]

    if campaign:
        results = sorted(campaign.results.all(), attrgetter('location.name'))
        results = groupby(results, attrgetter('location.name'))

    ctx = locals()

    return render_to_response('who_base/index.html',  ctx,
                              context_instance=RequestContext(request))
