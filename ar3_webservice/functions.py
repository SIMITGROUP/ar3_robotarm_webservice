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
import calculation as calc
# import webbrowser
# import pickle
err_log = {}
try:
    hardware = Hardware(v.teensyport, paras.teensybaudrate, v.arduinoport, paras.arduinobaudrate)
    print("Try connecting and try")
except Exception as e:
    err_log = log.getMsg("ERR_CONNECT_FAILED01", e)
print("Arm connected")

# show first page info, depends on what we want to show at the list
def index():
    return '{"status":"OK","msg":"Welcome index page of AR3 webservice, you can call /help, /info now"}'


def initSystemVariables():
    # define all joint value
    for i in range (0,5):
        jointvalue[i]=readJointValue(i)


# rotate joint "jointno" further by @angle degree
def changeJointValue(jointno,angle):
    global hardware

    print("changeJointValue 1")
    if len(jointno) != 2 or  left(jointno,1) != 'J':
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1 to J6 only"}'

    joint_id = int(right(jointno,1))

    if (joint_id < 1 and joint_id > 6):
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1 to J6 only"}'

    previousvalue = -1
    hardware.rotateJoint(joint_id, angle)
    # if v.jointvalue.get(jointno) is not None:
    #     previousvalue = v.jointvalue[jointno]
    # else
    #     previousvalue = readEncoderValue(jointno)
    # hardware.rotateJoint(jointno,angle)
    # v.jointvalue[jointno] = angle
    return '{"status":"OK","msg":' + jointno + ' change from '+str(previousvalue)+' to '+str(angle) +' "}'

# define servoname and how much degree to go
def changeServoValue(servoname,angle):
    global hardware
    previousvalue = -1
    if v.servovalue.get(servoname) is not None:
        previousvalue = v.servovalue[servoname]
    hardware.setServo(servoname,angle)
    v.servovalue[servoname] = angle
    return '{"status":"OK","msg":' + servoname + ' change from '+str(previousvalue)+' to '+str(angle) +' "}'

#  specifically  read joint encoder value, convert become angle
def readEncoderValue(jointno):
    hardware.readEncoderValue(jointno)

def readJointValue(jointno):
    return 0

# convert step no to human readable degree
def convertStepNoToDegree(stepno):
    global calc
    return calc.getDegreeFromStep()

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]