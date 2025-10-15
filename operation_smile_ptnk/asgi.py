"""ASGI config for Operation Smile PTNK project."""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operation_smile_ptnk.settings')

application = get_asgi_application()
