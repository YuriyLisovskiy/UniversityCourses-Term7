import os

# Telegram bot API settings.
# TODO


# DialogFlow API settings.

PRIVATE_KEY_PATH = 'set in local_settings.py'

DIALOGFLOW_PROJECT_ID = 'set in local_settings.py'

# Default language code, override in local_settings.py if it is necessary.
DIALOGFLOW_LANGUAGE_CODE = 'en-US'


try:
	from task_1.local_settings import *
except ImportError:
	pass


# Setup.
assert os.path.exists(PRIVATE_KEY_PATH)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PRIVATE_KEY_PATH
