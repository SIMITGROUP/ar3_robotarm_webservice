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
import json
# import webbrowser
# import pickle
err_log = {}

# show first page info, depends on what we want to show at the list
def index():
    return '{"status":"OK","msg":"Welcome index page of AR3 webservice, you can call /help, /info now"}'

def info():
    result1 = json.dumps(hardware.checkMachineStatus())
    result2 = hardware.checkAllBoard()
    return result2
def checkARMConnectionReady():
    print("checkARMConnectionReady")
    result = hardware.checkAllBoard()
    print("result",result)
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
        paras.jsetting[i]["degperstep"] = round( float((maxdeg - mindeg)/float(steplimit)),8)
        #print(i,".maxdeg",maxdeg,"mindeg",mindeg,"steplimit",steplimit,"degperstep",paras.jsetting[i]["degperstep"])
        #jointvalue[i]=readJointValue(i)


# rotate joint "jointno" further by @angle degree
def rotateJoint(jname,degree):
    global paras
    if type(degree) is str:
        degree = float(degree)

    jointname = jname.upper()

    if len(jointname) != 2 and left(jointname,1) != 'J' :
        return log.getMsg('ERR_JOINT_WRONGNAME','Joint name shall be J1, J2,j1,j2...')

    joint_id = int( right(jointname,1) ) - 1

    if joint_id < 0 and joint_id > paras.jointqty :
        return log.getMsg('ERR_JOINT_OUT_OF_RANGE','')
    encoders = hardware.refreshStepperMotorEncoderValue()
    newdegree = encoders[joint_id]['degree'] + degree
    newdegreestr = str(newdegree)
    result = hardware.rotateJoint(joint_id, degree)

    maxdegstr = str(paras.jsetting[joint_id]["maxdeg"])
    mindegstr = str(paras.jsetting[joint_id]["mindeg"])

    if result != 'OK':
        jsondata = log.getMsg(result, jname+" shift "+ str(degree) + " become "+ newdegreestr+" which is not within "+mindegstr+"/"+maxdegstr)
    else:
        jsondata = log.getMsg(result,jname+" shift "+ str(degree) + " become "+ newdegreestr+ " which is within "+mindegstr+"/"+maxdegstr)
    return jsondata


# define servoname and how much degree to go
def changeServoValue(servoname,degree):
    global hardware
    hardware.setServo(servoname,degree)
    return log.getMsg("OK","")


# run calibration task, either calibrate all=all joint, or single joint (J1,J2...)
def runCalibration(jname):
    global err_log, paras
    jointname = jname.upper()
    result = ""
    if jointname == "SETREST":
        result = hardware.writeARMPosition('rest',[1,1,1,1,1,1])
    elif len(jointname) == 2 and left(jointname,1)=='J':
        jointno = int(right(jname,1)) -1
        result = hardware.calibrateJoint(jointno)
        log.debug(result)
    elif jointname == 'ALL':
        joints = [1, 1, 1, 1, 1, 1]
        # joints = [1, 0,0,0,0,0]
        result = hardware.goAllJointLimit(joints)
        # hardware.moveFromLimitToRestPosition(alljoints)
        result2 = moveRestPosition()
        if result != "OK":
            return log.getMsg(result, "Cannot move all joint into limit switch")
    else:
        return log.getMsg("ERR_CALIBRATE_FAILED01", "Invalid calibration joint name "+jointname)
    # all success result return here
    return '{"code":"OK","msg":""}' #log.getMsg("OK", "");

# move arm's joints to rest positions
def moveRestPosition():
    alljoints = [1,1,1,1,1,1]
    # alljoints = [1, 0,0,0,0,0]
    return hardware.moveFromLimitToRestPosition(alljoints)

def updateJointValue():
    encodervalue = hardware.refreshStepperMotorEncoderValue()
    # result: b'00 000000 A7995 B2321 C9 D7594 E2277 F3308\r\n'
    #  01 100000 A7996 B2321 C9 D7594 E2277 F3308

# move travel track "distance " to "distance" mm
def moveTrack(trackname,distance):
    a=1
    # if JogStepsStat.get() == 1:
    #     TrackSteps = TrackjogEntryField.get()
    # else:
    #     TrackSteps = str(int((TrackStepLim / TrackLength) * CT))
    # command = "MJT1"+TrackSteps+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n"


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
