from flask import Flask,request,render_template
import functions as f
import json

# from flask_apscheduler import APScheduler
# class Config(object):
#     SCHEDULER_API_ENABLED = True

app = Flask(__name__,template_folder = "views")
# app.config.from_object(Config())
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()


# # to avoid something goes wrong, every few second refresh encoder value
# @scheduler.task('interval', id='refresh_position', seconds=3)
#     a=1


@app.route('/')
def index():
    return json.dumps(f.index())

@app.route('/help')
def help():
    return '{"status":"OK","msg":"Hello, this is help, you have nothing!"}'

@app.route('/info')
def info():
    return json.dumps(f.info())

@app.route('/servo')
def servolist():
    return '{"status":"OK","msg":"this will return servo guidance"}'


@app.route('/servo/<servo>')
def moveServo(servo):
    global f
    value =request.args.get("value")
    return json.dumps(f.changeServoValue(servo,value))

@app.route('/move_j')
def joiintlist():
    return '{"status":"OK","msg":"this will return list of stepper motor joint in database"}'

@app.route('/move_j/<jointname>')
def moveJoint(jointname):
    global f
    degree =request.args.get("degree")
    movetype = request.args.get("movetype")
    return json.dumps(f.rotateJoint(jointname,degree,movetype))


@app.route('/move_l')
def movelinear_info():
    return '{"status":"ERR_MOVE_LINEAR","msg":"linear moved is not supported yet"}'

@app.route('/move_l/<axis>')
def movelinear_action(axis):
    mm = request.args.get("mm")
    return json.dumps(f.moveLinear(axis,mm))

@app.route('/movetrack')
def tracklist():
    return '{"status":"ERR_MOVE_LINEAR","msg":"this will return list of command for movetrack"}'

@app.route('/movetrack/<trackname>')
def moveTrack(trackname):
    global f
    mm = request.args.get("mm")
    movetype = request.args.get("movetype")
    return json.dumps(f.moveTrack(trackname,mm,movetype))



@app.route('/calibrate')
def calibratelist():
    return '{"status":"OK","msg":"this will return list of calibration option"}'

@app.route('/calibrate/<jointname>')
def calibrateAction(jointname):
    return json.dumps(f.runCalibration(jointname))

@app.route('/calibratetrack')
def displayCalibrateTrack():
    return '{"status":"OK","msg":"this will return list of calibration track option"}'

@app.route('/calibratetrack/<trackname>')
def calibrateTrack(trackname):
    return json.dumps(f.calibrateTrack(trackname))


@app.route('/movetorestposition')
def moveToRest():
    return json.dumps(f.moveRestPosition([1,1,1,1,1,1]))

@app.route('/getposition')
def runGetPosition():
    return json.dumps(f.getAllPosition())

@app.route('/setposition')
def runSetPosition():
    parameters = request.args
    return json.dumps(f.setPosition(parameters))



## some override setting at below, just ignore it don't change ##
@app.before_request
def before_show():
    # return "OK"
    a=1
    armstatus = f.checkARMConnectionReady()
    if armstatus == "OK":
        result = f.updateJointValue()
    else:
        return armstatus
#

@app.after_request
def apply_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response

