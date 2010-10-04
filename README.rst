NTD
===

This project provides a platform for Neglicted Tropical Disease 
periodic data collection over SMS.

It is based on rapidsms (0.9.x) and depends on the following packages:

* `rapidsms <http://github.com/rapidsms/rapidsms>`_
* `handlers_i18n <http://github.com/yeleman/handlers_i18n>`_
* `direct_sms <http://github.com/rgaudin/Direct-SMS>`_ (new-core branch)
* `logger_ng <http://github.com/ksamuel/Logger-NG>`_ (new-core branch)
* `health_models <http://github.com/daveycrockett/healthmodels>`_ (simple branch)
* `simple_locations <http://github.com/yeleman/simple_locations>`_
* `auth <http://github.com/yeleman/auth>`_
* `django_simple_config <http://github.com/yeleman/django_simple_config>`_
* `code_generator <http://github.com/yeleman/code_generator>`_
* `report_parts <http://github.com/yeleman/report_parts>`_
* `django_eav <http://github.com/mvpdev/django-eav>`_

Setup
======

- Install all dependancies.
- Setup the DB and backends in settings.py or even better, in local_settings.py
  (you can find an exemple in the skeletons/ dir)
- run "./manage.py loaddata fixtures/*json"
- run "./manage.py runserver"
- In the django admin, in 'location hierarchies', create some entries.


