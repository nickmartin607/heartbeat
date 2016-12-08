from os.path import abspath, basename, dirname, join

ENVIRONMENT = 'dev'         # Either 'dev' or 'prod'

################## Paths/Files/Names ###########################################
PROJECT_PATH = dirname(abspath(__file__))       # Inner directory containing settings.py
BASE_PATH = dirname(PROJECT_PATH)               # Outer directory containing manage.py
PROJECT_NAME = basename(BASE_PATH)
STATIC_PATH = join(BASE_PATH, 'static')
################################################################################


################## URLs ########################################################
STATIC_URL = '/static/'
LOGIN_URL = '/login'
APPEND_SLASH = True
################################################################################


################## Applications ################################################
ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)
PERSONAL_APPS = [
    'core',
    'authentication',
    'heartbeat',
]
DEPENDENCY_APPS = [
    'datetimewidget',
    'crispy_forms',
    'celery',
    'django_celery_beat',
]
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]
INSTALLED_APPS = DEPENDENCY_APPS + DEFAULT_APPS + PERSONAL_APPS
################################################################################


################## Static Files ################################################
STATIC_ROOT = STATIC_URL
STATICFILES_DIRS = [STATIC_PATH]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]
################################################################################


################## Templates ###################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]
CRISPY_TEMPLATE_PACK = 'bootstrap3'
################################################################################


################## Database ####################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_PATH, 'db.sqlite3')
    }
}
################################################################################


################## WSGI ########################################################
WSGI_APPLICATION = 'config.wsgi.application'
################################################################################


################## Middleware ##################################################
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)
################################################################################


################## General #####################################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_TZ = True
USE_I18N = True
USE_L10N = True
DEFAULT_CHARSET = 'utf-8'
################################################################################


################## Debugging ###################################################
DEBUG = True if ENVIRONMENT == 'dev' else False
################################################################################


################## Security ####################################################
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
SECRET_KEY = '9e5p_b_va=^gq6l)1rkcf(t(!!=u_#&v+!@a6j5qp2%27y4%(u'
################################################################################
