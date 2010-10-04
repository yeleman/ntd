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

class WscHandler(KeywordHandler):
    u"""
        EXAMPLE SMS FORMAT: spm 32 56 76 87 2 5 
        32: 5-15 years old males not available
        56: 15+ years old males not available
        76: 5-15 years old malesr refusing treatment
        87: 15+ years old males refusing treatment
        2:  5-15 years old males having side effects
        5:  15+ years old males having side effects
    """

    keyword = "wsc"
    
    aliases = (('fr', ("cpf",)), 
               ('en', ("wsc",)),)


    def help(self, keyword, lang_code):
        return self.respond(_(u"To report, send 'WSC', followed by 6 numbers."))


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

        total_wsc = sum(args)

        if report_manager.status.wmen\
            and report_manager.status.men\
            and report_manager.status.msc:
            tot = total_wsc + results.total_treated_females +\
                  results.total_treated_males + results.total_untreated_males             

            if results.target_pop != tot:
                return self.respond(_(u"The sum of all the results for males and"\
                                      u" females (%(total)s) must be equal to "\
                                      u" the target population (%(target_pop)s)") % {
                                      'total': tot, 
                                      'target_pop': results.target_pop})      

        if results.target_pop < total_wsc:
            return self.respond(_(u"The sum of all the results for females special"\
                                  u" cases (%(total)s) can not be bigger than"\
                                  u" the target population (%(target_pop)s)") % {
                                  'total': total_wsc, 
                                  'target_pop': results.target_pop})

        results.child_females_not_available = args[0]
        results.adult_females_not_available = args[1]
        results.child_females_refusing = args[2]
        results.adult_females_refusing = args[3]
        results.child_females_side_effects = args[4]
        results.adult_females_side_effects = args[5]
        results.pregnant_child_females = args[6]
        results.pregnant_adult_females = args[7]
        
        results.report_manager.status.wsc = True
        results.report_manager.save()
        results.save()
        
        # todo: prefix successeful messages by 'OK'
        msg = _(u"The results for the campaign %(campaign)s in "\
                   u"%(location)s related to females special cases are saved.") % {
                   'campaign': results.campaign, 'location': results.area}
        
        # refactor this
        if not report_was_completed and report_manager.is_completed():
            msg += _(u" All reports for this location are completed!") 
        else:
            progress = results.report_manager.progress
            msg += _(u" You have sent %(completed)s over %(to_complete)s "\
                     u"reports for this location.") % {'completed': progress[0],
                                                     'to_complete': progress[1]} 
            
        return self.respond(msg)
        


            
