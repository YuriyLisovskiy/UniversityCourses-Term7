from app.bot import UniversityAssistanceBot
from app.settings import LUIS_APP_KEY, LUIS_APP_ID, TELEGRAM_BOT_TOKEN


if __name__ == '__main__':
	UniversityAssistanceBot(
		token=TELEGRAM_BOT_TOKEN,
		luis_config={
			'app_id': LUIS_APP_ID,
			'app_key': LUIS_APP_KEY
		}
	).start()
