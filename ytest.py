#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_B
#from ev3dev2.sound import Sound

m = LargeMotor(OUTPUT_B)

#sound = Sound()

#sound.speak('Initialising')

m.reset()
print("Move carriage to home and press return")
input()

m.reset()

print("Move carriage to end and press return")
input()

length = m.position

#sound.speak('Track length is ' + str(m.position))
#sound.speak('Returning to midpoint')
print('Track length is ' + str(m.position))

# 11.5cm movement range (measured by hand)

m.on_to_position(30, int(length/2))

m.wait_while('running')

#sound.speak('Found midpoint')

# length/10 = movement multiplier

mul = length/11.5

#sound.speak('Awaiting input')

while (True):
  print("Please enter a target position in cm, between 0 and 11.5.")
  try:
    target = float(input())
  except:
    print("invalid entry. quitting")
    exit()
  if (target > 11.5) or (target < 0):
    print("invalid distance. Please enter a number between 0 & 11.5")
    continue

  target_clicks = target * mul
  m.on_to_position(30, target_clicks)
  print("Moved to " + str(target_clicks))
