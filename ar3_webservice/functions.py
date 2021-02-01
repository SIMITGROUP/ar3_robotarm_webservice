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


# show first page info, depends on what we want to show at the list
def index():
    return '{"status":"OK","msg":"Welcome index page of AR3 webservice, you can call /help, /info now"}'


def initSystemVariables():
    global paras
    # define all joint value
    for i in range (0,6):
        maxdeg =paras.jsetting[i]["maxdeg"]
        mindeg =paras.jsetting[i]["mindeg"]
        steplimit = paras.jsetting[i]["steplimit"]
        # J1NegAngLim = float(J1NegAngLimEntryField.get())
        # J1PosAngLim = float(J1PosAngLimEntryField.get())
        # J1StepLim = int(J1StepLimEntryField.get())
        # J1DegPerStep = float((J1PosAngLim - J1NegAngLim) / float(J1StepLim))
        paras.jsetting[i]["degperstep"] = float((maxdeg - mindeg)/float(steplimit))
        print(i,".maxdeg",maxdeg,"mindeg",mindeg,"steplimit",steplimit,"degperstep",paras.jsetting[i]["degperstep"])
        #jointvalue[i]=readJointValue(i)


# rotate joint "jointno" further by @angle degree
def changeJointValue(jointname,degree):
    global hardware
    print("changeJointValue ",jointname," ",str(degree))
    if len(jointname) != 2 or (left(jointname,1) != 'J' and left(jointname,1) != 'j'):
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1/j1 to J6/j6 only"}'

    joint_id = int(right(jointname,1))-1

    if (joint_id < 0 and joint_id > 5):
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1 to J6 only"}'

    previousvalue = -1
    hardware.rotateJoint(joint_id, degree,paras.jsetting)
    # if v.jointvalue.get(jointno) is not None:
    #     previousvalue = v.jointvalue[jointno]
    # else
    #     previousvalue = readEncoderValue(jointno)
    # hardware.rotateJoint(jointno,angle)
    # v.jointvalue[jointno] = angle
    return '{"status":"OK","msg":' + jointname + ' change from '+str(previousvalue)+' to '+str(degree) +' "}'

# define servoname and how much degree to go
def changeServoValue(servoname,degree):
    global hardware
    previousvalue = -1
    if v.servovalue.get(servoname) is not None:
        previousvalue = v.servovalue[servoname]
    hardware.setServo(servoname,degree)
    v.servovalue[servoname] = degree
    return '{"status":"OK","msg":' + servoname + ' change from '+str(previousvalue)+' to '+str(degree) +' "}'

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



try:
    hardware = Hardware(v.teensyport, paras.teensybaudrate, v.arduinoport, paras.arduinobaudrate)
    initSystemVariables()
    print("Try connecting and try")
except Exception as e:
    err_log = log.getMsg("ERR_CONNECT_FAILED01", e)
print("Arm connected")
