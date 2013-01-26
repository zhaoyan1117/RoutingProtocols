from sim.api import *
from sim.basics import *

'''
Create your learning switch in this file.
'''
class LearningSwitch(Entity):
    def __init__(self):
        # Add your code here!
        self.routingTable = {}

    def handle_rx (self, packet, port):
        self.routingTable[packet.src] = port
        if packet.dst in self.routingTable:
            self.send(packet, self.routingTable[packet.dst], False)
        else:
            self.send(packet, port, True)
