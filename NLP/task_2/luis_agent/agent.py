import random

from luis_sdk import LUISClient


# Agent is a wrapper for LUIS API.
class LUISAgent:
	
	def __init__(self, app_id, app_key):
		self._client = LUISClient(app_id, app_key, True)
	
	# Sends text to LUIS for analysis.
	def analyze(self, text):
		response = self._client.predict(text)
		result = {
			'query': response.get_query(),
			'intent': response.get_top_intent().get_name(),
			'entities': [{
				'name': entity.get_name(),
				'type': entity.get_type(),
				'score': entity.get_score()
			} for entity in response.get_entities()]
		}
		dialog = response.get_dialog()
		if dialog is not None:
			dialog_dict = {
				'prompt': dialog.get_prompt(),
				'parameter': dialog.get_parameter_name(),
				'status': dialog.get_status()
			}
			if dialog_dict != {}:
				result['dialog'] = dialog_dict
		return result
	
	@staticmethod
	def welcome_response():
		return random.choice([
			'Hi! How are you doing?',
			'Hello! How can I help you?',
			'Good day! What can I do for you today?',
			'Greetings! How can I assist?'
		])
	
	@staticmethod
	def fallback_response():
		return random.choice([
			'I didn\'t get that. Can you say it again?',
			'I missed what you said. What was that?',
			'Sorry, could you say that again?',
			'Sorry, can you say that again?',
			'Can you say that again?',
			'Sorry, I didn\'t get that. Can you rephrase?',
			'Sorry, what was that?',
			'One more time?',
			'What was that?',
			'Say that one more time?',
			'I didn\'t get that. Can you repeat?',
			'I missed that, say that again?'
		])
	
	@staticmethod
	def gratitude_response():
		return random.choice([
			'You are welcome!',
			'Happy to help',
			'You got it'
		])


if __name__ == '__main__':
	from app.settings import LUIS_APP_ID, LUIS_APP_KEY
	from pprint import pprint
	
	agent = LUISAgent(LUIS_APP_ID, LUIS_APP_KEY)
	pprint(agent.analyze('my exams'))
