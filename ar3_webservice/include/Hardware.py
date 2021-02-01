# this file is hardware connection layer which use to connect to suitable hardware
# here all the processing like joint no and etc start from 0, like 0=Joint 1, 1=joint 2...
# this class most of the method return string, either status code "OK" or "ERR_SPECIFIC_CODE" only
import serial
import time
import log
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
    jointqty = 0
    jlabels = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}
    calibrationspeed = 20

    # constructor, connector to teensy and arduino when initialize

    def __init__(self,v,paras):
        self.teensyport = v.teensyport
        self.teensybaud = paras.teensybaudrate
        self.arduinoport = v.arduinoport
        self.arduinobaud = paras.arduinobaudrate
        self.connectAllSerialPort()
        self.jsetting = paras.jsetting
        self.jointqty = paras.jointqty

    def connectAllSerialPort(self):
        self.ser_teensy = self.connectSerial(self.teensyport, self.teensybaud)
        self.ser_arduino = self.connectSerial(self.arduinoport, self.arduinobaud)
        return "OK"

    def connectSerial(self,portname,baud):
        return serial.Serial(portname, baud)

    # write serial command
    def writeIO(self,board,command):
        log.info("access writeIO")
        command=command+"\n"
        log.debug("serial command: " + command)
        cmdstr = command.encode()
        board.write(cmdstr)
        board.flushInput()
        time.sleep(self.serialwritesleep )
        result = board.read()
        log.info("access done")
        return "OK"

    # read serial command
    def readIO(self, board, command):
        log.info("access readIO")
        command = command + "\n"
        log.debug("serial command: " + command)
        cmdstr = command.encode()
        board.write(cmdstr)
        time.sleep(self.serialwritesleep)
        result = board.readline()
        log.debug(result)
        log.info("access done")
        return result

    # move joint 0/1/2.. to x degree
    def rotateJoint(self,jointno,degree):

        #validate joint 0-5
        checkjointres = self.checkJointNo(jointno)
        if checkjointres != "OK":
            return checkjointres


        if type(degree) is str:
            degree = int(degree)

        direction = 0
        int_degree = int(degree)
        deg = abs(int_degree)
        if int_degree > 0 :
            direction = 1

        jdir = str(direction)  # 0,1 for +/- direction
        degperstep = self.jsetting [jointno]["degperstep"]
        jogsteps = str(   int(deg / degperstep) )  # jog how many step
        Speed = str(25) # value in %, shall fetch from runtime variables
        ACCdur = str(15) # accelerartion duration
        ACCspd = str(10) # accelerartion speed %
        DECdur = str(20) # deceleration duration
        DECspd = str(5) # deceleration duration %
        J1StepCur = str(7554)
        J2StepCur = str(2323)
        J3StepCur = str(10)
        J4StepCur = str(7596)
        J5StepCur = str(2279)
        J6StepCur = str(3310)
        command = "MJ" + self.jlabels[jointno] + jdir + jogsteps + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd + "U" + J1StepCur + "V" + J2StepCur + "W" + J3StepCur + "X" + J4StepCur + "Y" + J5StepCur + "Z" + J6StepCur
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        return self.writeIO(board, command)

    # calibrate all joint according variable joints. [1,1,1,1,1,1] = all, [0,0,1,0,0,0] = J3 only
    def goAllJointLimit(self,joints):
        jsteps = [0,0,0,0,0,0]
        jdir = [0,0,0,0,0,0]
        for i in range(0, self.jointqty):
            jdir[i] = str(self.jsetting[i]["caldir"])

            if joints[i] == 1:
                jsteps[i] = str(15110)
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
        else:
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
    def calibrateJoint(self,jointno):
        checkjointres = self.checkJointNo(jointno)
        if checkjointres != "OK":
            return checkjointres
        joints = [0,0,0,0,0,0]
        joints[jointno]=1
        return self.goAllJointLimit(joints)

    def setServo(self,servoname, degree):
        if type(degree) is int:
            degree = str(degree)
        command = "SV0P"+degree
        board = self.ser_arduino # most of the case, using arduino, this place reserved for future enhancement which add servo into more board
        return self.writeIO(board,command)

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

    # before any movement, have to check machine status
    # 1. check teensy ready (test serial)
    # 2. check arduino ready (test serial)
    # 3. check encoder/power/drive ready (have to read specific value from teensy)
    def checkMachineStatus(self):
        log.info("enter checkMachineStatus")
        # self.rotateJoint( 0,10)
        # self.rotateJoint(0, -10)
        command = "GPU7996V2322W10X7595Y2278Z3309"
        # commandCalc = "GP" + "U" + str(J1StepCur) + "V" + str(J2StepCur) + "W" + str(J3StepCur) + "X" + str(J4StepCur) + "Y" + str(J5StepCur) + "Z" + str(J6StepCur) + "\n"


        # get position: GPU7996V2322W10X7595Y2278Z3309
        # result: b'00 000000 A7995 B2321 C9 D7594 E2277 F3308\r\n'
                  #  01 100000 A7996 B2321 C9 D7594 E2277 F3308

        # Pcode fault   j1 j2 j3 j4 j5 j6
        result = self.readIO(self.ser_teensy,command)
        log.info("done checkMachineStatus")
        return result

    # set arm position, rest/limit position follow setting in armparameters.py
    def writeARMPosition(self,writeType,joints):
        log.info("enter writeARMPosition: "+writeType)
        fieldname = ""
        if writeType == "rest":
            fieldname = "reststep"
        elif writeType == 'limit':
            fieldname = "steplimit"
        else:
            return "ERR_UNKNOWN_WRITEARM_POSITIONTYPE"
        command = "LM"
        for i in range(0, self.jointqty):
            if joints[i] == 1:
                stepvalue = self.jsetting[i][fieldname]
                command = command + self.jlabels[i] + str(stepvalue)

        self.writeIO(self.ser_teensy, command)
        log.debug("serial command: "+command )
        log.info("done writeARMPosition")
        return "OK"

    def moveFromLimitToRestPosition(self,joints):
        log.info("access moveToRestPosition")
        for i in range(0, self.jointqty):
            if joints[i] == 1:
                # 0: {"maxdeg": 170, "mindeg": -170, "steplimit": 15110, "degperstep": 0, "caldir": 0, "restpos": 0, "reststep": 7555},
                # 1: {"maxdeg": 0, "mindeg": -129.6, "steplimit": 7198, "degperstep": 0, "caldir": 0, "restpos": -90, "reststep": 2199.3888888888887},
                # 2: {"maxdeg": 143.7, "mindeg": 1, "steplimit": 7984, "degperstep": 0, "caldir": 1, "restpos": 1.05, "reststep": 0},
                # 3: {"maxdeg": 164.5, "mindeg": -164.5, "steplimit": 14056, "degperstep": 0, "caldir": 0, "restpos": 0, "reststep": 7028},
                # 4: {"maxdeg": 104.15, "mindeg": -104.15, "steplimit": 4560, "degperstep": 0, "caldir": 0, "restpos": 0, "reststep": 2280},
                # 5: {"maxdeg": 148.1, "mindeg": -148.1, "steplimit": 6320, "degperstep": 0, "caldir": 1, "restpos": 0, "reststep": 3160},
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