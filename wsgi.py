"""
WSGI entry point for production servers.
Used by deployment platforms like Railway, Heroku, etc.
"""

from app.main import app

# Pour les serveurs WSGI compatibles
application = app
