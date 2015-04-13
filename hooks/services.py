#!/usr/bin/python

from charmhelpers.core.services.base import Manager
from charmhelpers.core.services import helpers

import actions


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
                helpers.MySQLRelation(optional=True),
            ],
            'callbacks': [
                helpers.render_template(
                    source='upstart.conf',
                    target='/etc/init/juju-pyramid'),
                actions.log_start,
            ],
        },
    ])
    manager.manage()
