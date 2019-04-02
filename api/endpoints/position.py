import falcon
import json
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from state import robotstate

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

Xm = LargeMotor(OUTPUT_A)
Ym = LargeMotor(OUTPUT_B)
Zm = LargeMotor(OUTPUT_C)
Gm = MediumMotor(OUTPUT_D)

class PositionResource(object):
    def on_post(self, req, resp):
        """ POST /position: 
            Asks the hardware to move the gantry to the requested position
            in mm."""

        body = req.stream.read()
        print(body)
        r = json.loads(body.decode('utf-8'))

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

        print("Moving gantry to {},{},{}.".format(targetX, targetY, targetZ))
        print(json.dumps(robotstate))

        Xm.on_to_position(80, targetX * robotstate['Xmul'], block=False)
        Ym.on_to_position(60, targetY * robotstate['Ymul'], block=False)
        Zm.on_to_position(90, targetZ * robotstate['Zmul'], block=False)

        Xm.wait_while('running', timeout=4000)
        Ym.wait_while('running', timeout=4000)
        Zm.wait_while('running', timeout=4000)

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'success': True,
            'Ypos': Ym.position * robotstate['Ymul'],
            'Xpos': Xm.position * robotstate['Xmul'],
            'Zpos': Zm.position * robotstate['Zmul']
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
            'Ypos': Ym.position * robotstate['Ymul'],
            'Xpos': Xm.position() * robotstate['Xmul'],
            'Zpos': Zm.position * robotstate['Zmul'],
        })
