from app.settings import (
	DIALOGFLOW_PROJECT_ID,
	DIALOGFLOW_LANGUAGE_CODE,
	TELEGRAM_BOT_TOKEN
)
from t_bot.bot import UniversityAssistanceBot
from df_agent.agent import get_sessions_client


if __name__ == '__main__':
	config = {
		'project_id': DIALOGFLOW_PROJECT_ID,
		'lang_code': DIALOGFLOW_LANGUAGE_CODE,
		'client': get_sessions_client()
	}
	UniversityAssistanceBot(
		token=TELEGRAM_BOT_TOKEN,
		df_config=config
	).start()
