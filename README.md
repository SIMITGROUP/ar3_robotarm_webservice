all http traffic use get at the moment
## get
---
Command | Description 
--- | ---
/help | provide some help in string 
/info	| get max/min value, limit, encoder status, some description and etc 
/info/all | loop for all motor, digital io and return data
/info/j1 | 
/info/j2 | 
/info/j3 | 
/info/j4 | 
/info/j5 | 
/info/j6 | 
/info/t1 | if use travel trail
/calibrate | help/guide
/calibrate/all | calibrate all join and track
/calibrate/j1 | 
/calibrate/j2 | 
/calibrate/j3 | 
/calibrate/j4 | 
/calibrate/j5 | 
/calibrate/j6 | 
/calibrate/t1 | calibrate travel trail, however now ar3 no limit switch yet...
/move_j | rotate stepper motor to n degrees
/move_j/j1 |
/move_j/j2 |
/move_j/j3 |
/move_j/j4 |
/move_j/j5 |
/move_j/j6 |
/move_j/t1 | move travel trail, maybe use maybe not
/move_l | linear move motor gripper into specific axis, it will send signal to few motor after ward
/move_l/x |
/move_l/y |
/move_l/z |
/move_l/w |
/move_l/p |
/move_l/r |
/movetrack | move travel track into spefic mm
/movetrack/t1 | at the moment, only t1 available
/read | read all electronic component data
/read/encoder | read all stepper motor encoder value
/read/encoder/j1 | can supply more joint like j1,j2,j3  to read more encoder in 1 time
/read/arduino |
/read/arduino/<n> | get arduino pin n value, some pin is true/false, some pin is number
/read/raspberrypi/<n> | if use raspberry pi, can get pi pin n value, some pin is true/false, some pin is number

/write
/write/arduino
/write/arduino/<pin no>

/write/raspberrypi
/write/raspberrypi/<pin no>
		

/pinsetting/raspberrypi/<pin>	# use to label pin and read some pin info for pi
/pinsetting/arduino/<pin>		# use to label pin and read some pin info for pi

/program						# provide list of program name
/program/<name>					# use program <name>, it list current program steps
/program/<name>/add				# function to add step into program
/program/<name>/add/armposition?row=n		# add current arm position into program, insert into row n. 0 =first, empty = last, return latest program list
/program/<name>/add/wait?value=<int>&row=n		# hold how many second
/program/<name>/add/positionstring?str=<string>&row=n		# add absolute arm position into program


/program/<name>/add/write/raspberrypi?pin=x&value=<int>&row=n		# write signal into io pin
/program/<name>/add/write/arduino?pin=x&value=<int>&row=n		# write signal into io pin



/program/<name>/delete?row=n		# remove row n. 0 =first, empty = last, return latest program list
