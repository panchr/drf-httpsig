DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'drf_httpsig',
    'django_nose',
)

ROOT_URLCONF = 'drf_httpsig.tests'

SECRET_KEY = 'MY PRIVATE SECRET'

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
