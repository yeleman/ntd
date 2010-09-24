#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4

import csv

from itertools import groupby
from operator import attrgetter

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

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
            
    if request.GET.get('format', None) == 'csv':

        response = HttpResponse(mimetype='text/csv')
        name = slugify(unicode(campaign))
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % name

        class CustomCSV(csv.excel):
            delimiter = ";"

        csv.register_dialect("CustomCSV", CustomCSV)

        writer = csv.writer(response, CustomCSV)
        
        convert_to_unicode = lambda l: [unicode(x if x is not None else '').encode('utf8') for x in l]
        
        writer.writerow(convert_to_unicode([_(u'Region'), _(u'Cercle'),
                         _(u'City'), _(u'Village'),
                        _(u'Drugs'), _(u'Distributor'), _(u'Treated on'), 
                        _(u'Reported on'),
                        _(u'1-4 years old males'), _(u'5-14 years old males'),
                         _(u'15+ years old males'),
                        _(u'1-4 years old females'), _(u'5-14 years old females'),
                         _(u'15+ years old females')]))
         
        for result in Results.objects.filter(campaign=campaign)\
                                     .order_by('area__parent__parent__parent__name', 
                                               'area__parent__parent__name',
                                               'area__parent__name'):
            writer.writerow(convert_to_unicode(
                             [result.area.parent.parent.parent.name, 
                             result.area.parent.parent.name, 
                             result.area.parent.name, 
                             result.area.name,
                             ', '.join(d.name for d in result.pack.drugs.all()),
                             result.distributor,
                             result.area.name, 
                             result.treatment_date,
                             result.report_date,
                             result.child_males_data,
                             result.teen_males_data,
                             result.adult_males_data,
                             result.child_females_data,
                             result.teen_females_data,
                             result.adult_females_data,]))

        return response


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
            
    ctx = locals()

    return render_to_response('who_base/index.html',  ctx,
                              context_instance=RequestContext(request))
