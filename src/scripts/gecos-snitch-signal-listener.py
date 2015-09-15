#!/usr/bin/env python

# Copyright (C) 2004-2006 Red Hat Inc. <http://www.redhat.com/>
# Copyright (C) 2005-2007 Collabora Ltd. <http://www.collabora.co.uk/>
# Copyright (C) 2014 Junta de Andalucia. <http://www.juntadeandalucia.es/>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import traceback

import gobject

import dbus
import dbus.mainloop.glib

DBUS_INTERFACE = 'org.guadalinex.ChefSnitch'
DBUS_PATH = '/org/guadalinex/ChefSnitch'

def get_is_active():
    remote_object = bus.get_object(DBUS_INTERFACE, DBUS_PATH)
    return bool(remote_object.GetActive(dbus_interface=DBUS_INTERFACE))

def get_message():
    remote_object = bus.get_object(DBUS_INTERFACE, DBUS_PATH)
    return str(remote_object.GetMessage(dbus_interface=DBUS_INTERFACE))

def is_active_has_changed_cb():
    is_active = get_is_active()
    print ("The Value of IsActive has changed to: %r" % (bool(is_active)))

def message_notified_cb():
    message = get_message()
    print ("A new message has been delivered: %s" % (message))

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    bus.add_signal_receiver(is_active_has_changed_cb, \
                            dbus_interface = DBUS_INTERFACE, \
                            signal_name = "IsActiveHasChanged")

    bus.add_signal_receiver(message_notified_cb, \
                            dbus_interface = DBUS_INTERFACE, \
                            signal_name = "MessageNotified")

    loop = gobject.MainLoop()
    loop.run()
