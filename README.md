# GECOS Agent 

GECOS Agent is a piece of GECOS architecture. Installed onto a GECOS compatible distribution,
makes it manageable from a remote GECOS Control Center.

Version 2 substitutes a complex network of packages, configuration files and recipes with 
a simple agent+notification app all in one package

**ATTENTION**: for GECOS v2 and v3, please use *gecos-agent* repository and package names. From v4 and on, use *gecosws-agent*.

## COMPONENTS

* Chef Client Wrapper: this script launches a chef-client after making some smart checks. It is called on...
  * ... Boot 
  * ... Login
  * ... Logout
  * ... Shutdown 
  * ... Periodic lapses 
* GECOS First Login: desktop application that locks the user screen the first time he/she logs in the system, until workstation and user policies are downloaded and executed.
* Configuration Files: needed files for autolaunching Chef Client Wrapper when certain events occur (boot, login...)
  * /etc/init/gecos-first-login.conf
  * /etc/init/gecos-snitch-service.conf
  * /etc/xdg/autostart/gecos-first-login.conf
  * /etc/xdg/autostart/gecos-snitch-systray.conf
  * /etc/dbus-1/system.d/org.gecos.firstlogin.conf
  * /etc/dbus-1/system.d/org.gecos.chefsnitch.conf
  * /etc/sudoers
  * /etc/mdm/PostSession/default
  * /home/USER/.gecos-firstlogin
* GECOS-snitch: small applet that sits on the desktop panel and notifies the user when policies are being installed.
 

## BUILDING

GECOS-Agent has a python standard setup script

You can use this setup to generate a source distribution gz (using python setup.py sdist) in deb_dist and then use
 py2dsc --suite trusty dist/gecosws-agent-X.Y.tar.gz  to generate Debian source package (change X.Y properly).

Or just launch a dpkg-buildpackage and use the .deb created in the parent directory.
 

## WINDOWS BUILDING

To build the GECOS Agent under Windows you will need the 32 bits versions of:
* Python 2.7 for Windows with the following modules:
* Py2exe: http://www.py2exe.org (py2exe-X.X.X.win32-py2.7.exe)
* wxPython 3.0.2 (AKA Classic): https://sourceforge.net/projects/wxpython/files/wxPython/3.0.2.0/
* Microsoft Visual C++ 2008 SP 1 redistributable package (https://www.microsoft.com/en-sa/download/details.aspx?id=5582)

The building process is:
```
python setup.py
```


