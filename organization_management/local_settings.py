import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = '*+rasda(@$^dg8)yus)*aghfcdpa(0_=n@c6*xtasdasoiumo'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'db_03': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'prod01',
        'PASSWORD': '5B%vOz8f',
        'HOST': '10.0.100.3',
        'PORT': '5432'
    }
}


STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
