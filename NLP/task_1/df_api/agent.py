import uuid

import dialogflow


class Agent:

	def __init__(self, project_id, lang_code, client):
		assert isinstance(project_id, str)
		self.project_id = project_id
		
		assert isinstance(lang_code, str)
		self.lang_code = lang_code
		
		self.session_id = uuid.uuid4()
		
		assert isinstance(client, dialogflow.SessionsClient)
		self.client = client
		
		self.session = self.client.session_path(self.project_id, self.session_id)
	
	def _make_text_input(self, text):
		return dialogflow.types.TextInput(text=text, language_code=self.lang_code)
	
	def _make_query_input(self, text_input):
		assert isinstance(text_input, dialogflow.types.TextInput)
		return dialogflow.types.QueryInput(text=text_input)

	def ask(self, question):
		response = self.client.detect_intent(
			session=self.session,
			query_input=self._make_query_input(
				text_input=self._make_text_input(question)
			)
		)
		return {
			'query_text': response.query_result.query_text,
			'detected_intent': response.query_result.intent.display_name,
			'detected_intent_confidence': response.query_result.intent_detection_confidence,
			'fulfillment_text': response.query_result.fulfillment_text
		}


def get_sessions_client():
	return dialogflow.SessionsClient()