from flask import Flask,request,render_template
from include.Kernel import Kernel
import json

# import functions as f
# from flask_apscheduler import APScheduler
# class Config(object):
#     SCHEDULER_API_ENABLED = True


kern = Kernel()
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
    return json.dumps(kern.api_index())


@app.route('/<methodname>',methods=['GET','POST'])
@app.route('/<methodname>/<resource>',methods=['GET','POST'])
@app.route('/<methodname>/<resource>/<subresource>',methods=['GET','POST'])
def getResource(methodname,resource=None,subresource=None):
    flexibleactionname = 'api_' + methodname

    if request.method == 'GET':
        primaryactionname = 'get_' + methodname
    else:
        primaryactionname = 'post_' + methodname


    if hasattr(kern, primaryactionname):
        actionname=primaryactionname
    elif hasattr(kern, flexibleactionname):
        actionname = flexibleactionname
    else:
        return json.dumps({'status': 'Failed', 'msg': f"method  {primaryactionname} or {flexibleactionname} does not exists"})

    if callable(getattr(kern, actionname)):
        func = getattr(kern, actionname)
        kern.methodname = methodname

        if type(resource) == str:
            resource = resource.lower()
        if type(subresource) == str:
            subresource = subresource.lower()

        kern.resource = resource
        kern.subresource = subresource
        kern.req = request.values
        result = func()
        return json.dumps(result)
    else:
        return json.dumps({'status':'Failed','msg': f"method  {actionname} is not callable function"})

@app.route('/routine',methods=['PUT'])
def putRoutine(routinename):
    result = kern.addRoutine(routinename)
    return json.dumps(result)

@app.route('/routine/<routinename>',methods=['PUT','DELETE'])
def deleteRoutine(routinename):
    if request.method == 'DELETE':
        result = kern.deleteRoutine(routinename)
    elif  request.method == 'PUT':
        result = kern.overrideRoutine(routinename)
    else:
        result = json.dumps( { "status":"Failed" ,"msg":f"routine {routinename} does not exists"})
    return json.dumps(result)





## some override setting at below, just ignore it don't change ##
@app.before_request
def before_show():
    # return "OK"
    a=1
    #armstatus = f.checkARMConnectionReady()
    #if armstatus == "OK":
    #    result = f.updateJointValue()
    #else:
    #    return armstatus
#

@app.after_request
def apply_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response

############### backup of all unused route, will delete afterward ########################


'''
@app.route('/help')
def help():
    return '{"status":"OK","msg":"Hello, this is help, you have nothing!"}'

    # @app.route('/info')
# def info():
#     return json.dumps(f.info())

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
def movelinear_action():
    x = float(request.args.get("x"))
    y = float(request.args.get("y"))
    z = float(request.args.get("z"))
    result = f.moveLinear(x, y, z)
    return json.dumps(result)

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
    limitswitch = request.args.get("limitswitch")
    return json.dumps(f.calibrateTrack(trackname,limitswitch))


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


#########################related the routines #################
# list all routines
@app.route('/routines')
def getRoutines():
    return json.dumps(f.getRoutines())

#get routine info, will verify routine syntax again
@app.route('/routines/<routinename>')
def getRoutineInfo(routinename):
    return json.dumps(f.getRoutineInfo(routinename))

#execute routine
@app.route('/routines/<routinename>/run')
def runRoutines(routinename):
    return json.dumps(f.runRoutine(routinename))


#delete routine, failed if it not exists
@app.route('/routines/<routinename>/delete')
def deleteRoutines(routinename):
    return json.dumps(f.deleteRoutine(routinename))

#upload routine file, override existing. failed if it not exists or syntax error
@app.route('/routines/override')
def overrideRoutine():
    return json.dumps(f.overrideRoutine())

#add new routine file, failed if there is existing or syntax error
@app.route('/routines/addnew')
def addRoutine():
    return json.dumps(f.addRoutine())





@app.route('/beep')
def beepInfo():
    return '{"status":"OK","msg":"this will beep function command"}'

@app.route('/beep/<onoff>')
def runBeep(onoff):
    return json.dumps(f.runBeep(onoff))


'''