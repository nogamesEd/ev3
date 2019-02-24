import falcon
import json

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_C, OUTPUT_D
from state import robotstate
from utils import Xmotors
from time import sleep

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

mY = LargeMotor(OUTPUT_C)
mZ = MediumMotor(OUTPUT_D)

class InitResource(object):
    def on_post(self, req, resp):
        """ POST /init: 
            Asks the hardware to reinitialise, reset tachometers from 
            limit switches and return to home position. Request completes 
            when finished."""

        print("[POST] /init")

        # X axis initialisation
        print("Initialising robot X axis:")
        Xm = Xmotors()
        Xm.on(20)
        xhit = Xm.wait_for_limit()
        Xm.stop()
        sleep(0.5)
        Xm.reset()
        Xm.on(-20)
        if xhit == 1:
            Xm.wait_for_limit(target=2)
        else:
            Xm.wait_for_limit(target=1)

        print('X axis track length is ' + str(Xm.position()))
        robotstate['Xmul'] = Xm.position()/robotstate['Xlength']
        Xm.on_to_position(20, int(Xm.position()/2))


        # Y axis initialisation
        print('Initialising robot Y axis:')

        mY.reset()
        print("Move carriage to home and press return")
        input()

        mY.reset()

        print("Move carriage to end and press return")
        input()

        print('Y axis length is ' + str(mY.position))
        robotstate['Ymul'] = mY.position/robotstate['Ylength']
        mY.on_to_position(20, int(mY.position/2))

        # Z axis initialisation
        print('Initialising robot Z axis:')

        mZ.reset()
        print("Move gripper to home and press return")
        input()

        mZ.reset()

        print("Move gripper to end and press return")
        input()

        print('Z axis length is ' + str(mZ.position))
        robotstate['Zmul'] = mZ.position/robotstate['Zlength']
        mZ.on_to_position(30, int(mZ.position/2))

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
