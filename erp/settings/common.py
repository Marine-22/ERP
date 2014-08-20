"""
List of common settings for the project. Will be used in all environments
"""

# E-mail server settings
EMAIL_HOST = 'mail.iquap.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'erp'
EMAIL_SUBJECT_PREFIX = 'ERP System'
EMAIL_USE_TLS = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Bratislava'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sk'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Contrib layers to locate static files
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

# Template context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'core.context.user_profile.user_profile',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!y3rffir2$@s@*7%^j9)_rn*=u^udk&j*%#i+q0yf=mdrzl%@+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

# List of middleware classes
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.auth.middleware.login_required.LoginRequiredMiddleware',
    )

# Basic URL router
ROOT_URLCONF = 'erp.urls'

# Urls that should be excluded out of LoginRequiredMiddleware
LOGIN_EXEMPT_URLS = (
    r'^static/',
    r'^assets/',
    )

# Url at which the user should be redirected after login
LOGIN_REDIRECT_URL = '/'