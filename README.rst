NTD
===

This project provides a platform for Neglicted Tropical Disease 
periodic data collection over SMS.

It is based on rapidsms (0.9.x) and depends on the following packages:

PIP URL(s)
~~~~~~~~~~

- **django-eav**

    ``pip install -e git+git://github.com/mvpdev/django-eav.git#egg=django-eav``

- **rapidsms-xforms**

    ``pip install -e git+git://github.com/nyaruka/rapidsms-xforms.git#egg=rapidsms_xforms``

Git repositor(y|ies)
~~~~~~~~~~~~~~~~~~~~

- **ntd**

    ``git clone git://github.com/yeleman/ntd.git``

- **rapidsms**

    ``git clone git://github.com/bolibana/bolibana.git``
    ``git checkout who``

- **direct_sms**

    ``git clone git://github.com/rgaudin/Direct-SMS.git``
    ``git checkout new-core``

- **logger_ng**

    ``git clone git://github.com/ksamuel/Logger-NG.git``
    ``git checkout new-core``

- **simple_locations**

    ``git clone git://github.com/yeleman/simple_locations.git``

- **django_simple_config**

    ``git clone git://github.com/yeleman/django_simple_config.git``

- **code_generator**

    ``git clone git://github.com/yeleman/code_generator.git``

- **report_parts**

    ``git clone git://github.com/yeleman/report_parts.git``


Optionnaly, if you wish to use an modem:

* install PyGSM: http://github.com/rapidsms/pygsm
* and it's dependancies: pip install pytz pyserial

Setup
======

- Install all dependancies.
- Setup the DB and backends in settings.py or even better, in local_settings.py
  (you can find an exemple in the skeletons/ dir)
- syncdb (you MUST create an admin user)
- run "./manage.py runserver" and  "./manage.py runrouter"
- load fixtures:
    * ./manage.py loaddata fixtures/init/*
    
    * Either:
      _ if you work on malian location: ./manage.py loaddata fixtures/mali/*
      _ if you want an out of the box malian demo: ./manage.py loaddata fixtures/demo-mali/*
    
    * Or you create locations, locations hierarchies in admin and a campaign in the dashboard 


