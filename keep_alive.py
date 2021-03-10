'''from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def main():
    return print("Your bot is alive!")
def run():
    app.run(host="0.0.0.0", port=8080) 4692
def keep_alive():
    server = Thread(target=run)
    server.start()'''


from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=4692) #4692 #1151

def keep_alive():
    t = Thread(target=run)
    t.start()