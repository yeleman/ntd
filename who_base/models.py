#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime

from django.utils.translation import ugettext as _, ugettext_lazy as __
from django.db import models

from simple_locations.models import Area

from code_generator.fields import CodeField


class Campaign(models.Model):
    
    name = models.CharField(max_length=64, verbose_name=__(u'name'))
    code = CodeField(verbose_name=__("code"),  max_length=12, prefix='c')
    start_date = models.DateField(default=datetime.datetime.today,
                                  verbose_name=__(u'start date'))
    end_date = models.DateField(blank=True, null=True, 
                                verbose_name=__(u'end date'))
    
    def __unicode__(self):
        return _(u'[%(date)s] %(name)s') % {'name': self.name, 
                                           'date': self.start_date}
    

class Drug(models.Model):

    name = models.CharField(max_length=64, verbose_name=__(u'name'),
                            unique=True)
    
    def __unicode__(self):
        return self.name
            
      
class DrugPack(models.Model):

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
        
        
class Result(models.Model):
    campaign = models.ForeignKey(Campaign, verbose_name=__(u'Campaign'))
    area =  models.ForeignKey(Area, verbose_name=__(u'area'))
    pack = models.ForeignKey(DrugPack, verbose_name=__(u'drug pack'))
    distributor = models.CharField(max_length=64, 
                                   verbose_name=__(u'distributor'))
    report_date = models.DateField(default=datetime.datetime.today,
                                  verbose_name=__(u'report date'))
    treatment_date = models.DateField(verbose_name=__(u'treatment date'))
    
    child_males_data = models.IntegerField(verbose_name=__(u'1-4 years old males'))
    teen_males_data = models.IntegerField(verbose_name=__(u'5-14 years old males'))
    adult_males_data = models.IntegerField(verbose_name=__(u'15 years old males'))
    
    child_females_data = models.IntegerField(verbose_name=__(u'1-4 years old females'))
    teen_females_data = models.IntegerField(verbose_name=__(u'5-14 years old females'))
    adult_females_data = models.IntegerField(verbose_name=__(u'15 years old females'))
    
    disabled = models.BooleanField(default=False, verbose_name=__(u'disabled'))
