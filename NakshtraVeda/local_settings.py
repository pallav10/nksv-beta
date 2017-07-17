from settings import *


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:8000',
    }
}

# BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'

# import djcelery
#
# djcelery.setup_loader()
#
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
# BROKER_URL = 'amqp://myuser:mypassword@127.0.0.1:5672//'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_IMPORTS = ('api.tasks',)


# STATIC_ROOT = '/home/pallav/LearningProjects/django_basic_static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
EMAIL_FILE_PATH = "../emails"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST_USER = 'webteam@convergentglobe.com'
EMAIL_HOST_PASSWORD = 'convergenow123@@'

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

DEBUG = True

LOGGING_LEVEL = 'DEBUG'

NAKSHTRAVEDA_LOG_FILE = "../NakshtraVeda/nksv.log"
