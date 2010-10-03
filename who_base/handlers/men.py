#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _

from auth.decorators import registration_required

from handlers_i18n.handlers.keyword import KeywordHandler
from handlers_i18n.helpers import require_args

from report_parts.models import Report


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
    
    ARGUMENTS = _(u"<location code> <drugs package> <start treatment date>"\
                  u" <end treatment date> <total population> "\
                  u"<target population> <treated under 6>")


    def help(self, keyword, lang_code):
        return self.respond(_(u"To report, send: VIL ") + self.__class__.ARGUMENTS)


    @registration_required()
    def handle(self, text, keyword, lang_code):
    
        # todo: factorize this
        args = [self.flatten_string(arg) for arg in text.split()]
        require_args(args, min=8, max=8)
        
        #todo: rename the report model in report manager
        contact = self.msg.contact
        
        try:
            report_manager = Report.objects.filter(status__contact=contact.pk)\
                                           .latest('updated')
        except Report.DoesNotExist:
            is_outdated = True
        else:
            is_outdated = report_manager.is_outdated()
        
        if is_outdated:
            return self.respond(_(u"You must specify the campaign and location you "\
                           u"are reporting for. Send 'VIL' first."))
                           
        if not report_manager.status.vil:
            return self.respond(_(u"You must specify the population of the location "\
                           u"your are reporting for. Send a complete "\
                           u"population report with 'VIL' first."))
        
        # make update the manager date so 
        report_manager.save()
        
        report_was_completed = report_manager.is_completed()
        
        results = report_manager.results
        
        try:
            args = [int(x) for x in args]
        except ValueError:
            return self.respond(_(u"All 8 values must be numbers"))

        total = sum((results.one_dose_child_females or 0,
                    results.one_dose_adult_females or 0,
                    results.two_doses_child_females or 0,
                    results.two_doses_adult_females or 0,
                    results.three_doses_child_females or 0,
                    results.three_doses_adult_females or 0,
                    results.four_doses_child_females or 0,
                    results.four_doses_adult_females or 0 )) + sum(args)

        if results.target_pop < total:
            return self.respond(_(u"The sum of all the results for females and"\
                                  u" males (%(total)s) can not be bigger than"\
                                  u" the target population (%(target_pop)s)") % {
                                  'total': total, 'target_pop': results.target_pop})

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
        
        if not report_was_completed and report_manager.is_completed():
            msg += _(u" All reports for this location are completed!") 
        else:
            progress = results.report_manager.progress
            msg += _(u" You have sent %(completed)s over %(to_complete)s "\
                     u"reports for this location.") % {'completed': progress[0],
                                                     'to_complete': progress[1]} 
            
        return self.respond(msg)
        


            
