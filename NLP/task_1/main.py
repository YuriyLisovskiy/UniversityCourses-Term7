import json
from google.api_core.exceptions import InvalidArgument

from monad.io import IO
from app.settings import (
	DIALOGFLOW_PROJECT_ID,
	DIALOGFLOW_LANGUAGE_CODE
)
from df_agent.agent import Agent, get_sessions_client

config = {
	'project_id': DIALOGFLOW_PROJECT_ID,
	'lang_code': DIALOGFLOW_LANGUAGE_CODE,
	'client': get_sessions_client()
}


def print_dict(d):
	print(json.dumps(d, sort_keys=True, indent=4))


def interact(question, agent):
	try:
		print_dict(agent.ask(question))
	except InvalidArgument:
		raise


def step(agent):
	return IO.print('Your question? ', end='').bind(
		lambda _: IO.read().bind(
			lambda q: IO.ret(interact(q, agent)).bind(
				lambda _: step(agent)
			) if q != '/stop' else IO.ret(None)
		)
	)


if __name__ == '__main__':
	a = Agent(**config)
	
	print(str(a))
	print(repr(a))
	
	step(a).run()
