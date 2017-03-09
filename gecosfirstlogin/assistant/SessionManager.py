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

__author__ = "Antonio Hernández <ahernandez@emergya.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


import os
import dbus
import syslog
import lsb_release
import traceback
import time


if 'Lite' in lsb_release.get_distro_information()['DESCRIPTION']:
    # Use org.lxde.SessionManager interface
    # (CanShutdown, Logout, RequestReboot, RequestShutdown, Shutdown
    # ReloadSettingsDaemon)
    # See: https://wiki.lxde.org/en/LXSession#Dbus_interface
    SM_DBUS_SERVICE = 'org.lxde.SessionManager'
    SM_DBUS_OBJECT_PATH = '/org/lxde/SessionManager'
    SM_DBUS_CLIENT_PRIVATE_PATH = 'org.lxde.SessionManager.ClientPrivate'
    SM_DBUS_EXIST_REGISTER_CLIENT_METHOD = False
    SM_DBUS_EXIST_UNREGISTER_CLIENT_METHOD = False
    SM_DBUS_EXIST_INHIBIT_METHOD = False
    SM_DBUS_EXIST_UNINHIBIT_METHOD = False
    
else:
    # Use org.gnome.SessionManager interface
    # (Setenv, InitializationError, RegisterClient, UnregisterClient, Inhibit,
    # Uninhibit, IsInhibited, GetClients, GetInhibitors, IsAutostartConditionHandled,
    # Shutdown, CanShutdown, Logout)
    # See: https://people.gnome.org/~mccann/gnome-session/docs/gnome-session.html#org.gnome.SessionManager
    SM_DBUS_SERVICE = 'org.gnome.SessionManager'
    SM_DBUS_OBJECT_PATH = '/org/gnome/SessionManager'
    SM_DBUS_CLIENT_PRIVATE_PATH = 'org.gnome.SessionManager.ClientPrivate'
    SM_DBUS_EXIST_REGISTER_CLIENT_METHOD = True
    SM_DBUS_EXIST_UNREGISTER_CLIENT_METHOD = True
    SM_DBUS_EXIST_INHIBIT_METHOD = True
    SM_DBUS_EXIST_UNINHIBIT_METHOD = True




INHIBIT_LOGGIN_OUT = 1
INHIBIT_USER_SWITCHING = 2
INHIBIT_SUSPENDING = 4
INHIBIT_IDLE = 8


class SessionManager:

    def __init__(self, client_name):

        self.state = 0
        self.sm_proxy = None
        self.sm_client = None
        self.sm_client_id = None
        self.sm_client_name = client_name
        self.inhibit_cookie = None
        self.desktop_autostart_id = os.getenv('DESKTOP_AUTOSTART_ID')

    def log(self, message, priority=syslog.LOG_INFO):
        message = message + '\n' + traceback.format_exc()
        syslog.syslog(priority, message)
        print("SessionManager: %s"%(message))

    def existServiceInSessionBus(self, service_name):
        for service in dbus.SessionBus().list_names():
            if service == service_name:
                return True
        return False

        
    def start(self):
        if self.state == 1:
            return

        if self.desktop_autostart_id is None:
            self.log('This script is intended to be executed from xdg-autostart, \
inside a gnome-session context.', syslog.LOG_ERR)
            self.desktop_autostart_id = '0'

        session_bus = dbus.SessionBus()

        # Check if service exists in session bus
        ntries = 1
        exists = self.existServiceInSessionBus(SM_DBUS_SERVICE)
        while ntries < 3 and not exists:
            time.sleep(1)
            ntries = ntries + 1
            exists = self.existServiceInSessionBus(SM_DBUS_SERVICE)
        
        if not exists:
            self.log('DBUS session bus service %s not found!'%(SM_DBUS_SERVICE), syslog.LOG_ERR)
            return
        
        self.sm_proxy = session_bus.get_object(SM_DBUS_SERVICE, SM_DBUS_OBJECT_PATH)

        try:
            self.register_client()
            self.connect_signals()
            self.inhibit()
            self.state = 1

        except Exception as e:
            self.log(str(e), syslog.LOG_ERR)

    def stop(self):
        if self.state == 0:
            return
        try:
            self.uninhibit()
            self.unregister_client()
        except Exception as e:
            self.log(str(e), syslog.LOG_ERR)

    def register_client(self):
        if not SM_DBUS_EXIST_REGISTER_CLIENT_METHOD:
            return
        
        register_client = self.sm_proxy.get_dbus_method('RegisterClient', SM_DBUS_SERVICE)
        self.sm_client_id = register_client(self.sm_client_name, self.desktop_autostart_id)
        self.log('Client Id: ' + str(self.sm_client_id))

    def unregister_client(self):
        if not SM_DBUS_EXIST_UNREGISTER_CLIENT_METHOD:
            return
        
        unregister_client = self.sm_proxy.get_dbus_method('UnregisterClient', SM_DBUS_SERVICE)
        unregister_client(self.sm_client_id)

    def connect_signals(self):
        if self.sm_client_id is None:
            return
        session_bus = dbus.SessionBus()
        self.sm_client = session_bus.get_object(SM_DBUS_SERVICE, self.sm_client_id)
        #self.sm_client.connect_to_signal('QueryEndSession', self.on_query_end_session)
        #self.sm_client.connect_to_signal('EndSession', self.on_end_session)
        #self.sm_client.connect_to_signal('CancelEndSession', self.on_cancel_end_session)

    def inhibit(self):
        if not SM_DBUS_EXIST_INHIBIT_METHOD:
            return
        
        if self.inhibit_cookie != None:
            return
        m_inhibit = self.sm_proxy.get_dbus_method('Inhibit', SM_DBUS_SERVICE)
        # TODO: Try to get the toplevel_xid from Gdk?, XLib?, ...
        # and try to figure out what flag is appropiate.
        toplevel_xid = 0
        self.inhibit_cookie = m_inhibit(self.sm_client_name, toplevel_xid, 'Reason', INHIBIT_LOGGIN_OUT)
        self.log('Inhibit cookie: ' + str(self.inhibit_cookie))

    def uninhibit(self):
        if not SM_DBUS_EXIST_UNINHIBIT_METHOD:
            return
        
        if self.inhibit_cookie == None:
            return
        m_uninhibit = self.sm_proxy.get_dbus_method('Uninhibit', SM_DBUS_SERVICE)
        m_uninhibit(self.inhibit_cookie)
        self.inhibit_cookie = None

