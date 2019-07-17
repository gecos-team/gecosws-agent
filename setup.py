#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# This file is part of Guadalinex
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import os
import sys
from distutils.core import setup
import shutil
import glob

setup_args = {}
setup_args['name'] = 'gecosws-agent'
setup_args['description'] = 'GECOS Agent for Workstations'
setup_args['author'] = 'Alfonso de Cala',
setup_args['author_email'] = 'alfonso.cala@juntadeandalucia.es'
setup_args['url'] = 'https://github.com/gecos-team/gecosws-agent'
setup_args['version'] = '1.5'


# OS detection
if sys.platform == 'win32':
    import py2exe
    sys.argv.append('py2exe')

    try:
        import modulefinder
        import win32com,sys

        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath('win32com', p)

        for extra in ['win32com.shell','win32com.mapi']:
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)

    except ImportError:
        # no build path setup, no worries.
        pass

    class Target:
        def __init__(self, script, description):
            self.script = script
            self.description = description
            self.company_name = 'Junta de Andalucia'
            self.copyright = 'Copyright (C) 2019 Junta de Andalucia'
            self.name = setup_args['name']
            self.icon_resources = [(0, 'data\\media\\gecos.ico')]


    setup_args['zipfile'] = 'lib/shared.zip'
    
    # Console applications
    setup_args['console'] = [
        Target('gecosws-chef-snitch-client', 'Chef snitch client'),
    ]
    
    # Windows applications
    setup_args['windows'] = [
        Target('gecos-notifier', 'GECOS notifier'),
        Target('gecos-snitch-client', 'GECOS snitch client'),
    ]
    setup_args['options'] = {'py2exe': {
        'dll_excludes': ['w9xpopen.exe'], 
        'includes':['_ssl', '_socket'],
    }}

else:
    setup_args['scripts'] = [
        'scripts/gecos-user-login', 
        'scripts/gecos-first-login', 
        'scripts/gecos-chef-client-wrapper',
        'scripts/gecos-first-login-dbusservice',
        'scripts/gecos-snitch-client',
        'scripts/gecos-notifier'
    ]


    setup_args['packages'] = [
        'gecosfirstlogin',
        'gecosfirstlogin_lib',
        'gecosfirstlogin.assistant',
        'gecosfirstlogin.dbus'
    ]

    setup_args['data_files'] = [
        ('/usr/share/gecos-first-login/html/',glob.glob('data/html/*')),
        ('/usr/share/gecos-first-login/ui/',glob.glob('data/ui/*')),
        ('/usr/share/gecos-first-login/media',glob.glob('data/media/*')),
        ('/etc/dbus-1/system.d/',glob.glob('etc/dbus-1/system.d/*.conf')),
        ('/etc/init/',glob.glob('etc/init/*.conf')),
        ('/lib/systemd/system/',glob.glob('lib/systemd/system/*.service')),
        ('/etc/xdg/autostart/',glob.glob('etc/xdg/autostart/*.desktop'))
    ]


if __name__ == '__main__':
    setup(**setup_args)
    
    # Copy the 'media' directory
    if os.path.exists('dist'):
        if os.path.exists('dist\\media'):
            shutil.rmtree('dist\\media')
        shutil.copytree('media', 'dist\\media')
        if os.path.exists('dist\\data'):
            shutil.rmtree('dist\\data')
        shutil.copytree('data', 'dist\\data')

