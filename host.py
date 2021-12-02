import os
import sys

#chemin du dossier de notre Application
path = '/home/agrosuivi/agro-logistique'
if path not in sys.path:
    sys.path.append(path)

# chemain de fichier Settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'agro_logistique.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()