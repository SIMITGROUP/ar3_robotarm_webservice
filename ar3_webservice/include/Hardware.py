# this file is hardware connection layer which use to connect to suitable hardware
# here all the processing like joint no and etc start from 0, like 0=Joint 1, 1=joint 2...
# this class most of the method return string, either status code "OK" or "ERR_SPECIFIC_CODE" only
import serial
import serial.tools
import serial.tools.list_ports
import time
import log
import platform
import os.path
import glob # use for search serial port file in mac
import pickle

import kinematics as kn
import numpy as np
#define a class to connect the things
class Hardware:

    ser_teensy = None
    ser_arduino = None
    teensyport = ""  # windows = COM3,4... Linux = /dev/ttyACM0,1,2,.. MAC = /dev/tty.usbmodem0000000
    teensybaud = 115200
    arduinoport = "" # windows = COM4,5... Linux = /dev/ttyUSB0,1,2.. MAC = /dev/tty.usbserial-0000000
    arduinobaud = 115200
    serialwritesleep = .2
    jsetting = None
    tracksetting = None
    jointqty = 0
    jlabels = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}
    calibrationspeed = 20
    jointvalue = {}
    trackvalue = {}
    servovalue = {}
    t_matrix = [0,0,0]
    Speed = 0
    ACCdur = 0
    ACCspd = 0
    DECdur = 0
    DECspd = 0

    # constructor, connector to teensy and arduino when initialize

    def __init__(self,v,paras):
        self.cachefile = 'memory.cache'
        self.teensyport = v.teensyport
        self.teensybaud = paras.teensybaudrate
        self.arduinoport = v.arduinoport
        self.arduinobaud = paras.arduinobaudrate
        self.jsetting = paras.jsetting
        self.jointqty = paras.jointqty
        self.jointvalue = v.jointvalue
        self.servosetting = paras.servosetting
        self.servovalue = v.servovalue
        self.tracksetting = paras.tracksetting
        self.trackvalue = v.trackvalue
        self.Speed = paras.Speed
        self.ACCdur = paras.ACCdur
        self.ACCspd = paras.ACCspd
        self.DECdur = paras.DECdur
        self.DECspd = paras.DECspd
        self.loadData()
        self.connectAllSerialPort()
        # self.restoreAllServo()
        self.saveData()
        self.refreshStepperMotorEncoderValue()



    def connectAllSerialPort(self):
        if self.teensyport == "":
            self.teensyport = self.autoDetectSerialPort('teensy')


        if self.arduinoport == "":
            self.arduinoport = self.autoDetectSerialPort('arduino')

        self.ser_teensy = self.connectSerial(self.teensyport, self.teensybaud)

        if self.ser_teensy == False:
            self.teensyport = self.autoDetectSerialPort('teensy')
            self.ser_teensy = self.connectSerial(self.teensyport, self.teensybaud)

        self.ser_arduino = self.connectSerial(self.arduinoport, self.arduinobaud)

        if self.ser_arduino == False:
            self.ser_arduino = self.autoDetectSerialPort('arduino')
            self.ser_arduino = self.connectSerial(self.arduinoport, self.arduinobaud)

        return "OK"

    def saveData(self):
        pickle.dump([self.teensyport,self.arduinoport,self.servovalue,self.jointvalue,self.trackvalue], open(self.cachefile, "wb"))

    def loadData(self):
        if os.path.isfile(self.cachefile):
            self.teensyport,self.arduinoport,self.servovalue,self.jointvalue,self.trackvalue = pickle.load(open(self.cachefile,"rb"))

    def autoDetectSerialPort(self,boardname):
        defteensyboard = ''
        defarduinoboard = ''
        osname = platform.system()
        if osname == "Linux":
            defteensyboard = "/dev/ttyACM0"
            defarduinoboard = "/dev/ttyUSB0"

        elif osname == "Darwin":

            teensyboardprefix = "/dev/tty.usbmodem"
            teensylist = glob.glob(teensyboardprefix + '*')
            arduinoboardprefix = "/dev/tty.usbserial"
            arduinolist = glob.glob(arduinoboardprefix + '*')

            if len(teensylist) > 0:
                defteensyboard = teensylist[0]

            if len(arduinolist) > 0:
                defarduinoboard = arduinolist[0]

        elif osname == "Windows":
            defteensyboard = "COM3"
            defarduinoboard = "COM4"

        if boardname == "teensy":
            return defteensyboard
        elif boardname == "arduino":
            return defarduinoboard
        else:
            return ""


    def connectSerial(self,portname,baud):
        ser = None
        try:
            ser = serial.Serial(portname, baud)
            return ser
        except:
            return False

    def checkAllBoard(self):
        if self.checkTeensy() == False:
            return "ERR_CHECK_TEENSYOFF"
        if self.checkArduino() == False:
            return "ERR_CHECK_ARDUINOOFF"
        return "OK"

    def checkTeensy(self):
        return self.checkSerial("teensy")

    def checkArduino(self):
        return self.checkSerial("arduino")

    def checkSerial(self,boardname):
        try:
            osname = platform.system()
            # windows temporary always return true
            if osname == "Windows":
                return True
            else:
                if boardname == "teensy":
                    return os.path.exists(self.teensyport)
                elif boardname == "arduino":
                    return os.path.exists(self.arduinoport)
                else:
                    return False



        except:
            return False


    # write serial command
    def writeIO(self,board,command):
        log.info("access writeIO")
        command=command+"\n"
        log.debug("serial command: " + command)
        cmdstr = command.encode()
        try:
            board.write(cmdstr)
            board.flushInput()
            time.sleep(self.serialwritesleep )
            result = board.read()
        except Exception as e:
            errorcode = "ERR_SERIAL_DEVICENOTWRITABLE"
            log.error(errorcode+": cannot send signal to serial board")
            return errorcode
        log.info("access done")
        self.saveData()
        return "OK"

    # read serial command
    def readIO(self, board, command):
        log.info("access readIO")
        command = command + "\n"
        log.debug("serial command: " + command)
        cmdstr = command.encode()
        try:
            board.write(cmdstr)
            time.sleep(self.serialwritesleep)
            result = board.readline()
            log.debug(result)
        except Exception as e:
            errorcode = "ERR_SERIAL_DEVICENOTWRITABLE"
            log.error(errorcode+": cannot send signal to serial board")
            return errorcode
        log.info("access done")
        self.saveData()
        return result

    def convertDegToStep(self,deg,degperstep):
        jogstep = int(deg / degperstep)  # jog how many step
        return jogstep

    # linear movement
    def moveLinear(self,x,y,z):
        print(self.t_matrix)
        return "OK"
        self.t_matrix.t[0] += x
        self.t_matrix.t[1] += y
        self.t_matrix.t[2] += z
        solution = kn.iKinematic(self.t_matrix)
        degrees = np.degrees(solution.q)
        # validate all joint value got exists limit
        for i in range(0, self.jointqty):
            maxdeg = self.jsetting[i]['maxdeg']
            mindeg = self.jsetting[i]['mindeg']
            if degrees[i] > maxdeg:
                return "ERR_ROTATEJOINT_OVERMAXLIMIT"
            elif degrees[i] < mindeg:
                return "ERR_ROTATEJOINT_OVERMINLIMIT"

        #if no over limit, then move arm
        return self.changePosition(degrees, {},{})


    # generate forward kinematic formula
    def refreshKinematic(self):
        degrees = [0,0,0,0,0,0]
        for i in range(0, self.jointqty):
            degrees[i] = self.jointvalue[i]['degree']
        self.t_matrix = kn.fKinematic(degrees)

    # move joint 0/1/2.. to x degree
    def rotateJoint(self,jointno,degree):

        #validate joint 0-
        encodervalues = self.refreshStepperMotorEncoderValue()

        checkjointres = self.checkJointNo(jointno)
        if checkjointres != "OK":
            return checkjointres


        if type(degree) is str:
            degree = float(degree)
        nextdegree = degree + self.jointvalue[jointno]['degree']
        maxdeg = self.jsetting[jointno]['maxdeg']
        mindeg = self.jsetting[jointno]['mindeg']
        if nextdegree > maxdeg:
            return "ERR_ROTATEJOINT_OVERMAXLIMIT"
        elif nextdegree < mindeg:
            return "ERR_ROTATEJOINT_OVERMINLIMIT"

        direction = 0
        float_degree = float(degree)
        if float_degree > 0:
            direction = 1
        else:
            direction = 0


        deg = abs(float_degree)

        jdir = str(direction)  # 0,1 for +/- direction
        degperstep = self.jsetting[jointno]["degperstep"]
        jogstep = self.convertDegToStep(deg,degperstep)  # jog how many step
        jogstepsstr = str(jogstep)


        if float_degree > 0:
            encodervalues[jointno]["step"] = int(encodervalues[jointno]["step"]) - jogstep
        else:
            encodervalues[jointno]["step"] = int(encodervalues[jointno]["step"]) + jogstep


        Speed = str(self.Speed) # value in %, shall fetch from runtime variables
        ACCdur = str(self.ACCdur) # accelerartion duration
        ACCspd = str(self.ACCspd) # accelerartion speed %
        DECdur = str(self.DECdur) # deceleration duration
        DECspd = str(self.DECspd) # deceleration duration %
        J1StepCur = str(encodervalues[0]["step"])
        J2StepCur = str(encodervalues[1]["step"])
        J3StepCur = str(encodervalues[2]["step"])
        J4StepCur = str(encodervalues[3]["step"])
        J5StepCur = str(encodervalues[4]["step"])
        J6StepCur = str(encodervalues[5]["step"])
        command = "MJ" + self.jlabels[jointno] + jdir + jogstepsstr + "S" + Speed + \
                  "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd + \
                  "U" + J1StepCur + "V" + J2StepCur + "W" + J3StepCur + "X" + \
                  J4StepCur + "Y" + J5StepCur + "Z" + J6StepCur
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        result =  self.writeIO(board, command)
        encodervalues =self.refreshStepperMotorEncoderValue()
        #newdegreestr = str(encodervalues[jointno]['degree'])
        return result

    def changePosition(self,jointdata,trackdata,servodata):
        result="OK"
        command = "MJ"
        jsteps={}
        jdirs={}
        encodervalues = self.refreshStepperMotorEncoderValue()
        Speed = str(self.Speed)  # value in %, shall fetch from runtime variables
        ACCdur = str(self.ACCdur)  # accelerartion duration
        ACCspd = str(self.ACCspd)  # accelerartion speed %
        DECdur = str(self.DECdur)  # deceleration duration
        DECspd = str(self.DECspd)  # deceleration duration %
        newjointsteps={}
        newtrackdata = {}
        for k, v in jointdata.items():
            print(k,v)

            degperstep = self.jsetting[k]['degperstep']
            newjointsteps[k] = { 'deg': v, 'step': self.convertDegToStep(v, degperstep)}
            deg = v - self.jointvalue[k]['degree']
            jsteps[k] = abs(self.convertDegToStep(deg, degperstep))
            if deg >0:
                jdirs[k] = 1

            else:
                jdirs[k] = 0

            command = command + self.jlabels[k] + str(jdirs[k]) +  str(jsteps[k])


        for k, v in trackdata.items():
            mmperstep = self.tracksetting[k]['mmperstep']
            newstep = int( float(v) / float(mmperstep) )
            currentstep = self.trackvalue[k]['step']
            trstep = newstep - currentstep

            trstepstr = str(abs(trstep)) # teensy only accept +ve value
            if trstep > 0:
                trdir = 1
            else:
                trdir = 0
            # ar3 at the moment only support 1 track, just break after first item
            command = command + 'T'+ str(trdir) + trstepstr
            newtrackdata[k] = {"mm": v , "step": newstep}
            break

        command = command + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd
        command = command + "U" + str(newjointsteps[0]['step']) + "V" + str(newjointsteps[1]['step']) + "W" + str(newjointsteps[2]['step']) + \
                  "X" + str(newjointsteps[3]['step']) + "Y" + str(newjointsteps[4]['step']) + "Z" + str(newjointsteps[5]['step']) + "\n"

        #move all stepper motor, joint and track rail

        # MJA0444S25G15H10I20K5U7555.0V2199.3888888888887W559X7028.0Y2280.0Z3372

        result = self.writeIO(self.ser_teensy,command)
        # result="OK"
        # update new track data cause no encoder there
        for k, v in trackdata.items():
            self.trackvalue[k]= newtrackdata[k]

        self.refreshStepperMotorEncoderValue()

        # change servo position, 1 by 1
        for k, v in servodata.items():
            self.setServo(k,v)

        return result
    # calibrate all joint according variable joints. [1,1,1,1,1,1] = all, [0,0,1,0,0,0] = J3 only
    def goAllJointLimit(self,joints):
        jsteps = [0,0,0,0,0,0]
        jdir = [0,0,0,0,0,0]
        for i in range(0, self.jointqty):
            jdir[i] = str(self.jsetting[i]["caldir"])

            if joints[i] == 1:
                jsteps[i] = str(self.jsetting[i]["steplimit"])
            else:
                jsteps[i] = str(0)

        # calibration will repeat 2 times, faster and slower
        speed = str(self.calibrationspeed) # first time faster
        command = "LL"+ "A"+jdir[0] + jsteps[0] + "B" + jdir[1] + jsteps[1] + "C" + jdir[2] + jsteps[2] + \
                  "D" + jdir[3] + jsteps[3] + "E" + jdir[4] + jsteps[4] + "F" + jdir[5] + jsteps[5] +"S" + str(speed)
        board = self.ser_teensy   # most of the case, using teensy, this place reserved for future enhancement
        result = self.writeIO(board, command) # move all joint into limit

        if result == "OK":
            result2 = self.writeARMPosition("limit",joints) # set all encoder value to limit

            return result2
        else:
            return result


    def calibrateJoint(self,jointno):
        checkjointres = self.checkJointNo(jointno)
        if checkjointres != "OK":
            return checkjointres
        joints = [0,0,0,0,0,0]
        joints[jointno]=1
        result = self.goAllJointLimit(joints)
        self.moveFromLimitToRestPosition(joints)
        return result


    def restoreAllServo(self):
        for k,v in self.servovalue.items():
            self.setServo(k,v)


    def setServo(self,servoname, degree):
        if (self.checkKey(self.servosetting, servoname) == False):
            return log.getMsg('ERR_SERVO_INVALIDSERVO', servoname + ' does not exists')




        #identify which servo no, cause AR3 put firmware into arduino, recognise as 0,1,2,3
        servonumber=9999
        i = 0
        for k,v in self.servosetting.items():
            if k == servoname:
                servonumber = i
            i = i + 1

        maxdeg = self.servosetting[servoname]['maxdeg']
        mindeg = self.servosetting[servoname]['mindeg']

        if degree > maxdeg:
            return 'ERR_SERVO_MAX'
        elif degree < mindeg :
            return 'ERR_SERVO_MIN'
        degreestr = str(degree)
        command = "SV"+str(servonumber)+"P"+degreestr
        board = self.ser_arduino # most of the case, using arduino, this place reserved for future enhancement which add servo into more board
        result =  self.writeIO(board,command)
        self.servovalue[servoname] = degree
        self.saveData()
        return result

    def checkJointNo(self,jointno):
        if(type(jointno) is not int):
            return "ERR_JOINT_WRONG_DATA_TYPE"
        if jointno>5 or jointno <0:
            return "ERR_JOINT_OUT_OF_RANGE"
        else:
            return "OK"



    # get all stepper motor encoder value
    def refreshStepperMotorEncoderValue(self):
        log.info("enter refreshStepperMotorEncoderValue")
        # self.rotateJoint( 0,10)
        # self.rotateJoint(0, -10)
        # command = "GPU7996V2322W10X7595Y2278Z3309"
        steps=[0,0,0,0,0,0]
        jointindex = [0,0,0,0,0,0,0]
        results = [0,0,0,0,0,0]
        for i in range (0, self.jointqty):
            steps[i] = self.jointvalue[i]["step"]
        command = "GP" + "U" + str(steps[0]) + "V" + str(steps[1]) + "W" + str(steps[2]) + "X" + str(steps[3]) + "Y" + str(steps[4]) + "Z" + str(steps[5]) + "\n"
        RobotCode = self.readIO(self.ser_teensy, command).decode()
        if RobotCode == "":
            return "ERR_ENCODER_NOREPLY"
        # get position index of A/B/C...
        for i in range(0, self.jointqty):
            jointindex[i] = RobotCode.find(self.jlabels[i])

        #get currentstep value of all joint
        jointdegree = [0,0,0,0,0,0];
        for i in range(0, self.jointqty):
            startposition = jointindex[i]

            nextposition = None
            if self.jointqty - i > 1 : #not last loop
                nextposition = jointindex[i+1]
            else :
                nextposition = -2    # remove trailing /r/n
            currentstep = RobotCode[  startposition + 1: nextposition]

            self.jointvalue[i]["step"] = currentstep
            degperstep = self.jsetting[i]["degperstep"]


            if self.jsetting[i]["caldir"] == 0:
                degreefromlimit = round(degperstep * ( float(currentstep)  ),2)
                currentdegree = self.jsetting[i]["mindeg"] + degreefromlimit
            else:
                degreefromlimit =  round(degperstep * ( float(currentstep)  ),2)
                currentdegree = self.jsetting[i]["mindeg"] + degreefromlimit

            currentdegree = round(currentdegree,2)
            self.jointvalue[i]["degree"] = currentdegree
            jointdegree[i]=currentdegree
            log.debug("currentdegree: "+str(currentdegree)+", degreeperstep:"+str(degperstep)+", currentstep: " + str(currentstep) + ", degreefromlimit:"+str(degreefromlimit))
        log.info("done refreshStepperMotorEncoderValue")
        self.refreshKinematic()
        self.saveData()
        return self.jointvalue


    # before any movement, have to check machine status
    # 1. check teensy ready (test serial)
    # 2. check arduino ready (test serial)
    # 3. check encoder/power/drive ready (have to read specific value from teensy)
    def checkMachineStatus(self):
        log.info("enter checkMachineStatus")
        encodervalues = self.refreshStepperMotorEncoderValue() #arrays
        result = {
            "jointvalues":self.jointvalue,
            "xyz":self.t_matrix,
            "servovalues": self.servovalue,
            "trackvalues": self.trackvalue,
            "board":self.checkAllBoard()
        }
        log.info("done checkMachineStatus")
        return result

    # set arm position, rest/limit position follow setting in armparameters.py
    def writeARMPosition(self,writeType,joints):
        log.info("enter writeARMPosition: "+writeType)
        fieldname = ""

        if writeType != 'limit' and writeType != 'rest':  # process only support rest and limit inside for loop
            return "ERR_UNKNOWN_WRITEARM_POSITIONTYPE"
        command = "LM"
        for i in range(0, self.jointqty):
            if joints[i] == 1:
                if writeType == "rest":
                    stepvalue = self.jsetting[i]['reststep']
                else:
                    if self.jsetting[i]['caldir'] == 0:
                        stepvalue = 0
                    else:
                        stepvalue = self.jsetting[i]['steplimit']

                command = command + self.jlabels[i] + str(stepvalue)
        self.writeIO(self.ser_teensy, command)
        log.debug("serial command: "+command )
        log.info("done writeARMPosition")
        return "OK"

    #only use during calibrate all, from arm from all limit switch back to centre rest position
    def moveFromLimitToRestPosition(self,joints):
        log.info("access moveToRestPosition")
        for i in range(0, self.jointqty):
            if joints[i] == 1:
                log.info("move joint: "+str(i))
                caldir = self.jsetting[i]["caldir"]
                restpos = self.jsetting[i]["restpos"]
                mindeg = self.jsetting[i]["mindeg"]
                maxdeg = self.jsetting[i]["maxdeg"]
                degree = 0

                if caldir  == 0: # now stay at mindeg there
                    degree = restpos - mindeg
                elif caldir == 1:
                    degree = restpos - maxdeg
                else:
                    a=1

                self.rotateJoint(i, degree)
        log.info("done moveToRestPosition")
        self.saveData()
        return "OK"

    # move travel track to limit switch
    def moveTravelTrackToLimitSwitch(self,trackname):
        command ='LT'
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        result = self.writeIO(board, command)
        result2 = self.setTrackValue(trackname, 0)



    # move travel track to limit switch
    def beep(self,isbeep):
        command ='BP'+isbeep
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        result = self.writeIO(board, command)
        return result
    # set track position value
    def setTrackValue(self,trackname,mm):

        TrackStepLim = self.tracksetting[trackname]['steplimit']
        TrackLength = self.tracksetting[trackname]['length']
        self.trackvalue[trackname]["mm"] = mm
        self.trackvalue[trackname]["step"] = int((TrackStepLim / TrackLength) * mm)
        self.saveData()
        return "OK"

    def getTrackValues(self):
        return self.trackvalue

    def getServoValues(self):
        return self.servovalue

    def moveTrack(self,trackname,mm):
        # t + ve: MJT1772S25G15H10I20K5
        # t - ve: MJT0772S25G15H10I20K5
        TrackStepLim = self.tracksetting[trackname]['steplimit']
        TrackLength = self.tracksetting[trackname]['length']
        newmm = self.trackvalue[trackname]["mm"] + mm

        if newmm > TrackLength or newmm <0:
            return "ERR_MOVETRACK_OVERLIMIT"
        absmm = abs(mm)
        TrackSteps = str(int((TrackStepLim / TrackLength) * absmm))
        Speed = str(self.Speed)  # value in %, shall fetch from runtime variables
        ACCdur = str(self.ACCdur)  # accelerartion duration
        ACCspd = str(self.ACCspd)  # accelerartion speed %
        DECdur = str(self.DECdur)  # deceleration duration
        DECspd = str(self.DECspd)  # deceleration duration %
        direction = 0
        if mm > 0:
            direction = 1
        command = "MJT"+str(direction) + TrackSteps + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        result = self.writeIO(board, command)
        result2 = self.setTrackValue(trackname,newmm)

        return "OK"




    def linearMove(self,axis,mm):
        # to support linear movement
        # 1. get current pos
        return "OK"
    def checkKey(self,arr, key):
        if key in arr.keys():
            return True
        else:
            return False
