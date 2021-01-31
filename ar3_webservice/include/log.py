error ={
    "ERR_SERVO_MAX": "Servo maximum limit hit",
    "ERR_SERVO_MIN": "Servo minimum limit hit",
    "ERR_CONNECT_FAILED01":"Robot arm serial connection failed",
}


def getMsg(code,e):
    # e standby for suitable environment use
    print(e)
    return {"code": code, "msg": error[code]}
