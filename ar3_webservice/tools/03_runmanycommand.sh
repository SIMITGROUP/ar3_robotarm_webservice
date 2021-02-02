#!/bin/bash
echo "This script will execute many robot movement, standby your hand at emergency stop button to prevent accident damage your arm\n"

echo "1. Try get machine info..."
curl http://127.0.0.1:5000/info
echo "\n"

##### calibration  ####
echo "2. Calibrate J1..."
curl http://127.0.0.1:5000/calibrate/J1
echo "done\n"

echo "3. Calibrate J2..."
curl http://127.0.0.1:5000/calibrate/J2
echo "done\n"

echo "4. Calibrate J3..."
curl http://127.0.0.1:5000/calibrate/J3
echo "done\n"

echo "5. Calibrate J4..."
curl http://127.0.0.1:5000/calibrate/J4
echo "done\n"

echo "6. Calibrate J5..."
curl http://127.0.0.1:5000/calibrate/J5
echo "done\n"

echo "7. Calibrate J6..."
curl http://127.0.0.1:5000/calibrate/J6
echo "done\n"

echo "8. Calibrate all together..."
curl http://127.0.0.1:5000/calibrate/all
echo "done\n"

##### move join  ####
echo "9. Move J1 -90 degree..."
curl http://127.0.0.1:5000/move_j/J1?degree=-90
echo "done\n"

echo "10. Move J1 back to 0..."
curl http://127.0.0.1:5000/move_j/J1?degree=90
echo "done\n"

echo "11. Move J2 -90 degree..."
curl http://127.0.0.1:5000/move_j/J2?degree=-90
echo "done\n"

echo "12. Move J2 back to 0..."
curl http://127.0.0.1:5000/move_j/J2?degree=90
echo "done\n"

echo "13. Move J2 -90 degree..."
curl http://127.0.0.1:5000/move_j/J3?degree=-90
echo "done\n"

echo "14. Move J2 back to 0..."
curl http://127.0.0.1:5000/move_j/J3?degree=90
echo "done\n"

echo "15. Move J2 -90 degree..."
curl http://127.0.0.1:5000/move_j/J4?degree=-90
echo "done\n"

echo "16. Move J2 back to 0..."
curl http://127.0.0.1:5000/move_j/J4?degree=90
echo "done\n"

echo "17. Move J2 -90 degree..."
curl http://127.0.0.1:5000/move_j/J5?degree=-90
echo "done\n"

echo "18. Move J2 back to 0..."
curl http://127.0.0.1:5000/move_j/J5?degree=90
echo "done\n"

echo "19. Move J2 -90 degree..."
curl http://127.0.0.1:5000/move_j/J6?degree=-90
echo "done\n"

echo "20. Move J2 back to 0..."
curl http://127.0.0.1:5000/move_j/J6?degree=90
echo "done\n"

##### try gripper  ####
echo "21. try put gripper 0 ..."
curl http://127.0.0.1:5000/servo/mygripper?degree=90
echo "done\n"
sleep 2

echo "22. try put gripper 90 ..."
curl http://127.0.0.1:5000/servo/mygripper?degree=90
echo "done\n"
sleep 2

echo "23. try put gripper 120 ..."
curl http://127.0.0.1:5000/servo/mygripper?degree=120
echo "\n"
sleep 2

echo "24. Try get machine info again"
curl http://127.0.0.1:5000/info
echo "\n"
