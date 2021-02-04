#!/bin/bash
while :
do
	curl "http://127.0.0.1:5000/setposition?J1=30&J2=-70&J3=30&J4=40&J5=30&J6=50&gripper1=90&t1=10&"
	curl "http://127.0.0.1:5000/setposition?J1=0&J2=-90&J3=0&J4=0&J5=10&J6=10&gripper1=110&t1=50&"
	curl "http://127.0.0.1:5000/setposition?J1=-30&J2=-40&J3=-30&J4=-20&J5=10&J6=-10&gripper1=160&t1=30&"
done