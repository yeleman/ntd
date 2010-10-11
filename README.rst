NTD
===

This project provides a platform for Neglicted Tropical Disease 
periodic data collection over SMS.

It is based on rapidsms (0.9.x) and depends on the following packages:

* PyPi packages you can install using 'pip install -r req.txt'

* rapidsms fork: `bolibana <http://github.com:bolibana/bolibana>`_ branch 'who'
  
    git clone git@github.com:bolibana/bolibana.git && ln -s bolibana/lib/rapidsms/ rapidsms
    cd bolibana && git checkout new-core
    cd ..
    
* `direct_sms <http://github.com/rgaudin/Direct-SMS>`_ (new-core branch) branch new-core

    git clone http://github.com/rgaudin/Direct-SMS.git && mv Direct-SMS/ direct_sms
    cd direct_sms && git checkout new-core
    cd ..

* `logger_ng <http://github.com/ksamuel/Logger-NG>`_ (new-core branch)

    git clone https://github.com/ksamuel/Logger-NG.git && mv Logger-NG/ logger_ng branch new-core
    cd logger_ng/ &&  git checkout new-core
    cd ..

* `simple_locations <http://github.com/yeleman/simple_locations>`_

     git clone git@github.com:yeleman/simple_locations.git
    
* `django_simple_config <http://github.com/yeleman/django_simple_config>`_

    clone git@github.com:yeleman/django_simple_config.git

* `code_generator <http://github.com/yeleman/code_generator>`_

    clone git@github.com:yeleman/code_generator.git

* `report_parts <http://github.com/yeleman/report_parts>`_

    git clone git@github.com:yeleman/report_parts.git

* `django_eav <http://github.com/mvpdev/django-eav>`_

    pip install -e git+git://github.com/mvpdev/django-eav.git#egg=django-eav

* `rapidsms-xforms <http://github.com/nicpottier/rapidsms-xforms>`_

    pip install -e git+git://github.com/rgaudin/rapidsms-xforms.git#egg=rapidsms_xforms

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


