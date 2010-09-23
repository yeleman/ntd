#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _

from auth.decorators import role_required

from handlers_i18n.handlers.callback import CallbackHandler
from handlers_i18n.exceptions import ExitHandle

from ..models import DrugsPack, Results, Campaign
from ..utils import check_location, check_exists, check_date, fix_date_year

#todo: do a customRoleHandler that you can inherit from, that register the 
# role you want

class NtdWithCampaignHandler(CallbackHandler):
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

        EXAMPLE SMS FORMAT: c001 A78 PA 1009 20 30 45 18 22 40
        c001: campaign code
        A78: location code
        PA: drug package code
        1009: date: September 10th
        20 30 45: Male data
        18 22 40: Female data
    
    """
    
    ARGUMENTS = _(u"<location code> <drugs package> <treatement delivery date>"\
                  u" <male data X3> <females data X 3>")

    @classmethod
    def match(cls, msg):
        """
            Check if the first keyword is a campaign
        """
        try:
            text = msg.text.split()
            code = text.pop(0).strip().lower()
            campaign = Campaign.objects.get(code=code)
        except (IndexError, Campaign.DoesNotExist):
            if code != 'ntd' and len(text) == 9:
                 raise ExitHandle(_(u"No running matching the code: "\
                                    u"'%(code)s'") % {'code': code})
        
            return False
        else:
            if campaign.end_date:
                raise ExitHandle(_(u"The campaign %(campaign)s is over.") % {
                                   'campaign': campaign})
            return campaign, ' '.join(text).strip()


    #todo: refactor handle
    @role_required('cscom')
    def handle(self, match):
        campaign, text = match
    
        args = [arg.strip().lower() for arg in text.split()]
        
        # todo: check for location type here
        
        try:
            location = check_location(args[0])
            
            try:
                result = campaign.results_set\
                                 .filter(area=location, disabled=False)\
                                 .filter(campaign__end_date__isnull=True)\
                                 .latest('campaign__start_date')
                                 
            except Results.DoesNotExist:
                return self.respond(_(u"The campaign %(campaign)s does not "\
                                       u"include %(location)s right now.") % {
                                       'campaign': campaign,
                                       'location': location})
            
            drugs_package = check_exists(args[1], DrugsPack)
            
            date = check_date(args[2], _("%d%m"), ('-', '/'))
            
            try:
                data = [int(x) for x in args[3:9]]
            except ValueError:
                self.respond(_(u"The last 6 values must be 3 numbers for male"\
                               " statistics, and 3 numbers for females statistics."))
        except IndexError:
            self.respond(_(u"This commands is expecting a keyword and 9 "\
                           u"values: ") + self.cls.ARGUMENTS)
         
        result.pack = drugs_package
        result.report_date = datetime.datetime.now()
        result.treatment_date = fix_date_year(date)
        # todo: make the registration for them
        # and link to them
        result.distributor = 'John Doe'
        
        result.child_males_data = data[0]
        result.teen_males_data = data[1]
        result.adult_males_data = data[2]
        result.child_females_data = data[3]
        result.teen_females_data = data[4]
        result.adult_females_data = data[5]
        
        if result.completed:
            self.respond(_(u"The %(results)s have been updated. Receipt is "\
                           u"still %(receipt)s") % {'results': result,
                                                    'receipt': result.receipt })
        else:
            self.respond(_(u"The %(results)s have been saved. Receipt is"\
                           u" %(receipt)s") % {'results': result,
                                               'receipt': result.receipt })
            result.completed = True
        
        result.save()
        
        # close the campaign
        if not result.campaign.results_set.filter(completed=False).exists():
            result.campaign.end_date = datetime.datetime.now()
            result.campaign.save()
            
