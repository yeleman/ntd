#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

'''
    YLM fabfile deploying Mali NTD Field Test

    Will install the project with all its dependencies

    Instructions:
        sudo aptitude install git-core pip python-virtualenv
        sudo pip install Fabric ylmfab
        fab install_dep -- installs all dependencies
        fab deploy -- installs dependencies then creates database

'''

import os

from fabric.api import *
import ylmfab


# dependencies as Dependency objects

ntd = ylmfab.Dependency()
ntd.source = 'git://github.com/yeleman/ntd.git'
ntd.pip_file = 'req.txt'

bolibana = ylmfab.Dependency()
bolibana.source = 'git://github.com/bolibana/bolibana.git'
bolibana.branch = 'who'
bolibana.lib_path = os.path.join('lib', 'rapidsms')
bolibana.lib_name = 'rapidsms'
bolibana.pip_file = 'pip-requires.txt'
#bolibana.revision = 'ac43a836e0de060de2af4dae259f4db6a387999c'

direct_sms = ylmfab.Dependency()
direct_sms.source = 'git://github.com/rgaudin/Direct-SMS.git'
direct_sms.branch = 'new-core'
direct_sms.lib_name = 'direct_sms'

logger_ng = ylmfab.Dependency()
logger_ng.source = 'git://github.com/ksamuel/Logger-NG.git'
logger_ng.branch = 'new-core'
logger_ng.lib_name = 'logger_ng'

simple_locations = ylmfab.Dependency()
simple_locations.source = 'git://github.com/yeleman/simple_locations.git'

django_simple_config = ylmfab.Dependency()
django_simple_config.source = \
                            'git://github.com/yeleman/django_simple_config.git'
django_simple_config.lib_name = 'django_simple_config'

code_generator = ylmfab.Dependency()
code_generator.source = 'git://github.com/yeleman/code_generator.git'

report_parts = ylmfab.Dependency()
report_parts.source = 'git://github.com/yeleman/report_parts.git'

django_eav = ylmfab.Dependency()
django_eav.source = 'git+git://github.com/mvpdev/django-eav.git#egg=django-eav'
django_eav.kind = ylmfab.Dependency.PIP_URL

rapidsms_xforms = ylmfab.Dependency()
rapidsms_xforms.source = \
         'git+git://github.com/nyaruka/rapidsms-xforms.git#egg=rapidsms_xforms'
rapidsms_xforms.kind = ylmfab.Dependency.PIP_URL

dependencies = [ntd, bolibana, direct_sms, logger_ng, simple_locations, \
                django_simple_config, code_generator, report_parts, \
                django_eav, rapidsms_xforms]

root = ntd

root_dir = os.path.join(root.clone_name, 'django_ntd')
root_fixtures = os.path.join('fixtures', 'init', '*.json')
local_settings = os.path.join(root_dir, 'local_settings.py')
local_settings_skel = os.path.join(root_dir, 'skeletons', 'local_settings.py')

# fabric available options


def deploy():

    """ complete deployment of the system:

    - install all dependencies
    - creates the database with admin user
    - load initial fixtures

    """

    # install dependencies
    install_dep()

    # syncdb on
    syncdb()

    # load fixtures
    loadfixtures()


def install_dep():

    """ installs all the dependencies """

    for dependency in dependencies:
        ylmfab.install(dependency)


def syncdb():

    """ creates the dabatase through django

    - copies local_settings skeleton
    - django syncdb
    - south migrate

    """

    import shutil

    if not os.path.exists(local_settings):
        shutil.copyfile(local_settings_skel, local_settings)
    ylmfab.syncdb(rep=root, working_dir=root_dir)
    ylmfab.migrate(rep=root, working_dir=root_dir)


def loadfixtures():

    """ loads the basic fixtures into the database """

    ylmfab.loadfixtures(rep=root, fixtures=root_fixtures, working_dir=root_dir)


def gitrw():

    """ changes repositories url to use private ones (rw access) """

    for dependency in dependencies:
        ylmfab.github_to_private(dependency)


def rst():

    """ outputs the list of dependencies for inclusion in an RST file """

    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'), \
        warn_only=True):

        print(ylmfab.dependencies_to_rst(dependencies))
