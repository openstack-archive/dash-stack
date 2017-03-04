import os, sys


sys.path.append('/usr/share/dash-stack/dash_stack_dashboard')

sys.path.append('/usr/share/dash-stack/venv/lib/python2.7/site-packages')


from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dash_stack_dashboard.settings")

application = get_wsgi_application()
