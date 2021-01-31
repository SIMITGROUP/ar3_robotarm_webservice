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
        cmdstr = command.encode()
        print(cmdstr)
        board.write(cmdstr)
        board.flushInput()
        time.sleep(self.serialwritesleep )
        board.read()

    def setServo(self,servoname, angle):
        print("Change servoname:",servoname)
        command = "SV0P"+str(angle)+"\n"
        board = self.ser_arduino # most of the case, using arduino, this place reserved for future enhancement which add servo into more board
        self.writeIO(board,command)
    #define a class to connect the things
# constructor connect arms and init all default value, and go to rest position automagically
