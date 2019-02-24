import falcon
import json
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

mX = LargeMotor(OUTPUT_A)
mY = LargeMotor(OUTPUT_B)
bx1 = TouchSensor(INPUT_1)
bx2 = TouchSensor(INPUT_2)

class PositionResource(object):
    def on_post(self, req, resp):
        """ POST /position: 
            Asks the hardware to move the gantry to the requested position
            in mm."""

        print("[POST] /position")

        if not self.options['initialised']:
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
            req.context['doc'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            print("[ERROR] 400: Invalid JSON")
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Invalid JSON in body. Check request is UTF-8 encoded.'
                })
            )

        if not ('x' in req.context['doc'] and 'y' in req.context['doc']):
            print("[ERROR] 400: Missing x and y parameters in request.")
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Missing x and y parameters in request body.'
                })
            )
        
        if (req.context.doc['x'] > self.options['Xlength'] 
                or req.context.doc['y'] > self.options['Ylength']):
            print('[ERROR] 400: Requested location out of range.')
            raise falcon.HTTPBadRequest(
                description = json.dumps({
                'success': False,
                'error': 'Requested location out of range.'
                })
            )

        targetX = req.context.doc['x']
        targetY = req.context.doc['y']

        print("Moving gantry to {},{}.".format(targetX, targetY))

        mX.on_to_position(30, targetX * self.options['Xmul'])
        mY.on_to_position(30, targetY * self.options['Ymul'])
        mX.wait_while('running')
        mY.wait_while('running')

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'success': True,
            'Ypos': mY.position * self.options['Ymul'],
            'Xpos': mY.position * self.options['Xmul']
        })
    
    def on_get(self, req, resp):
        """ GET /position: 
            Returns current gantry position."""
        
        if not self.options['initialised']:
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
            'Ypos': mY.position * self.options['Ymul'],
            'Xpos': mY.position * self.options['Xmul']
        })
