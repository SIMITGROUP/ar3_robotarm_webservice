# this file dedicated use for store mathmetical calculation like change rotation to linear movement
# not in use yet


# copy exactly from ARCS.py

def CalcFwdKin():
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  global WC
  if (J1AngCur == 0):
    J1AngCur = .0001
  if (J2AngCur == 0):
    J2AngCur = .0001
  if (J3AngCur == 0):
    J3AngCur = .0001
  if (J4AngCur == 0):
    J4AngCur = .0001
  if (J5AngCur == 0):
    J5AngCur = .0001
  if (J6AngCur == 0):
    J6AngCur = .0001
  ## Set Wrist Config
  if (J5AngCur > 0):
    WC = "F"
  else:
    WC = "N"
  ## CONVERT TO RADIANS
  C4 = math.radians(float(J1AngCur)+DHt1)
  C5 = math.radians(float(J2AngCur)+DHt2)
  C6 = math.radians(float(J3AngCur)+DHt3)
  C7 = math.radians(float(J4AngCur)+DHt4)
  C8 = math.radians(float(J5AngCur)+DHt5)
  C9 = math.radians(float(J6AngCur)+DHt6)
  ## DH TABLE
  C13 = C4
  C14 = C5
  C15 = C6
  C16 = C7
  C17 = C8
  C18 = C9
  D13 = math.radians(DHr1)
  D14 = math.radians(DHr2)
  D15 = math.radians(DHr3)
  D16 = math.radians(DHr4)
  D17 = math.radians(DHr5)
  D18 = math.radians(DHr6)
  E13 = DHd1
  E14 = DHd2
  E15 = DHd3
  E16 = DHd4
  E17 = DHd5
  E18 = DHd6
  F13 = DHa1
  F14 = DHa2
  F15 = DHa3
  F16 = DHa4
  F17 = DHa5
  F18 = DHa6
  ## WORK FRAME INPUT
  H13 = float(UFxEntryField.get())
  H14 = float(UFyEntryField.get())
  H15 = float(UFzEntryField.get())
  H16 = float(UFrxEntryField.get())
  H17 = float(UFryEntryField.get())
  H18 = float(UFrzEntryField.get())
  ## TOOL FRAME INPUT
  J13 = float(TFxEntryField.get())
  J14 = float(TFyEntryField.get())
  J15 = float(TFzEntryField.get())
  J16 = float(TFrxEntryField.get())
  J17 = float(TFryEntryField.get())
  J18 = float(TFrzEntryField.get())
  ## WORK FRAME TABLE
  B21 = math.cos(math.radians(H18))*math.cos(math.radians(H17))
  B22 = math.sin(math.radians(H18))*math.cos(math.radians(H17))
  B23 = -math.sin(math.radians(H18))
  B24 = 0
  C21 = -math.sin(math.radians(H18))*math.cos(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  C22 = math.cos(math.radians(H18))*math.cos(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  C23 = math.cos(math.radians(H17))*math.sin(math.radians(H16))
  C24 = 0
  D21 = math.sin(math.radians(H18))*math.sin(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  D22 = -math.cos(math.radians(H18))*math.sin(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  D23 = math.cos(math.radians(H17))*math.cos(math.radians(H16))
  D24 = 0
  E21 = H13
  E22 = H14
  E23 = H15
  E24 = 1
  ## J1 FRAME
  B27 = math.cos(C13)
  B28 = math.sin(C13)
  B29 = 0
  B30 = 0
  C27 = -math.sin(C13)*math.cos(D13)
  C28 = math.cos(C13)*math.cos(D13)
  C29 = math.sin(D13)
  C30 = 0
  D27 = math.sin(C13)*math.sin(D13)
  D28 = -math.cos(C13)*math.sin(D13)
  D29 = math.cos(D13)
  D30 = 0
  E27 = F13*math.cos(C13)
  E28 = F13*math.sin(C13)
  E29 = E13
  E30 = 1
  ## J2 FRAME
  B33 = math.cos(C14)
  B34 = math.sin(C14)
  B35 = 0
  B36 = 0
  C33 = -math.sin(C14)*math.cos(D14)
  C34 = math.cos(C14)*math.cos(D14)
  C35 = math.sin(D14)
  C36 = 0
  D33 = math.sin(C14)*math.sin(D14)
  D34 = -math.cos(C14)*math.sin(D14)
  D35 = math.cos(D14)
  D36 = 0
  E33 = F14*math.cos(C14)
  E34 = F14*math.sin(C14)
  E35 = E14
  E36 = 1
  ## J3 FRAME
  B39 = math.cos(C15)
  B40 = math.sin(C15)
  B41 = 0
  B42 = 0
  C39 = -math.sin(C15)*math.cos(D15)
  C40 = math.cos(C15)*math.cos(D15)
  C41 = math.sin(D15)
  C42 = 0
  D39 = math.sin(C15)*math.sin(D15)
  D40 = -math.cos(C15)*math.sin(D15)
  D41 = math.cos(D15)
  D42 = 0
  E39 = F15*math.cos(C15)
  E40 = F15*math.sin(C15)
  E41 = 0
  E42 = 1
  ## J4 FRAME
  B45 = math.cos(C16)
  B46 = math.sin(C16)
  B47 = 0
  B48 = 0
  C45 = -math.sin(C16)*math.cos(D16)
  C46 = math.cos(C16)*math.cos(D16)
  C47 = math.sin(D16)
  C48 = 0
  D45 = math.sin(C16)*math.sin(D16)
  D46 = -math.cos(C16)*math.sin(D16)
  D47 = math.cos(D16)
  D48 = 0
  E45 = F16*math.cos(C16)
  E46 = F16*math.sin(C16)
  E47 = E16
  E48 = 1
  ## J5 FRAME
  B51 = math.cos(C17)
  B52 = math.sin(C17)
  B53 = 0
  B54 = 0
  C51 = -math.sin(C17)*math.cos(D17)
  C52 = math.cos(C17)*math.cos(D17)
  C53 = math.sin(D17)
  C54 = 0
  D51 = math.sin(C17)*math.sin(D17)
  D52 = -math.cos(C17)*math.sin(D17)
  D53 = math.cos(D17)
  D54 = 0
  E51 = F17*math.cos(C17)
  E52 = F17*math.sin(C17)
  E53 = E17
  E54 = 1
  ## J6 FRAME
  B57 = math.cos(C18)
  B58 = math.sin(C18)
  B59 = 0
  B60 = 0
  C57 = -math.sin(C18)*math.cos(D18)
  C58 = math.cos(C18)*math.cos(D18)
  C59 = math.sin(D18)
  C60 = 0
  D57 = math.sin(C18)*math.sin(D18)
  D58 = -math.cos(C18)*math.sin(D18)
  D59 = math.cos(D18)
  D60 = 0
  E57 = F18*math.cos(C18)
  E58 = F18*math.sin(C18)
  E59 = E18
  E60 = 1
  ## TOOL FRAME
  B63 = math.cos(math.radians(J18))*math.cos(math.radians(J17))
  B64 = math.sin(math.radians(J18))*math.cos(math.radians(J17))
  B65 = -math.sin(math.radians(J18))
  B66 = 0
  C63 = -math.sin(math.radians(J18))*math.cos(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  C64 = math.cos(math.radians(J18))*math.cos(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  C65 = math.cos(math.radians(J17))*math.sin(math.radians(J16))
  C66 = 0
  D63 = math.sin(math.radians(J18))*math.sin(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  D64 = -math.cos(math.radians(J18))*math.sin(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  D65 = math.cos(math.radians(J17))*math.cos(math.radians(J16))
  D66 = 0
  E63 = J13
  E64 = J14
  E65 = J15
  E66 = 1
  ## WF*J1
  G24 = (B21*B27)+(C21*B28)+(D21*B29)+(E21*B30)
  G25 = (B22*B27)+(C22*B28)+(D22*B29)+(E22*B30)
  G26 = (B23*B27)+(C23*B28)+(D23*B29)+(E23*B30)
  G27 = (B24*B27)+(C24*B28)+(D24*B29)+(E24*B30)
  H24 = (B21*C27)+(C21*C28)+(D21*C29)+(E21*C30)
  H25 = (B22*C27)+(C22*C28)+(D22*C29)+(E22*C30)
  H26 = (B23*C27)+(C23*C28)+(D23*C29)+(E23*C30)
  H27 = (B24*C27)+(C24*C28)+(D24*C29)+(E24*C30)
  I24 = (B21*D27)+(C21*D28)+(D21*D29)+(E21*D30)
  I25 = (B22*D27)+(C22*D28)+(D22*D29)+(E22*D30)
  I26 = (B23*D27)+(C23*D28)+(D23*D29)+(E23*D30)
  I27 = (B24*D27)+(C24*D28)+(D24*D29)+(E24*D30)
  J24 = (B21*E27)+(C21*E28)+(D21*E29)+(E21*E30)
  J25 = (B22*E27)+(C22*E28)+(D22*E29)+(E22*E30)
  J26 = (B23*E27)+(C23*E28)+(D23*E29)+(E23*E30)
  J27 = (B24*E27)+(C24*E28)+(D24*E29)+(E24*E30)
  ## (WF*J1)*J2
  G30 = (G24*B33)+(H24*B34)+(I24*B35)+(J24*B36)
  G31 = (G25*B33)+(H25*B34)+(I25*B35)+(J25*B36)
  G32 = (G26*B33)+(H26*B34)+(I26*B35)+(J26*B36)
  G33 = (G27*B33)+(H27*B34)+(I27*B35)+(J27*B36)
  H30 = (G24*C33)+(H24*C34)+(I24*C35)+(J24*C36)
  H31 = (G25*C33)+(H25*C34)+(I25*C35)+(J25*C36)
  H32 = (G26*C33)+(H26*C34)+(I26*C35)+(J26*C36)
  H33 = (G27*C33)+(H27*C34)+(I27*C35)+(J27*C36)
  I30 = (G24*D33)+(H24*D34)+(I24*D35)+(J24*D36)
  I31 = (G25*D33)+(H25*D34)+(I25*D35)+(J25*D36)
  I32 = (G26*D33)+(H26*D34)+(I26*D35)+(J26*D36)
  I33 = (G27*D33)+(H27*D34)+(I27*D35)+(J27*D36)
  J30 = (G24*E33)+(H24*E34)+(I24*E35)+(J24*E36)
  J31 = (G25*E33)+(H25*E34)+(I25*E35)+(J25*E36)
  J32 = (G26*E33)+(H26*E34)+(I26*E35)+(J26*E36)
  J33 = (G27*E33)+(H27*E34)+(I27*E35)+(J27*E36)
  ## (WF*J1*J2)*J3
  G36 = (G30*B39)+(H30*B40)+(I30*B41)+(J30*B42)
  G37 = (G31*B39)+(H31*B40)+(I31*B41)+(J31*B42)
  G38 = (G32*B39)+(H32*B40)+(I32*B41)+(J32*B42)
  G39 = (G33*B39)+(H33*B40)+(I33*B41)+(J33*B42)
  H36 = (G30*C39)+(H30*C40)+(I30*C41)+(J30*C42)
  H37 = (G31*C39)+(H31*C40)+(I31*C41)+(J31*C42)
  H38 = (G32*C39)+(H32*C40)+(I32*C41)+(J32*C42)
  H39 = (G33*C39)+(H33*C40)+(I33*C41)+(J33*C42)
  I36 = (G30*D39)+(H30*D40)+(I30*D41)+(J30*D42)
  I37 = (G31*D39)+(H31*D40)+(I31*D41)+(J31*D42)
  I38 = (G32*D39)+(H32*D40)+(I32*D41)+(J32*D42)
  I39 = (G33*D39)+(H33*D40)+(I33*D41)+(J33*D42)
  J36 = (G30*E39)+(H30*E40)+(I30*E41)+(J30*E42)
  J37 = (G31*E39)+(H31*E40)+(I31*E41)+(J31*E42)
  J38 = (G32*E39)+(H32*E40)+(I32*E41)+(J32*E42)
  J39 = (G33*E39)+(H33*E40)+(I33*E41)+(J33*E42)
  ## (WF*J1*J2*J3)*J4
  G42 = (G36*B45)+(H36*B46)+(I36*B47)+(J36*B48)
  G43 = (G37*B45)+(H37*B46)+(I37*B47)+(J37*B48)
  G44 = (G38*B45)+(H38*B46)+(I38*B47)+(J38*B48)
  G45 = (G39*B45)+(H39*B46)+(I39*B47)+(J39*B48)
  H42 = (G36*C45)+(H36*C46)+(I36*C47)+(J36*C48)
  H43 = (G37*C45)+(H37*C46)+(I37*C47)+(J37*C48)
  H44 = (G38*C45)+(H38*C46)+(I38*C47)+(J38*C48)
  H45 = (G39*C45)+(H39*C46)+(I39*C47)+(J39*C48)
  I42 = (G36*D45)+(H36*D46)+(I36*D47)+(J36*D48)
  I43 = (G37*D45)+(H37*D46)+(I37*D47)+(J37*D48)
  I44 = (G38*D45)+(H38*D46)+(I38*D47)+(J38*D48)
  I45 = (G39*D45)+(H39*D46)+(I39*D47)+(J39*D48)
  J42 = (G36*E45)+(H36*E46)+(I36*E47)+(J36*E48)
  J43 = (G37*E45)+(H37*E46)+(I37*E47)+(J37*E48)
  J44 = (G38*E45)+(H38*E46)+(I38*E47)+(J38*E48)
  J45 = (G39*E45)+(H39*E46)+(I39*E47)+(J39*E48)
  ## (WF*J1*J2*J3*J4)*J5
  G48 = (G42*B51)+(H42*B52)+(I42*B53)+(J42*B54)
  G49 = (G43*B51)+(H43*B52)+(I43*B53)+(J43*B54)
  G50 = (G44*B51)+(H44*B52)+(I44*B53)+(J44*B54)
  G51 = (G45*B51)+(H45*B52)+(I45*B53)+(J45*B54)
  H48 = (G42*C51)+(H42*C52)+(I42*C53)+(J42*C54)
  H49 = (G43*C51)+(H43*C52)+(I43*C53)+(J43*C54)
  H50 = (G44*C51)+(H44*C52)+(I44*C53)+(J44*C54)
  H51 = (G45*C51)+(H45*C52)+(I45*C53)+(J45*C54)
  I48 = (G42*D51)+(H42*D52)+(I42*D53)+(J42*D54)
  I49 = (G43*D51)+(H43*D52)+(I43*D53)+(J43*D54)
  I50 = (G44*D51)+(H44*D52)+(I44*D53)+(J44*D54)
  I51 = (G45*D51)+(H45*D52)+(I45*D53)+(J45*D54)
  J48 = (G42*E51)+(H42*E52)+(I42*E53)+(J42*E54)
  J49 = (G43*E51)+(H43*E52)+(I43*E53)+(J43*E54)
  J50 = (G44*E51)+(H44*E52)+(I44*E53)+(J44*E54)
  J51 = (G45*E51)+(H45*E52)+(I45*E53)+(J45*E54)
  ## (WF*J1*J2*J3*J4*J5)*J6
  G54 = (G48*B57)+(H48*B58)+(I48*B59)+(J48*B60)
  G55 = (G49*B57)+(H49*B58)+(I49*B59)+(J49*B60)
  G56 = (G50*B57)+(H50*B58)+(I50*B59)+(J50*B60)
  G57 = (G51*B57)+(H51*B58)+(I51*B59)+(J51*B60)
  H54 = (G48*C57)+(H48*C58)+(I48*C59)+(J48*C60)
  H55 = (G49*C57)+(H49*C58)+(I49*C59)+(J49*C60)
  H56 = (G50*C57)+(H50*C58)+(I50*C59)+(J50*C60)
  H57 = (G51*C57)+(H51*C58)+(I51*C59)+(J51*C60)
  I54 = (G48*D57)+(H48*D58)+(I48*D59)+(J48*D60)
  I55 = (G49*D57)+(H49*D58)+(I49*D59)+(J49*D60)
  I56 = (G50*D57)+(H50*D58)+(I50*D59)+(J50*D60)
  I57 = (G51*D57)+(H51*D58)+(I51*D59)+(J51*D60)
  J54 = (G48*E57)+(H48*E58)+(I48*E59)+(J48*E60)
  J55 = (G49*E57)+(H49*E58)+(I49*E59)+(J49*E60)
  J56 = (G50*E57)+(H50*E58)+(I50*E59)+(J50*E60)
  J57 = (G51*E57)+(H51*E58)+(I51*E59)+(J51*E60)
  ## (WF*J1*J2*J3*J4*J5*J6)*TF
  G60 = (G54*B63)+(H54*B64)+(I54*B65)+(J54*B66)
  G61 = (G55*B63)+(H55*B64)+(I55*B65)+(J55*B66)
  G62 = (G56*B63)+(H56*B64)+(I56*B65)+(J56*B66)
  G63 = (G57*B63)+(H57*B64)+(I57*B65)+(J57*B66)
  H60 = (G54*C63)+(H54*C64)+(I54*C65)+(J54*C66)
  H61 = (G55*C63)+(H55*C64)+(I55*C65)+(J55*C66)
  H62 = (G56*C63)+(H56*C64)+(I56*C65)+(J56*C66)
  H63 = (G57*C63)+(H57*C64)+(I57*C65)+(J57*C66)
  I60 = (G54*D63)+(H54*D64)+(I54*D65)+(J54*D66)
  I61 = (G55*D63)+(H55*D64)+(I55*D65)+(J55*D66)
  I62 = (G56*D63)+(H56*D64)+(I56*D65)+(J56*D66)
  I63 = (G57*D63)+(H57*D64)+(I57*D65)+(J57*D66)
  J60 = (G54*E63)+(H54*E64)+(I54*E65)+(J54*E66)
  J61 = (G55*E63)+(H55*E64)+(I55*E65)+(J55*E66)
  J62 = (G56*E63)+(H56*E64)+(I56*E65)+(J56*E66)
  J63 = (G57*E63)+(H57*E64)+(I57*E65)+(J57*E66)
  ## GET YPR
  I8 = math.atan2(math.sqrt((I60**2)+(I61**2)),-I62)
  I7 = math.atan2((G62/I8),(H62/I8))
  I9 = math.atan2((I60/I8),(I61/I8))
  H4 = J60
  H5 = J61
  H6 = J62
  H7 = math.degrees(I7)
  H8 = math.degrees(I8)
  H9 = math.degrees(I9)
  XcurPos = J60
  YcurPos = J61
  ZcurPos = J62
  RxcurPos = H9
  RycurPos = H8
  RzcurPos = H7
  XcurEntryField.delete(0, 'end')
  XcurEntryField.insert(0,str(XcurPos))
  YcurEntryField.delete(0, 'end')
  YcurEntryField.insert(0,str(YcurPos))
  ZcurEntryField.delete(0, 'end')
  ZcurEntryField.insert(0,str(ZcurPos))
  RxcurEntryField.delete(0, 'end')
  RxcurEntryField.insert(0,str(RxcurPos))
  RycurEntryField.delete(0, 'end')
  RycurEntryField.insert(0,str(RycurPos))
  RzcurEntryField.delete(0, 'end')
  RzcurEntryField.insert(0,str(RzcurPos))



def CalcRevKin(CX,CY,CZ,CRx,CRy,CRz,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz):
  global J1out
  global J2out
  global J3out
  global J4out
  global J5out
  global J6out
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  if (J1AngCur == 0):
    J1AngCur = .0001
  if (J2AngCur == 0):
    J2AngCur = .0001
  if (J3AngCur == 0):
    J3AngCur = .0001
  if (J4AngCur == 0):
    J4AngCur = .0001
  if (J5AngCur == 0):
    J5AngCur = .0001
  if (J6AngCur == 0):
    J6AngCur = .0001
  #input
  O4 = CX
  O5 = CY
  O6 = CZ
  O9 = CRx
  O8 = CRy
  O7 = CRz
  V8 = WC
  if (O4 == 0):
    O4 = .0001
  if (O5 == 0):
    O5 = .0001
  if (O6 == 0):
    O6 = .0001
  if (O7 == 0):
    O7 = .0001
  if (O8 == 0):
    O8 = .0001
  if (O9 == 0):
    O9 = .0001
  #quadrant
  if (O4>0 and O5>0):
    V9 = 1
  elif (O4>0 and O5<0):
    V9 = 2
  elif (O4<0 and O5<0):
    V9 = 3
  elif (O4<0 and O5>0):
    V9 = 4
  ## DH TABLE
  D13 = math.radians(DHr1)
  D14 = math.radians(DHr2)
  D15 = math.radians(DHr3)
  D16 = math.radians(DHr4)
  D17 = math.radians(DHr5)
  D18 = math.radians(DHr6)
  E13 = DHd1
  E14 = DHd2
  E15 = DHd3
  E16 = DHd4
  E17 = DHd5
  E18 = DHd6
  F13 = DHa1
  F14 = DHa2
  F15 = DHa3
  F16 = DHa4
  F17 = DHa5
  F18 = DHa6
  ## WORK FRAME INPUT
  H13 = -float(UFxEntryField.get())
  H14 = -float(UFyEntryField.get())
  H15 = -float(UFzEntryField.get())
  H16 = -float(UFrxEntryField.get())
  H17 = -float(UFryEntryField.get())
  H18 = -float(UFrzEntryField.get())
  ## TOOL FRAME INPUT
  J13 = -float(TFxEntryField.get()) + TCX
  J14 = -float(TFyEntryField.get()) + TCY
  J15 = -float(TFzEntryField.get()) + TCZ
  J16 = -float(TFrxEntryField.get()) + TCRx
  J17 = -float(TFryEntryField.get()) + TCRy
  J18 = -float(TFrzEntryField.get()) + TCRz
  ## WORK FRAME TABLE
  N30 = math.cos(math.radians(H18))*math.cos(math.radians(H17))
  O30 = -math.sin(math.radians(H18))*math.cos(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  P30 = math.sin(math.radians(H18))*math.sin(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  Q30 = H13
  N31 = math.sin(math.radians(H18))*math.cos(math.radians(H17))
  O31 = math.cos(math.radians(H18))*math.cos(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  P31 = -math.cos(math.radians(H18))*math.sin(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  Q31 = H14
  N32 = -math.sin(math.radians(H18))
  O32 = math.cos(math.radians(H17))*math.sin(math.radians(H16))
  P32 = math.cos(math.radians(H17))*math.cos(math.radians(H16))
  Q32 = H15
  N33 = 0
  O33 = 0
  P33 = 0
  Q33 = 1
  ## R 0-T
  X30 = math.cos(math.radians(O7))*math.cos(math.radians(O9))-math.cos(math.radians(O8))*math.sin(math.radians(O7))*math.sin(math.radians(O9))
  Y30 = math.cos(math.radians(O9))*math.sin(math.radians(O7))+math.cos(math.radians(O7))*math.cos(math.radians(O8))*math.sin(math.radians(O9))
  Z30 = math.sin(math.radians(O8))*math.sin(math.radians(O9))
  AA30 = O4
  X31 = math.cos(math.radians(O8))*math.cos(math.radians(O9))*math.sin(math.radians(O7))+math.cos(math.radians(O7))*math.sin(math.radians(O9))
  Y31 = math.cos(math.radians(O7))*math.cos(math.radians(O8))*math.cos(math.radians(O9))-math.sin(math.radians(O7))*math.sin(math.radians(O9))
  Z31 = math.cos(math.radians(O9))*math.sin(math.radians(O8))
  AA31 = O5
  X32 = math.sin(math.radians(O7))*math.sin(math.radians(O8))
  Y32 = math.cos(math.radians(O7))*math.sin(math.radians(O8))
  Z32 = -math.cos(math.radians(O8))
  AA32 = O6
  X33 = 0
  Y33 = 0
  Z33 = 0
  AA33 = 1
  ## R 0-T   offset by work frame
  X36 = ((N30*X30)+(O30*X31)+(P30*X32)+(Q30*X33))*-1
  Y36 = (N30*Y30)+(O30*Y31)+(P30*Y32)+(Q30*Y33)
  Z36 = (N30*Z30)+(O30*Z31)+(P30*Z32)+(Q30*Z33)
  AA36 = (N30*AA30)+(O30*AA31)+(P30*AA32)+(Q30*AA33)
  X37 = (N31*X30)+(O31*X31)+(P31*X32)+(Q31*X33)
  Y37 = (N31*Y30)+(O31*Y31)+(P31*Y32)+(Q31*Y33)
  Z37 = (N31*Z30)+(O31*Z31)+(P31*Z32)+(Q31*Z33)
  AA37 = (N31*AA30)+(O31*AA31)+(P31*AA32)+(Q31*AA33)
  X38 = (N32*X30)+(O32*X31)+(P32*X32)+(Q32*X33)
  Y38 = (N32*Y30)+(O32*Y31)+(P32*Y32)+(Q32*Y33)
  Z38 = (N32*Z30)+(O32*Z31)+(P32*Z32)+(Q32*Z33)
  AA38 = (N32*AA30)+(O32*AA31)+(P32*AA32)+(Q32*AA33)
  X39 = (N33*X30)+(O33*X31)+(P33*X32)+(Q33*X33)
  Y39 = (N33*Y30)+(O33*Y31)+(P33*Y32)+(Q33*Y33)
  Z39 = (N33*Z30)+(O33*Z31)+(P33*Z32)+(Q33*Z33)
  AA39 = (N33*AA30)+(O33*AA31)+(P33*AA32)+(Q33*AA33)
  ## TOOL FRAME
  X42 = math.cos(math.radians(J18))*math.cos(math.radians(J17))
  Y42 = -math.sin(math.radians(J18))*math.cos(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  Z42 = math.sin(math.radians(J18))*math.sin(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  AA42 = (J13)
  X43 = math.sin(math.radians(J18))*math.cos(math.radians(J17))
  Y43 = math.cos(math.radians(J18))*math.cos(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  Z43 = -math.cos(math.radians(J18))*math.sin(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  AA43 = (J14)
  X44 = -math.sin(math.radians(J18))
  Y44 = math.cos(math.radians(J17))*math.sin(math.radians(J16))
  Z44 = math.cos(math.radians(J17))*math.cos(math.radians(J16))
  AA44 = (J15)
  X45 = 0
  Y45 = 0
  Z45 = 0
  AA45 = 1
  ## INVERT TOOL FRAME
  X48 = X42
  Y48 = X43
  Z48 = X44
  AA48 = (X48*AA42)+(Y48*AA43)+(Z48*AA44)
  X49 = Y42
  Y49 = Y43
  Z49 = Y44
  AA49 = (X49*AA42)+(Y49*AA43)+(Z49*AA44)
  X50 = Z42
  Y50 = Z43
  Z50 = Z44
  AA50 = (X50*AA42)+(Y50*AA43)+(Z50*AA44)
  X51 = 0
  Y51 = 0
  Z51 = 0
  AA51 = 1
  ## R 0-6
  X54 =(X36*X48)+(Y36*X49)+(Z36*X50)+(AA36*X51)
  Y54 =(X36*Y48)+(Y36*Y49)+(Z36*Y50)+(AA36*Y51)
  Z54 =(X36*Z48)+(Y36*Z49)+(Z36*Z50)+(AA36*Z51)
  AA54 =(X36*AA48)+(Y36*AA49)+(Z36*AA50)+(AA36*AA51)
  X55 =(X37*X48)+(Y37*X49)+(Z37*X50)+(AA37*X51)
  Y55 =(X37*Y48)+(Y37*Y49)+(Z37*Y50)+(AA37*Y51)
  Z55 =(X37*Z48)+(Y37*Z49)+(Z37*Z50)+(AA37*Z51)
  AA55 =(X37*AA48)+(Y37*AA49)+(Z37*AA50)+(AA37*AA51)
  X56 =(X38*X48)+(Y38*X49)+(Z38*X50)+(AA38*X51)
  Y56 =(X38*Y48)+(Y38*Y49)+(Z38*Y50)+(AA38*Y51)
  Z56 =(X38*Z48)+(Y38*Z49)+(Z38*Z50)+(AA38*Z51)
  AA56 =(X38*AA48)+(Y38*AA49)+(Z38*AA50)+(AA38*AA51)
  X57 =(X39*X48)+(Y39*X49)+(Z39*X50)+(AA39*X51)
  Y57 =(X39*Y48)+(Y39*Y49)+(Z39*Y50)+(AA39*Y51)
  Z57 =(X39*Z48)+(Y39*Z49)+(Z39*Z50)+(AA39*Z51)
  AA57 =(X39*AA48)+(Y39*AA49)+(Z39*AA50)+(AA39*AA51)
  ## REMOVE R 0-6
  X60 =math.cos(math.radians(180))
  Y60 =math.sin(math.radians(180))
  Z60 = 0
  AA60 = 0
  X61 =-math.sin(math.radians(180))*math.cos(D18)
  Y61 =math.cos(math.radians(180))*math.cos(D18)
  Z61 =math.sin(D18)
  AA61 = 0
  X62 =math.sin(math.radians(180))*math.sin(D18)
  Y62 =-math.cos(math.radians(180))*math.sin(D18)
  Z62 =math.cos(D18)
  AA62 = -E18
  X63 = 0
  Y63 = 0
  Z63 = 0
  AA63 = 1
  ## R 0-5 (center spherica wrist)
  X66 =(X54*X60)+(Y54*X61)+(Z54*X62)+(AA54*X63)
  Y66 =(X54*Y60)+(Y54*Y61)+(Z54*Y62)+(AA54*Y63)
  Z66 =(X54*Z60)+(Y54*Z61)+(Z54*Z62)+(AA54*Z63)
  AA66 =(X54*AA60)+(Y54*AA61)+(Z54*AA62)+(AA54*AA63)
  X67 =(X55*X60)+(Y55*X61)+(Z55*X62)+(AA55*X63)
  Y67 =(X55*Y60)+(Y55*Y61)+(Z55*Y62)+(AA55*Y63)
  Z67 =(X55*Z60)+(Y55*Z61)+(Z55*Z62)+(AA55*Z63)
  AA67 =(X55*AA60)+(Y55*AA61)+(Z55*AA62)+(AA55*AA63)
  X68 =(X56*X60)+(Y56*X61)+(Z56*X62)+(AA56*X63)
  Y68 =(X56*Y60)+(Y56*Y61)+(Z56*Y62)+(AA56*Y63)
  Z68 =(X56*Z60)+(Y56*Z61)+(Z56*Z62)+(AA56*Z63)
  AA68 =(X56*AA60)+(Y56*AA61)+(Z56*AA62)+(AA56*AA63)
  X69 =(X57*X60)+(Y57*X61)+(Z57*X62)+(AA57*X63)
  Y69 =(X57*Y60)+(Y57*Y61)+(Z57*Y62)+(AA57*Y63)
  Z69 =(X57*Z60)+(Y57*Z61)+(Z57*Z62)+(AA57*Z63)
  AA69 =(X57*AA60)+(Y57*AA61)+(Z57*AA62)+(AA57*AA63)
  ## CALCULATE J1 ANGLE
  O13 = math.atan((AA67)/(AA66))
  if (V9 == 1):
    P13 = math.degrees(O13)
  if (V9 == 2):
    P13 = math.degrees(O13)
  if (V9 == 3):
    P13 = -180 + math.degrees(O13)
  if (V9 == 4):
    P13 = 180 + math.degrees(O13)
  ## CALCULATE J2 ANGLE	FWD

  O16 = math.sqrt(((abs(AA67))**2)+((abs(AA66))**2))
  O17 = AA68-E13
  O18 = O16-F13
  O19 = math.sqrt((O17**2)+(O18**2))
  O20 = math.sqrt((E16**2)+(F15**2))
  O21 = math.degrees(math.atan(O17/O18))
  O22 = math.degrees(math.acos(((F14**2)+(O19**2)-(abs(O20)**2))/(2*F14*O19)))
  try:
    O25 = math.degrees(math.atan(abs(E16)/F15))
  except:
    O25 = 90
  O23 = 180-math.degrees(math.acos(((abs(O20)**2)+(F14**2)-(O19**2))/(2*abs(O20)*F14)))+(90-O25)
  O26 = -(O21+O22)
  O27 = O23
  ## CALCULATE J2 ANGLE	MID
  P18 = -O18
  P19 = math.sqrt((O17**2)+(P18**2))
  P21 = math.degrees(math.acos(((F14**2)+(P19**2)-(abs(O20)**2))/(2*F14*P19)))
  P22 = math.degrees(math.atan(P18/O17))
  P23 = 180-math.degrees(math.acos(((abs(O20)**2)+(F14**2)-(P19**2))/(2*abs(O20)*F14)))+(90-O25)
  P24 = 90-(P21+P22)
  P26 = -180+P24
  P27 = P23
  ## J1,J2,J3
  Q4 = P13
  if (O18<0):
    Q5 = P26
    Q6 = P27
  else:
    Q5 = O26
    Q6 = O27
  ## J1
  N36 =math.cos(math.radians(Q4))
  O36 =-math.sin(math.radians(Q4))*math.cos(D13)
  P36 =math.sin(math.radians(Q4))*math.sin(D13)
  Q36 =F13*math.cos(math.radians(Q4))
  N37 =math.sin(math.radians(Q4))
  O37 =math.cos(math.radians(Q4))*math.cos(D13)
  P37 =-math.cos(math.radians(Q4))*math.sin(D13)
  Q37 =F13*math.sin(math.radians(Q4))
  N38 = 0
  O38 =math.sin(D13)
  P38 =math.cos(D13)
  Q38 =E13
  N39 = 0
  O39 = 0
  P39 = 0
  Q39 = 1
  ## J2
  N42 =math.cos(math.radians(Q5))
  O42 =-math.sin(math.radians(Q5))*math.cos(D14)
  P42 =math.sin(math.radians(Q5))*math.sin(D14)
  Q42 =F14*math.cos(math.radians(Q5))
  N43 =math.sin(math.radians(Q5))
  O43 =math.cos(math.radians(Q5))*math.cos(D14)
  P43 =-math.cos(math.radians(Q5))*math.sin(D14)
  Q43 =F14*math.sin(math.radians(Q5))
  N44 = 0
  O44 =math.sin(D14)
  P44 =math.cos(D14)
  Q44 =E14
  N45 = 0
  O45 = 0
  P45 = 0
  Q45 = 1
  ## J3
  N48 =math.cos(math.radians((Q6)-90))
  O48 =-math.sin(math.radians((Q6)-90))*math.cos(D15)
  P48 =math.sin(math.radians((Q6)-90))*math.sin(D15)
  Q48 =F15*math.cos(math.radians((Q6)-90))
  N49 =math.sin(math.radians((Q6)-90))
  O49 =math.cos(math.radians((Q6)-90))*math.cos(D15)
  P49 =-math.cos(math.radians((Q6)-90))*math.sin(D15)
  Q49 =F15*math.sin(math.radians((Q6)-90))
  N50 =0
  O50 =math.sin(D15)
  P50 =math.cos(D15)
  Q50 =E15
  N51 =0
  O51 =0
  P51 =0
  Q51 =0
  ## R 0-1
  S33 =(N30*N36)+(O30*N37)+(P30*N38)+(Q30*N39)
  T33 =(N30*O36)+(O30*O37)+(P30*O38)+(Q30*O39)
  U33 =(N30*P36)+(O30*P37)+(P30*P38)+(Q30*P39)
  V33 =(N30*Q36)+(O30*Q37)+(P30*Q38)+(Q30*Q39)
  S34 =(N31*N36)+(O31*N37)+(P31*N38)+(Q31*N39)
  T34 =(N31*O36)+(O31*O37)+(P31*O38)+(Q31*O39)
  U34 =(N31*P36)+(O31*P37)+(P31*P38)+(Q31*P39)
  V34 =(N31*Q36)+(O31*Q37)+(P31*Q38)+(Q31*Q39)
  S35 =(N32*N36)+(O32*N37)+(P32*N38)+(Q32*N39)
  T35 =(N32*O36)+(O32*O37)+(P32*O38)+(Q32*O39)
  U35 =(N32*P36)+(O32*P37)+(P32*P38)+(Q32*P39)
  V35 =(N32*Q36)+(O32*Q37)+(P32*Q38)+(Q32*Q39)
  S36 =(N33*N36)+(O33*N37)+(P33*N38)+(Q33*N39)
  T36 =(N33*O36)+(O33*O37)+(P33*O38)+(Q33*O39)
  U36 =(N33*P36)+(O33*P37)+(P33*P38)+(Q33*P39)
  V36 =(N33*Q36)+(O33*Q37)+(P33*Q38)+(Q33*Q39)
  ## R 0-2
  S39 =(S33*N42)+(T33*N43)+(U33*N44)+(V33*N45)
  T39 =(S33*O42)+(T33*O43)+(U33*O44)+(V33*O45)
  U39 =(S33*P42)+(T33*P43)+(U33*P44)+(V33*P45)
  V39 =(S33*Q42)+(T33*Q43)+(U33*Q44)+(V33*Q45)
  S40 =(S34*N42)+(T34*N43)+(U34*N44)+(V34*N45)
  T40 =(S34*O42)+(T34*O43)+(U34*O44)+(V34*O45)
  U40 =(S34*P42)+(T34*P43)+(U34*P44)+(V34*P45)
  V40 =(S34*Q42)+(T34*Q43)+(U34*Q44)+(V34*Q45)
  S41 =(S35*N42)+(T35*N43)+(U35*N44)+(V35*N45)
  T41 =(S35*O42)+(T35*O43)+(U35*O44)+(V35*O45)
  U41 =(S35*P42)+(T35*P43)+(U35*P44)+(V35*P45)
  V41 =(S35*Q42)+(T35*Q43)+(U35*Q44)+(V35*Q45)
  S42 =(S36*N42)+(T36*N43)+(U36*N44)+(V36*N45)
  T42 =(S36*O42)+(T36*O43)+(U36*O44)+(V36*O45)
  U42 =(S36*P42)+(T36*P43)+(U36*P44)+(V36*P45)
  V42 =(S36*Q42)+(T36*Q43)+(U36*Q44)+(V36*Q45)
  ## R 0-3
  S45 =(S39*N48)+(T39*N49)+(U39*N50)+(V39*N51)
  T45 =(S39*O48)+(T39*O49)+(U39*O50)+(V39*O51)
  U45 =(S39*P48)+(T39*P49)+(U39*P50)+(V39*P51)
  V45 =(S39*Q48)+(T39*Q49)+(U39*Q50)+(V39*Q51)
  S46 =(S40*N48)+(T40*N49)+(U40*N50)+(V40*N51)
  T46 =(S40*O48)+(T40*O49)+(U40*O50)+(V40*O51)
  U46 =(S40*P48)+(T40*P49)+(U40*P50)+(V40*P51)
  V46 =(S40*Q48)+(T40*Q49)+(U40*Q50)+(V40*Q51)
  S47 =(S41*N48)+(T41*N49)+(U41*N50)+(V41*N51)
  T47 =(S41*O48)+(T41*O49)+(U41*O50)+(V41*O51)
  U47 =(S41*P48)+(T41*P49)+(U41*P50)+(V41*P51)
  V47 =(S41*Q48)+(T41*Q49)+(U41*Q50)+(V41*Q51)
  S48 =(S42*N48)+(T42*N49)+(U42*N50)+(V42*N51)
  T48 =(S42*O48)+(T42*O49)+(U42*O50)+(V42*O51)
  U48 =(S42*P48)+(T42*P49)+(U42*P50)+(V42*P51)
  V48 =(S42*Q48)+(T42*Q49)+(U42*Q50)+(V42*Q51)
  ## R 0-3 transposed
  S51 =S45
  T51 =S46
  U51 =S47
  S52 =T45
  T52 =T46
  U52 =T47
  S53 =U45
  T53 =U46
  U53 =U47
  ## R 3-6 (spherical wrist  orietation)
  X72 =(S51*X66)+(T51*X67)+(U51*X68)
  Y72 =(S51*Y66)+(T51*Y67)+(U51*Y68)
  Z72 =(S51*Z66)+(T51*Z67)+(U51*Z68)
  X73 =(S52*X66)+(T52*X67)+(U52*X68)
  Y73 =(S52*Y66)+(T52*Y67)+(U52*Y68)
  Z73 =(S52*Z66)+(T52*Z67)+(U52*Z68)
  X74 =(S53*X66)+(T53*X67)+(U53*X68)
  Y74 =(S53*Y66)+(T53*Y67)+(U53*Y68)
  Z74 =(S53*Z66)+(T53*Z67)+(U53*Z68)
  ## WRIST ORENTATION
  R7 = math.degrees(math.atan2(Z73,Z72))
  R8 = math.degrees(math.atan2(+math.sqrt(1-Z74**2),Z74))
  if (Y74 < 0):
    R9 = math.degrees(math.atan2(-Y74,X74))-180
  else:
    R9 = math.degrees(math.atan2(-Y74,X74))+180
  S7 = math.degrees(math.atan2(-Z73,-Z72))
  S8 = math.degrees(math.atan2(-math.sqrt(1-Z74**2),Z74))
  if (Y74 < 0):
    S9 = math.degrees(math.atan2(Y74,-X74))+180
  else:
    S9 = math.degrees(math.atan2(Y74,-X74))-180
  if (V8 == "F"):
    Q8 = R8
  else:
    Q8 = S8
  if(Q8>0):
    Q7 = R7
  else:
    Q7 = S7
  if(Q8<0):
    Q9 = S9
  else:
    Q9 = R9
  ## FINAL OUTPUT
  J1out = Q4
  J2out = Q5
  J3out = Q6
  J4out = Q7
  J5out = Q8
  J6out = Q9
  return (J1out,J2out,J3out,J4out,J5out,J6out)