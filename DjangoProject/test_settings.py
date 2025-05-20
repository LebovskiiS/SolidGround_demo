from .settings import *

print("*** Overridden settings for testing with SQLite ***")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
BASE_DIR = Path(__file__).resolve().parent.parent
