"""
Django settings for ghs_med project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
import os
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '94)b(3zk2^1jq=mn(-i9==kvv^=%)s)%yik2nopr!+7dhh856)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SEND_BROKEN_LINK_EMAILS = True
ADMINS = (
    ('TOURE', 'parheto10@gmail.com'),
)
MANAGERS = ADMINS

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = "P@premium2@#"
EMAIL_HOST_USER = "bebeto10toure@gmail.com"
EMAIL_USE_TLS = True

#SERVER_EMAIL = "eba@sigfne.net"
#DEFAULT_FROM_EMAIL = "eba@sigfne.net"

GRAPPELLI_ADMIN_TITLE = "GHS"

# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'rest_framework.filters.DjangoFilterBackend',
    # ),
    # 'DATETIME_FORMAT': '%a, %d %b %Y %H:%M:%S %z',
    # 'DATETIME_INPUT_FORMATS': ['iso-8601', '%Y-%m-%d %H:%M:%S', '%a, %d %b %Y %H:%M:%S %z'],
    # 'DATE_FORMAT': '%Y-%m-%d',
    # 'DATE_INPUT_FORMATS': ['%Y-%m-%d', '%m/%d/%YYYY'],
    # 'PAGE_SIZE': 20
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #other App
    "django_dramatiq",
    'bootstrap4',
    'corsheaders',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    # 'dj_rest_auth',
    # 'livereload',
    # 'djangobower',
    # 'schedule',
    'widget_tweaks',
    'import_export',

    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',
    'otp_messagebird',

    "parametres.apps.ParametresConfig",
    "patients.apps.PatientsConfig",
    "personnels.apps.PersonnelsConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'livereload.middleware.LiveReloadScript',
]

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": "amqp://localhost:5672",
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ]
}

# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled.  The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {
        "url": "redis://localhost:6379",
    },
    "MIDDLEWARE_OPTIONS": {
        "result_ttl": 60000
    }
}



ROOT_URLCONF = 'ghs_med.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'patients.context_processors.inscription',
            ],
        },
    },
]

WSGI_APPLICATION = 'ghs_med.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'ghs',
#         # 'CLIENT': {
#         #    'host': 'mongodb://admin:Samuel10@ds111012.mlab.com:11012/ghs',
#         # }
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

FIRST_DAY_OF_WEEK = 0     # 0 is Sunday
# Convert to calendar module, where 0 is Monday :/
FIRST_DAY_OF_WEEK_CAL = (FIRST_DAY_OF_WEEK - 1) % 7

# figure locale name
LOCAL_LANG = LANGUAGE_CODE.split('-')[0]
LOCAL_COUNTRY = LANGUAGE_CODE.split('-')[1].upper()
LOCALE_NAME = LOCAL_LANG + '_' + LOCAL_COUNTRY + '.UTF8'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# ENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = (os.path.join(BASE_DIR, 'static', 'assets'))

MEDIA_URL = "/media/"
MEDIA_ROOT = (os.path.join(BASE_DIR, 'static', 'medias'))

# LOGIN_URL = 'login'
# LOGOUT_URL = 'index'
# LOGIN_REDIRECT_URL = 'patient:dashboard'
# LOGOUT_REDIRECT_URL = 'index'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Client("AC7538f3cd9e32c282bfe2794c300d3a1b", "a203471476d1f63807e60883fee01140")

TWILIO_VERIFY_SERVICE_SID =  'VA45f8cac6a8928094259a3f5daef3d168'
TWILIO_ACCOUNT_SID = 'AC7538f3cd9e32c282bfe2794c300d3a1b'
TWILIO_AUTH_TOKEN = 'a203471476d1f63807e60883fee01140'
TWILIO_NUMBER = '+2250748566846'

MESSAGE_BIRD_ACCESS_KEY = "TAu4RUJ4kp4CGgDxmoDiiFPdM"

# #Configure Redis as Django cache
# CACHES = {
# "default": {
# "BACKEND": "django_redis.cache.RedisCache",
# "LOCATION": "redis://127.0.0.1: 6379 / 0 ",
# "OPTIONS": {
# "CLIENT_CLASS": "django_redis.client.DefaultClient",
# }
# }
# }
# # Cache session in Redis
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"
# # session settings (can not be written)
# SESSION_COOKIE_AGE = 60 * 15 # 15 mn
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True # If the browser is closed, COOKIE fails
