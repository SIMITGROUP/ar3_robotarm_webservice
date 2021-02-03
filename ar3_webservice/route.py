from flask import Flask,request
import functions as f
import json

# from flask_apscheduler import APScheduler
# class Config(object):
#     SCHEDULER_API_ENABLED = True



app = Flask(__name__)
# app.config.from_object(Config())
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()


# # to avoid something goes wrong, every few second refresh encoder value
# @scheduler.task('interval', id='refresh_position', seconds=3)
#     a=1


@app.route('/')
def index():
    return f.index()

@app.route('/help')
def help():
    return '{"status":"OK","msg":"Hello, this is help, you have nothing!"}'

@app.route('/info')
def info():
    return f.info()

@app.route('/servo')
def servolist():
    return '{"status":"OK","msg":"this will return list of servo in database"}'


@app.route('/servo/<servo>')
def moveServo(servo):
    global f
    degree =int(request.args.get("degree"))
    return f.changeServoValue(servo,degree)

@app.route('/move_j')
def joiintlist():
    return '{"status":"OK","msg":"this will return list of stepper motor joint in database"}'

@app.route('/move_j/<jointname>')
def moveJoint(jointname):
    global f
    degree =request.args.get("degree")
    movetype = request.args.get("movetype")
    return f.rotateJoint(jointname,degree,movetype)

@app.route('/movetrack')
def tracklist():
    return '{"status":"OK","msg":"this will return list of command for movetrack"}'

@app.route('/movetrack/<trackname>')
def moveTrack(trackname):
    global f
    mm = request.args.get("mm")
    movetype = request.args.get("movetype")
    print("test ok")
    return f.moveTrack(trackname,mm,movetype)





@app.route('/calibrate')
def calibratelist():
    return '{"status":"OK","msg":"this will return list of calibration option"}'

@app.route('/calibrate/<jointname>')
def calibrateAction(jointname):
    return f.runCalibration(jointname)

@app.route('/calibratetrack')
def calibrateTrack():
    return f.calibrateTrack()


@app.route('/movetorestposition')
def moveToRest():
    return f.moveRestPosition([1,1,1,1,1,1])

## some override setting at below, just ignore it don't change ##
@app.before_request
def before_show():
    armstatus = f.checkARMConnectionReady()
    if  f.checkARMConnectionReady() == "OK":
        return f.updateJointValue()
    else:
        return f.checkARMConnectionReady()


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response

