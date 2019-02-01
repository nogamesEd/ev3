#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
#from ev3dev2.sound import Sound

m = LargeMotor(OUTPUT_A)
b2 = TouchSensor(INPUT_1) # sensor on left when looking at motor side
b1 = TouchSensor(INPUT_2) # sensor on right when looking at motor side

#sound = Sound()

#sound.speak('Initialising')

m.on(-30)
b1.wait_for_pressed()
m.stop()
m.reset()

#sound.speak('Reset position. Measuring length')

m.on(30)
b2.wait_for_pressed()
m.stop()

#sound.speak('Track length is ' + str(m.position))
#sound.speak('Returning to midpoint')
print('Track length is ' + str(m.position))

length = m.position

# 22cm carriage 12cm, so 10cm movement range (measured by hand)

m.on_to_position(30, int(length/2))

m.wait_while('running')

#sound.speak('Found midpoint')

# length/10 = movement multiplier

mul = length/10

#sound.speak('Awaiting input')

while (True):
  print("Please enter a target position in cm, between 0 and 10.")
  try:
    target = int(input())
  except:
    print("invalid entry. quitting")
    exit()
  if (target > 10) or (target < 0):
    print("invalid distance. Please enter a number between 0 & 10")
    continue

  target_clicks = target * mul
  m.on_to_position(30, target_clicks)
  print("Moved to " + str(target_clicks))