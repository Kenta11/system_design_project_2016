# -*- coding: utf-8 -*-


# state machine
# 0: Running
# 1: Collision
# 2: Avoiding 
# 3: Goal
class myState:
  def __init__(self):
    self.statelist = ['Running','Collision','Avoiding','Goal']
    self.state = self.statelist[0]

  def transition(self, key):
    if self.statelist[0] == self.state and key == 'Collision':
      self.state = self.statelist[1]
    elif self.statelist[1] == self.state and key == 'Avoiding' :
      self.state = self.statelist[2]
    elif self.statelist[2] == self.state and key == 'Running':
      self.state = self.statelist[0]
    elif self.statelist[2] == self.state and key == 'Goal':
      self.state = self.statelist[3]
    else:
      pass

  def current(self):
    return self.state
