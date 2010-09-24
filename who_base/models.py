#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime
import re

from django.utils.translation import ugettext as _, ugettext_lazy as __
from django.db import models
from django.db.models import Q

from simple_locations.models import Area

from code_generator.fields import CodeField


class Campaign(models.Model):

    class Meta:
        verbose_name = __('campaign')
    
    name = models.CharField(max_length=64, verbose_name=__(u'name'))
    code = CodeField(verbose_name=__("code"),  max_length=12, prefix='c')
    start_date = models.DateField(default=datetime.datetime.today,
                                  verbose_name=__(u'start date'))
    end_date = models.DateField(blank=True, null=True, 
                                verbose_name=__(u'end date'))
    
    def __unicode__(self):
        return _(u'%(name)s (started on %(date)s)') % {'name': self.name, 
               'date': self.start_date.strftime(_('%m/%d/%Y'))}
    

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
        
        
class Results(models.Model):

    class Meta:
        verbose_name = __('results')
        verbose_name_plural = __('results')
        unique_together = (('campaign', 'area'),)

    campaign = models.ForeignKey(Campaign, verbose_name=__(u'campaign'))
    area =  models.ForeignKey(Area, verbose_name=__(u'area'),
                              limit_choices_to = ~Q(kind__slug__in= \
                                    ('country', 'region', 'district', \
                                     'cercle', 'commune')))
    
    pack = models.ForeignKey(DrugsPack, verbose_name=__(u'drugs pack'),  
                             blank=True, null=True)
    distributor = models.CharField(max_length=64,  blank=True, null=True,
                                   verbose_name=__(u'distributor'))
    report_date = models.DateField(verbose_name=__(u'report date'),
                                     blank=True, null=True)
    treatment_date = models.DateField(verbose_name=__(u'treatment date'),
                                       blank=True, null=True)
    
    child_males_data = models.IntegerField(verbose_name=__(u'1-4 years old males'),
                                             blank=True, null=True)
    teen_males_data = models.IntegerField(verbose_name=__(u'5-14 years old males'),
                                             blank=True, null=True)
    adult_males_data = models.IntegerField(verbose_name=__(u'15+ years old males'),
                                             blank=True, null=True)
    
    child_females_data = models.IntegerField(verbose_name=__(u'1-4 years old females'),
                                             blank=True, null=True)
    teen_females_data = models.IntegerField(verbose_name=__(u'5-14 years old females'),
                                             blank=True, null=True)
    adult_females_data = models.IntegerField(verbose_name=__(u'15+ years old females'),
                                             blank=True, null=True)
    
    completed = models.BooleanField(default=False, verbose_name=__(u'completed'))
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
