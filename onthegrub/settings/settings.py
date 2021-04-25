import os

from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '5r&bht!1rco2-fe@aa4a%#5#uds+#fw(to+y%--5t%87pe3(q0'
EMAIL_HOST_USER = 'grubtrucksapp@gmail.com'
EMAIL_HOST_PASSWORD = 'arsfuuwlccjxqqrw'

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = [
    "10.0.2.2",
    "127.0.0.1",
    'localhost'
]

INTERNAL_IPS = [
    '127.0.0.1',  # This is needed for the Django debug toolbar
]

SITE_ID = 1

# App settings

ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'

GRAPHENE = {
    'SCHEMA': 'onthegrub.schema.schema'
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

GOOGLE_MAPS_API_KEY = 'AIzaSyCHX-SHtIOkmTMLLKIcFHpL0YSiVojWVm8'

WAGTAIL_SITE_NAME = 'OnTheGrub'

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAvYJnq44:APA91bHoPGfkFciJYrP0fny8G9kGVSZ-92g2qZrSDx9Q2E6eX9_-kVtcPqiGUX6rGnEoBFowFMqEa3j_DtE9XtARqwdZkRlK3UCD4pj9HPZDyY1QCb5nkcVP88oGh2DM8gdsvbg9A2z9",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}

## Geospatial libraries
GEOS_LIBRARY_PATH = BASE_DIR[0:-10] + r'env\lib\site-packages\osgeo\geos_c.dll'
GDAL_LIBRARY_PATH = BASE_DIR[0:-10] + r'env\lib\site-packages\osgeo\gdal300.dll'

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder'
]

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',

    # OTG Apps
    'announcements.apps.AnnouncementsConfig',
    'catering.apps.CateringConfig',
    'events.apps.EventsConfig',
    'trucks.apps.TrucksConfig',
    'users.apps.UsersConfig',
    'util.apps.UtilConfig',
    'dashboard.apps.DashboardConfig',
    'notifications.apps.NotificationsConfig',

    # Dev/Util
    'debug_toolbar',
    'sass_processor',

    # 3rd party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'django_filters',
    'django_google_maps',
    'django_property_filter',
    'fcm_django',
    'graphene_django',
    'markdownx',
    'model_utils',
    'phone_field',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    # 'djstripe',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # This needs to be before other middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'onthegrub.urls'
# TEMPLATE_DIRS = (
# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
#     os.path.join(BASE_DIR, 'templates'),
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            # 'builtins': [
            #     'sass_processor.templatetags.sass_tags' # TODO: Figure this out
            # ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.request"
            ],
        },
    },
]

WSGI_APPLICATION = 'onthegrub.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Allauth Providers
SOCIALACCOUNT_PROVIDERS = {
    # GOOGLE PROVIDER
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },

    # FACEBOOK PROVIDER
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    }
}

# Location Settings
LOCATION_FIELD_PATH = STATIC_URL + 'location_field'
LOCATION_FIELD = {
    # Map Settings
    'map.provider': 'google',
    'map.zoom': 13,
    'search.provider': 'google',
    'search.suffix': '',

    # Google
    'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
    'provider.google.api_key': 'AIzaSyCHX-SHtIOkmTMLLKIcFHpL0YSiVojWVm8',
    'provider.google.api_libraries': '',
    'provider.google.map.type': 'ROADMAP',

    # Mapbox
    'provider.mapbox.access_token': '',
    'provider.mapbox.max_zoom': 18,
    'provider.mapbox.id': 'mapbox.streets',

    # OpenStreetMap
    'provider.openstreetmap.max_zoom': 18,

    # Misc
    'resources.root_path': LOCATION_FIELD_PATH,
    'resources.media': {
        'js': (
            LOCATION_FIELD_PATH + '/js/form.js',
        ),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

### UNUSED STUFF FOR NOW THAT WE MIGHT USE IN THE FUTURE

# dj-stripe vars
# STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "<your publishable key>")
# STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
# STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "<your publishable key>")
# STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "<your secret key>")
# STRIPE_LIVE_MODE = False  # Change to True in production
# DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx" # Get from section in Stripe dashboard where you added the webhook endpoint
