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

class InitResource(object):
    def on_post(self, req, resp):
        """ POST /init: 
            Asks the hardware to reinitialise, reset tachometers from 
            limit switches and return to home position. Request completes 
            when finished."""

        print("[POST] /init")
        print("Initialising robot X axis:")

        # X-axis
        mX.on(-30)
        bx1.wait_for_pressed()
        mX.stop()
        mX.reset()
        mX.on(30)
        bx2.wait_for_pressed()
        mX.stop()

        print('X axis track length is ' + str(mX.position))
        mX.on_to_position(30, int(mX.position/2))

        self.options['Xmul'] = mX.position/self.options['Xlength']

        print('Initialising robot Y axis:')

        mY.reset()
        print("Move carriage to home and press return")
        input()

        mY.reset()

        print("Move carriage to end and press return")
        input()

        print('Y axis length is ' + str(mY.position))
        mY.on_to_position(30, int(mY.position/2))

        self.options['Ymul'] = mY.position/self.options['Ylength']

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({
            'success': True,
            'Ylength': self.options['Ylength'],
            'Xlength': self.options['Xlength'],
            'Ypos': mY.position * self.options['Ymul'],
            'Xpos': mY.position * self.options['Xmul'],
            'Ymul': self.options['Ymul'],
            'Xmul': self.options['Xmul']
        })
