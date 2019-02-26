import falcon
import json

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from state import robotstate
from utils import Xmotors, wait_for_limit
from time import sleep

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

Ym = LargeMotor(OUTPUT_C)
bX1 = TouchSensor(INPUT_1)
bX2 = TouchSensor(INPUT_2)
bY1 = TouchSensor(INPUT_3)
bY2 = TouchSensor(INPUT_4)
Zm = MediumMotor(OUTPUT_D)

class InitResource(object):
    def on_post(self, req, resp):
        """ POST /init: 
            Asks the hardware to reinitialise, reset tachometers from 
            limit switches and return to home position. Request completes 
            when finished."""

        print("[POST] /init")

        # X axis initialisation
        print("Initialising robot X axis:")

        if (bX1.value == 1) or (bX2.value == 1):
            print('[ERROR] 500: Limit switch already pressed. Unable to reset.')
            raise falcon.HTTPInternalServerError(
                description = 'Limit switch already pressed'
            )

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

        if (bY1.value == 1) or (bY2.value == 1):
            print('[ERROR] 500: Limit switch already pressed. Unable to reset.')
            raise falcon.HTTPInternalServerError(
                description = 'Limit switch already pressed'
            )

        Ym.on(20)
        yhit = wait_for_limit(bY1, bY2, Ym)
        Ym.stop()
        sleep(0.5)
        Ym.reset()
        Ym.on(-20)
        if yhit == 1:
            wait_for_limit(bY1, bY2, Ym, target=2)
        else:
            wait_for_limit(bY1, bY2, Ym, target=1)

        print('Y axis track length is ' + str(Ym.position))
        robotstate['Ymul'] = Ym.position/robotstate['Ylength']
        Ym.on_to_position(20, int(Ym.position/2))

        # Z axis initialisation
        print('Initialising robot Z axis:')

        Zm.reset()
        print("Move gripper to home and press return")
        input()

        Zm.reset()

        print("Move gripper to end and press return")
        input()

        print('Z axis length is ' + str(Zm.position))
        robotstate['Zmul'] = Zm.position/robotstate['Zlength']
        Zm.on_to_position(30, int(Zm.position/2))

        robotstate['initialised'] = True

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({
            'success': True,
            'Ylength': robotstate['Ylength'],
            'Xlength': robotstate['Xlength'],
            'Ypos': Ym.position * robotstate['Ymul'],
            'Xpos': Ym.position * robotstate['Xmul'],
            'Ymul': robotstate['Ymul'],
            'Xmul': robotstate['Xmul']
        })
