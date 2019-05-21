from gevent import monkey
monkey.patch_all()
import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template, make_response
import telegram
import pymongo
import logging
import json
from flask_socketio import SocketIO,emit



app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, async_handlers=True)
bot = telegram.Bot(token="710118383:AAFJuBvAtwZ4yWvkjdmBGL6pZb6ocP4e0S4")

#---------------------------------------------

client = pymongo.MongoClient("mongodb+srv://wurg:wurg@pythonacademy-9pn3o.gcp.mongodb.net/test?retryWrites=true")
db = client.get_database('PythonAcademy_db')

#---------------------------------------------

def GetUserId(user_name):
	res = db.messages.find({'user_name': user_name})
	for x in res:
		return x['user_id']

#---------------------------------------------

def GetAllUsers():
	users={}
	res = db.messages.find()
	for x in res:
		nam =[]
		for key,val in x.items():
			if(key=='user_name'):
				nam.append(val)
			elif (key=='first_name'):
				nam.append(val)

		if nam[0] not in users:
			users[nam[0]] = nam[1]
	return users

#---------------------------------------------

def GetAllMessage():
	messsagesFrom = {}
	res = db.messages.find()
	dex=True
	for x in res:
		nam=[]
		for key,val in x.items():
			if  (key == 'bot_bool'):
				dex = False
			elif (key == 'user_name'):
				nam.append(val)
			elif (key=='first_name'):
				if dex:
					nam.append(val)	
				else:
					nam.append('Бот')
					dex=False
			elif(key == 'message_text'):
				nam.append(val)

		if nam[0] in messsagesFrom:
			messsagesFrom[nam[0]].append({nam[1]:nam[2]})
		else:
			messsagesFrom[nam[0]] = [{nam[1]:nam[2]}]
	return messsagesFrom

#---------------------------------------------

@app.route('/')
def index():
	return render_template('index.html')

#---------------------------------------------

@app.route('/getJSONfromBot',methods=['POST'])
def json_handle():
	print('json_handle was started')
	if request.method == 'POST':
		content = request.get_json()
		if content['message_text'] != None:
			db.messages.insert_one({'user_id': content['user_id'], 'user_name':content['user_nick'], 'first_name':content['user_name'],'message_text':content['message_text']})
			socketio.emit('my_response', {'user_name':content['user_name'],'message_text':content['message_text'],'user_nick':content['user_nick']},namespace='/test')
	return 'okay'
#---------------------------------------------

@app.route('/getJSONBOTfromBot',methods=['POST'])
def jsonbot_handle():
	print('json_handle was started')
	if request.method == 'POST':
		content = request.get_json()
		if content['message_text'] != None:
			db.messages.insert_one({'bot_bool': 'bot','user_id': content['user_id'], 'user_name':content['user_nick'], 'first_name':content['user_name'],'message_text':content['message_text']})
			socketio.emit('bot_msg', {'user_name':content['user_name'],'message_text':content['message_text'],'user_nick':content['user_nick']},namespace='/test')
	return 'okay'	

#---------------------------------------------

@app.route('/messages',methods=['GET','POST'])
def add_message():
	return render_template('messages.html', async_mode=socketio.async_mode, users=GetAllUsers(), messages = GetAllMessage())

#---------------------------------------------

@socketio.on('connect', namespace='/test')
def test_connect():
	emit('connected', {'data': 'Connected'})

#---------------------------------------------

@socketio.on('send_message', namespace='/test')
def sending(mes):
	cht_id=GetUserId(mes['username'])
	users = db.messages.find({'user_id':cht_id}).limit(1) 
	user =users[0]
	db.messages.insert_one({'user_id': user['user_id'], 'user_name':user['user_name'], 'first_name':user['first_name'],'message_text':mes['message_text']})
	socketio.emit('bot_msg', {'user_name':user['first_name'],'message_text':mes['message_text'],'user_nick':user['user_name']},namespace='/test')

	bot.send_message(chat_id=cht_id, text=mes['message_text'])





if __name__ == '__main__':
	socketio.run(app)
	