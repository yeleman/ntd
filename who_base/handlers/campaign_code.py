#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _
from django.utils import translation

from auth.decorators import registration_required

from handlers_i18n.handlers.callback import CallbackHandler
from handlers_i18n.helpers import require_args, check_exists, check_date

from ..models import DrugsPack, Results, Campaign
from ..utils import check_location, fix_date_year

from vil import VilHandler


class CampaignCodeHandler(CallbackHandler):
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

        EXAMPLE SMS FORMAT: c001 A78 PA 1009 1009 20 30 45 
        c001: campaign code
        A78: location code
        PA: drug package code (optional)
        1009: start treament date (dd/mm)
        1009: end treament date (dd/mm)
        20: total population
        30: target population
        15: treated under 6 years old 
    """

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
                 raise ExitHandle(_(u"No running campaign matching the code: "\
                                    u"'%(code)s'") % {'code': code})
        
            return False
        else:
            if campaign.end_date:
                raise ExitHandle(_(u"The campaign %(campaign)s is over.") % {
                                   'campaign': campaign})
            return campaign, ' '.join(text).strip()


    @registration_required()
    def handle(self, match):
        campaign, text = match
    
        if match:
            handler = VilHandler(self.router, self.msg)
            lang_code = self.msg.contact.language or translation.get_language()
            return handler.handle(text, 'vil', lang_code, campaign)
            

            
