import falcon
import json
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from state import robotstate
from utils import Xmotors

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

mX = Xmotors()
mY = LargeMotor(OUTPUT_C)
mZ = LargeMotor(OUTPUT_D)
bx1 = TouchSensor(INPUT_1)
bx2 = TouchSensor(INPUT_2)

class PositionResource(object):
    def on_post(self, req, resp):
        """ POST /position: 
            Asks the hardware to move the gantry to the requested position
            in mm."""

        print("[POST] /position")

        if not robotstate['initialised']:
            print("[ERROR] 428: Robot not initalised. Cannot move yet.")
            raise falcon.HTTPPreconditionRequired(
                title = "428: Robot not initialised",
                description = json.dumps({
                'success': False,
                'error': 'Robot has not been initialised, POST to /init first.'
            }))

        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()

        if not body:
            print("[ERROR] 400: Request missing body.")
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Request missing body.'
                })
            )

        try:
            r = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            print("[ERROR] 400: Invalid JSON")
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Invalid JSON in body. Check request is UTF-8 encoded.'
                })
            )

        if not ('x' in r and 'y' in r and 'z' in r):
            print("[ERROR] 400: Missing x and y and z parameters in request.")
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Missing x and y and z parameters in request body.'
                })
            )
        
        if (r['x'] > robotstate['Xlength'] 
                or r['y'] > robotstate['Ylength']
                    or r['z'] > robotstate['Zlength']):
            print('[ERROR] 400: Requested location out of range.')
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Requested location out of range.'
                })
            )

        targetX = r['x']
        targetY = r['y']
        targetZ = r['z']

        print("Moving gantry to {},{}.".format(targetX, targetY))
        print(json.dumps(robotstate))

        mX.on_to_position(30, targetX * int(robotstate['Xmul']))
        mY.on_to_position(30, targetY * int(robotstate['Ymul']))
        mZ.on_to_position(30, targetZ * int(robotstate['Zmul']))

        mX.wait_while('running')
        mY.wait_while('running')
        mZ.wait_while('running')

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'success': True,
            'Ypos': mY.position * robotstate['Ymul'],
            'Xpos': mX.position() * robotstate['Xmul'],
            'Zpos': mZ.position() * robotstate['Zmul']
        })
    
    def on_get(self, req, resp):
        """ GET /position: 
            Returns current gantry position."""
        
        if not robotstate['initialised']:
            print("[ERROR] 428: Robot not initalised. Cannot move yet.")
            raise falcon.HTTPPreconditionRequired(
                title = "428: Robot not initialised",
                description = json.dumps({
                'success': False,
                'error': 'Robot has not been initialised, POST to /init first.'
            }))

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'success': True,
            'Ypos': mY.position * robotstate['Ymul'],
            'Xpos': mX.position() * robotstate['Xmul'],
            'Zpos': mZ.position() * robotstate['Zmul'],
        })
