#!/usr/bin/env python
# -*- coding= UTF-8 -*-

import settings
import os

settings.DEBUG = settings.TEMPLATE_DEBUG = True
settings.LOG_FILE    = "/tmp/rapidsms.log"

settings.DATABASES.update({
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(settings.PROJECT_DIR, "who.db")
    }
})

settings.INSTALLED_BACKENDS = {
    #"att": {
    #    "ENGINE": "rapidsms.backends.gsm",
    #    "PORT": "/dev/ttyUSB0"
    #},
    #"verizon": {
    #    "ENGINE": "rapidsms.backends.gsm,
    #    "PORT": "/dev/ttyUSB1"
    #},
    "message_tester": {
        "ENGINE": "rapidsms.backends.bucket"
    }
}

settings.MEDIA_URL = '/static/'
