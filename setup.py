#!/usr/bin/env python

from distutils.core import setup
import glob

setup(name='gecosws-agent',
      version='1.5',
      description='GECOS Agent for Workstations',
      author='Alfonso de Cala',
      author_email='alfonso.cala@juntadeandalucia.es',
      url='https://github.com/gecos-team/gecosws-agent',
      scripts=['scripts/gecos-user-login', 'scripts/gecos-first-login', 'scripts/gecos-chef-client-wrapper','scripts/gecos-first-login-dbusservice','scripts/gecos-snitch-client','scripts/gecos-snitch-service','scripts/gecos-snitch-signal-listener.py','scripts/gecos-snitch-systray'],
      packages=['gecosfirstlogin','gecosfirstlogin_lib','gecosfirstlogin.assistant','gecosfirstlogin.dbus'],
      data_files=[('/usr/share/gecos-first-login/html/',glob.glob('data/html/*')),
                  ('/usr/share/gecos-first-login/ui/',glob.glob('data/ui/*')),
                  ('/usr/share/gecos-first-login/media',glob.glob('data/media/*')),
                  ('/etc/dbus-1/system.d/',glob.glob('etc/dbus-1/system.d/*.conf')),
                  ('/etc/init/',glob.glob('etc/init/*.conf')),
                  ('/lib/systemd/system/',glob.glob('lib/systemd/system/*.service')),
                  ('/etc/xdg/autostart/',glob.glob('etc/xdg/autostart/*.desktop'))]
     )


