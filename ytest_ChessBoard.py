#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_B
#from ev3dev2.sound import Sound

m = LargeMotor(OUTPUT_B)

m.reset()
print("Move carriage to furthest left square and press return")
input()

m.reset()

print("Move carriage to furthest right square and press return")
input()

length = m.position

# 8 square y axis movement range
m.on_to_position(30, 0)

m.wait_while('running')

mul = length/7

while (True):
  print("Please enter a target square, between 0 and 7.")
  try:
    target = float(input())
  except:
    print("invalid entry. quitting")
    exit()
  if (target > 7) or (target < 0):
    print("invalid distance. Please enter a number between 0 & 7")
    continue

  target_clicks = target * mul
  m.on_to_position(30, target_clicks)
  print("Moved to " + str(target_clicks))

