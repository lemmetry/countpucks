import os
import sys


apache_dir = os.path.dirname(__file__)
site_dir = os.path.dirname(apache_dir)
project_dir = os.path.dirname(site_dir)

sys.path.append(project_dir)
sys.path.append(site_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'countpucks.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()