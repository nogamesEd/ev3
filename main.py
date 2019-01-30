#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound
from ev3dev2.led import Leds

m = LargeMotor(OUTPUT_A)
b1 = TouchSensor(INPUT_1)
b2 = TouchSensor(INPUT_2)

sound = Sound()

sound.speak('Initialising positions on track. Please wait')

m.on(-30)
b1.wait_for_pressed()
m.stop()
m.reset()

sound.speak('Reset position. Measuring track length')

m.on(30)
b2.wait_for_pressed()
m.stop()

sound.speak('Track length is ' + str(m.position))
sound.speak('Returning to midpoint')

length = m.position

m.on_to_position(30, int(length/2))

m.wait_while('running')

sound.speak('Found midpoint')
