# define all system default arm parameter, it came from original dekstop app. better don;t change it



# leave degperstep=0, it will calculate runtime
jsetting = {
    0:{"maxdeg":170, "mindeg":-170, "steplimit":15110, "degperstep": 0, "caldir":0, "restpos":0, "reststep": 7555 },
    1:{"maxdeg":0, "mindeg":-129.6, "steplimit":7198, "degperstep": 0, "caldir":0, "restpos":-90, "reststep": 2199.3888888888887 },
    2:{"maxdeg":143.7, "mindeg":1, "steplimit":7984, "degperstep": 0, "caldir":1, "restpos":1.05, "reststep": 56 },
    3:{"maxdeg":164.5, "mindeg":-164.5, "steplimit":14056, "degperstep": 0, "caldir":0, "restpos":0, "reststep": 7028 },
    4:{"maxdeg":104.15, "mindeg":-104.15, "steplimit":4560, "degperstep": 0, "caldir":0, "restpos":0, "reststep": 2280 },
    5:{"maxdeg":148.1, "mindeg":-148.1, "steplimit":6320, "degperstep": 0, "caldir":1, "restpos":0, "reststep": 3160 },
}

# leave mmperstep =0, it will auto calculate
tracksetting = {
    't1': {"length":850,"steplimit":65650,"mmperstep": 0}
}

servosetting = {
    'gripper1': { 'maxdeg':180, 'mindeg':0, 'positions': {'open':90,'close':180} }
}

jointqty = 6
teensybaudrate=115200
arduinobaudrate=115200
Speed = 25 # value in %, shall fetch from runtime variables
ACCdur =15 # accelerartion duration
ACCspd = 10 # accelerartion speed %
DECdur = 20 # deceleration duration
DECspd = 5 # deceleration duration %


