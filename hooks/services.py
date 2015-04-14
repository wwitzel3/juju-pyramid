#!/usr/bin/python

import subprocess

from charmhelpers.core.charmframework.base import Manager
from charmhelpers.core.charmframework import helpers
from charmhelpers.fetch import install_remote
from charmhelpers.core import hookenv


def clone_repo():
    install_remote(hookenv.config('repo', dest='/home/ubuntu/repo'))
    subprocess.check_call(['python', '/home/ubuntu/repo/setup.py', 'install'])
    # check for requirements file..
    # subprocess.check_call(['pip', 'install', '-r', '/home/ubuntu/repo/requirements.txt'])

def manage():
    manager = Manager([
        {
            'service': 'juju-pyramid',
            'provides': [
                # context managers for provided relations
                # e.g.: helpers.HttpRelation()
                helpers.HttpRelation(port=6543)
            ],
            'requires': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
                helpers.config_is_set('repo'),
                helpers.MySQLRelation(relation_name='mysql', optional=True),
            ],
            'callbacks': [
                clone_repo,
                helpers.render_template(
                    source='/home/ubuntu/repo/juju.ini.tmpl',
                    target='/home/ubuntu/repo/juju.ini'
                ),
            ],
        },
    ])
    manager.manage()
