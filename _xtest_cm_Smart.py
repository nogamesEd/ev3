#Currently moves 1 cm forward, waits till button at input 2 is pressed them moves to start
#   Based on 1188 being the average for 25 cm or motion
#   currently overshoots by 6 points, needs adjustment build in

#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
#from ev3dev2.sound import Sound

m = LargeMotor(OUTPUT_A)
b2 = TouchSensor(INPUT_1)
b1 = TouchSensor(INPUT_2)

#sound = Sound()

#sound.speak('Initialising')

#m.on(-30)
#b1.wait_for_pressed()
#m.stop()
m.reset()

#sound.speak('Reset position. Measuring length')

#m.on(30)
#b2.wait_for_pressed()
#m.stop()

#m.on_to_position(30, 1188) #overshoot of 6 (47.5 per cm w/ current gears)
m.on_to_position(30, 47.5) #overshoot of 6 (47.5 per cm w/ current gears)

m.wait_while('running')


#sound.speak('Track length is ' + str(m.position))
#sound.speak('Returning to midpoint')
print('Track length is ' + str(m.position))

b1.wait_for_pressed()
length = m.position

# 22cm carriage 12cm, so 10cm movement range

m.on_to_position(30, int(0))

m.wait_while('running')

#sound.speak('Found midpoint')

# length/10 = movement multiplier

mul = length/10
exit()
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

