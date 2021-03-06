#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
import myState
import struct
import time
import create2api
from ros_electro.msg import Rstate
from ros_electro.msg import Length

class Acceron(object):
  def __init__(self):
    # Runner
    rospy.init_node('Runner', anonymous = True)

    # instance of publisher
    self.pub = rospy.Publisher('Roomba_State', Rstate, queue_size = 100)
    # instance of subscriber
    self.sub = None

    # create2api
    self.bot = create2api.Create2()
    self.bot.start()
    self.bot.safe()

    # sensor
    self.bump = 0
    self.uss = 0

    # state machine
    self.state = myState.myState()

    # Goal checker
    self.goal = False

  def callbackA(self, data):
    self.uss = data.l
    self.sub.unregister()

  def subscribe_uss(self):
    self.sub = rospy.Subscriber('Sensor', Length, self.callbackA)

  def acceler(self):
    r = rospy.Rate(3)
    while not rospy.is_shutdown():
      # Roombaの状況把握
      # バンパから読み込み
      self.bot.sensors(7)
      self.bump = self.bot.SCI.Read(1)
      self.bump = struct.unpack('B', self.bump)
      # stateに応じた動作 =====================================
      if self.state.current() == 'Running':
        if self.bump[0] == 3:
          self.bot.drive_straight(0)
          self.state.transition('Collision')
        elif self.bump[0] == 1:
          self.bot.drive_straight(0)
          time.sleep(0.5)
          self.bot.drive_straight(-100)
          time.sleep(1)
          self.bot.drive(100, 1)
          time.sleep(0.5)
        elif self.bump[0] == 2:
          self.bot.drive_straight(0)
          time.sleep(0.5)
          self.bot.drive_straight(-100)
          time.sleep(1)
          self.bot.drive(100, -1)
          time.sleep(0.5)
        else:
          self.bot.drive_straight(250)
      elif self.state.current() == 'Collision':
        # ちょっと下がる
        self.bot.drive_straight(-100)
        time.sleep(1)
        self.bot.drive_straight(0)
        self.state.transition('Avoiding')
      elif self.state.current() == 'Avoiding':
        # 周りに信号を送り，走れそうな方向を探す
        arround = []
        # 右斜め前を向く =======================
        """self.bot.drive(100, -1)
        time.sleep(0.85)
        self.bot.drive_straight(0)
        time.sleep(0.5)
        # 超音波センサから読み込み
        self.subscribe_uss()
        arround.append(self.uss)"""
        # 右を向く =============================
        self.bot.drive(100, -1)
        time.sleep(1.72)
        self.bot.drive_straight(0)
        time.sleep(0.5)
        # 超音波センサから読み込み
        self.subscribe_uss()
        arround.append(self.uss)
        # 左斜め前を向く =======================
        """self.bot.drive(100, 1)
        time.sleep(2.66)
        self.bot.drive_straight(0)
        time.sleep(0.8)
        # 超音波センサから読み込み
        self.subscribe_uss()
        arround.insert(0, self.uss)"""
        # 左を向く =============================
        self.bot.drive(100, 1)
        time.sleep(3.4)
        self.bot.drive_straight(0)
        time.sleep(1)
        # 超音波センサから読み込み
        self.subscribe_uss()
        arround.insert(0, self.uss)

        # 周りが何かしらあれば終了
        arround_min = min(arround)
        if arround_min >= 6:
          self.state.transition('Goal')
          print arround
          continue

        # 超音波が返る時間が長い方向を向く
        if arround[0] == arround_min:
          self.bot.drive(100, -1)
          time.sleep(3.4)
          self.bot.drive_straight(0)
        """
        for x in range(0, 2):
          if arround[x] == arround_min:
            if x != 0:
              self.bot.drive(100, -1)
            if x == 0:
              pass
            elif x == 1:
              time.sleep(3.4)
            elif x == 2:
              time.sleep(2.66)
            elif x == 3:
              time.sleep(3.4)
            self.bot.drive_straight(0)
            break
          else:
            pass
         """
        self.state.transition('Running')
      elif self.state.current() == 'Goal':
        if self.goal == False:
          self.goal = True
          print "Goal!"

      # stateに応じた動作ここまで ==================================

      # 状態送出
      msg = Length()
      msg = self.state.current()
      if msg == 'Running':
        msg = 3
      elif msg == 'Collision':
        msg = 1
      elif msg == 'Avoiding':
        msg = 2
      else:
        msg = 0

      self.pub.publish(msg)

      r.sleep()

def runner():
  Runner = Acceron()
  Runner.acceler()

if __name__ == '__main__':
  runner()
