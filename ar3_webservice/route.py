from flask import Flask,request
import functions as f
import json

app = Flask(__name__)
@app.route('/')
def index():
    return f.index()

@app.route('/help')
def help():
    return '{"status":"OK","msg":"Hello, this is help, you have nothing!"}'

@app.route('/info')
def info():
    return '{"status":"OK","msg":"Hello, this is info, you have more then hello world!"}'

@app.route('/servo')
def servolist():
    return '{"status":"OK","msg":"this will return list of servo in database"}'

@app.route('/servo/<servo>')
def moveServo(servo):
    global f
    angle = request.args.get("angle")
    return f.changeServoValue(servo,angle)

@app.route('/move_j')
def joiintlist():
    return '{"status":"OK","msg":"this will return list of stepper motor joint in database"}'

@app.route('/move_j/<jointno>')
def moveJoint(jointno):
    global f
    angle = request.args.get("angle")
    return f.changeJointValue(jointno,angle)

## some override setting at below, just ignore it don't change ##
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
