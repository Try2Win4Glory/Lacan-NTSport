from flask import Flask
from threading import Thread
from logging import getLogger, ERROR
import time, sys, os
from nitrotype import l
import asyncio
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET', 'HEAD'])#'POST'
def home():
      return 'POG! U looking for me? I\'m right there! Online and running, everything is working smoothly! :-)'
run_time = time.time()
def run():
    app.run(host='0.0.0.0')

def start_server():
    t = Thread(target=run)
    t.start()
def restart_program():
    time.sleep(3600)
    python = sys.executable
    os.execl(python, python, * sys.argv)
start_time = time.time()
thread = Thread(target=restart_program)
thread.start()
'''
from flask import Flask
from waitress import serve
from threading import Thread
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(60).hex()

@app.route('/')
def home():
    return 'Server is ready'

def run():
    serve(app, host='0.0.0.0',port='8080')

def start_server():  
    t = Thread(target=run)
    t.start()
'''