#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
    Various helpers and shortcuts
"""

import string
import datetime

from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from handlers_i18n.exceptions import ExitHandle

from simple_locations.models import Area

def check_location(location_code, location_type=None):
    """
        Exit the handle if the location does not exists.
        
        If it does, returns it.
    """
    
    try:
        location = Area.objects.get(code__iexact=location_code)
    except Area.DoesNotExist:
    
        raise ExitHandle(_(u"The code %(code)s doesn't match any known "\
                           u"location. Ask your administrator the right code "\
                           u"for your location") % {'code': location_code})
    else:
        if location_type and location.type.slug != slugify(location_type):
            current_type = location.type.name
            expected_type = AreaType.objects.get(slug=slugify(location_type)).name
            raise ExitHandle(_(u"You can only do this with a %(expected_type)s"\
                               u" but %(location)s is a %(current_type)s.") % {
                               'expected_type': _(expected_type),
                               'location': location,
                               'current_type': _(current_type)})
                               
    return location                        


    
def fix_date_year(date):
    """
        If the date if not provided with the year, get the closest year.
        Makes sure the date is in the past.
    """
    
    if date.year == 1900:
        now = datetime.datetime.today()
        date = datetime.datetime(now.year, date.month, date.day)
        
        if date > now:
            date = datetime.datetime(now.year - 1, date.month, date.day)
        
    return date           
