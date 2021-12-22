"""
ASGI config for django_task_schedule project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
})
