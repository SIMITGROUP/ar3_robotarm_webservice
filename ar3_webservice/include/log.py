errorcodes ={
    "OK":"",
    "ERR_SERVO_MAX": "Servo maximum limit hit",
    "ERR_SERVO_MIN": "Servo minimum limit hit",
    "ERR_SERVO_INVALIDVALUE": "You shall submit integer or name of position using variable 'value'",
    "ERR_SERVO_INVALIDSERVO": "Servo name not exists in servo database",
    "ERR_TRACK_INVALID": "Track name not exists in track database",
    "ERR_MOVE_INVALIDMM":"parameter mm is undefined",
    "ERR_MOVEL_UNDEFINEDPARA":"undefined 1 or more parameter of x,y,z",
    "ERR_SETSPEED_UNDEFINEDVALUE":"speed undefined",
    "ERR_KINEMATIC_UNDEFINEMATRIX": "undefine kinematic value (t_matrix), put initHardwareConnection = True in Hardware.py and restart web service",
    "ERR_CONNECT_FAILED01":"Robot arm serial connection failed",
    "ERR_SETPOSITION_NOPARA":"no parameter assigned (j1-j6, servos, tracks), workable example: /setposition?j1=10&j2=10&j3=10&j4=10&j5=10&j6=10&t1=20&gripper1=20",
    "ERR_JOINT_OUT_OF_RANGE":"Invalid joint no",
    "ERR_JOINT_WRONGNAME":"Joint name shall be J1, J2,j1,j2...",
    "ERR_JOINT_NODEGREEDEFINED":"Parameter degree undefined",
    "ERR_JOINT_WRONG_DATA_TYPE":"Submited value is not number",
    "ERR_TRACK_WRONG_DATA_TYPE":"Submited value is not number",
    "ERR_ENCODER_NOREPLY":"No receive response from AR3 joint's encoder",
    "ERR_UNKNOWN_WRITEARM_POSITIONTYPE": "Unknown write arm position type, rest/limit only is supported",
    "ERR_ROTATEJOINT_OVERMAXLIMIT": "One of the joint received rotation request which is over maximum degree limit",
    "ERR_ROTATEJOINT_OVERMINIMIT": "One of the joint received rotation request which is lower then minimum degree limit",
    "ERR_SERIAL_DEVICENOTWRITABLE": "Serial device not writable, you need to restart web services to reconnect serial device",
    "ERR_MOVE_INVALIDTYPE": "Invalid movement type parameter, you shall submit 'move' or 'absolute' into parameter 'movetype' ",
    "ERR_MOVETRACK_OVERLIMIT": "Track movement blocked due to movement over control limit",
    "ERR_MOVE_LINEAR":"Linear movement is not supported at the moment",
    "ERR_ROUTINE_INVALIDJSON":"Routine content cannot parse to json",
    "ERR_ROUTINE_UNDEFINESUBROUTINE":"Sub routine undefined",
    "ERR_UNDEFINED_SUBROUTINEUNDEFINETYPE":"There is 1 or more task in sub routine undefine type",
    "ERR_UNDEFINED_SUBROUTINEWRONGTYPE":"There is 1 or more task in sub routine use unsupported type",
    "ERR_SUBROUTINE_CALL_SUBROUTINEUNDEFINED":"There is 1 or more call task undefined subroutine",
    "ERR_SUBROUTINE_UNSUPPORTMOVETYPE":"Sub routine movetype is not supported"
}
# log 1=error/danger, 2 = warning, 3 = simple info, 4 = debug
ERROR = 1
WARNING = 2
INFO = 3
DEBUG = 4
showloglevel = DEBUG

def getMsg(code,moremsg):
    # e standby for suitable environment use
    print(code+":"+moremsg)
    try:
        msg=""
        if code in errorcodes.keys():
            if moremsg == "":
                msg = errorcodes[code]
            elif  errorcodes[code] == "":
                msg = moremsg
            else:
                msg = errorcodes[code]+', '+moremsg
        else:
            msg = moremsg
        return {"code": code, "msg":msg}
    except Exception as e:
        print(e)
        return {"code": code, "msg": 'System cannot provide more detail description'}

def returnJSON(texttowrite):
    return  texttowrite


## use to print console at terminal only, not display at web ##
def showLog(level,t):
    if showloglevel >= level:
        print(t)

def info(t):
    showLog(INFO,t)

def warning(t):
    showLog(WARNING,t)

def error(t):
    showLog(ERROR,t)


def debug(t):
    showLog(DEBUG,t)