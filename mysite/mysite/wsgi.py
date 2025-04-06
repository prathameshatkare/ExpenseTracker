import sys
import os

path = '/home/asus/expense_tracker'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'expense_tracker.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
