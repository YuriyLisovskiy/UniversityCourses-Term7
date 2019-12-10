from datetime import datetime

from luis_agent import intents
from app.storage import Storage
from luis_agent.agent import LUISAgent
from app.logger import logger as log

from telegram.ext.filters import Filters
from telegram.ext import Updater, MessageHandler, CommandHandler


# Bot wrapper for telegram bot API.
class UniversityAssistanceBot:
	
	def __init__(self, token, luis_config):
		
		# Configuration for LUIS agent.
		assert luis_config is not None
		self.df_config = luis_config
		
		# Available bot handlers, order is required.
		handlers = [
			
			# Handlers on standard bot's commands.
			# Bot will answer using a default DialogFlow responses.
			CommandHandler('start', self._text_message),
			CommandHandler('stop', self._text_message),
			CommandHandler('help', self._text_message),
			
			# Create new exam command.
			CommandHandler('newexam', self._make_new_course_command(8, 'exam')),
			
			# Create new course which is not an exam.
			CommandHandler('newcourse', self._make_new_course_command(10, 'credit')),
			
			# Handlers on text message.
			MessageHandler(Filters.text, self._text_message),
			
			# Handle all other message types, i.e. stickers, emoji, gifs, etc.
			MessageHandler(Filters.all, self._reply('Invalid: please, send me only text messages and valid commands!'))
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
		
		self.agent = LUISAgent(**luis_config)
	
	def start(self):
		log.info('Bot started at {}'.format(datetime.now()))
		
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
		text_to_response = self._process_question(chat_id, update.message.text)
		update.message.reply_text(text_to_response)
	
	# Logs errors caused by updates.
	@staticmethod
	def _log_error(update, context):
		update.message.reply_text('Oops... Something went wrong...')
		log.warning('Update "%s" caused error "%s"', update, context.error)
	
	# Process user question using LUIS agent.
	def _process_question(self, chat_id, text):
		response = self.agent.analyze(text)
		detected_intent = response['intent'].lower()
		log.info(detected_intent)

		# Return when University Courses intent is triggered.
		def university_courses():
			if self.storage.has_user(chat_id):
				courses = self.storage.get_courses(chat_id)
				if courses != '':
					return 'Your courses for current term:\n{}'.format(courses)
			return 'You have not added any courses yet.'
		
		# TODO: retrieve exam name from response!
		# Return when Course intent is triggered.
		def course():
			course_name = response['entities'][0]['name'].lower()
			exam = self.storage.get_exam_info(chat_id, course_name)
			if exam:
				return exam
			credit = self.storage.get_credit_info(chat_id, course_name)
			if credit:
				return credit
			return 'Information not found, please, try again.'
		
		# Return when Exams intent is triggered.
		def exams():
			if self.storage.has_user(chat_id):
				exams_res = self.storage.get_exams(chat_id)
				if exams_res != '':
					return 'Your exams for current term:\n{}'.format(exams_res)
			return 'You have not added any exams yet.'
		
		# Return when Bot Information intent is triggered.
		def bot_info():
			return """I'm your university assistant =)
You can ask me about your current courses and exams.

Add course:
/newcourse <Full name>, <Date(dd/mm/yyyy)>, <Time>

Add exam:
/newexam <Full name>, <Date(dd/mm/yyyy)>, <Time>"""

		return {
			# Welcome intent handler.
			intents.WELCOME_INTENT: LUISAgent.welcome_response,
			
			# University Courses intent handler.
			intents.UNIVERSITY_COURSES_INTENT: university_courses,
			
			# Course intent handler.
			intents.COURSE_INTENT: course,
			
			# Exams intent handler.
			intents.EXAMS_INTENT: exams,
			
			# Bot Information intent handler.
			intents.BOT_INFO_INTENT: bot_info,
			
			# Gratitude intent handler.
			intents.GRATITUDE_INTENT: LUISAgent.gratitude_response
			
		}.get(detected_intent, LUISAgent.fallback_response)()
