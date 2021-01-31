# this file is hardware connection layer which use to connect to suitable hardware
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

    def rotateJoint(self,jointno,angle):
        # joint no 1 = A, 2 = B, 3 = C, 4 = D, 5 = E, 6 = F
        joints = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F"}
        jointlabel = joints[jointno]

        # move j1
        # command  MJA-0-444-S-25-G-15-H-10-I-20-K-5-U-7554-V-2323-W-10-X-7596-Y-2279-Z-3310
        # command = "MJA" + J1motdir + str( J1jogSteps) + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd + "U" + str( J1StepCur) + "V" + str(J2StepCur) + "W" + str(J3StepCur) + "X" + str(J4StepCur) + "Y" + str(J5StepCur) + "Z" + str(J6StepCur) + "\n"
        # J1+MJA 1 444S25G15H10I20K5U 8442 V2878W10X7596Y2279Z3310
        # J1-MJA 0 444S25G15H10I20K5U 7998 V2878W10X7596Y2279Z3310
        # move j2 positive
        # command = "MJB" + J2drivedir + str(J2jogSteps) + "S" + Speed + "G" + ACCdur + "H" + ACCspd + "I" + DECdur + "K" + DECspd + "U" + str(J1StepCur) + "V" + str(J2StepCur) + "W" + str(J3StepCur) + "X" + str(J4StepCur) + "Y" + str(J5StepCur) + "Z" + str(J6StepCur) + "\n"
        # MJB1555S25G15H10I20K5U7554V2878W10X7596Y2279Z3310
        #command = "MJ"+jointlabel=
        command = "MJA1444S25G15H10I20K5U8442V2878W10X7596Y2279Z3310"
        # command = "MJA0444S25G15H10I20K5U7998V2878W10X7596Y2279Z3310"
        board = self.ser_teensy  # most of the case, using teensy, this place reserved for future enhancement
        self.writeIO(board, command)

    def setServo(self,servoname, angle):
        print("Change servoname:",servoname)
        command = "SV0P"+str(angle)
        board = self.ser_arduino # most of the case, using arduino, this place reserved for future enhancement which add servo into more board
        self.writeIO(board,command)
    #define a class to connect the things
# constructor connect arms and init all default value, and go to rest position automagically
