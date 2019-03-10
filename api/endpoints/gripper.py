import falcon
import json
from ev3dev2.motor import MediumMotor, OUTPUT_D
from state import robotstate

Gm = MediumMotor(OUTPUT_D)

class GripperResource(object):
    def on_post(self, req, resp):
        """ POST /gripper: 
            Grabs the piece."""

        body = json.load(req.stream)

        Gm.on_to_position(30, 0 if body["move"]=="grab" else 400, block=False)
        Gm.wait_while('running')

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'success': True
        })
