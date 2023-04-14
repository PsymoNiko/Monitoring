"""
Django settings for monitoring project.
<<<<<<< HEAD
Generated by 'django-admin startproject' using Django 4.1.7.
For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/
=======

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
<<<<<<< HEAD
# from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv()

=======
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
<<<<<<< HEAD
# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = 'rrrrr'
=======
SECRET_KEY = os.environ.get("SECRET_KEY")
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

<<<<<<< HEAD

=======
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
<<<<<<< HEAD
    # apps
    "student",
    "ceo",
    "mentor",
    "dailyreport",
    "exercis",
=======

    # apps
    "student",
    "ceo",
    "mentor.apps.MentorConfig",
    "payment",
    'DailyReport',
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
    # framework
    "rest_framework",
    'rest_framework.authtoken',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monitoring.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'monitoring.wsgi.application'

<<<<<<< HEAD

=======
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

<<<<<<< HEAD

=======
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

<<<<<<< HEAD

=======
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

<<<<<<< HEAD

=======
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

<<<<<<< HEAD

=======
MEDIA_ROOT = os.path.join(BASE_DIR, 'profile_images')
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',

        'mentor.authentication.CustomAuthentication',
    ),
<<<<<<< HEAD
}
=======
}
>>>>>>> baa25d8406b5bc6065395071fe8c7c8f0f23acc8
