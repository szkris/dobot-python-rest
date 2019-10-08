from flask import Flask
import DobotDllType as dType
import threading

app = Flask(__name__)
api = dType.load()

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/connect')
def connectDobot():
    state = dType.ConnectDobot(api, "", 115200)[0]
    return "Connect status:" + CON_STR[state]

if __name__ == '__main__':
    app.run(debug=True)
