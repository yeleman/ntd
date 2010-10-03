#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime
import re

from django.utils.translation import ugettext as _, ugettext_lazy as __
from django.db import models
from django.db.models import Q
from django.db.models import permalink

from simple_locations.models import Area

from code_generator.fields import CodeField

from report_parts.models import Report

class Campaign(models.Model):

    class Meta:
        verbose_name = __('campaign')
        unique_together = (('name', 'start_date'),)
    
    name = models.CharField(max_length=64, verbose_name=__(u'name'))
    code = CodeField(verbose_name=__("code"),  max_length=12, prefix='c')
    start_date = models.DateField(default=datetime.datetime.today,
                                  verbose_name=__(u'start date'))
    end_date = models.DateField(blank=True, null=True, 
                                verbose_name=__(u'end date'))
    drugs_pack = models.ForeignKey('DrugsPack', verbose_name=__(u'drugs pack'),
                                  blank=True, null=True)
    
    def __unicode__(self):
        return _(u'%(name)s (starts on %(date)s)') % {'name': self.name, 
               'date': self.start_date.strftime(_('%m/%d/%Y'))}
    

    @permalink  
    def get_absolute_url(self):
        return ('edit-campaign', (self.pk,))
        
    
    def delete(self, *args, **kwargs):
        for results in self.results_set.all():
            results.delete()
        return models.Model.delete(self, *args, **kwargs)


class Drug(models.Model):

    class Meta:
        verbose_name = __('drug')

    name = models.CharField(max_length=64, verbose_name=__(u'name'),
                            unique=True)
    
    def __unicode__(self):
        return self.name
            
      
class DrugsPack(models.Model):

    class Meta:
        verbose_name = __('drugs pack')
        verbose_name_plural = __('drugs packs')

    name = models.CharField(max_length=64, blank=True, null=True,
                            verbose_name=__(u'name')) 
    code = code = CodeField(verbose_name=__("code"),  max_length=12, prefix='p') 
    drugs = models.ManyToManyField(Drug, related_name='packs', 
                                    verbose_name=__(u'drugs'))
    
    
    def __unicode__(self):
        if self.name:
            return _(u'[%(code)s] %(name)s') % {'name': self.name, 
                                                'code': self.code}
                                                
        drugs = " + ".join((unicode(drug) for drug in self.drugs.all()))
        return u"[%(code)s] %(drugs)s" % {'code': self.code, 'drugs': drugs}
        
        
