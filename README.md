all http traffic use http GET at the moment

# General Testing
---
This section move or read the robot arm in real time
Command | Description 
--- | ---
/help | provide some help in string 
/info	| get list of available information (not actual value)
/info/all | loop for all motor, digital io and return data
/info/j1 | get J1 encoder value, and hardware configuration like motor type, current and etc
/info/j2 | same as above with J2
/info/j3 | same as above with J3
/info/j4 | same as above with J4
/info/j5 | same as above with J5
/info/j6 | same as above with J6
/info/t1 | same as above with with travel rail (if in use)
/info/arduino | get all pin data type, labels, and value
/info/arduino/__n__ | get arduino pin __n__ value, some pin is true/false, some pin is number
/info/raspberrypi | get all pin data type, labels, and value
/inf/raspberrypi/__n__ | if use raspberry pi, can get pi pin __n__ value, some pin is true/false, some pin is number
/calibrate | help/guide on how to use this
/calibrate/all | calibrate all joint and track in 1 go
/calibrate/j1 | calibrate all J1 only
/calibrate/j2 | same as above with J2
/calibrate/j3 | same as above with J3
/calibrate/j4 | same as above with J4
/calibrate/j5 | same as above with J5
/calibrate/j6 | same as above with J6
/calibrate/t1 | calibrate travel trail, however now ar3 no limit switch yet...
/move_j | provide guide how to use this api
/move_j/j1?value=__n__ | rotate J1 into __n__ degree
/move_j/j2?value=__n__ | same as above with J2
/move_j/j3?value=__n__ | same as above with J3
/move_j/j4?value=__n__ | same as above with J4
/move_j/j5?value=__n__ | same as above with J5
/move_j/j6?value=__n__ | same as above with J6
/move_j/t1?value=__n__  |  same as above with travel rail (it maybe not make sense and will remove it)
/move_l | provide guidance on how to use linear movement
/move_l/x?value=__n__ | linear move gripper into axis X in value __n__ mm
/move_l/y?value=__n__ | linear move gripper into axis Y in value __n__ mm
/move_l/z?value=__n__ | linear move gripper into axis Z in value __n__ mm
/move_l/w?value=__n__ | linear move gripper into axis W in value __n__ mm
/move_l/p?value=__n__ | linear move gripper into axis P in value __n__ mm
/move_l/r?value=__n__ | linear move gripper into axis R in value __n__ mm
/movetrack | provide guidance move travel track into spefic mm
/movetrack/t1?value=__n__ | move T1 __n__ mm
/write | provide facilities to write io value into  arduino and raspberry pi
/write/arduino | provide guidance
/write/arduino/__pin_no/label__?value=__n__ |  write __n__ into  specifc pin no or pin label (refer setting section) for arduino
/write/raspberrypi |  provide guidance
/write/raspberrypi/__pin_no/label__?value=__n__ |  write __n__ into  specifc pin no or pin label (refer setting section) for raspberry pi

# Setting	
Here allow us store some setting so our program more user friendly. At the moment we don't provide setting in Teensy. We only allow access io pin at Arduino or Raspberry PI (If you use Pi instead of computer)
Command | Description
| --- | --- |
/setting/arduino/__pin__?label=__str__ | label arduino pin __n__ as label __str__. So that afterward we can give more user friendly name to assign value
/setting/raspberrypi/__pin__?label=__str__ | same as above, for raspberry pi GPIO pin

# training section
Command | Description
| --- | --- |
/program | provide list of program name
/program/__name__ | use program __name__, it list current program steps
/program/__name__/run?row=<int> | run program name, start from which row, empty will follow default (line 1)
/program/__name__/add  | function to add step into program
/program/__name__/add/armposition?row=n | add current arm position into program, insert into row n. 0 =first, empty = last, return latest program list
/program/__name__/add/wait?value=<int>&row=n | hold how many second
/program/__name__/add/positionstring?str=<string>&row=n | add absolute arm position into program
/program/__name__/add/write/raspberrypi?pin=x&value=<int>&row=n | write signal into io pin
/program/__name__/add/write/arduino?pin=x&value=<int>&row=n | write signal into io pin
/program/__name__/delete?row=n | remove row n. 0 =first, empty = last, return latest program list
