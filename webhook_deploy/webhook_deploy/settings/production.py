from webhook_deploy.settings import *  # NOQA
import dj_database_url


ALLOWED_HOSTS = ['*']

DEBUG = False

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

DATABASES = {
    'default':
        dj_database_url.config(default=os.environ['DATABASE_URL'])
}
