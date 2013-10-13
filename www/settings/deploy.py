from defaults import *

import os
from os import path

# Static file finders in order of precedence
#######################################
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

# Template file loads in order of precedence
#######################################
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
]

# Middlewares
#######################################
MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'geoware.middleware.GeowareSessionMiddleware',
    'freshly.middleware.assets.AssetVersioningMiddleware',
    'userware.middleware.switch.UserSwitchMiddleware',
    'activityware.middleware.user.UserActivityAuitMiddleware',
    'activityware.middleware.logout.LogoutEnforcementMiddleware',
    'profileware.middleware.UserProfileSetCountryMiddleware',

    # last resort, keep last
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

# Context processor
#######################################
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    
    'finalware.context_processors.contextify',
]

# Authentication backend
#######################################
AUTHENTICATION_BACKENDS = [
    'userware.backends.ModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Cache Related Stuff
#######################################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_KEY_PREFIX = '{}:'.format(PROJ_NAME.lower())
CACHE_MIDDLEWARE_SECONDS = 15*60


# Installed Apps
#######################################
INSTALLED_APPS = [
    # first app
    'preware',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.gis',
    # 'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'postware',
    'south',

    # apps
    # 'activityware',
    # 'userware',
    # 'signupware',
    # 'contactware',
    # 'profileware',


    # last app
    'finalware',
]


# Account activities
#######################################
LOGIN_REDIRECT_URL = '/user/settings/profile/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/user/settings/login/'
LOGOUT_URL = '/user/settings/logout/'


# Database
#######################################
DATABASES = {
    'default': {
        'ENGINE':   "django.contrib.gis.db.backends.postgis",
        'NAME':     DB_NAME,
        'USER':     DB_USER,
        'PASSWORD': DB_PASS,
        # 'HOST':     "",
        # 'PORT':     "",
    }
}

# Site loggin
#######################################
non_core_app_index_start = INSTALLED_APPS.index('postware')
for index, app in enumerate(INSTALLED_APPS, start=0):
    if index == 0 or index >= non_core_app_index_start:
        LOGGING['loggers'].update({
            app: {
                "handlers": ["mail_admins", "logfile"],
                "level": "ERROR",
                "propagate": False,
            }
        })

# Static / Media URL
#######################################
# URL to the static assets
STATIC_URL = '//{0}/s/'.format(PROJ_DOMAIN)
# URL to the user uploaded assets
MEDIA_URL = '//{0}/m/'.format(PROJ_DOMAIN)
# Bump this up if you have changed a static file with .xyz ext
FRESHLY_ASSETS_VERSION = '0000'


# Site objects auto config
#######################################
# site info (you need at least one site)
SITE_OBJECTS_INFO_DICT = {
    '1': {
        'name': PROJ_NAME,
        'domain': PROJ_DOMAIN
    },
}
SITE_ID = 1

# Site Specific Info - What does your site do?
SITE_TITLE = 'Western Influenced South Asian Content Hub'
SITE_KEYWORDS = "South Asian Video Content Culture Hub"
SITE_DESCRIPTION = "A Social Hub for Western Influenced South Asian Content"

# Email send key
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_SENDER = DEFAULT_FROM_EMAIL

# Google Analytics
SITE_GOOGLE_ANALYTICS = ''



