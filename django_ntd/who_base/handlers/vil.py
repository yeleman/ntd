#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _, ugettext_lazy as __

from rapidsms.contrib.auth.decorators import registration_required

from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.contrib.handlers.helpers import require_args, check_exists, check_date

from ..models import DrugsPack, Results, DrugsStockMovement
from ..utils import check_location, fix_date_year

#todo: do a customRoleHandler that you can inherit from, that register the
# role you want

class VilHandler(KeywordHandler):
    u"""
        EXAMPLE SMS FORMAT: vil A78 PA 1009 1009 20 30 45
        A78: location code
        PA: drug package code (optional)
        1009: start treament date (dd/mm)
        1009: end treament date (dd/mm)
        20: total population
        30: target population
        15: treated under 6 years old
    """

    keyword = "vil"

    aliases = (('fr', ("vil", "village", "ville")),
               ('en', ("vil", "village")),)

    ARGUMENTS = __(u"<location code> <drugs package> <start treatment date>"\
                  u" <end treatment date> <total population> "\
                  u"<target population> <treated under 6 months>")


    def help(self, keyword, lang_code):
        return self.respond(_(u"To report, send: VIL ") \
               + unicode(self.__class__.ARGUMENTS))


    # todo: reset other metrics if the report is complete and they try to change the target population
    @registration_required()
    def handle(self, text, keyword, lang_code, campaign=None):

        args = [self.flatten_string(arg) for arg in text.split()]
        count = len(args)
        require_args(args, slices=(1, (6, 8)))

        # todo: check for location type here
        location = check_location(args[0])

        if campaign:
            try:
                result = campaign.results_set.get(area=location, disabled=False)
            except Results.DoesNotExist:
                return self.respond(_(u"The location %(location)s is not part "\
                                       u"of the campaign %(campaign)s.") % {
                                       'location': location,
                                       'campaign': campaign})
        else:

            try:
                result = Results.objects.filter(area=location, disabled=False)\
                                        .filter(campaign__end_date__isnull=True)\
                                        .latest('campaign__start_date')
                campaign = result.campaign
            except Results.DoesNotExist:
                return self.respond(_(u"There are no active campaigns for "\
                                       u"%(location)s right now.") % {
                                       'location': location})
            except Results.MultipleObjectsReturned:
                return self.respond(_(u"There are several active campaigns for "\
                           u"%(location)s right now. Replace 'VIL' by the "\
                           u"campagne code and resend your message.") % {
                           'location': location})

        # update last sent sms
        result.report_manager.status.contact = self.msg.contact.pk
        result.report_manager.save()

        if count == 1:
            return self.respond(_(u"You are now reporting results for the "\
                           u"campaign %(campaign)s in %(location)s.") % {
                           'campaign': campaign, 'location': location })

        if count == 6:
            if not result.drugs_pack:
                return self.respond(_(u"You must provide a drug package with these "\
                               u"results. It should be the second value alfter 'VIL'."))
            args.insert(1, result.drugs_pack.code)
        else:
            result.drugs_pack = check_exists(args[1], DrugsPack)

        result.treatment_start_date = fix_date_year(check_date(args[2],
                                                                _("%d%m"),
                                                                ('-', '/')))
        result.treatment_end_date = fix_date_year(check_date(args[3],
                                                             _("%d%m"),
                                                             ('-', '/')))

        if result.treatment_start_date > result.treatment_end_date:
            return self.respond(_(u"Start treatment date (%(start)s) "\
                                  u"can not be after end treatment date "\
                                  u"(%(end)s).") % {
                                  'start': result.treatment_start_date.strftime(_('%m/%d/%Y')),
                                  'end': result.treatment_end_date.strftime(_('%m/%d/%Y'))})

        try:
            data = [int(x) for x in args[4:]]
            for x in data: 
                if x < 0:
                    raise ValueError()
        except ValueError:
            return self.respond(_(u"The last 3 values must be 3 positive numbers"))


        if data[2] + data[1] > data[0]:
            return self.respond(_(u"The sum of patients under six months and "\
                                  u"the target population %(sum)s can not be greater "\
                                  u"than the population value (%(total_pop)s).") % {
                               'sum': data[2] + data[1],
                               'total_pop': data[0]})

        result.total_pop = data[0]
        result.target_pop = data[1]
        result.treated_under_six = data[2]

        result.distributor = location.as_data_source.distributor

        result.report_manager.status.vil = True
        result.report_manager.save()
        result.save()

        # todo: move that in form creation
        # creating the empty drug stock movement
        if not result.stock_movements.exists():
            for drug in result.drugs_pack.drugs.all():
                DrugsStockMovement.objects.create(drug=drug, for_results=result)

        # todo: maybe this is too long...
        self.respond(_(u"The results for the campaign %(campaign)s in "\
                       u"%(location)s are saved. From %(start)s, to %(end)s "\
                       u"targetting %(target_pop)s/%(total_pop)s people and "\
                       u"%(under_six_pop)s under six months.") % {'total_pop': data[0],
                       'under_six_pop': data[2], 'target_pop': data[1],
                       'campaign': campaign,
                       'start': result.treatment_start_date.strftime(_('%m/%d/%Y')),
                       'end': result.treatment_end_date.strftime(_('%m/%d/%Y')),
                       'location': location})


