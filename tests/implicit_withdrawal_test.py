#!/bin/env python

import sys
sys.path.append('.')

from sim.api import *
from sim.basics import *
from rip_router import RIPRouter
import sim.topo as topo
import os
import time

failed = False

class FakeEntity (Entity):
    def __init__(self, expected, to_announce):
        self.expect = expected
        self.announce = to_announce
        self.num_rx = 0
        if(self.announce):
            self.timer = create_timer(5, self.send_announce)    
            

    def handle_rx(self, packet, port):
        global failed
        global received
        if(self.expect):
            if(isinstance(packet, RoutingUpdate)):
                self.num_rx += 1
                for dest, cost in packet.paths.iteritems():
                  if dest not in self.expect.keys():
                    failed = True
                  elif cost != self.expect[dest]:
                    failed = True

    def send_announce(self):
        if(self.announce):
            update = RoutingUpdate()
            for dest, cost in self.announce.iteritems():
              update.add_destination(dest, cost)
            self.send(update, flood=True)

def create (switch_type = FakeEntity, host_type = FakeEntity, n = 2):
    RIPRouter.create('A')
    RIPRouter.create('B')
    FakeEntity.create('C', {A: 1}, {})
    topo.link(A, B)
    topo.link(B, C)
    
import sim.core
from hub import Hub as switch

import sim.api as api
import logging
api.simlog.setLevel(logging.DEBUG)
api.userlog.setLevel(logging.DEBUG)

_DISABLE_CONSOLE_LOG = True

create(switch)
start = sim.core.simulate
start()
time.sleep(10)
topo.unlink(A, B)
time.sleep(10)
if(failed):
  print("You have failed since I got unexpected updates!")
  os._exit(0)
else:
  print("Test is successful!")
  os._exit(2)
