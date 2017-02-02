#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
import RPi.GPIO as GPIO
import time

from ros_electro.msg import Length

def UltraSonicSensor():
  # ROS
  rospy.init_node('UltraSonicSensor', anonymous = True)
  pub = rospy.Publisher('Sensor', Length, queue_size = 100)
  r = rospy.Rate(3)

  # message
  msg = Length()

  # GPIO
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(6, GPIO.IN)
  GPIO.setup(13, GPIO.IN)
  GPIO.setup(19, GPIO.IN)
  GPIO.setup(26, GPIO.IN)
  GPIO.setup(21, GPIO.IN)
  GPIO.setup(20, GPIO.IN)
  GPIO.setup(16, GPIO.IN)
  GPIO.setup(12, GPIO.IN)

  while not rospy.is_shutdown():
    if GPIO.input(6) == 1:
      data = 7
    elif GPIO.input(13) == 1:
      data = 6
    elif GPIO.input(19) == 1:
      data = 5
    elif GPIO.input(26) == 1:
      data = 4
    elif GPIO.input(21) == 1:
      data = 3
    elif GPIO.input(20) == 1:
      data = 2
    elif GPIO.input(16) == 1:
      data = 1
    elif GPIO.input(12) == 1:
      data = 0

    msg.l = data
    pub.publish(msg)
    r.sleep()

if __name__ == '__main__':
  try:
    UltraSonicSensor()
  except rospy.ROSInterruptException: pass

  GPIO.cleanup()
