#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _

from rapidsms.contrib.auth.decorators import registration_required

from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.contrib.handlers.helpers import require_args

from report_parts.models import Report

from ..utils import check_against_last_report

#todo: do a customRoleHandler that you can inherit from, that register the 
# role you want

class MenHandler(KeywordHandler):
    u"""
        EXAMPLE SMS FORMAT: men 32 56 76 87 2 5 65 2 
        32: 5-15 years old males given one dose 
        56: 15+ years old males given one dose
        76: 5-15 years old males given two doses
        87: 15+ years old males given two doses 
        2:  5-15 years old males given three doses
        5:  15+ years old males given three doses
        65: 5-15 years old males given four doses
        2:  15+ years old males given four doses
    """

    keyword = "men"
    
    aliases = (('fr', ("hom", "homme", "hommes")), 
               ('en', ("men", "man")),)


    def help(self, keyword, lang_code):
        return self.respond(_(u"To report, send 'MEN', followed by 8 numbers."))


    @registration_required()
    def handle(self, text, keyword, lang_code):
    
        # todo: factorize this
        args = [self.flatten_string(arg) for arg in text.split()]
        require_args(args, min=8, max=8)
        
        #todo: rename the report model in report manager
        report_manager = check_against_last_report(self.msg.contact)
        
        # make update the manager date so 
        report_manager.save()
        
        results = report_manager.results
        
        try:
            args = [int(x) for x in args]
            for x in args: 
                if x < 0:
                    raise ValueError()
        except ValueError:
            return self.respond(_(u"All 8 values must be positive numbers"))

        total_men = sum(args)

        if report_manager.status.wmen\
            and report_manager.status.msc\
            and report_manager.status.wsc:
            tot = total_men + results.total_treated_females +\
                  results.total_untreated_males + results.total_untreated_females             

            if results.target_pop != tot:
                return self.respond(_(u"The sum of all the results for males and"\
                                      u" females (%(total)s) must be equal to "\
                                      u" the target population (%(target_pop)s)") % {
                                      'total': tot, 
                                      'target_pop': results.target_pop})              

        if results.target_pop < total_men:
            return self.respond(_(u"The sum of all the results for all"\
                                  u" males (%(total)s) can not be bigger than"\
                                  u" the target population (%(target_pop)s)") % {
                                  'total': total_men, 
                                  'target_pop': results.target_pop})

        results.one_dose_child_males = args[0]
        results.one_dose_adult_males = args[1]
        results.two_doses_child_males = args[2]
        results.two_doses_adult_males = args[3]
        results.three_doses_child_males = args[4]
        results.three_doses_adult_males = args[5]
        results.four_doses_child_males = args[6]
        results.four_doses_adult_males = args[7]
        
        results.report_manager.status.men = True
        results.report_manager.save()
        results.save()
        
        # todo: prefix successeful messages by 'OK'
        msg = _(u"The results for the campaign %(campaign)s in "\
                   u"%(location)s related to men are saved.") % {
                   'campaign': results.campaign, 'location': results.area}
        
        if report_manager.is_completed():
            msg += _(u" All reports for this location are completed! Receipt: "\
                     u"%(receipt)s") % {'receipt': results.receipt}
        else:
            progress = results.report_manager.progress
            msg += _(u" You have sent %(completed)s over %(to_complete)s "\
                     u"reports for this location.") % {'completed': progress[0],
                                                     'to_complete': progress[1]} 
            
        return self.respond(msg)
        


            
