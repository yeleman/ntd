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
        
        results_by_cities = {}
        for result in Results.objects.filter(campaign=campaign):
            data = results_by_cities.setdefault(result.area.parent, {})
            data['count'] = data.get('count', 0) + 1
            data.setdefault('results', []).append(result)
            
        cities_by_cercle = {}
        for city, city_data in results_by_cities.iteritems():
            data = cities_by_cercle.setdefault(city.parent, {})
            data['count'] = data.get('count', 0) + 1
            data.setdefault('cities', []).append((city, city_data))
    
        cercles_by_region = {}
        for cercle, cercle_data in cities_by_cercle.iteritems():
            data = cercles_by_region.setdefault(cercle.parent, {})
            data['count'] = data.get('count', 0) + 1
            data.setdefault('cercles', []).append((cercle, cercle_data))
            
        import pprint
        pprint.pprint(cercles_by_region)

    ctx = locals()

    return render_to_response('who_base/index.html',  ctx,
                              context_instance=RequestContext(request))
