
import threading
import DobotDllType as dType
from flask import Flask
app = Flask(__name__)


#Load Dll
api = dType.load()

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/connect')
def connect_dobot():
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}



    #Connect Dobot
    state = dType.ConnectDobot(api, "", 115200)[0]


    return "Connect status:" +  CON_STR[state]

@app.route('/home')
def home_dobot():
    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    #Async Home
    lastIndex=dType.SetHOMECmd(api, temp = 0, isQueued = 1)[0]
    lastIndex=lastIndex
    #Start to Execute Command Queued
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)
    return 'Homing'

@app.route('/disconnect')
def disconnect_dobot():
    #Disconnect Dobot
    dType.DisconnectDobot(api)
    return 'Disconnected'
