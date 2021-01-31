from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '{"status":"OK","msg":"Welcome index page of AR3 webservice, you can call /help, /info now"}'

@app.route('/help')
def help():
    return '{"status":"OK","msg":"Hello, this is help, you have nothing!"}'

@app.route('/info')
def info():
    return '{"status":"OK","msg":"Hello, this is info, you have more then hello world!"}'
