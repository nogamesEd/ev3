#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

mX = LargeMotor(OUTPUT_A)
mY = LargeMotor(OUTPUT_B)

#Get X-Axis control distances
mX.reset()
print("Move x-axis carriage to center of furthest left square and press return")
input()

mX.reset()

print("Move x-axis carriage to center of furthest right square and press return")
input()

lengthX = mX.position

#Get Y-Axis control distances
mY.reset()
print("Move y-axis carriage to center of furthest left square and press return")
input()

mY.reset()

print("Move y-axis carriage to center of furthest right square and press return")
input()

lengthY = mY.position


# 8 square axis movement range
mX.on_to_position(30, 0)
mX.wait_while('running')

mY.on_to_position(30, 0)
mY.wait_while('running')

mulX = lengthX/7
mulY = lengthY/7

testPos = 1

while (True):
  print("Please enter x-axis target square, between 0 and 7.")
  try:
    target = float(testPos)
  except:
    print("invalid entry. quitting")
    exit()
  if (target > 7) or (target < 0):
    print("invalid distance. Please enter a number between 0 & 7")
    continue

  target_clicks = target * mulX
  mX.on_to_position(30, target_clicks)
  print("Moved to " + str(target_clicks))



  print("Please enter y-axis target square, between 0 and 7.")
  try:
    target = float(testPos)
  except:
    print("invalid entry. quitting")
    exit()
  if (target > 7) or (target < 0):
    print("invalid distance. Please enter a number between 0 & 7")
    continue

  target_clicks = target * mulY
  mY.on_to_position(30, target_clicks)
  print("Moved to " + str(target_clicks))

  testPos = testPos + 1
  if (testPos == 8):
    testPos = 0
    continue


