import requests
import time

host = "192.168.105.110"

def _request(method, endpoint, body=None):
    response = requests.request(method, "http://{}:8000{}".format(host, endpoint), json=body)
    return response.text

# Just specify what Y-coordinates (in percentage) you want the tour to take
y_positions = [0, 50, 100, 50, 0]
GRIPPER_RELEASE = 700
GRIPPER_GRAB = GRIPPER_RELEASE-500

_request("POST", "/position", body={"x":0,"y":y_positions[0],"z":50})
time.sleep(2)

for i, y_position in enumerate(y_positions[:-1]):
    next_position = y_positions[i+1]
    _request("POST", "/position", body={"x":0,"y":y_position,"z":10})
    _request("POST", "/gripper", body={"move":GRIPPER_GRAB})
    _request("POST", "/position", body={"x":0,"y":y_position,"z":100})
    _request("POST", "/position", body={"x":0,"y":next_position,"z":100})
    _request("POST", "/position", body={"x":0,"y":next_position,"z":10})
    _request("POST", "/gripper", body={"move":GRIPPER_RELEASE})
