from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from state import robotstate
from statistics import mean 

"""
  Helper class holding handy things...
  """

class Xmotors():
  # Wrapper for paired X motors.

  def __init__(self):
    self.mX1 = LargeMotor(OUTPUT_A)
    self.mX2 = LargeMotor(OUTPUT_B)
    self.bX1 = TouchSensor(INPUT_1)
    self.bX2 = TouchSensor(INPUT_2)

  def on(self, speed):
    self.mX1.on(speed)
    self.mX2.on(speed)
  
  def wait_for_limit(self):
    while not (self.bX1.value or self.bX2.value):
      continue
    self.stop()

  def stop(self):
    self.mX1.stop()
    self.mX2.stop()
  
  def on_to_position(self, speed, position):
    self.mX1.on_to_position(speed, position, block=False)
    self.mX2.on_to_position(speed, position, block=False)
    self.wait_while('running')

  def reset(self):
    self.mX1.reset()
    self.mX2.reset()

  def position(self):
    return int(mean([self.mX1.position, self.mX2.position]))

  def wait_while(self, action):
    self.mX1.wait_while(action)
    self.mX2.wait_while(action)
