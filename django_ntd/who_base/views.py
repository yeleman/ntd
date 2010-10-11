#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4

from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum
from django.conf import settings

from .models import Campaign, Results, DrugsStockMovement

from simple_locations.models import Area, AreaType

from .forms import CampaignForm
from utils import rowdata_to_excel, campaign_all_datas


@login_required
def campaigns_results(request):

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

        results = Results\
             .objects\
             .filter(campaign=campaign)\
             .select_related('area__as_data_source__data_collection__parent')\
             .order_by('area__as_data_source__data_collection__parent',
                       'area__as_data_source__data_collection',
                       'area')

        sumup = lambda x: sum(y or 0 for y in x)

        # men totals
        totals = results.aggregate(
               total_pop=Sum('total_pop'),
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
        totals['total_child_males'] = sumup(total_child_males)

        total_adult_males = (totals['total_one_dose_adult_males'],
                             totals['total_two_doses_adult_males'],
                             totals['total_three_doses_adult_males'],
                             totals['total_four_doses_adult_males'])
        totals['total_adult_males'] =  sumup(total_adult_males)

        total_males = (totals['total_child_males'],
                       totals['total_adult_males'])
        totals['total_males'] = sumup(total_males)

        # women totals
        totals.update(results.aggregate(
           total_one_dose_child_females=Sum('one_dose_child_females'),
           total_two_doses_child_females=Sum('two_doses_child_females'),
           total_three_doses_child_females=Sum('three_doses_child_females'),
           total_four_doses_child_females=Sum('four_doses_child_females'),
           total_one_dose_adult_females=Sum('one_dose_adult_females'),
           total_two_doses_adult_females=Sum('two_doses_adult_females'),
           total_three_doses_adult_females=Sum('three_doses_adult_females'),
           total_four_doses_adult_females=Sum('four_doses_adult_females')))

        total_child_females = (totals['total_one_dose_child_females'],
                             totals['total_two_doses_child_females'],
                             totals['total_three_doses_child_females'],
                             totals['total_four_doses_child_females'])
        totals['total_child_females'] = sumup(total_child_females)

        total_adult_females = (totals['total_one_dose_adult_females'],
                             totals['total_two_doses_adult_females'],
                             totals['total_three_doses_adult_females'],
                             totals['total_four_doses_adult_females'])
        totals['total_adult_females'] =  sumup(total_adult_females)

        total_females = (totals['total_child_females'],
                       totals['total_adult_females'])
        totals['total_females'] = sumup(total_females)

        # men special case totals
        totals.update(results.aggregate(
           total_child_males_not_available=Sum('child_males_not_available'),
           total_child_males_refusing=Sum('child_males_refusing'),
           total_child_males_side_effects=Sum('child_males_side_effects'),
           total_adult_males_not_available=Sum('adult_males_not_available'),
           total_adult_males_refusing=Sum('adult_males_refusing'),
           total_adult_males_side_effects=Sum('adult_males_side_effects')))

        total_males_not_available = (totals['total_child_males_not_available'],
                                    totals['total_adult_males_not_available'])
        totals['total_males_not_available'] = sumup(total_males_not_available)

        total_males_refusing = (totals['total_child_males_refusing'],
                                       totals['total_adult_males_refusing'])
        totals['total_males_refusing'] = sumup(total_males_refusing)

        total_males_side_effects = (totals['total_child_males_side_effects'],
                                    totals['total_adult_males_side_effects'])
        totals['total_males_side_effects'] = sumup(total_males_side_effects)

        total_untreated_males = (totals['total_males_not_available'],
                                 totals['total_males_refusing'],
                                 totals['total_males_side_effects'])
        totals['total_untreated_males'] = sumup(total_untreated_males)

        # women special case totals
        totals.update(results.aggregate(
          total_child_females_not_available=Sum('child_females_not_available'),
          total_child_females_refusing=Sum('child_females_refusing'),
          total_child_females_side_effects=Sum('child_females_side_effects'),
          total_pregnant_child_females=Sum('pregnant_child_females'),
          total_adult_females_not_available=Sum('adult_females_not_available'),
          total_adult_females_refusing=Sum('adult_females_refusing'),
          total_adult_females_side_effects=Sum('adult_females_side_effects'),
          total_pregnant_adult_females=Sum('pregnant_adult_females')))

        tot_females_not_available = (
                                   totals['total_child_females_not_available'],
                                   totals['total_adult_females_not_available'])

        totals['total_females_not_available'] = sumup(tot_females_not_available)

        total_females_refusing = (totals['total_child_females_refusing'],
                                       totals['total_adult_females_refusing'])
        totals['total_females_refusing'] = sumup(total_females_refusing)

        tot_females_side_effects = (
                                    totals['total_child_females_side_effects'],
                                    totals['total_adult_females_side_effects'])
        totals['total_females_side_effects'] = sumup(tot_females_side_effects)

        total_pregnant_females = (totals['total_pregnant_child_females'],
                                       totals['total_pregnant_adult_females'])
        totals['total_pregnant_females'] = sumup(total_pregnant_females)

        total_untreated_females = (totals['total_females_not_available'],
                            totals['total_females_refusing'],
                            totals['total_females_side_effects'])
        totals['total_untreated_females'] = sumup(total_untreated_females)

        # stock movements
        totals['stocks'] = DrugsStockMovement.objects\
                                             .filter(for_results__campaign=campaign)\
                                             .values('drug__name')\
                                             .annotate(
                                                total_received=Sum('received'),
                                                total_returned=Sum('returned'))
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

     # todo: use the django view for this
def switch_lang(request):

    # todo: add more checks here
    lang_code = (request.GET.get('lang_code',
                                 settings.LANGUAGE_CODE)).lower().strip()
    if lang_code not in ('en', 'fr'):
        lang_code = settings.LANGUAGE_CODE
    request.session['django_language'] = lang_code

    return redirect('campaigns-results')


@login_required
def codes_campaign(request, pk):

    campaign = Campaign.objects.get(pk=int(pk))
    results = Results.objects.filter(campaign=campaign)
    locations = Area.objects.filter(as_data_source__isnull=False)

    ctx = locals()
    return render_to_response('codes_campaign.html',  ctx,
                              context_instance=RequestContext(request))

@login_required
def xls_campaign(request, pk):

    campaign = Campaign.objects.get(pk=int(pk))

    filename = 'campaign%(id)d-%(date)s.xls' % {'id': campaign.id, \
                                'date': datetime.today().strftime('%Y-%b-%d')}

    data = campaign_all_datas(campaign)
    excel = rowdata_to_excel(data)

    response = HttpResponse(excel, mimetype="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment;filename="%s"' % filename
    return response
