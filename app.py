import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template, make_response


msg_RESPONSE = 'ADESQ#$@#s'
name_RESPONSE = 'None'
dex = True
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
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
					time.sleep(1)
				yield "data:{\"user_message\":\""+msg_RESPONSE+"\","+"\"user_name\":\""+name_RESPONSE+"\"}\n\n"
				msg_RESPONSE='ADESQ#$@#s'
				dex = True
			return Response(events(), content_type='text/event-stream')
		return redirect(url_for('static', filename='messages.html'))

@app.route('/getJSONfromBot',methods=['POST'])
def json_handle():
	global msg_RESPONSE
	global name_RESPONSE
	global dex
	print('json_handle was started')
	if request.method == 'POST':
		dex = False
		print (request.is_json)
		content = request.get_json()
		print (content)
		msg_RESPONSE = content['message_text']
		name_RESPONSE = content['user_name']

if __name__ == '__main__':
	app.run()