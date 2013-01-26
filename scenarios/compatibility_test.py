#!/bin/env python
# This is a basic compatibility test to make sure you're using the built-in
# classes properly.
#
# If this crashes, or you get an error message, or you never get any messages, 
# you're likely
# using the built-ins (particularly: RoutingUpdate) in such a way that your
# implementation will fail the grading scripts - make sure you fix before 
# turning in!
from sim.api import *
from sim.basics import *
from rip_router import RIPRouter
import sim.topo as topo


class FakeEntity (Entity):
    def __init__(self, expected, to_announce):
        self.expect = expected
        self.announce = to_announce
        self.num_rx = 0
        if(self.announce):
            self.timer = create_timer(5, self.send_announce)    

    def handle_rx(self, packet, port):
        if(self.expect):
            if(isinstance(packet, RoutingUpdate)):
                self.num_rx += 1
                if(self.expect[0] in packet.all_dests() and packet.get_distance(self.expect[0]) == (self.expect[1])):
                    print("SUCCESS! You passed the compatibility test! Move along now...")
                elif(self.num_rx > 2): 
                    print("Received a number of routing updates, none that performed the expected behavior. Better double-check your compatibility with the spec before turning in!")
                   
    def send_announce(self):
        if(self.announce):
            update = RoutingUpdate()
            update.add_destination(self.announce[0], self.announce[1])
            self.send(update, flood=True)

def create (switch_type = FakeEntity, host_type = FakeEntity, n = 2):
    RIPRouter.create('student')
    BasicHost.create('dest')
    FakeEntity.create('announcer', None, [dest, 7])
    FakeEntity.create('listener', [dest, 8], None)

    topo.link(student, announcer)
    topo.link(student, listener)
    

