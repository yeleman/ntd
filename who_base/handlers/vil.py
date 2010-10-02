#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _

from auth.decorators import registration_required

from handlers_i18n.handlers.keyword import KeywordHandler
from handlers_i18n.helpers import require_args, check_exists, check_date

from ..models import DrugsPack, Results
from ..utils import check_location, fix_date_year

#todo: do a customRoleHandler that you can inherit from, that register the 
# role you want

class VilHandler(KeywordHandler):
    u"""
    
    Given this workflow:
        
        1. Campaign is created.
        2. Campaign Manager distributes reporting codes to CSCOM: cscom code + areas codes.
        3. Field agents receives drug from drug stores
        4. Field agents distribute drugs and fills report
        5. CSCOM collects (or agents bring to) forms.
        6. CSCOM sends SMS report.
        7. System sends back report-receipt.

    Allow stage 6:    

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
    
    ARGUMENTS = _(u"<location code> <drugs package> <start treatment date>"\
                  u" <end treatment date> <total population> "\
                  u"<target population> <treated under 6>")


    def help(self, keyword, lang_code):
        return self.respond(_(u"To report, send: VIL ") + self.__class__.ARGUMENTS)


    @registration_required()
    def handle(self, text, keyword, lang_code):
    
        args = [self.flatten_string(arg) for arg in text.split()]
        count = len(args)
        require_args(args, slices=(1, (6, 8)))
        
        # todo: check for location type here
        location = check_location(args[0])
        
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
        result.report_manager.status.contact = self.msg.contact
        result.report_manager.save()
        
        if count == 1:
            return self.respond(_(u"You are now reporting results for the "\
                           u"campaign %(campaign)s in %(location)s.") % {
                           'campaign': campaign, 'location': location })
        
        if count == 6:
            if not result.drugs_pack:
                return self.respond(_(u"You must provide a drug package with these "\
                               u"results. It should be the second value alfter 'VIL'."))
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
        except ValueError:
            return self.respond(_(u"The last 3 values must be 3 numbers"))

        if data[1] > data[0]:
            return self.respond(_(u"Target population value (%(target_pop)s) "\
                                  u"can not be bigger than the total "\
                                  u"population value (%(total_pop)s).") % {
                                  'target_pop': data[1], 'total_pop': data[0]})

        if data[2] > data[1]:
            return self.respond(_(u"Patients under six value (%(under_six_pop)s) "\
                                  u"can not be bigger than the target "\
                                  u"population value (%(target_pop)s).") % {
                               'under_six_pop': data[2], 'target_pop': data[1]})

        result.total_pop = data[0]
        result.target_pop = data[1]                                   
        result.treated_under_six = data[2]  
        
        result.report_manager.status.vil = True
        result.report_manager.save()
        result.save()
        
        # todo: maybe this is too long...
        self.respond(_(u"The results for the campaign %(campaign)s in "\
                       u"%(location)s are saved. From %(start)s, to %(end)s "\
                       u"targetting %(target_pop)s/%(total_pop)s people with "\
                       u"%(under_six_pop)s under six.") % {'total_pop': data[0],
                       'under_six_pop': data[2], 'target_pop': data[1], 
                       'campaign': campaign, 
                       'start': result.treatment_start_date.strftime(_('%m/%d/%Y')),
                       'end': result.treatment_end_date.strftime(_('%m/%d/%Y')), 
                       'location': location})

            
