# this file dedicated use for store mathmetical calculation like change rotation to linear movement
# not in use yet
from ar3model import AR3
robot = AR3()


def fKinematic(degrees):
    rad  = np.radians(degrees)
    T = robot.fkine(rad)
    return T

def getXYZ(T):
    return T.t


def iKinematic(T):
    sol = robot.ikine_LM(T)
    return sol