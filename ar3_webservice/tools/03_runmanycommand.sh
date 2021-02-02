#!/bin/bash
echo "1. Try get machine info"
curl http://127.0.0.1:5000/info

##### calibration  ####
echo "2. Calibrate J1"
curl http://127.0.0.1:5000/calibrate/J1

echo "3. Calibrate J2"
curl http://127.0.0.1:5000/calibrate/J2

echo "4. Calibrate J3"
curl http://127.0.0.1:5000/calibrate/J3

echo "5. Calibrate J4"
curl http://127.0.0.1:5000/calibrate/J4

echo "6. Calibrate J5"
curl http://127.0.0.1:5000/calibrate/J5

echo "7. Calibrate J6"
curl http://127.0.0.1:5000/calibrate/J6

echo "8. Calibrate all together"
curl http://127.0.0.1:5000/calibrate/all

##### move join  ####
echo "9. Move J1 -90 degree"
curl http://127.0.0.1:5000/move_j/J1?degree=-90

echo "10. Move J1 back to 0"
curl http://127.0.0.1:5000/move_j/J1?degree=90

echo "11. Move J2 -90 degree"
curl http://127.0.0.1:5000/move_j/J2?degree=-90

echo "12. Move J2 back to 0"
curl http://127.0.0.1:5000/move_j/J2?degree=90

echo "13. Move J2 -90 degree"
curl http://127.0.0.1:5000/move_j/J3?degree=-90

echo "14. Move J2 back to 0"
curl http://127.0.0.1:5000/move_j/J3?degree=90

echo "15. Move J2 -90 degree"
curl http://127.0.0.1:5000/move_j/J4?degree=-90

echo "16. Move J2 back to 0"
curl http://127.0.0.1:5000/move_j/J4?degree=90

echo "17. Move J2 -90 degree"
curl http://127.0.0.1:5000/move_j/J5?degree=-90

echo "18. Move J2 back to 0"
curl http://127.0.0.1:5000/move_j/J5?degree=90

echo "19. Move J2 -90 degree"
curl http://127.0.0.1:5000/move_j/J6?degree=-90

echo "20. Move J2 back to 0"
curl http://127.0.0.1:5000/move_j/J6?degree=90

##### try gripper  ####
echo "21. try put gripper 0 "
curl http://127.0.0.1:5000/servo/mygripper?degree=90
sleep 2

echo "21. try put gripper 90 "
curl http://127.0.0.1:5000/servo/mygripper?degree=90
sleep 2

echo "21. try put gripper 120 "
curl http://127.0.0.1:5000/servo/mygripper?degree=120
sleep 2
