#!/usr/bin/python

from charmhelpers.core.services.base import Manager
from charmhelpers.core.services import helpers
from charmhelpers.fetch import install_remote
from charmhelpers.core import hookenv

import actions


def clone_repo():
    install_remote(hookenv.config('repo'))

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
                helpers.MySQLRelation(optional=True),
            ],
            'callbacks': [
                clone_repo,
                helpers.render_template(
                    source='/home/ubuntu/repo/juju.ini.tmpl',
                    target='/home/ubuntu/repo/juju.ini'),
                actions.log_start,
            ],
        },
    ])
    manager.manage()
