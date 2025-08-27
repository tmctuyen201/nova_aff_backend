"""
WSGI config for nova_aff project - Production Version
Domain: https://novaaff.id.vn/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Load environment variables from .env.production
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.production'))

# Set Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova_aff.settings_production')

application = get_wsgi_application()
