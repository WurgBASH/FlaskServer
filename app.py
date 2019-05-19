import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template, make_response


TOKEN = "710118383:AAFJuBvAtwZ4yWvkjdmBGL6pZb6ocP4e0S4"
PORT = int(os.environ.get('PORT', '8445'))


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
translator = Translator()

msg_RESPONSE = 'ADESQ#$@#s'
name_RESPONSE = 'None'

app = Flask(__name__)

@app.route('/')
def index():
	updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
	updater.bot.set_webhook("https://flaskappprogram.herokuapp.com/" + TOKEN)
	updater.idle()
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

@app.route('/getJSONfromBot',methods=['POST'])
def json_handle():
	print (request.is_json)
	content = request.get_json()
	print (content)

if __name__ == '__main__':
	app.run()