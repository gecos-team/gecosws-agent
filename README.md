#GECOS Agent 

GECOS Agent is a piece of GECOS architecture. Installed onto a GECOS compatible distribution,
makes it manageable from a remote GECOS Control Center.

Version 2 substitutes a complex network of packages, configuration files and recipes with 
a simple agent+notification app all in one package

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

GECOS-Agent has a python standard setup in src/
This setup generates a debian source package skel (using python setup.py sdist from src/) in deb_dist
Then, with py2dsc --maintainer "NAME <EMAIL> src/dist/gecos-agent-1.0.tar.gz --suite trusty
Finally, a debian package is constructed with debuild in deb_dist/gecos-agent-1.0 after
some configuration tuning (debian/control, debian/copyright, debian/changelog)


