from datetime import datetime

from app.storage import Storage
from df_agent.agent import Agent
from app.logging import logger as default_logger

from telegram.ext.filters import Filters
from telegram.ext import Updater, MessageHandler, CommandHandler


class UniversityAssistanceBot:

	def __init__(self, token, df_config, logger=None):
		# If passed logger is None, setup default logger.
		if not logger:
			logger = default_logger
		self._logger = logger
		
		assert df_config is not None
		self.df_config = df_config

		# Available bot handlers, order is required.
		handlers = [
			# Handlers on different commands
			CommandHandler('start', self._text_message),
			CommandHandler('stop', self._text_message),
			
			# Send a message when the command /help is issued.
			CommandHandler('help', self._text_message),
			
			# Create new exam.
			CommandHandler('newexam', self._newexam_command),
			
			# Create new credit.
			CommandHandler('newcredit', self._newcredit_command),
			
			# Handlers on text message.
			MessageHandler(Filters.text, self._text_message),

			# Handle all other message types.
			MessageHandler(Filters.all, self._reply('Invalid: please, send me only text messages!'))
		]

		# Create the Updater and pass it bot's token.
		# Make sure to set use_context=True to use the new context based callbacks.
		self._updater = Updater(token, use_context=True)

		# Get the dispatcher to register handlers.
		dp = self._updater.dispatcher

		# Setup handlers.
		for handler in handlers:
			dp.add_handler(handler)

		# log all errors.
		dp.add_error_handler(self._log_error)
		
		# TODO: temporary!
		# Simple data storage.
		self.storage = Storage()
		
		# List of agents, one per user.
		self.agents = {}

	def start(self):
		self._logger.info('Bot started at {}'.format(datetime.now()))

		# Start the bot.
		self._updater.start_polling()

		# Block until the user presses Ctrl-C or the process receives SIGINT,
		# SIGTERM or SIGABRT. This should be used most of the time, since
		# start_polling() is non-blocking and will stop the bot gracefully.
		self._updater.idle()

	# Wrapper to send a text message.
	@staticmethod
	def _reply(message):
		def inner(update, context):
			return update.message.reply_text(message)
		return inner
	
	# Handles new exam from user.
	def _newexam_command(self, update, context):
		len_of_command = 8
		chat_id = update.message['chat']['id']
		if not self.storage.contains_user(chat_id):
			self.storage.add_user(chat_id)
		
		new_exam = update.message.text[len_of_command:].split(',')
		if len(new_exam) != 3:
			response_message = '''Incorrect exam information.
Format: <Full name>, <Date(dd/mm/yyyy)>, <Time>
Please, try again.'''
		else:
			if self.storage.has_exam(chat_id, new_exam):
				response_message = '{} exam already exists.'.format(new_exam[0].strip())
			else:
				self.storage.add_exam(chat_id, new_exam)
				response_message = 'Successfully added!'
		update.message.reply_text(response_message)

	# Handles new credit from user.
	def _newcredit_command(self, update, context):
		len_of_command = 10
		chat_id = update.message['chat']['id']
		if not self.storage.contains_user(chat_id):
			self.storage.add_user(chat_id)

		new_credit = update.message.text[len_of_command:].split(',')
		if len(new_credit) != 3:
			response_message = '''Incorrect credit information.
Format: <Full name>, <Date(dd/mm/yyyy)>, <Time>
Please, try again.'''
		else:
			if self.storage.has_credit(chat_id, new_credit):
				response_message = '{} credit already exists.'.format(new_credit[0].strip())
			else:
				self.storage.add_credit(chat_id, new_credit)
				response_message = 'Successfully added!'
		update.message.reply_text(response_message)

	# Handles the text message.
	def _text_message(self, update, context):
		chat_id = update.message['chat']['id']
		if chat_id not in self.agents:
			self.agents[chat_id] = Agent(**self.df_config)
		text_to_response = self._process_question(chat_id, update.message.text)
		update.message.reply_text(text_to_response)

	# Logs errors caused by updates.
	def _log_error(self, update, context):
		update.message.reply_text('Oops... Something went wrong...')
		self._logger.warning('Update "%s" caused error "%s"', update, context.error)

	# Process user question using DialogFlow agent.
	def _process_question(self, chat_id, text):
		response = self.agents[chat_id].detect_intent(text)
		if 'course intent' in response['detected_intent'].lower():
			exam = self.storage.get_exam_info(chat_id, text)
			if exam:
				return exam
			credit = self.storage.get_credit_info(chat_id, text)
			if credit:
				return credit
			return 'Information not found, please, try again.'
		else:
			return response['fulfillment_text']
