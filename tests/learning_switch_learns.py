#!/bin/env python
#
# This is a basic test of the learning switch.

import sys
sys.path.append('.')

from sim.api import *
from sim.basics import *
from rip_router import RIPRouter
from learning_switch import LearningSwitch as switch
import sim.topo as topo
import os
import time


class ReceiveEntity (Entity):
    def __init__(self, expected):
        self.expect = expected
        self.unexpecteds = -1 # we expect a single packet

    def handle_rx(self, packet, port):
        if isinstance(packet, DiscoveryPacket):
            return
        self.unexpecteds += 1
        self.send(packet, port, flood=True)

def create (switch_type):
    switch_type.create('student')
    BasicHost.create('dest')
    BasicHost.create('src')
    ReceiveEntity.create('announcer1', src)
    ReceiveEntity.create('announcer2', dest)
    ReceiveEntity.create('announcer3', None)

    topo.link(student, announcer1)
    topo.link(student, announcer2)
    topo.link(student, announcer3)
    topo.link(src, announcer1)
    topo.link(dest, announcer2)

import sim.core

import sim.api as api
import logging
api.simlog.setLevel(logging.DEBUG)
api.userlog.setLevel(logging.DEBUG)

_DISABLE_CONSOLE_LOG = True

create(switch)
start = sim.core.simulate
start()
time.sleep(10)
src.ping(dest)
time.sleep(30)
if(announcer3.unexpecteds != 0):
    print("listener received incorrect number of unexpected packets for 1st ping: %d" % announcer3.unexpecteds)
    exit()
src.ping(dest)
time.sleep(30)
if(announcer3.unexpecteds != 0):
    print("listener received incorrect number of unexpected packets for 2nd ping: %d" % announcer3.unexpecteds)
    exit()
print "learning switch learned! <(^_^<)  <(^_^)^  ^(^_^)^  ^(^_^)>  (>^_^)>"
