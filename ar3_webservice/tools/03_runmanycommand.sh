#!/bin/bash
echo "This script will execute many robot movement, standby your hand at emergency stop button to prevent accident damage your arm\n"

echo "Try get machine info..."
curl http://127.0.0.1:5000/info
echo "\n"

##### calibration  ####
echo "Calibrate J1..."
curl http://127.0.0.1:5000/calibrate/J1
echo "done\n"

echo "Calibrate J2..."
curl http://127.0.0.1:5000/calibrate/J2
echo "done\n"

echo "Calibrate J3..."
curl http://127.0.0.1:5000/calibrate/J3
echo "done\n"

echo "Calibrate J4..."
curl http://127.0.0.1:5000/calibrate/J4
echo "done\n"

echo "Calibrate J5..."
curl http://127.0.0.1:5000/calibrate/J5
echo "done\n"

echo "Calibrate J6..."
curl http://127.0.0.1:5000/calibrate/J6
echo "done\n"

echo "Calibrate all together..."
curl http://127.0.0.1:5000/calibrate/all
echo "done\n"

##### move join  ####
#J1
echo "Move J1 -90 degree..."
curl http://127.0.0.1:5000/move_j/J1?degree=-90
echo "done\n"

echo "Move J1 back to 0..."
curl http://127.0.0.1:5000/move_j/J1?degree=90
echo "done\n"

#J2
echo "Move J2 80 degree..."
curl http://127.0.0.1:5000/move_j/J2?degree=80
echo "done\n"

echo "Move J2 another 30 degree wish to break limit ..."
curl http://127.0.0.1:5000/move_j/J2?degree=30
echo "done\n"

echo "Move J2 back to 0..."
curl http://127.0.0.1:5000/move_j/J2?degree=-80
echo "done\n"

#J3
echo "13. Move J3 -80 degree..."
curl http://127.0.0.1:5000/move_j/J3?degree=80
echo "done\n"

echo "14. Move J3 back to 0..."
curl http://127.0.0.1:5000/move_j/J3?degree=-80
echo "done\n"

#J4
echo "ove J4 90 degree..."
curl http://127.0.0.1:5000/move_j/J4?degree=-90
echo "done\n"

echo "Move J4 back to 0..."
curl http://127.0.0.1:5000/move_j/J4?degree=90
echo "done\n"

#J5
echo "Move J5 -90 degree..."
curl http://127.0.0.1:5000/move_j/J5?degree=-90
echo "done\n"

echo "Move J5 back to 0..."
curl http://127.0.0.1:5000/move_j/J5?degree=90
echo "done\n"

#J6
echo "Move J6 -90 degree..."
curl http://127.0.0.1:5000/move_j/J6?degree=-90
echo "done\n"

echo "Move J6 back to 0..."
curl http://127.0.0.1:5000/move_j/J6?degree=90
echo "done\n"

#recheck ifo
echo "ry get machine info again"
curl http://127.0.0.1:5000/info
echo "\n"



##### try gripper  ####
echo "try put gripper 0 ..."
curl http://127.0.0.1:5000/servo/mygripper?degree=90
echo "done\n"
sleep 2

echo "try put gripper 90 ..."
curl http://127.0.0.1:5000/servo/mygripper?degree=90
echo "done\n"
sleep 2

echo "try put gripper 120 ..."
curl http://127.0.0.1:5000/servo/mygripper?degree=120
echo "\n"
sleep 2

