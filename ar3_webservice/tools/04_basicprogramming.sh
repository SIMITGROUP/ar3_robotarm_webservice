#!/bin/bash
echo "Insert server api url, leave empty to use http://127.0.0.1:5000  (default):"
read hostname
echo $hostname


if [ -z $hostname ]
  then
    hostname="http://127.0.0.1:5000"
fi

echo "API url = $hostname"

while :
do
  echo "run program 1.."
	curl "$hostname/setposition?J1=90&J2=-70&J3=60&J4=30&J5=30&J6=50&gripper1=90" #&t1=10&
	echo "done"
	sleep 1
	echo "run program 2..."
	curl "$hostname/setposition?J1=0&J2=-20&J3=0&J4=0&J5=80&J6=10&gripper1=110" #&t1=100&
	echo "done"
	sleep 1
	echo "run program 3..."
	curl "$hostname/setposition?J1=-90&J2=-90&J3=-50&J4=-20&J5=50&J6=-10&gripper1=160" #
	echo "done, sleep 2 sec and continue next loop"
	sleep 2
done