"""
Django settings for MegaSupload project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ffurn5+!ay_)ng8w5t21!z^)s(o!vd@pnpn*ngz=v+%5dcfai'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['megasupload.lsd-music.fr', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MegaSuploadApp.apps.MegasuploadappConfig',
    'MegaSuploadAPI.apps.MegasuploadapiConfig',
    'social_django'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'MegaSupload.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'MegaSupload.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'megasupload',
        'USER': 'megasupload',
        'PASSWORD': 'InsertYourPassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'django.contrib.auth.backends.ModelBackend'
)

AUTH_USER_MODEL = 'MegaSuploadAPI.User'

LOGIN_URL = "/app/login/"
LOGOUT_URL = "/api/auth/logout"
LOGIN_REDIRECT_URL = '/app/'

#Social auth FB
SOCIAL_AUTH_FACEBOOK_KEY = '186888078747587'
SOCIAL_AUTH_FACEBOOK_SECRET = '2743735e32a32525732a05274660801d'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}
#Social auth Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '481016636670-mumclrmgs44d3ksfa8jnh0u6rj01ut96.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'VGm5j3XXoVOPAz_pGAwNIGoZ'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']
# Todo : Switch to true on server
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
SOCIAL_AUTH_CLEAN_USERNAMES = False