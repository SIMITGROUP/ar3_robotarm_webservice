import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath import SE3

class AR3(DHRobot):

    def __init__(self, symbolic=False):
        if symbolic:
            import spatialmath.base.symbolic as sym
            zero = sym.zero()
            pi = sym.pi()
        else:
            from math import pi
            zero = 0.0

        deg = pi / 180
        inch = 0.0254

        super().__init__(
            [

                RevoluteDH(d=0.16977, alpha=-pi / 2, a=0.0642),
                RevoluteDH(d=0, alpha=0, a=0.305),
                RevoluteDH(d=0, alpha=pi / 2, a=0),
                RevoluteDH(d=-0.22263, alpha=-pi / 2, a=0),
                RevoluteDH(d=0, alpha=pi / 2, a=0),
                RevoluteDH(d=-0.03625, alpha=0, a=0),

            ],
            name="AR3",
            manufacturer="AR3 ",
            # keywords=('dynamics', 'symbolic'),
            # symbolic=symbolic
        )

        self.addconfiguration("qz", np.array([0, 0, 0, 0, 0, 0]))
        # horizontal along the x-axis
        self.addconfiguration("qr", np.r_[180, 0, 0, 0, 90, 0] * deg)


if __name__ == '__main__':  # pragma nocover

    ar3 = AR3(symbolic=False)
    print(ar3)
    print(ar3.dyntable())