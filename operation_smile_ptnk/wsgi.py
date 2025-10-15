"""WSGI config for Operation Smile PTNK project."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operation_smile_ptnk.settings')

application = get_wsgi_application()
