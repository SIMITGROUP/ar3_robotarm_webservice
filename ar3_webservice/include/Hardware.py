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


    # constructor, connector to teensy and arduino when initialize

    def __init__(self,v,paras):
        self.teensyport = v.teensyport
        self.teensybaud = paras.teensybaudrate
        self.arduinoport = v.arduinoport
        self.arduinobaud = paras.arduinobaudrate
        self.connectAllSerialPort()
        self.jsetting = paras.jsetting
        self.jointqty = paras.jointqty
        self.jointvalue = v.jointvalue
        self.servovalue = v.servovalue
        self.tracksetting = paras.tracksetting
        self.trackvalue = v.trackvalue

    def connectAllSerialPort(self):
        if self.teensyport == "":
            self.teensyport = self.autoDetectSerialPort('teensy')

        if self.arduinoport == "":
            self.arduinoport = self.autoDetectSerialPort('arduino')

        self.ser_teensy = self.connectSerial(self.teensyport, self.teensybaud)
        self.ser_arduino = self.connectSerial(self.arduinoport, self.arduinobaud)
        return "OK"


    def autoDetectSerialPort(self,boardname):
        print("run autoDetectSerialPort")
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
        return serial.Serial(portname, baud)

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
        return result

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

        jogstep = int(deg / degperstep)  # jog how many step
        jogstepsstr = str(jogstep)


        if float_degree > 0:
            encodervalues[jointno]["step"] = int(encodervalues[jointno]["step"]) - jogstep
        else:
            encodervalues[jointno]["step"] = int(encodervalues[jointno]["step"]) + jogstep


        Speed = str(25) # value in %, shall fetch from runtime variables
        ACCdur = str(15) # accelerartion duration
        ACCspd = str(10) # accelerartion speed %
        DECdur = str(20) # deceleration duration
        DECspd = str(5) # deceleration duration %
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
        newdegreestr = str(encodervalues[jointno]['degree'])
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

    def setServo(self,servoname, degree):
        if type(degree) is int:
            degree = str(degree)
        command = "SV0P"+degree
        board = self.ser_arduino # most of the case, using arduino, this place reserved for future enhancement which add servo into more board
        result =  self.writeIO(board,command)
        self.servovalue[servoname] = degree

    def readEncoderValue(self,jointno):
        checkjointres = self.checkJointNo(jointno)
        if checkjointres != "OK":
            return checkjointres

        print("readEncoderValue:", jointno)
        return 0

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
            log.debug("currentdegree: "+str(currentdegree)+", degreeperstep:"+str(degperstep)+", currentstep: " + str(currentstep) + ", degreefromlimit:"+str(degreefromlimit))
        log.info("done refreshStepperMotorEncoderValue")

        # 0: {"maxdeg": 170, "mindeg": -170, "steplimit": 15110, "degperstep": 0, "caldir": 0, "restpos": 0, "reststep": 7555},
        # 1: {"maxdeg": 0, "mindeg": -129.6, "steplimit": 7198, "degperstep": 0, "caldir": 0, "restpos": -90, "reststep": 2199.3888888888887},
        # 2: {"maxdeg": 143.7, "mindeg": 1, "steplimit": 7984, "degperstep": 0, "caldir": 1, "restpos": 1.05, "reststep": 56},
        # 3: {"maxdeg": 164.5, "mindeg": -164.5, "steplimit": 14056, "degperstep": 0, "caldir": 0, "restpos": 0, "reststep": 7028},
        # 4: {"maxdeg": 104.15, "mindeg": -104.15, "steplimit": 4560, "degperstep": 0, "caldir": 0, "restpos": 0, "reststep": 2280},
        # 5: {"maxdeg": 148.1, "mindeg": -148.1, "steplimit": 6320, "degperstep": 0, "caldir": 1, "restpos": 0, "reststep": 3160},
        return self.jointvalue


    # before any movement, have to check machine status
    # 1. check teensy ready (test serial)
    # 2. check arduino ready (test serial)
    # 3. check encoder/power/drive ready (have to read specific value from teensy)
    def checkMachineStatus(self):
        log.info("enter checkMachineStatus")
        encodervalues = self.refreshStepperMotorEncoderValue() #arrays
        log.info("done checkMachineStatus")
        return encodervalues

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
        # 0:{"maxdeg":170, "mindeg":-170, "steplimit":15110, "degperstep": 0, "caldir":0, "restpos":0, "reststep": 7555 },
        # 1:{"maxdeg":0, "mindeg":-129.6, "steplimit":7198, "degperstep": 0, "caldir":0, "restpos":-90, "reststep": 2199.3888888888887 },
        # 2:{"maxdeg":143.7, "mindeg":1, "steplimit":7984, "degperstep": 0, "caldir":1, "restpos":1.05, "reststep": 56 },
        # 3:{"maxdeg":164.5, "mindeg":-164.5, "steplimit":14056, "degperstep": 0, "caldir":0, "restpos":0, "reststep": 7028 },
        # 4:{"maxdeg":104.15, "mindeg":-104.15, "steplimit":4560, "degperstep": 0, "caldir":0, "restpos":0, "reststep": 2280 },
        # 5:{"maxdeg":148.1, "mindeg":-148.1, "steplimit":6320, "degperstep": 0, "caldir":1, "restpos":0, "reststep": 3160 },


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
                            # j1 = 0 - -170 = 170
                            # j2 = -90 - -129.6 = 39.6
                            # j4 = 0 - -164.5  = 164.5
                            # j5 = 0 - -104.15 = 104.15
                elif caldir == 1:
                    degree = restpos - maxdeg
                        # j3 =  1.05 - 143.7 = -142.02
                        # j6 = 0 - 148.1 = -148.1
                else:
                    # not supported value, ignore and no movement
                    a=1

                self.rotateJoint(i, degree)
        log.info("done moveToRestPosition")
        return "OK"

    def setTrackValue(self,trackno,mm):
        TrackStepLim = self.tracksetting[trackno]['steplimit']
        TrackLength = self.tracksetting[trackno]['length']
        self.trackvalue[trackno]["mm"] = mm
        self.trackvalue[trackno]["step"] = int((TrackStepLim / TrackLength) * mm)
        return "OK"

    def getTrackValues(self):
        return self.trackvalue

    def moveTrack(self,trackno,mm):
        # t + ve: MJT1772S25G15H10I20K5
        # t - ve: MJT0772S25G15H10I20K5
        TrackStepLim = self.tracksetting[trackno]['steplimit']
        TrackLength = self.tracksetting[trackno]['length']
        absmm = abs(mm)
        TrackSteps = str(int((TrackStepLim / TrackLength) * absmm))
        Speed = str(25)  # value in %, shall fetch from runtime variables
        ACCdur = str(15)  # accelerartion duration
        ACCspd = str(10)  # accelerartion speed %
        DECdur = str(20)  # deceleration duration
        DECspd = str(5)  # deceleration duration %
        direction = 0
        if mm > 0:
            direction = 1
        command = "MJT"+str(direction) + TrackSteps + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        result = self.writeIO(board, command)
        result2 = self.setTrackValue(trackno,mm)
        return result
    # #move joints into rest position, [1,1,1,1,1,1] = all, [1,0,0,0,0,0]
    # def goToRestPosition(self,joints):
    #     print("move to rest position")
    #     for i in range(0, self.jointqty):
    #         #only selected joint move to rest position
    #         if joints[i] == 1:
    #             degree = int(self.jsetting[i]["restpos"])
    #             self.rotateJoint(joints[i],degree)
    #     print("done")
    #     return "OK"
    # calibration single joint to limit switch


