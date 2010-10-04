#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _

from auth.decorators import registration_required

from handlers_i18n.handlers.keyword import KeywordHandler
from handlers_i18n.helpers import require_args

from report_parts.models import Report

from ..utils import check_against_last_report

#todo: do a customRoleHandler that you can inherit from, that register the 
# role you want

class WmenHandler(KeywordHandler):
    u"""


        EXAMPLE SMS FORMAT: wmen 32 56 76 87 2 5 65 2 
        32: 5-15 years old females given one dose 
        56: 15+ years old females given one dose
        76: 5-15 years old females given two doses
        87: 15+ years old females given two doses 
        2:  5-15 years old females given three doses
        5:  15+ years old females given three doses
        65: 5-15 years old females given four doses
        2:  15+ years old females given four doses
    """

    keyword = "wmen"
    
    aliases = (('fr', ("fem", "femme", "femmes")), 
               ('en', ("wmen", "wman")),)
    
    def help(self, keyword, lang_code):
        return self.respond(_(u"To report, send 'WMEN', followed by 8 numbers."))


    @registration_required()
    def handle(self, text, keyword, lang_code):
    
        # todo: factorize this
        args = [self.flatten_string(arg) for arg in text.split()]
        require_args(args, min=8, max=8)
        
        #todo: rename the report model in report manager
        report_manager = check_against_last_report(self.msg.contact)
        
        # make update the manager date so 
        report_manager.save()
        
        report_was_completed = report_manager.is_completed()
        
        results = report_manager.results
        
        try:
            args = [int(x) for x in args]
        except ValueError:
            return self.respond(_(u"All 8 values must be numbers"))

        total_wmen = sum(args)

        if report_manager.status.men\
            and report_manager.status.msc\
            and report_manager.status.wsc:
            tot = total_wmen + results.total_untreated_females \
                  + results.total_treated_males + results.total_untreated_males             

            if results.target_pop != tot:
                return self.respond(_(u"The sum of all the results for males and"\
                                      u" females (%(total)s) must be equal to "\
                                      u" the target population (%(target_pop)s)") % {
                                      'total': tot, 
                                      'target_pop': results.target_pop})              

        if results.target_pop < total_wmen:
            return self.respond(_(u"The sum of all the results for all"\
                                  u" females (%(total)s) can not be bigger than"\
                                  u" the target population (%(target_pop)s)") % {
                                  'total': total_wmen, 
                                  'target_pop': results.target_pop})

        results.one_dose_child_females = args[0]
        results.one_dose_adult_females = args[1]
        results.two_doses_child_females = args[2]
        results.two_doses_adult_females = args[3]
        results.three_doses_child_females = args[4]
        results.three_doses_adult_females = args[5]
        results.four_doses_child_females = args[6]
        results.four_doses_adult_females = args[7]
        
        results.report_manager.status.wmen = True
        results.report_manager.save()
        results.save()
        
        # todo: prefix successeful messages by 'OK'
        msg = _(u"The results for the campaign %(campaign)s in "\
                   u"%(location)s related to women are saved.") % {
                   'campaign': results.campaign, 'location': results.area}
        
        if not report_was_completed and report_manager.is_completed():
            msg += _(u" All reports for this location are completed!") 
        else:
            progress = results.report_manager.progress
            msg += _(u" You have sent %(completed)s over %(to_complete)s "\
                     u"reports for this location.") % {'completed': progress[0],
                                                     'to_complete': progress[1]} 
            
        return self.respond(msg)
        


            
