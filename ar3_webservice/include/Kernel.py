import sys
import os
import json
sys.path.append("include")
from Hardware import Hardware
from Routine import Routine
import armparameters as paras
import time
import threading
import queue
import math
import numpy as np
import datetime
import log
import armparameters as paras
import values as values
# import webbrowser
# import pickle
err_log = {}

class Kernel:
    hw = None
    routinepath = ""
    routineextenstion = ".json"
    methodname = ""
    resource = ""
    subresource = ""
    req = {}
    def __init__(self):
        try:
            self.routinepath =  os.getcwd() + '/routines'
            for i in range(0, paras.jointqty):
                maxdeg = paras.jsetting[i]["maxdeg"]
                mindeg = paras.jsetting[i]["mindeg"]
                steplimit = paras.jsetting[i]["steplimit"]
                paras.jsetting[i]["degperstep"] = round(float((maxdeg - mindeg) / float(steplimit)), 8)
            for k, v in paras.tracksetting.items():
                steplimit = paras.tracksetting[k]['steplimit']
                length = paras.tracksetting[k]['length']
                paras.tracksetting[k]['mmperstep'] = round((length / steplimit), 8)
            self.hw = Hardware(values,paras)
        except Exception as e:
            print("Failed connect arm ", e)
            exit()


    ########################################################################
    ######################## process http route ############################
    ######################## return result in json #########################
    ########################################################################

    # display welcome msg
    def api_index(self):
        return {"status":"OK","msg":"Welcome index page of AR3 webservice, you can call /info now"}

    # display robot arm environment data
    def api_info(self):
        result = {}
        result = self.hw.checkMachineStatus()
        # result['xyz'] = self.getEndPointPosition(result['jointvalues'])
        return result

    def api_calibrate(self):
        # display calibration options
        x = self.resource
        if x == "setrest":
            result = self.overrideRestPosition()
        elif x == "all":
            result = self.calibrateAll()
        elif len(x)==2 and self.left(x,1) == 'j':
            result = self.calibrateJoints(x)
        elif x is None:
            return log.getMsg('OK', 'You can calibrate all joint with /calibrate/all, calibrate single joint (j1-j6) like /calibrate/j1, set new rest position /calibrate/setrest')
        else:
            return log.getMsg('ERR_CALIBRATION_UNKNOWN', x + " is not valid calibration command")
        return log.getMsg(result,"")

    def api_movetorestposition(self):
        result = self.moveToRestPosition([1,1,1,1,1,1])
        return log.getMsg(result, "")

    def api_calibratetrack(self):
        if self.resource is None:
            tracks = self.hw.getAllTracks()
            separator = ','
            txttracks = separator.join(tracks)
            return log.getMsg("OK", "Available travel track is "+txttracks)
        else:
            result = self.calibrateTrack(self.resource)
        return log.getMsg(result, "")

    def api_movetrack(self):
        if self.resource is None:
            tracks = self.hw.getAllTracks()
            separator = ','
            txttracks = separator.join(tracks)
            return log.getMsg("OK", "Available travel track is " + txttracks)
        else:
            mm = self.req.get("mm")
            movetype = self.req.get("movetype")
            result = self.moveTrack(self.resource,mm,movetype)
        return log.getMsg(result, "")

    def api_servo(self):
        if self.resource is None:
            servos = self.hw.getAllServos()
            separator = ','
            txtservos = separator.join(servos)
            return log.getMsg("OK", "Available servo is "+txtservos)
        else:
            value = self.req.get("value")

            result = self.moveServo(self.resource,value)
        return log.getMsg(result, "")

    def api_move_j(self):
        if self.resource is None:
            return log.getMsg("OK", "You can move joint j1-j6, like /move_j/j1?movetype=absolute/move&degree=10")
        else:
            degree = self.req.get("degree")
            movetype = self.req.get("movetype")
            result = self.moveJoint(self.resource, degree, movetype)
            return log.getMsg(result, "")

    def api_move_l(self):
        x=self.req.get('x')
        y=self.req.get('y')
        z=self.req.get('z')
        result = self.moveLinear(x, y, z)
        return log.getMsg(result, "")

    def api_getpositionurl(self):
        result =  self.getPositionUrl()
        return log.getMsg("OK", result)

    def api_setposition(self):
        allparas={}
        for k, v in self.req.items():
            allparas[k]=v
        result = self.setPosition(allparas)
        return log.getMsg(result, "")

    def api_setspeed(self):
        result = self.setSpeed(self.req.get('percent'))
        return log.getMsg(result, "")

    def api_io(self):
        l = self.getAllIO()
        if self.resource is None:
            return log.getMsg("OK", "Only support digital input/output at the moment", {'inputpin':l['input'],'outputpin':l['output']})
        elif self.subresource is None:
            operation = self.resource.lower()
            if operation ==  'on' or operation ==  'off':
                return log.getMsg("OK", "You can output digital signal to following pins", {'pins': l['output']})
            elif operation == 'read':
                return log.getMsg("OK", "You can read digital input from following pins", {'pins': l['input']})
            else:
                return log.getMsg("ERR_IO_INVALIDOPERATION","")
        else:
            operation = self.resource.lower()
            pinno = int(self.subresource)
            if operation == 'read':
                result = self.readDigitalInput(pinno)
                if self.isErrorCode(result):
                    return log.getMsg(result, "")
                else:
                    return log.getMsg("OK", "",{"value":result})
            #write digital io
            elif operation == 'on' or operation == 'off':
                result = self.sendDigitalOutput(pinno,operation)
            else:
                result = "ERR_IO_INVALIDOPERATION"
            return log.getMsg(result, "")


    def api_routine(self):
        if self.resource is None:
            list = self.getAllRoutines()
            separator = ","
            availableroutine = separator.join(list)
            return log.getMsg('OK',f"Available routines is {availableroutine}",{'routines':list})

        routinename = self.resource
        othersinfo = self.subresource
        # direct give routine json content
        if othersinfo is None:
            result = self.getRoutineInfo(routinename)

            if not self.isErrorCode(result):
                return result
            else:
                return log.getMsg(result,f"Invalid json content, please check again {routinename}.json.")
        elif othersinfo == "run":
            result = self.runRoutine(routinename)
        else:
            result ="ERR_ROUTINE_OPERATIONUNKNOWN"

        return log.getMsg(result,"")

    ########################################################################
    ##################  process robot arm operations #######################
    ##################  return result in string only #######################
    ########################################################################

    ##################  calibration #######################
    def showCalibrateGuide(self):
        return "OK"

    def overrideRestPosition(self):
        result = self.hw.writeARMPosition('rest', [1, 1, 1, 1, 1, 1])
        return result

    def calibrateJoints(self,jname):
        jointno = int(self.right(jname, 1)) - 1
        result = self.hw.calibrateJoint(jointno)
        return result

    def calibrateAll(self):
        joints = [1, 1, 1, 1, 1, 1]
        result = self.hw.goAllJointLimit(joints)
        if result == "OK":
            result2 = self.moveToRestPosition(joints)
            return result2
        else:
            return result

    def calibrateTrack(self,trackname):
        return self.hw.setTrackValue(trackname, 0)

    def moveToRestPosition(self,joints=[1,1,1,1,1,1]):
        for i in range(0, paras.jointqty):
            restpos = paras.jsetting[i]["restpos"]
            jname = 'J' + str(i + 1)

            if joints[i] == 1:
                result = self.moveJoint(jname, restpos, 'absolute')
                #if error, stop and move and return err code
                if self.isErrorCode(result):
                    return result

        return "OK"

    ################# move arm #########################
    def moveJoint(self,jname,degree,movetype):
        # validate movetype is received, and with proper value
        if type(movetype) is not str:
            return 'ERR_MOVE_INVALIDTYPE'
        else:
            movetype = movetype.upper()
            if movetype != 'MOVE' and movetype != 'ABSOLUTE':
                return 'ERR_MOVE_INVALIDTYPE'

        if degree is None:
            return "ERR_JOINT_NODEGREEDEFINED"
        elif type(degree) is str:
            degree = float(degree)

        jointname = jname.lower()

        if len(jointname) != 2 and self.left(jointname, 1) != 'j':
            return 'ERR_JOINT_WRONGNAME'

        joint_id = int(self.right(jointname, 1)) - 1

        if joint_id < 0 and joint_id > paras.jointqty:
            return log.getMsg('ERR_JOINT_OUT_OF_RANGE', '')

        encoders = self.hw.refreshStepperMotorEncoderValue()
        if type(encoders) == str:
            return encoders


        if movetype == 'MOVE':
            newdegree = encoders[joint_id]['degree'] + degree
        else:
            # put joint into absolute degree, need add existing position
            # newdegree = currentdegree + changedegree
            newdegree = degree
            exisdegree = encoders[joint_id]['degree']
            degree = newdegree - exisdegree
        newdegreestr = str(newdegree)
        result = self.hw.rotateJoint(joint_id, degree)

        maxdegstr = str(paras.jsetting[joint_id]["maxdeg"])
        mindegstr = str(paras.jsetting[joint_id]["mindeg"])

        return result
        # if result != 'OK':
        #     jsondata = log.getMsg(result, jname + " shift " + str(
        #         degree) + " become " + newdegreestr + " which is not within " + mindegstr + "/" + maxdegstr)
        # else:
        #     jsondata = log.getMsg(result, jname + " shift " + str(
        #         degree) + " become " + newdegreestr + " which is within " + mindegstr + "/" + maxdegstr)
        # log.info("done rotateJoint")

    def moveLinear(self,x, y, z):

        if x is None or y is None or z is None:
            return "ERR_MOVEL_UNDEFINEDPARA"
        if type(x) == str:
            x = float(x)
        if type(y) == str:
            y = float(y)
        if type(z) == str:
            z = float(z)
        return self.hw.moveLinear(x, y, z)


    ################# move track #########################
    def moveTrack(self, trackname, mm, movetype):
        # at the moment, any trackname also convert to track1
        if not self.checkKey(paras.tracksetting, trackname) :
            return 'ERR_TRACK_INVALID'


        # validate movetype is received, and with proper value
        if type(movetype) is not str:
            return 'ERR_MOVE_INVALIDTYPE'
        else:
            movetype = movetype.upper()
            if movetype != 'MOVE' and movetype != 'ABSOLUTE':
                return 'ERR_MOVE_INVALIDTYPE'

        trackdata = self.hw.getTrackValues()[trackname]
        bufferlength = 10
        lengthlimit = paras.tracksetting[trackname]['length'] - bufferlength

        if mm is None:
            return "ERR_MOVE_INVALIDMM"
        if type(mm) is str:

            if mm.strip('-').isnumeric():
                mm = float(mm)
            else:
                return "ERR_TRACK_WRONG_DATA_TYPE"

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
            return 'ERR_MOVETRACK_OVERLIMIT'
        else:
            result = self.hw.moveTrack(trackname, mm)
            return result

    ################# move servo #########################
    def moveServo(self, servoname, value):
        degree = 0
        # validate servo exists
        if (self.checkKey(paras.servosetting, servoname) == False):
            return 'ERR_SERVO_INVALIDSERVO'

        if value is None :
            return "ERR_SERVO_INVALIDVALUE"

        # if given value is position name, get position degree from servosetting, or direct use integer value
        valuestr = ''
        if type(value) is int or type(value) is float:
            degree = value
            valuestr = str(valuestr)
        elif type(value) is str and value != '':
            # doublecheck, maybe value is number but data type is string
            if value.strip('-').isnumeric():
                degree = float(value)
            else:
                degree = paras.servosetting[servoname]['positions'][value]
            valuestr = value


        else:
            return 'ERR_SERVO_INVALIDVALUE'

        result = self.hw.setServo(servoname, degree)
        if result == "OK":
            return log.getMsg(result, "")
        else:
            maxdeg = paras.servosetting[servoname]['maxdeg']
            mindeg = paras.servosetting[servoname]['mindeg']
            return result
            # return log.getMsg(result, "assigned invalid value '" + valuestr + "' to servo '" + servoname + "', please check is it within " + str(
            #                       mindeg) + "/" + str(maxdeg) + ".")

    ################# modifying arm speed ################
    def setSpeed(self, percent):
        if percent is None:
            return "ERR_SETSPEED_UNDEFINEDVALUE"
        if type(percent) == str:
            percent = float(percent)
        return self.hw.setSpeed(percent)

    ############### covert arm position as restful url ####
    def getPositionUrl(self):
        joinvalues = self.hw.refreshStepperMotorEncoderValue()
        if self.isErrorCode(joinvalues):
            return joinvalues

        servovalues = self.hw.getServoValues()
        trackvalues = self.hw.getTrackValues()
        txt = '/setposition?'
        for k, v in joinvalues.items():
            txt = txt + 'J' + str(k + 1) + '=' + str(v['degree']) + '&'
        for k, v in servovalues.items():
            txt = txt + k + '=' + str(v) + '&'

        for k, v in trackvalues.items():
            txt = txt + k + '=' + str(v['mm']) + '&'
        return txt

    ################# move all arm parts in 1 go #########
    def setPosition(self,allpara):
        print("allpara:")
        print(allpara)
        # sample url =  /setposition?J1=19.71&J2=-90.22&J3=1.89&J4=-0.07&J5=-0.23&J6=-0.47&gripper1=0&t1=0&
        # commandCalc = "MJA"+J1dir+J1steps+"B"+J2dir+J2steps+"C"+J3dir+J3steps+"D"+J4dir+J4steps+"E"+J5dir+J5steps+"F"+J6dir+J6steps+"T"+TRdir+TRstep+"S"+newSpeed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"

        jointdata = {}
        trackdata = {}
        servodata = {}
        loop=0
        for k, v in allpara.items():
            loop=loop+1
            if type(v) is str or type(v) is int:
                v = float(v)

            if self.checkKey(paras.servosetting, k):
                servodata[k] = v
            elif self.checkKey(paras.tracksetting, k):
                trackdata[k] = v
            elif len(k) == 2 and (self.left(k, 1) == 'j' or self.left(k, 1) == 'J') and self.right(k,1).isnumeric():  # j1,j2,j3,j4,j5,j6
                jointno = int(self.right(k, 1)) - 1  # J1 => 0, J2=>1
                jointdata[jointno] = v
            else:
                # dont know what is the parameter for, ignore it
                a = 1
        if loop > 0:
            result = self.hw.changePosition(jointdata, trackdata, servodata)
        else:
            result = "ERR_SETPOSITION_NOPARA"
        return result

    ########################################################################
    ##################  process io operations  #############################
    ##################  return value (mixed) ###############################
    ########################################################################
    def readDigitalInput(self,pin):
        return self.hw.readDigitalInput(pin)

    def sendDigitalOutput(self,pin,value):
        digitalvalue = None
        if type(value) == str:
            if value.lower() in ['on','1'] :
                digitalvalue= 1
            elif  value.lower() in ['off','0']:
                digitalvalue = 0
            else:
                return 'ERR_IO_INVALIDVALUE'
        elif value:
            digitalvalue = 1
        else:
            digitalvalue = 0

        return self.hw.sendDigitalOutput(pin,digitalvalue)

    def waitDigitalInput(self, pin, value):
        digitalvalue = None
        if type(value) == str:
            if value.lower() in ['on', '1']:
                digitalvalue = 1
            elif value.lower() in ['off', '0']:
                digitalvalue = 0
            else:
                return 'ERR_WAITIO_INVALIDVALUE'
        elif value:
            digitalvalue = 1
        else:
            digitalvalue = 0

        return self.hw.waitDigitalInput(pin, digitalvalue)

    def getAllIO(self):
        result = {
            "input": self.hw.inputpins,
            "output": self.hw.outputpins,
        }

        return result

    ########################################################################
    ##################  process robot arm routines  ########################
    ##################  return multiple type result ########################
    ########################################################################
    def getAllRoutines(self):
        files=[]
        for file in os.listdir(self.routinepath):
            if file.endswith(self.routineextenstion):
                routinename = file.replace(self.routineextenstion,'')
                files.append(routinename)
        return files

    def getRoutineInfo(self,routinename, getcleartext= False):
        rt = Routine(self)
        result = rt.load(routinename)
        return result

    #upload new routine.json
    def addRoutine(self):
        return "OK"

    #upload new routine and override existing
    def overrideRoutine(self,routinename):
        return "OK"

    def deleteRoutine(self,routinename):
        return "OK"

    def runRoutine(self,routinename):
        rt = Routine(self)
        success = rt.load(routinename)
        if not success:
            return "ERR_ROUTINE_INVALIDJSON"
        else:
            result = rt.execute()
            return result

    ########################################################################
    ##################  Others useful method not related arm  ##############
    ##################  return multiple type result ########################
    ########################################################################

    #### below store others function for string and data processing only ####
    def left(self,s, amount):
        return s[:amount]

    def right(self,s, amount):
        return s[-amount:]

    def checkKey(self,arr, key):
        if key in arr.keys():
            return True
        else:
            return False

    def isErrorCode(self,data):
        if type(data) == str and  self.left(data, 4) == 'ERR_':
            return True
        else:
            return False
