import falcon
import json
from ev3dev2.motor import MediumMotor, OUTPUT_D
from state import robotstate

Gm = MediumMotor(OUTPUT_D)

class GripperResource(object):
    def on_post(self, req, resp):
        """ POST /gripper: 
            Grabs the piece."""
        
        body = req.stream.read()
        body = json.loads(body.decode('utf-8'))

        print("Moving gripper to position {}".format(body["move"]))
        Gm.on_to_position(30, body["move"], block=False)
        Gm.wait_while('running')

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'success': True
        })
