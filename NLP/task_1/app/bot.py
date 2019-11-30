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
			CommandHandler('newexam', self._make_new_course_command(8, 'exam')),
			
			# Create new credit.
			CommandHandler('newcourse', self._make_new_course_command(10, 'credit')),
			
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
	
	# Makes new course handler.
	def _make_new_course_command(self, cmd_len, typ_):
		def inner(update, context):
			len_of_command = cmd_len
			chat_id = update.message['chat']['id']
			if not self.storage.has_user(chat_id):
				self.storage.add_user(chat_id)
			
			new_course = update.message.text[len_of_command:].split(',')
			if len(new_course) != 3:
				response_message = '''Incorrect format.

Format: <Full name>, <Date(dd/mm/yyyy)>, <Time>

Please, try again.'''.format(typ_)
			else:
				if typ_ == 'exam':
					fn_has = self.storage.has_exam
					fn_add = self.storage.add_exam
				else:
					fn_has = self.storage.has_credit
					fn_add = self.storage.add_credit
				if fn_has(chat_id, new_course):
					response_message = '{} course already exists.'.format(new_course[0].strip())
				else:
					fn_add(chat_id, new_course)
					response_message = 'A new course is added successfully!'
			update.message.reply_text(response_message)
		return inner

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
		detected_intent = response['detected_intent'].lower()
		if 'course intent' in detected_intent:
			exam = self.storage.get_exam_info(chat_id, text)
			if exam:
				return exam
			credit = self.storage.get_credit_info(chat_id, text)
			if credit:
				return credit
			return 'Information not found, please, try again.'
		elif 'exams intent' in detected_intent:
			if self.storage.has_user(chat_id):
				return 'Your exams for current term:\n{}'.format(self.storage.get_exams(chat_id))
			return 'You have not added any exams yet.'
		elif 'university courses intent' in detected_intent:
			if self.storage.has_user(chat_id):
				return 'Your courses for current term:\n{}'.format(self.storage.get_courses(chat_id))
			return 'You have not added any courses yet.'
		else:
			return response['fulfillment_text']
