import os

# Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Telegram bot API settings.

# Bot token received from BotFather.
TELEGRAM_BOT_TOKEN = 'set in local_settings.py'


# LUIS API settings.

LUIS_APP_ID = 'set in local settings'
LUIS_APP_KEY = 'set in local settings'


try:
	from app.local_settings import *
except ImportError:
	pass
