#!/bin/bash
while :
do
	curl "http://127.0.0.1:5000/setposition?J1=90&J2=-70&J3=60&J4=30&J5=30&J6=50&gripper1=90" #&t1=10&
	curl "http://127.0.0.1:5000/setposition?J1=0&J2=-20&J3=0&J4=0&J5=80&J6=10&gripper1=110" #&t1=100&
	curl "http://127.0.0.1:5000/setposition?J1=-90&J2=-90&J3=-50&J4=-20&J5=50&J6=-10&gripper1=160" #
done