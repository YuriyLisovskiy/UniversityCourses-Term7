import uuid

import dialogflow

from df_agent import util


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
		
	def __str__(self):
		return '<Agent: id={}>'.format(self.session_id)

	def __repr__(self):
		return str(self)

	def detect_intent(self, text_to_analyze):
		return self.client.detect_intent(
			session=self.session,
			query_input=util.make_query_input(
				text_input=util.make_text_input(text_to_analyze, self.lang_code)
			)
		)

	def ask(self, question):
		response = self.detect_intent(question)
		return {
			'query_text': response.query_result.query_text,
			'detected_intent': response.query_result.intent.display_name,
			'detected_intent_confidence': response.query_result.intent_detection_confidence,
			'fulfillment_text': response.query_result.fulfillment_text
		}


def get_sessions_client():
	return dialogflow.SessionsClient()
