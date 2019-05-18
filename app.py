import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template

text1 ='Nothing'
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def add_message():
	global text1
	if request.method == "POST":
		content = request.json
		text1=content['mytext']
		return render_template('hello.html', text=text1)
	else:
		return render_template('hello.html', text=text1)

if __name__ == '__main__':
	app.run()