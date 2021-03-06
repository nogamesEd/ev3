import falcon
import json
import time
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev.ev3 import Button, Sound
from state import robotstate
from time import sleep

# Falcon resource class for robot control, probably ought to be split
# into smaller files at some point.

Xm = LargeMotor(OUTPUT_A)
Ym = LargeMotor(OUTPUT_B)
Zm = LargeMotor(OUTPUT_C)
Gm = MediumMotor(OUTPUT_D)
Btn = Button()

# movement speed while button held
X_SPEED = 800
Y_SPEED = 400
Z_SPEED = 1000
G_SPEED = 400


def moveTo(motor, percent, mult, speed):
    print("Moving to", percent)
    if (mult not in robotstate):
        print("No previous calibration available")
        return
    motor.on_to_position(speed, percent * robotstate[mult], block=False)
    motor.wait_while('running', timeout=8000)

class InitResource(object):
    def on_post(self, req, resp):
        """ POST /init: 
            Asks the hardware to reinitialise, reset tachometers from 
            limit switches and return to home position. Request completes 
            when finished."""

        moveTo(Xm, 50, "Xmul", 80)
        Sound.beep()

        # Z axis initialisation
        print('Initialising robot Z axis:')
        
        # move to where it thinks 0 is
        moveTo(Zm, 0, "Zmul", 90)
        
        # Zm.reset() # Reset in order to release breaks
        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Zm.run_timed(time_sp=50, speed_sp=Z_SPEED)
            elif Btn.down:
                Zm.run_timed(time_sp=50, speed_sp=(-1 * Z_SPEED)/3)
        while Btn.enter:
            pass
        Sound.beep()

        Zm.reset()

        # move to where it thinks 100 is
        moveTo(Zm, 100, "Zmul", 90)
        
        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Zm.run_timed(time_sp=50, speed_sp=Z_SPEED/3)
            elif Btn.down:
                Zm.run_timed(time_sp=50, speed_sp=(-1 * Z_SPEED))
        while Btn.enter:
            pass

        Sound.beep()

        print('Z axis length is ' + str(Zm.position))

        robotstate['Zmul'] = Zm.position/robotstate['Zlength']
        moveTo(Zm, 100, "Zmul", 90)

        # X axis initialisation
        print("Initialising robot X axis:")

        # move to where it thinks 0 is
        moveTo(Xm, 0, "Xmul", 80)

        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Xm.run_timed(time_sp=50, speed_sp=(-1 * X_SPEED))
            elif Btn.down:
                Xm.run_timed(time_sp=50, speed_sp=X_SPEED/3)
        while Btn.enter:
            pass
        Sound.beep()

        Xm.reset()

        # move to where it thinks 100 is
        moveTo(Xm, 100, "Xmul", 80)

        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Xm.run_timed(time_sp=50, speed_sp=(-1 * X_SPEED)/3)
            elif Btn.down:
                Xm.run_timed(time_sp=50, speed_sp=X_SPEED)
        while Btn.enter:
            pass
        Sound.beep()

        print('X axis track length is ' + str(Xm.position))
        robotstate['Xmul'] = Xm.position / robotstate['Xlength']
        moveTo(Xm, 50, "Xmul", 80)

        # Y axis initialisation

        # move to where it thinks 100 is
        moveTo(Ym, 100, "Ymul", 60)

        print('Initialising robot Y axis:')
        # Ym.reset() # Reset in order to release breaks
        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Ym.run_timed(time_sp=50, speed_sp=(-1 * Y_SPEED))
            elif Btn.down:
                Ym.run_timed(time_sp=50, speed_sp=(Y_SPEED)/3)
        while Btn.enter:
            pass
        Sound.beep()

        Ym.reset()

        # move to where it thinks 0 is
        moveTo(Ym, -100, "Ymul", 60)

        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Ym.run_timed(time_sp=50, speed_sp=(-1 * Y_SPEED)/3)
            elif Btn.down:
                Ym.run_timed(time_sp=50, speed_sp=Y_SPEED)
        while Btn.enter:
            pass
        Sound.beep()

        print('Y axis track length is ' + str(Ym.position))
        robotstate['Ymul'] = -1 * Ym.position / robotstate['Ylength']
        Ym.reset()
        moveTo(Ym, 50, "Ymul", 60)

        # Gripper initialisation
        moveTo(Gm, 100, "Gmul", 40)
        print('Initialising the gripper:')
        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Gm.run_timed(time_sp=50, speed_sp=G_SPEED)
            elif Btn.down:
                Gm.run_timed(time_sp=50, speed_sp=(-1 * G_SPEED)/3)
        while Btn.enter:
            pass
        Sound.beep()

        Gm.reset()

        moveTo(Gm, -100, "Gmul", 40)

        Sound.beep()
        while not Btn.enter:
            if Btn.up:
                Gm.run_timed(time_sp=50, speed_sp=G_SPEED/3)
            elif Btn.down:
                Gm.run_timed(time_sp=50, speed_sp=(-1 * G_SPEED))
        while Btn.enter:
            pass
        Sound.beep()

        print("G axis length is " + str(Gm.position))
        robotstate['Gmul'] = -1 * Gm.position / robotstate['Glength']
        Gm.reset()
        #moveTo(Gm, 0, "Gmul", 40)

        robotstate['initialised'] = True

        Xm.on_to_position(80, 100 * robotstate['Xmul'], block=False)
        Zm.on_to_position(60, 0 * robotstate['Zmul'], block=False)

        Xm.wait_while('running', timeout=4000)
        Ym.wait_while('running', timeout=4000)
        Zm.wait_while('running', timeout=4000)

        Sound.beep()
        time.sleep(0.2)
        Sound.beep()

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
