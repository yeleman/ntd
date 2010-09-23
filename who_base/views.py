#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4

from itertools import groupby
from operator import attrgetter

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage


from .models import Campaign, Results


@login_required
def dashboard(request):

    paginator = Paginator(Campaign.objects.order_by('-start_date'), 1)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    campaign = None
    try:
        page = paginator.page(page)
        campaign = page.object_list[0]
    except (EmptyPage, InvalidPage, IndexError):
        page = paginator.page(paginator.num_pages)
        if page.object_list:
            campaign = page.object_list[0]

    if campaign:
        # group by commune
        results = sorted(Results.objects.filter(campaign=campaign), 
                                                key=attrgetter('area'))
        results = groupby(results, attrgetter('area')) 
        
        # group by cercle (nested lambda, don't you like it :-) ?)
        get_ = lambda i, k: (lambda o: getattr(o[i], k) ) 
        results = groupby(results, get_(0, 'parent'))      
        
        # group by region
        results = groupby(results, get_(0, 'parent')) 

    ctx = locals()

    return render_to_response('who_base/index.html',  ctx,
                              context_instance=RequestContext(request))
