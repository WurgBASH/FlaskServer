import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template, make_response
import telegram
import pymongo
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

msg_RESPONSE = 'ADESQ#$@#s'
name_RESPONSE = 'None'
dex = True
app = Flask(__name__)


bot = telegram.Bot(token="710118383:AAFJuBvAtwZ4yWvkjdmBGL6pZb6ocP4e0S4")


client = pymongo.MongoClient("mongodb+srv://wurg:wurg@pythonacademy-9pn3o.gcp.mongodb.net/test?retryWrites=true")
db = client.get_database('PythonAcademy_db')





@app.route('/')
def index():
	return render_template('index.html')
@app.route('/getJSONfromBot',methods=['POST'])
def json_handle():
	global msg_RESPONSE
	global name_RESPONSE
	global dex
	print('json_handle was started')
	if request.method == 'POST':
		print (request.is_json)
		content = request.get_json()
		print (content)
		if content['message_text'] != None:
			db.messages.insert_one({'user_id': content['user_id'], 'user_name':content['user_nick'], 'first_name':content['user_name'],'message_text':content['message_text']})
			msg_RESPONSE = content['message_text']
			name_RESPONSE = content['user_name']
			dex = False

@app.route('/send_message',methods=['POST'])
def send_message():
	global msg_RESPONSE
	global name_RESPONSE
	global dex
	if request.method == 'POST':
		text = request.form['msg_text']
		bot.send_message(chat_id=781804238, text=text)
		msg_RESPONSE = text
		name_RESPONSE = 'bot'
		dex = False
		return redirect(url_for('static', filename='messages.html'))

@app.route('/messages',methods=['GET'])
def add_message():
	if request.method == 'GET':
		print('messages was started')
		if (request.headers.get('accept') == 'text/event-stream'):
			def events():
				global msg_RESPONSE
				global name_RESPONSE
				global dex
				while dex==True:
					time.sleep(0.1)
				yield "data:{\"user_message\":\""+msg_RESPONSE+"\","+"\"user_name\":\""+name_RESPONSE+"\"}\n\n"
				msg_RESPONSE='ADESQ#$@#s'
				dex = True
			return Response(events(), content_type='text/event-stream')
		return redirect(url_for('static', filename='messages.html'))



if __name__ == '__main__':
	print('dsd')


	app.run()