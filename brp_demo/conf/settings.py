import os
import json
import environ

from base import *  # NOQA

curdir = os.path.dirname(os.path.abspath(__file__))

root = environ.Path(__file__) - 3  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env('{0}.env'.format(env('APP_ENV')))  # reading .env file

ALLOWED_HOSTS = []

TIME_ZONE = env('TIME_ZONE', default='America/New_York')
DEBUG = env('DEBUG')

DATABASES = {
    'default': env.db()
}

CACHES = {
    'default': env.cache()
}

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_SUBJECT_PREFIX = '[brp]'
FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME')
SECRET_KEY = env('SECRET_KEY')

if FORCE_SCRIPT_NAME:
    ADMIN_MEDIA_PREFIX = os.path.join(FORCE_SCRIPT_NAME, ADMIN_MEDIA_PREFIX[1:])

    STATIC_URL = os.path.join(FORCE_SCRIPT_NAME, STATIC_URL[1:])
    MEDIA_URL = os.path.join(FORCE_SCRIPT_NAME, MEDIA_URL[1:])

    LOGIN_URL = os.path.join(FORCE_SCRIPT_NAME, LOGIN_URL[1:])
    LOGOUT_URL = os.path.join(FORCE_SCRIPT_NAME, LOGOUT_URL[1:])
    LOGIN_REDIRECT_URL = os.path.join(FORCE_SCRIPT_NAME, LOGIN_REDIRECT_URL[1:])
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'query'
    SOCIAL_AUTH_LOGIN_URL = 'query'
