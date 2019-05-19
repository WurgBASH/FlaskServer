import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template, make_response
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater,CallbackQueryHandler,RegexHandler,ConversationHandler
import telegram
import apiai, json
from googletrans import Translator
from telegram import ReplyKeyboardMarkup


TOKEN = "710118383:AAFJuBvAtwZ4yWvkjdmBGL6pZb6ocP4e0S4"
PORT = int(os.environ.get('PORT', '8443'))


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
translator = Translator()

msg_RESPONSE = 'ADESQ#$@#s'
name_RESPONSE = 'None'

dex = True

lesson1_button = telegram.InlineKeyboardButton(text='Як встановити Python?',url="https://telegra.ph/YAk-vstanoviti-Python-05-13")
lesson2_button = telegram.InlineKeyboardButton(text='Основи Python',url="https://telegra.ph/Osnovi-Python-05-16")
lesson3_button = telegram.InlineKeyboardButton(text='Рядки в Python',url="https://telegra.ph/Ryadki-v-Python-05-16")

def main_menu(bot, update):
	kb = [[telegram.KeyboardButton('Список уроків')],
			[telegram.KeyboardButton('Тестування')],
			[telegram.KeyboardButton('Посилання на додаткові матеріали')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)

	bot.send_message(chat_id=update.message.chat_id,
					text="Ти хочеш вивчачи Python?",
					reply_markup=kb_markup) 

def handle_message(bot, update):
	global msg_RESPONSE
	global name_RESPONSE
	global dex
	if update.message.text != None:
		dex = False
		msg_RESPONSE =update.message.text
		name_RESPONSE = update.message.chat.first_name
	if update.message.text == 'Список уроків':
		sendingAllLessons(bot, update)
	elif update.message.text == 'Тестування':
		sendingTestingMenu(bot,update)
	elif update.message.text == 'Посилання на додаткові матеріали':
		sendingAdditionalLinks(bot,update)
	elif update.message.text == 'Повернутися до головного меню':
		main_menu(bot, update)
	else:
		request = apiai.ApiAI('a60c7793525a40ac9b5876bfef6590d3').text_request() 
		request.lang = 'ru' 
		request.session_id = 'BatlabAIBot' 
		request.query = update.message.text 
		responseJson = json.loads(request.getresponse().read().decode('utf-8'))
		response = responseJson['result']['fulfillment']['speech']
		msg = translator.translate(response, dest='ukrainian',src='ru').text
		if response:
			bot.send_message(chat_id=update.message.chat_id, text=msg)
		else:
			bot.send_message(chat_id=update.message.chat_id, text='Я вас не розумію!')
	data = {'message': 'Created', 'code': 'SUCCESS'}
	return make_response(jsonify(data), 201)



def sendingAllLessons(bot,update):
	kb = [[telegram.KeyboardButton('Повернутися до головного меню')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	buts =[[lesson1_button],[lesson2_button],[lesson3_button]]
	msg = '<b>Натисни на урок, який ти хочеш вивчити</b>\n'
	bot.send_message(chat_id=update.message.chat_id, text=msg,
							  parse_mode=telegram.ParseMode.HTML,
							  reply_markup=telegram.InlineKeyboardMarkup(buts))

	bot.send_message(chat_id=update.message.chat_id, text='Для кращого вивчення потрібно прочитати всі уроки', reply_markup=kb_markup) 


def sendingTestingMenu(bot,update):
	kb = [[telegram.KeyboardButton('Повернутися до головного меню')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id, text='Цей модуль ще не написаний',
					reply_markup=kb_markup) 

def sendingAdditionalLinks(bot,update):
	kb = [[telegram.KeyboardButton('Повернутися до головного меню')]]
	kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
	bot.send_message(chat_id=update.message.chat_id, text='Цей модуль ще не написаний',
					reply_markup=kb_markup) 


def callback_query_handler(bot, update):
	cqd = update.callback_query.data
	if cqd == l1_cqd:
		bot.send_message(chat_id=update.callback_query.message.chat_id,
					text="https://telegra.ph/YAk-vstanoviti-Python-05-13") 

dispatcher.add_handler(CommandHandler('start', main_menu))


dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
app = Flask(__name__)


def test():
	# updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
	# updater.bot.set_webhook("https://flaskappprogram.herokuapp.com/" + TOKEN)
	# updater.idle()
	updater.start_polling()
	
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/messages',methods=['GET'])
def add_message():
	print('messages was started')
	if (request.headers.get('accept') == 'text/event-stream'):
		def events():
			global msg_RESPONSE
			global name_RESPONSE
			global dex
			while dex==True:
				time.sleep(1)
			yield "data:{\"user_message\":\""+msg_RESPONSE+"\","+"\"user_name\":\""+name_RESPONSE+"\"}\n\n"
			msg_RESPONSE='ADESQ#$@#s'
			dex = True
		return Response(events(), content_type='text/event-stream')
	return redirect(url_for('static', filename='messages.html'))


if __name__ == '__main__':
	t1 = threading.Thread(target=test)
	t1.start()
	app.run()