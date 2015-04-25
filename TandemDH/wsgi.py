"""
WSGI config for TandemDH project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TandemDH.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

'''
sys.path.append('/usr/lib/python2.7/site-packages/setuptools-15.0-py2.7.egg')
sys.path.append('/usr/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/python2.7/site-packages/numpy-1.9.2-py2.7-linux-x86_64.egg')
sys.path.append('/usr/lib/python27.zip')
sys.path.append('/usr/lib/python2.7')
sys.path.append('/usr/lib/python2.7/plat-linux2')
sys.path.append('/usr/lib/python2.7/lib-tk')
sys.path.append('/usr/lib/python2.7/lib-old')
sys.path.append('/usr/lib/python2.7/lib-dynload')
sys.path.append('/usr/lib/python2.7/site-packages')
'''