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
T.t[0]+=0.01


print("New T.t")
print(kn.getXYZ(T))
# get new 6 joints value in rad
sol = kn.iKinematic(T)
print("init degrees:")
print(deg)
print("new degrees:")

newdeg=np.degrees(sol.q)
# newdeg[2] = newdeg[2] + 90
# newdeg[5] = newdeg[5] - 180
print(newdeg)