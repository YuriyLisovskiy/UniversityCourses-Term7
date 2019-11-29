from app import settings as s
from app.bot import UniversityAssistanceBot
from df_agent.agent import get_sessions_client


if __name__ == '__main__':
	config = {
		'project_id': s.DIALOGFLOW_PROJECT_ID,
		'lang_code': s.DIALOGFLOW_LANGUAGE_CODE,
		'client': get_sessions_client()
	}
	UniversityAssistanceBot(
		token=s.TELEGRAM_BOT_TOKEN,
		df_config=config
	).start()
