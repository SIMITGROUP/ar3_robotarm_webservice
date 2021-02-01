This is web services design for open source robot arm (https://www.anninrobotics.com/) project name AR3.

AR3 is cool robot arm project, however it is written as python desktop application, to increase mobility and flexibility I build this web service. It allow all developer develop all kind of front end application included web/desktop/mobile app to integrate with this web service. Beside, it also possible to allow single front end application control multiple instance of web services.

I rewrite the source code and reorganize it using FLASK (PYTHON) framework. The code is 100% independ with existing AR3 desktop app, Teensy and Arduino code remain same with the original unchange. The desktop app in the respository purely for reference and no related with web services.

All http traffic use http GET at the moment, for testing and design simplicity, and return will be in json format.

** NO authentication function in this stage yet. We have to build authentication backend before launch it.

# Setup
1. Edit `ar3_robotarm_webservice/ar3_webservice/include/values.py`, change the teensy and arduino port value to match your computer setting. Example:
```
windows, Teensy=COM3, Arduino Mega: COM4)
linux, Teensy=/dev/ttyACM0, Arduino Mega=/dev/ttyUSB0
MAC, Teensy=/dev/tty.usbmodem70426001 (or /dev/cu.usbmodem...), Arduino Mega=/dev/tty.usbserial-14410 (or /dev/cu.usbserial...)
```
You can double check port using Arduino IDE if you not sure. 

2. in terminal, cd into ar3_robotarm_webservice/ar3_webservice, run following command
```
export FLASK_APP=route.py
flask run
```

You will notice your statement like ARM conneced, and show "Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)"


3. use terminal, execute `sh path_to_ar3_webservice/tools/trymotor.sh`

If success, you will notice AR3 gripper and joint move by itself, important content of trymotor.sh as below:
```
curl http://127.0.0.1:5000/servo/mygripper?degree=90
curl http://127.0.0.1:5000//move_j/j1?degree=10
```

# Project Status
Refer project plan
https://github.com/SIMITGROUP/ar3_robotarm_webservice/projects/1

# API
Refer https://github.com/SIMITGROUP/ar3_robotarm_webservice/wiki to see detail API

