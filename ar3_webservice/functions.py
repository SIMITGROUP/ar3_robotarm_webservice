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

    result = hardware.checkMachineStatus()
    return json.dumps(result)

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
        paras.jsetting[i]["degperstep"] = round( float((maxdeg - mindeg
                                                        )/float(steplimit)),8)
        #print(i,".maxdeg",maxdeg,"mindeg",mindeg,"steplimit",steplimit,"degperstep",paras.jsetting[i]["degperstep"])
        #jointvalue[i]=readJointValue(i)


# rotate joint "jointno" according movetype, "absolute" = absolute degree, "move"= rotate n degree
def rotateJoint(jname,degree,movetype):
    log.info("access rotateJoint")
    #validate movetype is received, and with proper value
    if type(movetype) is not str:
         return log.getMsg('ERR_MOVE_INVALIDTYPE','move type is not str')
    else:
        movetype = movetype.upper()
        if movetype != 'MOVE' and  movetype != 'ABSOLUTE':
            return log.getMsg('ERR_MOVE_INVALIDTYPE','movetype is not move or absolute')

    if type(degree) is str:
        degree = float(degree)

    jointname = jname.upper()

    if len(jointname) != 2 and left(jointname,1) != 'J' :
        return log.getMsg('ERR_JOINT_WRONGNAME','Joint name shall be J1, J2,j1,j2...')

    joint_id = int( right(jointname,1) ) - 1

    if joint_id < 0 and joint_id > paras.jointqty :
        return log.getMsg('ERR_JOINT_OUT_OF_RANGE','')

    encoders = hardware.refreshStepperMotorEncoderValue()

    if movetype == 'MOVE':
        newdegree = encoders[joint_id]['degree'] + degree
    else:
        # put joint into absolute degree, need add existing position
        # newdegree = currentdegree + changedegree
        newdegree = degree
        exisdegree = encoders[joint_id]['degree']
        degree = newdegree - exisdegree
    newdegreestr = str(newdegree)
    result = hardware.rotateJoint(joint_id, degree)

    maxdegstr = str(paras.jsetting[joint_id]["maxdeg"])
    mindegstr = str(paras.jsetting[joint_id]["mindeg"])

    if result != 'OK':
        jsondata = log.getMsg(result, jname+" shift "+ str(degree) + " become "+ newdegreestr+" which is not within "+mindegstr+"/"+maxdegstr)
    else:
        jsondata = log.getMsg(result,jname+" shift "+ str(degree) + " become "+ newdegreestr+ " which is within "+mindegstr+"/"+maxdegstr)

    log.info("done rotateJoint")
    return jsondata

def calibrateTrack(trackname):
    result = hardware.setTrackValue(trackname,0)
    return log.getMsg(result,"Assign Travel Track Position to 0mm")

def moveTrack(trackname, mm, movetype):
    #at the moment, any trackname also convert to track1
    if (checkKey(paras.tracksetting, trackname) == False):
        return log.getMsg('ERR_TRACK_INVALIDTRACK', trackname + ' does not exists')

    # validate movetype is received, and with proper value
    if type(movetype) is not str:
        return log.getMsg('ERR_MOVE_INVALIDTYPE', 'movetype is not str')
    else:
        movetype = movetype.upper()
        if movetype != 'MOVE' and movetype != 'ABSOLUTE':
            return log.getMsg('ERR_MOVE_INVALIDTYPE', 'movetype is not move or absolute')

    trackdata= hardware.getTrackValues()[trackname]
    bufferlength = 10
    lengthlimit = paras.tracksetting[trackname]['length'] - bufferlength
    if type(mm) is str:
        if mm.isnumeric():
            mm = float(mm)
        else:
            return log.getMsg("ERR_TRACK_WRONG_DATA_TYPE","'mm' is require numeric value within 0-"+str(lengthlimit))

    if movetype == 'MOVE':
        newmm = trackdata['mm'] + mm
    else:
        # put joint into absolute degree, need add existing position
        # newdegree = currentdegree + changedegree
        newmm = mm
        exismm = trackdata['mm']
        mm = newmm - exismm


    newmmstr = str(newmm)
    if newmm < 0 or newmm > lengthlimit:
        return log.getMsg('ERR_MOVETRACK_OVERLIMIT', "Track " + trackname + " blocked cause you wish to move " + str(mm) + " mm, to "+newmmstr+". It hit limit 0 - " + str(lengthlimit))
    else:
        result = hardware.moveTrack(trackname, mm)
        return log.getMsg(result, "Track "+trackname+" moved "+str(mm)+" mm, to "+newmmstr + ',  limit 0 - ' + str(lengthlimit))


# define servoname and how much degree to go
def changeServoValue(servoname,value):
    degree = 0
    #validate servo exists
    if(checkKey(paras.servosetting,servoname) == False):
        return log.getMsg('ERR_SERVO_INVALIDSERVO',servoname+' does not exists')

    #if given value is position name, get position degree from servosetting, or direct use integer value
    valuestr=''
    if type(value) is int or type(value) is float:
        degree = value
        valuestr = str(valuestr)
    elif type(value) is str and value != '':
        # doublecheck, maybe value is number but data type is string
        if value.strip('-').isnumeric():
            degree = float(value)
        else:
            degree = paras.servosetting[servoname][value]
        valuestr = value
    else:
        return log.getMsg('ERR_SERVO_INVALIDVALUE','invalid value')


    result = hardware.setServo(servoname,degree)
    if result == "OK":
        return log.getMsg(result,"")
    else:
        maxdeg = paras.servosetting[servoname]['maxdeg']
        mindeg = paras.servosetting[servoname]['mindeg']
        return log.getMsg(result,"assigned invalid value '"+valuestr+"' to servo '"+servoname+"', please check is it within "+str(mindeg)+"/"+str(maxdeg)+".")


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
        result2 = moveRestPosition(joints)
        if result != "OK":
            return log.getMsg(result, "Cannot move all joint into limit switch")
    else:
        return log.getMsg("ERR_CALIBRATE_FAILED01", "Invalid calibration joint name "+jointname)
    # all success result return here
    return '{"code":"OK","msg":""}' #log.getMsg("OK", "");

# move arm's joints to rest positions
def moveRestPosition(joints):

    for i in range (0,paras.jointqty):
        restpos =paras.jsetting[i]["restpos"]
        jname = 'J'+str(i+1)
        if joints[i]==1:
            rotateJoint(jname, restpos, 'absolute')
    return log.getMsg("OK","all joint at rest position now")

def updateJointValue():
    encodervalue = hardware.refreshStepperMotorEncoderValue()
    return encodervalue
    # result: b'00 000000 A7995 B2321 C9 D7594 E2277 F3308\r\n'
    #  01 100000 A7996 B2321 C9 D7594 E2277 F3308


def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]


def checkKey(arr, key):
    if key in arr.keys():
        return True
    else:
        return False


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
