#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from distutils.core import setup
import django_ntd

setup(
    name='django-ntd',
    version=django_ntd.__version__,
    license = 'GNU Lesser General Public License (LGPL), Version 3',

    requires = ['python (>= 2.5)', 'django (>= 1.2)'],
    provides = ['django_ntd'],

    description='Management software for neglicted tropical diseases.',
    long_description=open('README.rst').read(),

    url='http://github.com/yeleman/ntd',

    packages=['django_ntd',
              'django_ntd.formats',
              'django_ntd.formats.fr',
              'django_ntd.who_base',
              'django_ntd.who_base.locale',
              'django_ntd.who_base.locale.fr',
              'django_ntd.who_base.handlers'],


    classifiers  = [
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
            'Programming Language :: Python',
            'Topic :: Database',
            'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
