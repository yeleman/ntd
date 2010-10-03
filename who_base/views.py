#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4


from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.conf import settings

from .models import Campaign, Results

from simple_locations.models import Area

from .forms import CampaignForm


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
        
        results = Results.objects\
                         .filter(campaign=campaign)\
                         .select_related('area__as_data_source__data_collection__parent')\
                         .order_by('area__as_data_source__data_collection__parent',
                                   'area__as_data_source__data_collection',
                                   'area')
        
        totals = results.aggregate(total_pop=Sum('total_pop'), 
                                   target_pop=Sum('target_pop'), 
                                   total_one_dose_child_males=Sum('one_dose_child_males'),
                                   total_two_doses_child_males=Sum('two_doses_child_males'),
                                   total_three_doses_child_males=Sum('three_doses_child_males'),
                                   total_four_doses_child_males=Sum('four_doses_child_males'),
                                   total_one_dose_adult_males=Sum('one_dose_adult_males'),
                                   total_two_doses_adult_males=Sum('two_doses_adult_males'),
                                   total_three_doses_adult_males=Sum('three_doses_adult_males'),
                                   total_four_doses_adult_males=Sum('four_doses_adult_males'),
                                   treated_under_six=Sum('treated_under_six'))
                  
        total_child_males = (totals['total_one_dose_child_males'],
                             totals['total_two_doses_child_males'],
                             totals['total_three_doses_child_males'],
                             totals['total_four_doses_child_males'])
        total_child_males = (x or 0 for x in total_child_males)
        totals['total_child_males'] = sum(total_child_males)
                      
        total_adult_males = (totals['total_one_dose_adult_males'],
                             totals['total_two_doses_adult_males'],
                             totals['total_three_doses_adult_males'],
                             totals['total_four_doses_adult_males']) 
        total_adult_males = (x or 0 for x in total_adult_males)          
        totals['total_adult_males'] =  sum(total_adult_males)
                                                
        total_males = (totals['total_child_males'],
                       totals['total_adult_males'])                                  
        total_males = (x or 0 for x in total_males)   
        totals['total_males'] = sum(total_males) 
            
        totals.update(results.aggregate(total_pop=Sum('total_pop'), 
                       target_pop=Sum('target_pop'), 
                       total_one_dose_child_females=Sum('one_dose_child_females'),
                       total_two_doses_child_females=Sum('two_doses_child_females'),
                       total_three_doses_child_females=Sum('three_doses_child_females'),
                       total_four_doses_child_females=Sum('four_doses_child_females'),
                       total_one_dose_adult_females=Sum('one_dose_adult_females'),
                       total_two_doses_adult_females=Sum('two_doses_adult_females'),
                       total_three_doses_adult_females=Sum('three_doses_adult_females'),
                       total_four_doses_adult_females=Sum('four_doses_adult_females'),
                       treated_under_six=Sum('treated_under_six')))
                  
        total_child_females = (totals['total_one_dose_child_females'],
                             totals['total_two_doses_child_females'],
                             totals['total_three_doses_child_females'],
                             totals['total_four_doses_child_females'])
        total_child_females = (x or 0 for x in total_child_females)
        totals['total_child_females'] = sum(total_child_females)
                      
        total_adult_females = (totals['total_one_dose_adult_females'],
                             totals['total_two_doses_adult_females'],
                             totals['total_three_doses_adult_females'],
                             totals['total_four_doses_adult_females']) 
        total_adult_females = (x or 0 for x in total_adult_females)          
        totals['total_adult_females'] =  sum(total_adult_females)
                                                
        total_females = (totals['total_child_females'],
                       totals['total_adult_females'])                                  
        total_females = (x or 0 for x in total_females)   
        totals['total_females'] = sum(total_females) 
                                   
    ctx = locals()

    return render_to_response('who_dashboard.html',  ctx,
                              context_instance=RequestContext(request)) 
 
 
            
@login_required                          
def edit_campaign(request, pk):

    # todo: add more checks here
    campaign = Campaign.objects.get(pk=int(pk))
    results = Results.objects.filter(campaign=campaign)
    locations = Area.objects.filter(as_data_source__isnull=False)
    
    if request.method == 'POST':
        campaign_form = CampaignForm(request.POST, instance=campaign)
        if campaign_form.is_valid():
           campaign_form.save() 
           return redirect(campaign.get_absolute_url())
    else:
        campaign_form = CampaignForm(instance=campaign)

    ctx = locals()
    return render_to_response('edit_campaign.html',  ctx,
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
                              
  
@login_required                          
def delete_campaign(request, pk):

    # todo: add more checks here
    campaign = Campaign.objects.get(pk=int(pk))
    
    if request.GET.get('confirm'):
        campaign.delete()
        return redirect('campaigns-list')

    ctx = locals()
    return render_to_response('delete_campaign.html',  ctx,
                              context_instance=RequestContext(request))

                              
def switch_lang(request):

    # todo: add more checks here
    lang_code = (request.GET.get('lang_code',  
                                 settings.LANGUAGE_CODE)).lower().strip()
    if lang_code not in ('en', 'fr'):
        lang_code = settings.LANGUAGE_CODE
    request.session['django_language'] = lang_code
    
    return redirect('who-dashboard')
