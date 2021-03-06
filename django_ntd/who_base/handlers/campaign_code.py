#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _
from django.utils import translation

from rapidsms.contrib.auth.decorators import registration_required

from rapidsms.contrib.handlers.handlers.callback import CallbackHandler
from rapidsms.contrib.handlers.helpers import require_args, check_exists, check_date

from ..models import DrugsPack, Results, Campaign
from ..utils import check_location, fix_date_year

from vil import VilHandler


class CampaignCodeHandler(CallbackHandler):
    u"""
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
            

            
