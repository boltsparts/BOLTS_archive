#!/usr/bin/python
#This script is the WSGI entrypoint for deployment on OpenShift. It is not
#useful for local operation.

#set up virtualenv for openshift
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

from website import app as application
