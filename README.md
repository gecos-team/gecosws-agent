#GECOS Agent 

GECOS Agent is a piece of GECOS architecture. Installed onto a GECOS compatible distribution,
makes it manageable from a remote GECOS Control Center.

Version 2 substitutes a complex network of packages, configuration files and recipes with 
a simple agent+notification app all in one package

## COMPONENTS

* Chef Client Wrapper
* GECOS First Login
* Configuration Files



## BUILDING

GECOS-Agent has a python standard setup in src/
This setup generates a debian souce package skel (using python setup.py sdist) in deb_dist
Finally, a debian package is constructed with debuild in deb_dist/gecos-agent-1.0 after
some configuration tuning