# TODO: we may want to use the EAV for this eventually
class Results(models.Model):

    class Meta:
        verbose_name = __('results')
        verbose_name_plural = __('results')
        unique_together = (('campaign', 'area'),)

    campaign = models.ForeignKey(Campaign, verbose_name=__(u'campaign'))
    
    area =  models.ForeignKey(Area, related_name='related_results', 
                              verbose_name=__(u'area'),
                              limit_choices_to = ~Q(kind__slug__in=(
                                                           'country', 'region', 
                                                           'district', 'cercle',
                                                            'commune')))
    data_collection_location =  models.ForeignKey(Area, 
                                                  related_name='results_collected_here',
                                                  verbose_name=__(u'data collection location'))
                                                         
    drugs_pack = models.ForeignKey(DrugsPack, verbose_name=__(u'drugs pack'),  
                                  blank=True, null=True)
                                   
    treatment_start_date = models.DateField(verbose_name=__(u'treatment start date'),
                                       blank=True, null=True)
    treatment_end_date = models.DateField(verbose_name=__(u'treatment end date'),
                                       blank=True, null=True)

    total_pop = models.IntegerField(verbose_name=__(u'total population'),
                                    blank=True, null=True)
    target_pop = models.IntegerField(verbose_name=__(u'target population'),
                                    blank=True, null=True)                                   
    treated_under_six = models.IntegerField(verbose_name=__(u'treated under 6 years old'),
                                    blank=True, null=True)  
                                    
    distributor = distributor = models.CharField(max_length=64, 
                                                 verbose_name=__(u'distributor'),
                                                 blank=True, null=True)                                  

    one_dose_child_males = models.IntegerField(verbose_name=__(u'5-15 ans years old males given one dose'),
                                             blank=True, null=True)
    one_dose_adult_males = models.IntegerField(verbose_name=__(u'15+ years old males given one dose'),
                                             blank=True, null=True)
    two_doses_child_males = models.IntegerField(verbose_name=__(u'5-15 ans years old males given two doses'),
                                             blank=True, null=True)
    two_doses_adult_males = models.IntegerField(verbose_name=__(u'15+ years old males given two doses'),
                                             blank=True, null=True)
    three_doses_child_males = models.IntegerField(verbose_name=__(u'5-15 ans years old males given three doses'),
                                             blank=True, null=True)
    three_doses_adult_males = models.IntegerField(verbose_name=__(u'15+ years old males given three doses'),
                                             blank=True, null=True)                                            
    four_doses_child_males = models.IntegerField(verbose_name=__(u'5-15 ans years old males given four doses'),
                                             blank=True, null=True)
    four_doses_adult_males = models.IntegerField(verbose_name=__(u'15+ years old males given four doses'),
                                             blank=True, null=True)        
    
    one_dose_child_females = models.IntegerField(verbose_name=__(u'5-15 ans years old females given one dose'),
                                             blank=True, null=True)
    one_dose_adult_females = models.IntegerField(verbose_name=__(u'15+ years old females given one dose'),
                                             blank=True, null=True)
    two_doses_child_females = models.IntegerField(verbose_name=__(u'5-15 ans years old females given two doses'),
                                             blank=True, null=True)
    two_doses_adult_females = models.IntegerField(verbose_name=__(u'15+ years old females given two doses'),
                                             blank=True, null=True)
    three_doses_child_females = models.IntegerField(verbose_name=__(u'5-15 ans years old females given three doses'),
                                             blank=True, null=True)
    three_doses_adult_females = models.IntegerField(verbose_name=__(u'15+ years old females given three doses'),
                                             blank=True, null=True)                                            
    four_doses_child_females = models.IntegerField(verbose_name=__(u'5-15 ans years old females given four doses'),
                                             blank=True, null=True)
    four_doses_adult_females = models.IntegerField(verbose_name=__(u'15+ years old females given four doses'),
                                             blank=True, null=True)       
    
    report_manager = models.OneToOneField(Report, related_name='results',
                                          editable=False)
    disabled = models.BooleanField(default=False, verbose_name=__(u'disabled'))
    
    
    def __unicode__(self):
        return _(u"Results of campaign %(campaign)s at %(area)s") % {
                  'campaign': self.campaign, 'area': self.area  }

    @property
    def receipt(self):
        if self.completed and self.report_date:
            return _(u"%(campaign)sD%(day)s/%(reportid)s") % \
                     {'campaign': self.campaign.id, \
                      'day': self.report_date.timetuple().tm_yday,
                      'reportid': self.id}
        else:
            return None

    @classmethod
    def by_receipt(cls, receipt):
        campaign_id, day_id, report_id = \
                    re.search('([0-9]+)D([0-9]+)\/([0-9]+)', receipt).groups()
        return cls.objects.get(campaign=Campaign.objects.get(id=campaign_id),
                               id=report_id)
      
      
    def delete(self, *args, **kwargs):
        self.report_manager.delete()
        return models.Model.delete(self, *args, **kwargs)


class LocationHierarchy(models.Model):

    class Meta:
        verbose_name = _('locations hierarchy')
        verbose_name_plural = _('locations hierarchies')

    data_collection = models.ForeignKey(Area, related_name='as_data_collector',
                                        verbose_name=_('data collection location'))
    data_source = models.OneToOneField(Area, related_name='as_data_source',
                                       verbose_name=_('data source location'),
                                       limit_choices_to = ~Q(kind__slug__in=(
                                                           'country', 'region', 
                                                           'district', 'cercle',
                                                            'commune')))
                                                            
    distributor = models.CharField(max_length=64, 
                                   verbose_name=__(u'distributor'))
                                                            
    def __unicode__(self):
        return u"%s < %s" % (self.data_collection, self.data_source)
