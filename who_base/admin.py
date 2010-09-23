#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.contrib import admin
from .models import *

admin.site.register(Campaign)
admin.site.register(Drug)  
admin.site.register(DrugPack)
admin.site.register(Result)
