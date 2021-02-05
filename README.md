This is web services design for open source robot arm (https://www.anninrobotics.com/) project name AR3.
## this web service work reasonable well in my environment, not mean work in your environment, you has been warn and test it with care!! 


AR3 is cool robot arm project, however it is written as python desktop application, to increase mobility and flexibility I build this web service. It allow all developer develop all kind of front end application included web/desktop/mobile app to integrate with this web service. Beside, it also possible to allow single front end application control multiple instance of web services.

I rewrite the source code and reorganize it using FLASK (PYTHON) framework. The code is 100% independ with existing AR3 desktop app, Teensy and Arduino code remain same with the original unchange. The desktop app in the respository purely for reference and no related with web services.

All http traffic use http GET at the moment, for testing and design simplicity, and return will be in json format.

** NO authentication function in this stage yet. We have to build authentication backend before launch it.

# Setup
Before anything you have to make sure your environment able to run ARCS source code, that require you install python environment in your computer. This webservice developed in Flask, so you may follow flask installation guide https://flask.palletsprojects.com/en/1.1.x/installation/

After the Flask ready, you may follow below step:
1. Edit configuration files
`ar3_robotarm_webservice/ar3_webservice/include/values.py` and `ar3_robotarm_webservice/ar3_webservice/include/armparameters.py`
change the teensy and arduino port value to match your computer setting. Example:

windows
```
teensyport="COM3"
arduinoport="COM4"
# above value will auto assign if you no make any changes. if you luck and port exactly same, the web service just work without configure it.
```
linux
```
teensyport="/dev/ttyACM0"
arduinoport="/dev/ttyUSB0"
# above value will auto assign if you no make any changes. if you luck and port exactly same with me, the web service just work without configure it.
```
MAC
```
teensyport="/dev/tty.usbmodemxxxxx"
arduinoport="/dev/tty.usbserial-xxxx"
# I wrote special file check is there any similar file name in /dev folder, if yes it help you configure automatically
```
You can double check port using Arduino IDE if you not sure. 

2. in terminal, run following command
```
cd  your_path/ar3_robotarm_webservice/ar3_webservice
export FLASK_APP=route.py
flask run
```

You will notice your statement like ARM conneced, and show "Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)"


3. use terminal, execute `sh path_to_ar3_webservice/tools/01_trymotor.sh`

If success, you will notice AR3 gripper and joint move by itself, important content of trymotor.sh as below:
```
curl http://127.0.0.1:5000/servo/mygripper?degree=90
curl http://127.0.0.1:5000//move_j/j1?degree=10&movetype=move
```

4. You can try another 2 script: 02_calibratealljoint.sh, 03_runmanycommand.sh too, or use any web browser run above url to see your arm move as expect?

# Project Status
Refer project plan
https://github.com/SIMITGROUP/ar3_robotarm_webservice/projects/1

# API
Refer https://github.com/SIMITGROUP/ar3_robotarm_webservice/wiki to see detail API

