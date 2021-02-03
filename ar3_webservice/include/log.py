errorcodes ={
    "OK":"",
    "ERR_SERVO_MAX": "Servo maximum limit hit",
    "ERR_SERVO_MIN": "Servo minimum limit hit",
    "ERR_CONNECT_FAILED01":"Robot arm serial connection failed",
    "ERR_JOINT_OUT_OF_RANGE":"Invalid joint no",
    "ERR_JOINT_WRONGNAME":"Joint name shall be J1, J2,j1,j2...",

    "ERR_JOINT_WRONG_DATA_TYPE":"Joint value is not integer",
    "ERR_ENCODER_NOREPLY":"No receive response from AR3 joint's encoder",
    "ERR_UNKNOWN_WRITEARM_POSITIONTYPE": "Unknown write arm position type, rest/limit only is supported",
    "ERR_ROTATEJOINT_OVERMAXLIMIT": "One of the joint received rotation request which is over maximum degree limit",
    "ERR_ROTATEJOINT_OVERMINIMIT": "One of the joint received rotation request which is lower then minimum degree limit",
    "ERR_SERIAL_DEVICENOTWRITABLE": "Serial device not writable, you need to restart web services to reconnect serial device",
    "ERR_MOVE_INVALIDTYPE": "Invalid movement type parameter, you shall submit 'move' or 'absolute' into parameter 'movetype' ",
    "ERR_MOVETRACK_OVERLIMIT": "Track movement blocked due to movement over control limit"
}
# log 1=error/danger, 2 = warning, 3 = simple info, 4 = debug
ERROR = 1
WARNING = 2
INFO = 3
DEBUG = 4
showloglevel = WARNING

def getMsg(code,moremsg):
    # e standby for suitable environment use
    print(code+":"+moremsg)
    try:
        msg=""
        if code in errorcodes.keys():
            if moremsg == "":
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