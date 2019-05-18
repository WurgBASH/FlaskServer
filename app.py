import threading,os,sys,socket
import time
from flask import Flask, Response, redirect, request, url_for, jsonify,render_template

users= {}
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def add_message():
	if request.method == "POST":
		content = request.json
		users[text2] = content['message']
		return render_template('index.html', users=users)
	else:
		return render_template('index.html', users=users)

if __name__ == '__main__':
	app.run()