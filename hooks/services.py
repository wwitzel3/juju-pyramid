#!/usr/bin/python

import subprocess

from charmhelpers.core.charmframework.base import Manager
from charmhelpers.core.charmframework import helpers
from charmhelpers.fetch import install_remote
from charmhelpers.core import hookenv

import relations

RELATIONS = {
    'JUJU_POSTGRESQL': relations.PostgreSQLRelation(relation_name='postgresql', optional=True),
    'JUJU_REDIS': relations.RedisRelation(relation_name='redis', optional=True),
}

REQUIRES = [helpers.config_is_set('repo'),]
REQUIRES.extend(RELATIONS.values())

REPO = 'review-queue.git'

def clone_repo():
    install_remote(hookenv.config('repo'), dest='/home/ubuntu/repo')
    subprocess.check_call(['apt-get', 'install', '-y', 'libpq-dev', 'python-dev'])
    # TODO(wwitzel3) fix the hard coded repo path
    subprocess.check_call(['python', '/home/ubuntu/repo/%s/setup.py' % (REPO), 'install'])

def manage():
    manager = Manager([
        {
            'service': 'juju-pyramid',
            'provides': [
                # context managers for provided relations
                # e.g.: helpers.HttpRelation()
                helpers.HttpRelation(port=6543)
            ],
            'requires': REQUIRES,
            'callbacks': [
                clone_repo,
                helpers.render_template(
                    source='juju.ini.tmpl',
                    target='/home/ubuntu/repo/%s/juju.ini' % (REPO),
                    context={k: v.filtered_data() for k,v in RELATIONS.items()},
                    templates_dir='/home/ubuntu/repo/%s' % (REPO),
                ),
            ],
        },
    ])
    manager.manage()
