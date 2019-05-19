import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater,CallbackQueryHandler,RegexHandler,ConversationHandler
import telegram

TOKEN = "710118383:AAFJuBvAtwZ4yWvkjdmBGL6pZb6ocP4e0S4"
PORT = int(os.environ.get('PORT', '8443'))

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

text = 'testing'

def handle_message1(bot, update):
	global text
	text =update.message.text



dispatcher.add_handler(MessageHandler(Filters.text, handle_message1))

app = Flask(__name__)

@app.route('/')
def add_message():
	global text
	updater.start_polling()

	if request.headers.get('accept') == 'text/event-stream':
		def events():
			yield "data: %s\n\n" % (text)
			time.sleep(.5)
		return Response(events(), content_type='text/event-stream')
	return redirect(url_for('static', filename='index.html'))


if __name__ == '__main__':
	app.run()