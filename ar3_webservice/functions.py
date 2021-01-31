## this file define actual execution of the program ##
import sys
sys.path.append("include")

from Hardware import Hardware
import time
import threading
import queue
import math
import numpy as np
import datetime
import log
import armparameters as paras

import values as v


# import webbrowser
# import pickle
err_log = {}
try:
    hardware = Hardware(v.teensyport, paras.teensybaudrate, v.arduinoport, paras.arduinobaudrate)
    print("Try connecting and try")
except Exception as e:
    err_log = log.getMsg("ERR_CONNECT_FAILED01", e)
print("Arm connected")




def index():
    return '{"status":"OK","msg":"Welcome index page of AR3 webservice, you can call /help, /info now"}'

def connectHardwares():
    global hardware
    return True

def changeServoValue(servoname,angle):
    global hardware
    connectHardwares()
    previousvalue = -1
    if v.servovalue.get(servoname) is not None:
        previousvalue = v.servovalue[servoname]
    hardware.setServo(servoname,angle)
    v.servovalue[servoname] = angle
    return '{"status":"OK","msg":' + servoname + ' change from '+str(previousvalue)+' to '+str(angle) +' "}'



