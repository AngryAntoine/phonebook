from .base import *

INSTALLED_APPS += [
    #  third party apps

    #  local apps
    'contacts',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
