import platform 
import sys
sys.path.append("templates")
myplatform = platform.system()


stopProgButX=190
ProgButX=202
progViewWidth=84
calibration_joinx=440
calibration_entryjoinx=380
calibration_entrydhx=650
calibration_alphax = 710
ProgEntryFieldW=20
jogbuttonwidth=3
comportlabelx=310
comPortEntryFieldX=450
comPortEntryFieldw=12
manualprogramentryx=630
manualprogramentryw=95
calibrate_buttoncol2x=170
tab1_instructionbuttonw=20
comPortButx=495
if myplatform == "Linux":
    import Linux as themes
elif myplatform == "Darwin":
    import MacOS as themes
elif myplatform == "Windows":
    import Windows as themes


progViewWidth = themes.progViewWidth
calibration_joinx = themes.calibration_joinx
calibration_alphax = themes.calibration_alphax 
stopProgButX = themes.stopProgButX
ProgButX = themes.ProgButX
ProgEntryFieldW=themes.ProgEntryFieldW
comportlabelx = themes.comportlabelx
comPortEntryFieldX = themes.comPortEntryFieldX
comPortButx=themes.comPortButx
calibration_entryjoinx = themes.calibration_entryjoinx
calibration_entrydhx = themes.calibration_entrydhx
calibrate_buttoncol2x = themes.calibrate_buttoncol2x

tab1_instructionbuttonw=themes.tab1_instructionbuttonw
jogbuttonwidth = themes.jogbuttonwidth
manualprogramentryx=themes.manualprogramentryx
manualprogramentryw=themes.manualprogramentryw