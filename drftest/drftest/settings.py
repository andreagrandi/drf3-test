"""
Django settings for drftest project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """ Get the environment variable or return exception """

    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DRFTEST_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_variable('DRFTEST_DEBUG')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'shop',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'drftest.urls'

WSGI_APPLICATION = 'drftest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_env_variable("DRFTEST_DB_ENGINE"), # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': get_env_variable("DRFTEST_DB_NAME"),                      # Or path to database file if using sqlite3.
        'USER': get_env_variable("DRFTEST_DB_USER"),                      # Not used with sqlite3.
        'PASSWORD': get_env_variable("DRFTEST_DB_PASSWORD"),                  # Not used with sqlite3.
        'HOST': get_env_variable("DRFTEST_DB_HOST"),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': get_env_variable("DRFTEST_DB_PORT"),                      # Set to empty string for default. Not used with sqlite3.
    }
}

ADMINS = (
     (get_env_variable("DRFTEST_ADMIN_NAME"), get_env_variable("DRFTEST_ADMIN_EMAIL")),
)

MANAGERS = ADMINS

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

#PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
#TEST_DISCOVER_TOP_LEVEL = PROJECT_ROOT
#TEST_DISCOVER_ROOT = PROJECT_ROOT
#TEST_DISCOVER_PATTERN = "test_*"
