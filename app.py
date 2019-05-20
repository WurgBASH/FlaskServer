import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect,Namespace
import telegram
import pymongo
import logging
import json
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


async_mode = None
dex = False
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


bot = telegram.Bot(token="710118383:AAFJuBvAtwZ4yWvkjdmBGL6pZb6ocP4e0S4")


client = pymongo.MongoClient("mongodb+srv://wurg:wurg@pythonacademy-9pn3o.gcp.mongodb.net/test?retryWrites=true")
db = client.get_database('PythonAcademy_db')



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/getJSONfromBot',methods=['POST'])
def json_handle():
	print('json_handle was started')
	if request.method == 'POST':
		content = request.get_json()
		if content['message_text'] != None:
			socketio.emit('my_response',
                      {'text':content['message_text'] , 'user': content['user_name']},
                      namespace='/test')
			db.messages.insert_one({'user_id': content['user_id'], 'user_name':content['user_nick'], 'first_name':content['user_name'],'message_text':content['message_text']})

@app.route('/send_message',methods=['POST'])
def send_message():
	if request.method == 'POST':
		text = request.form['msg_text']
		bot.send_message(chat_id=781804238, text=text)
		return redirect(url_for('static', filename='messages.html'))

@app.route('/messages',methods=['GET','POST'])
def add_message():
	#if request.method == 'GET':
	return render_template('messages.html', async_mode=socketio.async_mode)
	# else:
	# 	data = {}
	# 	ges = db.messages.count()
	# 	res = db.messages.find()
	# 	for x in res:

	# 		nam=[]
	# 		for key,val in x.items():
	# 			if(key=='first_name'):
	# 				nam.append(val)
	# 				#data[val] = []
	# 			elif(key == 'message_text'):
	# 				nam.append(val)
	# 				#data[val].append(val)
	# 		if nam[0] in data:
	# 			data[nam[0]].append(nam[1])
	# 		else:
	# 			data[nam[0]] = [nam[1]]
	# 	print(data)
	# 	return json.dumps(data)


if __name__ == '__main__':
	socketio.run(app)
	