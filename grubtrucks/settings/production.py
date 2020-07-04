import dj_database_url
import django_heroku

from .settings import *

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'grubtrucks.herokuapp.com'
]

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

ROOT_URLCONF = 'grubtrucks.urls'

# MIDDLEWARE += [
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ]

# MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# from whitenoise.storage import CompressedManifestStaticFilesStorage
#
# class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
#     manifest_strict = False
#
# STATICFILES_STORAGE = 'grubtrucks.settings.production.WhiteNoiseStaticFilesStorage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', '')
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'us-east-2'
# AWS_QUERYSTRING_AUTH = False
# AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = 'public-read'
AWS_BUCKET_ACL = 'public-read'
# AWS_DEFAULT_ACL = None
# AWS_BUCKET_ACL = None

# ASSETS
MEDIA_URL = 'https://%s/%s/' % ('grubtrucks-app.s3.amazonaws.com', 'media')
STATIC_URL = 'https://%s/%s/' % ('grubtrucks-app.s3.amazonaws.com', 'static')

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
django_heroku.settings(locals())
