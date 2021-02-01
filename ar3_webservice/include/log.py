error ={
    "OK":"",
    "ERR_SERVO_MAX": "Servo maximum limit hit",
    "ERR_SERVO_MIN": "Servo minimum limit hit",
    "ERR_CONNECT_FAILED01":"Robot arm serial connection failed",
    "ERR_JOINT_OUT_OF_RANGE":"Invalid joint no",
    "ERR_JOINT_WRONG_DATA_TYPE":"Joint value is not integer",
    "ERR_UNKNOWN_WRITEARM_POSITIONTYPE": "Unknown write arm position type, rest/limit only is supported"

}
# log 1=error/danger, 2 = warning, 3 = simple info, 4 = debug
ERROR = 1
WARNING = 2
INFO = 3
DEBUG = 4
showloglevel = DEBUG

def getMsg(code,e):
    # e standby for suitable environment use
    print(e)
    return {"code": code, "msg": error[code]}

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