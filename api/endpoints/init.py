import falcon
import json
import time
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from state import robotstate
from time import sleep

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

Xm = LargeMotor(OUTPUT_A)
Ym = LargeMotor(OUTPUT_B)
Zm = MediumMotor(OUTPUT_C)
Gm = MediumMotor(OUTPUT_D)

class InitResource(object):
    def on_post(self, req, resp):
        """ POST /init: 
            Asks the hardware to reinitialise, reset tachometers from 
            limit switches and return to home position. Request completes 
            when finished."""

        # X axis initialisation
        print("Initialising robot X axis:")
        Xm.reset()
        Xm.run_forever(speed_sp=40)
        input()
        Xm.stop(stop_action="hold")
        time.sleep(0.5)
        Xm.reset()
        Xm.run_forever(speed_sp=-40)
        input()
        Xm.stop(stop_action="hold")
        print('X axis track length is ' + str(Xm.position))
        robotstate['Xmul'] = Xm.position/robotstate['Xlength']
        Xm.on_to_position(20, int(Xm.position/2))

        # Y axis initialisation
        print('Initialising robot Y axis:')
        Ym.reset() # Reset in order to release breaks
        Ym.run_forever(speed_sp=40)
        input()
        Ym.stop(stop_action="hold")
        time.sleep(0.5)
        Ym.reset()
        Ym.run_forever(speed_sp=-40)
        input()
        Ym.stop(stop_action="hold")
        print('Y axis track length is ' + str(Ym.position))
        robotstate['Ymul'] = Ym.position/robotstate['Ylength']
        Ym.on_to_position(20, int(Ym.position/2))

        # Z axis initialisation
        print('Initialising robot Z axis:')
        Zm.reset() # Reset in order to release breaks
        Zm.run_forever(speed_sp=40)
        input()
        Zm.stop(stop_action="hold")
        time.sleep(0.5)
        Zm.reset()
        Zm.run_forever(speed_sp=-40)
        input()
        Zm.stop(stop_action="hold")
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
