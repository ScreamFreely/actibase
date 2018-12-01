"""
Django settings for tpupa project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
sys.path.insert(0, '/var/www/mn.actibase')
#sys.path.insert(0, '/home/nkfx/ScreamFreely/ActiSites/MnActivist/server')
import siteauth as KF

import datetime

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.abspath(os.path.join(SITE_ROOT, ".."))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = KF.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
# TEMPLATE_DEBUG = False
DEBUG = True

USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = KF.allowed_hosts
ROOT_URLCONF = KF.root_urlconf
WSGI_APPLICATION = KF.wsgi_application
AUTH_USER_MODEL = 'accounts.User'

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'opencivicdata.core.apps.BaseConfig',
    'opencivicdata.legislative.apps.BaseConfig',
    'opencivicdata',
    'corsheaders',
    'rest_framework',

    'rest_framework.authtoken',
    'rest_framework_jwt',

    'phonenumber_field',
    'cities',
    'pupa',

    'accounts',
    'dex',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': KF.dbname,
        'USER': KF.dbuser,
        'PASSWORD': KF.dbpasswd,
        'HOST': 'localhost',
        'PORT': '',
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
# Additional static file locations.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
#STATIC_ROOT = os.path.join(os.path.dirname(SITE_ROOT), 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

CITIES_FILES = {
    'city': {
       'filenames': ["US.zip", "cities1000.zip", ],
       'urls': ['http://download.geonames.org/export/dump/'+'{filename}']
    },
}

CITIES_LOCALES = ['en', 'und', 'LANGUAGES']
CITIES_POSTAL_CODES = ['US',]
CITIES_PLUGINS = [
    'cities.plugin.reset_queries.Plugin',  # plugin that helps to reduce memory usage when importing large datasets (e.g. "allCountries.zip")
]

CITIES_SKIP_CITIES_WITH_EMPTY_REGIONS = True

GEOMETRY_BACKEND = 'geos'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',   
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'PAGE_SIZE': 25 
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_USERNAME_FIELD': 'email',
    'JWT_USER_IDENTIFIER_APP': 'accounts',
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

PHONENUMBER_DB_FORMAT = 'E164'

SCRAPELIB_RPM = 60
SCRAPELIB_TIMEOUT = 60
SCRAPELIB_RETRY_ATTEMPTS = 3
SCRAPELIB_RETRY_WAIT_SECONDS = 10

CACHE_DIR = os.path.join(os.getcwd(), '_cache')
SCRAPED_DATA_DIR = os.path.join(os.getcwd(), '_data')

CORS_ORIGIN_WHITELIST = (
    'google.com',
    'https://www.mnactivist.org',
    'https://mnactivist.org',    
    'localhost:3305'    
)



from corsheaders.defaults import default_headers
#CORS_ALLOW_HEADERS = default_headers 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': "%(asctime)s %(levelname)s %(name)s: %(message)s",
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'pupa.ext.ansistrm.ColorizingStreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'], 'level': 'DEBUG', 'propagate': True
        },
        'scrapelib': {
            'handlers': ['default'], 'level': 'INFO', 'propagate': False
        },
        'requests': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False
        },
        'boto': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'cities': {
            'handlers': ['console'],
            'level': 'INFO'
        },
    },
}
