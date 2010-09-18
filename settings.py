#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


# -------------------------------------------------------------------- #
#                          MAIN CONFIGURATION                          #
# -------------------------------------------------------------------- #


LANGUAGE_CODE = 'fr'

# you should configure your database here before doing any real work.
# see: http://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {

}


# the rapidsms backend configuration is designed to resemble django's
# database configuration, as a nested dict of (name, configuration).
#
# the ENGINE option specifies the module of the backend; the most common
# backend types (for a GSM modem or an SMPP server) are bundled with
# rapidsms, but you may choose to write your own.
#
# all other options are passed to the Backend when it is instantiated,
# to configure it. see the documentation in those modules for a list of
# the valid options for each.
INSTALLED_BACKENDS = {

}


# to help you get started quickly, many django/rapidsms apps are enabled
# by default. you may wish to remove some and/or add your own.
INSTALLED_APPS = [

     "south",
    # the essentials.
    "django_nose",
    "djtables",
    "rapidsms",
    
    # not mandatory but handy, you may grab it from 
    # http://github.com/adammck/djappsettings
    # "djappsettings", 
    # overwise, you'll have to copy app settings.py vars into this file

    # common dependencies (which don't clutter up the ui).
    "rapidsms.contrib.handlers",
    "rapidsms.contrib.ajax",

    # enable the django admin using a little shim app (which includes
    # the required urlpatterns), and a bunch of undocumented apps that
    # the AdminSite seems to explode without.
    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "rapidsms.contrib.djangoadmin",

    # the rapidsms contrib apps.
    "rapidsms.contrib.default",
    "rapidsms.contrib.export",
    "rapidsms.contrib.httptester",
    "rapidsms.contrib.locations",
    "rapidsms.contrib.messaging",
    "rapidsms.contrib.scheduler",
    "handlers_i18n",
    "direct_sms",
    "logger_ng",
    "healthmodels",
    "simple_locations",
    "register_ng",
    "django_simple_config",
    "who_base",
    'code_generator',
    "rapidsms_roles",
   
]


# this rapidsms-specific setting defines which views are linked by the
# tabbed navigation. when adding an app to INSTALLED_APPS, you may wish
# to add it here, also, to expose it in the rapidsms ui.
RAPIDSMS_TABS = [

    ("who_base.views.dashboard", "Acceuil"),
    ("logger_ng.views.index", "Journal des messages"),
    ("register_ng.views.registration", "Inscription"),
    ("rapidsms.contrib.messaging.views.messaging", "Envoyer des messages"),
    ("rapidsms.contrib.locations.views.locations", "Carte"),
    ("rapidsms.contrib.httptester.views.generate_identity", "Testeur de SMS"),
]


# -------------------------------------------------------------------- #
#                         BORING CONFIGURATION                         #
# -------------------------------------------------------------------- #


# debug mode is turned on as default, since rapidsms is under heavy
# development at the moment, and full stack traces are very useful
# when reporting bugs. don't forget to turn this off in production.
DEBUG = TEMPLATE_DEBUG = False


# use django-nose to run tests. rapidsms contains lots of packages and
# modules which django does not find automatically, and importing them
# all manually is tiresome and error-prone.
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"


# this is required for the django.contrib.sites tests to run, but also
# not included in global_settings.py, and is almost always ``1``.
# see: http://docs.djangoproject.com/en/dev/ref/contrib/sites/
SITE_ID = 1


# the default log settings are very noisy.
LOG_LEVEL   = "DEBUG"
LOG_FILE    = "/var/log/rapidsms/rapidsms.log"
LOG_FORMAT  = "[%(name)s]: %(message)s"
LOG_SIZE    = 8192 # 8192 bytes = 64 kb
LOG_BACKUPS = 256 # number of logs to keep


# these weird dependencies should be handled by their respective apps,
# but they're not, so here they are. most of them are for django admin.
TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request"
]

# -------------------------------------------------------------------- #
#                           HERE BE DRAGONS!                           #
#        these settings are pure hackery, and will go away soon        #
# -------------------------------------------------------------------- #


# these apps should not be started by rapidsms in your tests, however,
# the models and bootstrap will still be available through django.
TEST_EXCLUDED_APPS = [
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rapidsms",
    "rapidsms.contrib.ajax",
    "rapidsms.contrib.httptester",
]

# the default ROOT_URLCONF module, bundled with rapidsms, detects and
# maps the urls.py module of each app into a single project urlconf.
# this is handy, but too magical for the taste of some. (remove it?)
ROOT_URLCONF = "rapidsms.djangoproject.urls"

# since we might hit the database from any thread during testing, the
# in-memory sqlite database isn't sufficient. it spawns a separate
# virtual database for each thread, and syncdb is only called for the
# first. this leads to confusing "no such table" errors. We create
# a named temporary instance instead.
import os, tempfile, sys
if 'test' in sys.argv:
    for db_name in DATABASES:
        DATABASES[db_name]['TEST_NAME'] = os.path.join(
            tempfile.gettempdir(), 
            "%s.rapidsms.test.sqlite3" % db_name)
            
try:
    import local_settings.py
except ImportError:
    pass
