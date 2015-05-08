from webhook_deploy.settings import *  # NOQA
import dj_database_url


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default':
        dj_database_url.config(default=os.environ['DATABASE_URL'])
}
