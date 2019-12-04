from .settings import *

import django_heroku
import dj_database_url

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'grubtrucks.herokuapp.com'
]

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# ROOT_URLCONF = 'streamifye.urls'

# MIDDLEWARE += [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
# ]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY ')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
# AWS_S3_REGION_NAME = 'us-east-1'
# AWS_DEFAULT_ACL = None
# AWS_BUCKET_ACL = None

# ASSETS
# MEDIA_URL = 'https://%s/%s/' % ('grubtrucks.s3.amazonaws.com', 'media')
# STATIC_URL = 'https://%s/%s/' % ('grubtrucks.s3.amazonaws.com', 'static')

# EMAIL
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

django_heroku.settings(locals())
