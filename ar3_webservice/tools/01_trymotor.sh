#/bin/bash
curl http://127.0.0.1:5000/servo/mygripper?degree=90
sleep 2
curl http://127.0.0.1:5000/servo/mygripper?degree=120
sleep 2
curl http://127.0.0.1:5000/servo/mygripper?degree=140
sleep 2
curl http://127.0.0.1:5000/servo/mygripper?degree=90
sleep 2

curl http://127.0.0.1:5000//move_j/j1?degree=-10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j1?degree=10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j1?degree=-20&movetype=rotate
curl http://127.0.0.1:5000//move_j/j1?degree=20&movetype=rotate


curl http://127.0.0.1:5000//move_j/j2?degree=10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j2?degree=-10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j2?degree=20&movetype=rotate
curl http://127.0.0.1:5000//move_j/j2?degree=-20&movetype=rotate


curl http://127.0.0.1:5000//move_j/j3?degree=10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j3?degree=-10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j3?degree=20&movetype=rotate
curl http://127.0.0.1:5000//move_j/j3?degree=-20&movetype=rotate

curl http://127.0.0.1:5000//move_j/j4?degree=10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j4?degree=-10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j4?degree=20&movetype=rotate
curl http://127.0.0.1:5000//move_j/j4?degree=-20&movetype=rotate

curl http://127.0.0.1:5000//move_j/j5?degree=10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j5?degree=-10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j5?degree=20&movetype=rotate
curl http://127.0.0.1:5000//move_j/j5?degree=-20&movetype=rotate

curl http://127.0.0.1:5000//move_j/j6?degree=10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j6?degree=-10&movetype=rotate
curl http://127.0.0.1:5000//move_j/j6?degree=20&movetype=rotate
curl http://127.0.0.1:5000//move_j/j6?degree=-20&movetype=rotate
