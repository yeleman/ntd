#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django import forms

from .models import Campaign
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from simple_locations.models import Area

from report_parts.models import Report, ReportType

from .models import Results

class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        
        
    def clean(self, *args, **kwargs):
    
        if 'locations' not in self.data:
            raise ValidationError(_(u'You must select at least one location'))
        return forms.ModelForm.clean(self, *args, **kwargs)
            
            
    def save(self, *args, **kwargs):
        
        campaign = forms.ModelForm.save(self, *args, **kwargs)
    
        # todo : make add a slug to report type
        rt = ReportType.objects.get(name='NTD Mali')
        report_mgr = Report.objects.create(type=rt)
    
        # todo: put more validation here
        for location in self.data.getlist('locations'):
            area = Area.objects.get(pk=location)
            result = Results.objects.create(campaign=campaign,
                                           area=area,
                                           data_collection_location=area.as_data_source.data_collection,
                                           drug_pack=self.cleaned_data['drug_pack'],
                                           report_manager=report_mgr)
    
        return campaign
       
