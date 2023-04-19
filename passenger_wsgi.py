import imp
import os
import sys
# from ShiftScheduler import application
# import django.core.handlers.wsgi
from ShiftScheduler.wsgi import get_wsgi_application
# from django.core.wsgi import get_wsgi_application
from ShiftScheduler import wsgi

# application = wsgi.appligation

# sys.path.insert(0, os.path.dirname(__file__))

# wsgi = imp.load_source('wsgi', 'ShiftScheduler/wsgi.py')
# application = wsgi.application

# Set up paths and environment variables
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'ShiftScheduler.settings'

# Set script name for the PATH_INFO fix below
SCRIPT_NAME = os.getcwd()

class PassengerPathInfoFix(object):
    """
        Sets PATH_INFO from REQUEST_URI because Passenger doesn't provide it.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        from urllib.parse import unquote
        environ['SCRIPT_NAME'] = SCRIPT_NAME
        request_uri = unquote(environ['REQUEST_URI'])
        script_name = unquote(environ.get('SCRIPT_NAME', ''))
        offset = request_uri.startswith(script_name) and len(environ['SCRIPT_NAME']) or 0
        environ['PATH_INFO'] = request_uri[offset:].split('?', 1)[0]
        return self.app(environ, start_response)

# Set the application
# application = get_wsgi_application()
# application = PassengerPathInfoFix(application)
application = wsgi.application
