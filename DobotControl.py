import threading
import DobotDllType as dType
from flask import Flask

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "192.168.1.226", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    #Async PTP Motion
    #for i in range(0, 5):
    #    if i % 2 == 0:
    #        offset = 25
    #    else:
    #        offset = -25
    #    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset, offset, isQueued = 1)[0]
    #    lastIndex=lastIndex

    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 26.07, 153.56, -0.685, 161.0, isQueued = 1) [0]
    lastIndex=lastIndex
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 26.07, 153.56, -33.685, 161.0, isQueued = 1)
    dType.SetEndEffectorGripper(api, 1, 1, isQueued=1)
    dType.SetWAITCmd(api, 1, isQueued=1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 26.07, 153.56, 34.69, 161.0, isQueued = 1)
    dType.SetWAITCmd(api, 0.5, isQueued=1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, -116.6, 156.21, -28, 161.0, isQueued = 1)
    dType.SetEndEffectorGripper(api, 1, 0, isQueued=1)
    dType.SetWAITCmd(api, 1, isQueued=1)
    dType.SetEndEffectorGripper(api, 0, 0, isQueued=1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 26.07, 153.56, -0.685, 161.0, isQueued = 1)
    dType.SetWAITCmd(api, 1, isQueued=1)

    lastIndex = lastIndex+11



    #  This  EMotor
    #  This  EMotor
    #  This  EMotor
    #  This  EMotor

    # dType.SetEMotor(api, 0, 1, 10000, isQueued=1)
    # dType.SetEMotorS(api, 0, 1, 10000, 20000,isQueued=1)



    #Start to Execute Command Queued
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dType.DisconnectDobot(api)
