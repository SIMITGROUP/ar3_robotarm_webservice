import sys
import numpy as np
sys.path.append("include")
import kinematics as kn
deg = [-0.61,
-62.73,
123.99,
0.51,
-47.78,
-3.98]
T = kn.fKinematic(deg)
print("Initial T.t")
print(T.t)
# x+10mm, y+1mm, z-2mm
x = 200
y = 20
z = 200
T.t[0]+=x/1000
T.t[1]+=y/1000
T.t[2]+=z/1000


print("New T.t")
print(kn.getXYZ(T))
# get new 6 joints value in rad
sol = kn.iKinematic(T)
print("init degrees:")
print(deg)
print("new degrees:")

newdeg=np.degrees(sol.q)
newdeg[2] = newdeg[2] + 90
newdeg[3] =  newdeg[3] - 180

if newdeg[3] < -180:
    newdeg[3] =   newdeg[3] + 360

newdeg[4] = newdeg[4] * -1
print(newdeg)