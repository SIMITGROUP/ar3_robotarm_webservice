# this file is hardware connection layer which use to connect to suitable hardware
# here all the processing like joint no and etc start from 0, like 0=Joint 1, 1=joint 2...
import serial
import time
class Hardware:

    ser_teensy = None
    ser_arduino = None
    teensyport = ""  # windows = COM3,4... Linux = /dev/ttyACM0,1,2,.. MAC = /dev/tty.usbmodem0000000
    teensybaud = 115200
    arduinoport = "" # windows = COM4,5... Linux = /dev/ttyUSB0,1,2.. MAC = /dev/tty.usbserial-0000000
    arduinobaud = 115200
    serialwritesleep = .2
    # constructor, connector to teensy and arduino when initialize

    def __init__(self,teensyport,teensybaud,arduinoport,arduinobaud):
        self.teensyport = teensyport
        self.teensybaud = teensybaud
        self.arduinoport = arduinoport
        self.arduinobaud = arduinobaud
        self.connectAllSerialPort()

    def connectAllSerialPort(self):
        self.ser_teensy = self.connectSerial(self.teensyport, self.teensybaud)
        self.ser_arduino = self.connectSerial(self.arduinoport, self.arduinobaud)

    def connectSerial(self,portname,baud):
        return serial.Serial(portname, baud)

    # write serial command
    def writeIO(self,board,command):
        command=command+"\n"
        cmdstr = command.encode()
        print(cmdstr)
        board.write(cmdstr)
        board.flushInput()
        time.sleep(self.serialwritesleep )
        board.read()

    # move joint 0/1/2.. to x degree
    def rotateJoint(self,jointno,degree,jsetting):
        # joint no 0 = A, 1 = B, 2 = C, 3 = D, 4 = E, 5 = F
        jlabels = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F"}
        direction = 0
        deg = abs(degree)
        if degree > 0 :
            direction = 1
        else:
            direction = 0

        jdir = str(direction)  # 0,1 for +/- direction
        print("jsetting for ",jointno)
        print(jsetting)
        degperstep = jsetting [jointno]["degperstep"]
        print("deg:", str(deg), ", degperstep: ", degperstep)
        jogsteps = str(   int(deg / degperstep) )  # jog how many step
        print("jogsteps:",jogsteps)

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
        command = "MJ" + jlabels[jointno] + jdir + jogsteps + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd + "U" + J1StepCur + "V" + J2StepCur + "W" + J3StepCur + "X" + J4StepCur + "Y" + J5StepCur + "Z" + J6StepCur
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        self.writeIO(board, command)

        # move j1
        # command  MJA-0-444-S-25-G-15-H-10-I-20-K-5-U-7554-V-2323-W-10-X-7596-Y-2279-Z-3310
        # command = "MJA" + J1motdir + str( J1jogSteps) + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd + "U" + str( J1StepCur) + "V" + str(J2StepCur) + "W" + str(J3StepCur) + "X" + str(J4StepCur) + "Y" + str(J5StepCur) + "Z" + str(J6StepCur) + "\n"
        # J1+MJA 1 444S25G15H10I20K5U 8442 V2878W10X7596Y2279Z3310
        # J1-MJA 0 444S25G15H10I20K5U 7998 V2878W10X7596Y2279Z3310
        # move j2 positive
        # command = "MJB" + J2drivedir + str(J2jogSteps) + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd + "U" + str(J1StepCur) + "V" + str(J2StepCur) + "W" + str(J3StepCur) + "X" + str(J4StepCur) + "Y" + str(J5StepCur) + "Z" + str(J6StepCur) + "\n"
        # MJB1555S25G15H10I20K5U7554V2878W10X7596Y2279Z3310
        #command = "MJ"+jointlabel=

        # global JogStepsStat
        # global J1StepCur
        # global J2StepCur
        # global J3StepCur
        # global J4StepCur
        # global J5StepCur
        # global J6StepCur
        # global J1AngCur
        # global xboxUse
        # Speed = speedEntryField.get()
        # ACCdur = ACCdurField.get()
        # ACCspd = ACCspeedField.get()
        # DECdur = DECdurField.get()
        # DECspd = DECspeedField.get()
        # J1Degs = float(J1jogDegsEntryField.get())
        # if JogStepsStat.get() == 0:
        #     J1jogSteps = int(J1Degs / J1DegPerStep)
        # else:
        #     # switch from degs to steps
        #     J1jogSteps = J1Degs
        #     J1Degs = J1Degs * J1DegPerStep
        # command = "MJA1444S25G15H10I20K5U8442V2878W10X7596Y2279Z3310"
        # command = "MJA0444S25G15H10I20K5U7998V2878W10X7596Y2279Z3310"


    def setServo(self,servoname, angle):
        print("Change servoname:",servoname)
        command = "SV0P"+str(angle)
        board = self.ser_arduino # most of the case, using arduino, this place reserved for future enhancement which add servo into more board
        self.writeIO(board,command)
    #define a class to connect the things
# constructor connect arms and init all default value, and go to rest position automagically
