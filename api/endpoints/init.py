import falcon
import json

from ev3dev2.motor import LargeMotor, OUTPUT_C
from state import robotstate
from utils import Xmotors

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

mY = LargeMotor(OUTPUT_C)

class InitResource(object):
    def on_post(self, req, resp):
        """ POST /init: 
            Asks the hardware to reinitialise, reset tachometers from 
            limit switches and return to home position. Request completes 
            when finished."""

        print("[POST] /init")

        print("Initialising robot X axis:")
        Xm = Xmotors()
        Xm.on(-30)
        Xm.wait_for_limit()
        Xm.reset()
        Xm.on(30)
        Xm.wait_for_limit()

        print('X axis track length is ' + str(Xm.position()))
        Xm.on_to_position(30, int(Xm.position()/2))

        robotstate['Xmul'] = Xm.position()/robotstate['Xlength']

        print('Initialising robot Y axis:')

        mY.reset()
        print("Move carriage to home and press return")
        input()

        mY.reset()

        print("Move carriage to end and press return")
        input()

        print('Y axis length is ' + str(mY.position))
        mY.on_to_position(30, int(mY.position/2))

        robotstate['Ymul'] = mY.position/robotstate['Ylength']

        robotstate['initialised'] = True

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({
            'success': True,
            'Ylength': robotstate['Ylength'],
            'Xlength': robotstate['Xlength'],
            'Ypos': mY.position * robotstate['Ymul'],
            'Xpos': mY.position * robotstate['Xmul'],
            'Ymul': robotstate['Ymul'],
            'Xmul': robotstate['Xmul']
        })
