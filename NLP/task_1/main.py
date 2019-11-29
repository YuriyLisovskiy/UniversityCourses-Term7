import json
from google.api_core.exceptions import InvalidArgument

from monad.io import IO
from app.settings import (
	DIALOGFLOW_PROJECT_ID,
	DIALOGFLOW_LANGUAGE_CODE,
	TELEGRAM_BOT_TOKEN
)
from df_agent.agent import Agent, get_sessions_client

from t_bot.bot import UniversityAssistanceBot

config = {
	'project_id': DIALOGFLOW_PROJECT_ID,
	'lang_code': DIALOGFLOW_LANGUAGE_CODE,
	'client': get_sessions_client()
}


def print_dict(d):
	print(json.dumps(d, sort_keys=True, indent=4))


def interact(question, agent):
	try:
		# print_dict(agent.detect_intent(question))
		resp = agent.detect_intent(question)
		print('Bot[{}]:'.format(resp['detected_intent']), resp['fulfillment_text'])
	except InvalidArgument:
		raise


def step(agent):
	return IO.print('You: ', end='').bind(
		lambda _: IO.read().bind(
			lambda q: IO.ret(interact(q, agent)).bind(
				lambda _: step(agent)
			) if q != '/stop' else IO.ret(None)
		)
	)


if __name__ == '__main__':
	# a = Agent(**config)
	# step(a).run()
	bot = UniversityAssistanceBot(TELEGRAM_BOT_TOKEN, df_config=config)
	bot.start()
