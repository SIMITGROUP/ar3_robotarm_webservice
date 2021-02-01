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

def info():
    result = hardware.checkMachineStatus()

    return result

def initSystemVariables():
    global paras
    # define all joint value
    for i in range (0,paras.jointqty):
        maxdeg =paras.jsetting[i]["maxdeg"]
        mindeg =paras.jsetting[i]["mindeg"]
        steplimit = paras.jsetting[i]["steplimit"]
        # J1NegAngLim = float(J1NegAngLimEntryField.get())
        # J1PosAngLim = float(J1PosAngLimEntryField.get())
        # J1StepLim = int(J1StepLimEntryField.get())
        # J1DegPerStep = float((J1PosAngLim - J1NegAngLim) / float(J1StepLim))
        paras.jsetting[i]["degperstep"] = float((maxdeg - mindeg)/float(steplimit))
        #print(i,".maxdeg",maxdeg,"mindeg",mindeg,"steplimit",steplimit,"degperstep",paras.jsetting[i]["degperstep"])
        #jointvalue[i]=readJointValue(i)


# rotate joint "jointno" further by @angle degree
def rotateJoint(jname,degree):
    global paras
    if type(degree) is str:
        degree = int(degree)


    jointname = jname.upper()

    if len(jointname) != 2 and left(jointname,1) != 'J':
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1/j1 to J6/j6 only"}'

    joint_id = int( right(jointname,1) ) - 1

    if joint_id < 0 and joint_id > paras.jointqty :
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1 to J6 only"}'

    previousvalue = -1
    hardware.rotateJoint(joint_id, degree)
    if v.jointvalue.get(joint_id) is not None:
        previousvalue = v.jointvalue[joint_id]
    else:
        previousvalue = readEncoderValue(joint_id)

    newvalue = v.jointvalue[joint_id] + degree
    v.jointvalue[joint_id] = newvalue
    return '{"status":"OK","msg":' + jointname + ' change from '+str(previousvalue)+' to '+str(degree) +', become '+ str(newvalue) +'"}'


def setJointAbsoluteDegree(jname,degree):
    if type(degree) is str:
        degree = int(degree)


    jointname = jname.upper()

    if len(jointname) != 2 and left(jointname,1) != 'J':
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1/j1 to J6/j6 only"}'

    joint_id = int( right(jointname,1) ) - 1

    if joint_id < 0 and joint_id > 5 :
        return '{"status":"Failed","msg": "Joint [' + jointno + '] is invalid value, you shall supply joint with from J1 to J6 only"}'

    previousvalue = -1
    hardware.rotateJoint(joint_id, degree)
    if v.jointvalue.get(joint_id) is not None:
        previousvalue = v.jointvalue[joint_id]
    else:
        previousvalue = readEncoderValue(joint_id)

    newvalue = v.jointvalue[joint_id] + degree
    v.jointvalue[joint_id] = newvalue
    return '{"status":"OK","msg":' + jointname + ' change from '+str(previousvalue)+' to '+str(degree) +', become '+ str(newvalue) +'"}'


# define servoname and how much degree to go
def changeServoValue(servoname,degree):
    global hardware
    previousvalue = -1
    if v.servovalue.get(servoname) is not None:
        previousvalue = v.servovalue[servoname]
    hardware.setServo(servoname,degree)
    v.servovalue[servoname] = degree
    return '{"status":"OK","msg":' + servoname + ' change from '+str(previousvalue)+' to '+str(degree) +' "}'


# run calibration task, either calibrate all=all joint, or single joint (J1,J2...)
def runCalibration(jname):
    global err_log, paras
    jointname = jname.upper()
    result = ""
    if jointname == "SETREST":
        result = hardware.writeARMPosition('rest')
    elif len(jointname) == 2 and left(jointname,1)=='J':
        jointno = int(right(jname,1)) -1
        result = hardware.calibrateJoint(jointno)
        log.debug(result)
    elif jointname == 'ALL':
        joints = [1, 1, 1, 1, 1, 1]
        result = hardware.goAllJointLimit(joints)
        hardware.moveFromLimitToRestPosition(joints)
        if result != "OK":
            return log.getMsg(result, "Cannot move all joint into limit switch")
    else:
        return log.getMsg("ERR_CALIBRATE_FAILED01", "Invalid calibration joint name "+jointname)

    # all success result return here
    return '{"code":"OK","msg":""}' #log.getMsg("OK", "");



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
    initSystemVariables()
    print("after init system variables")
    hardware = Hardware(v, paras)
    print("hardware type=",type(hardware))
    print("Try connecting and try")
    print("Arm connected")
except Exception as e:
    err_log = log.getMsg("ERR_CONNECT_FAILED01", e)
    print("Failed connect arm ", e)
