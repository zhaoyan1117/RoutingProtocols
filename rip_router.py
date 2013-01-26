from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''
class RIPRouter (Entity):
    def __init__(self):
        """
        Create routing table as a dictionary.
        Key: neighbors of self.
        Value: dictionary with router, which can be reached through the key neighbor, as key,
               and tuple (distance, port through which can reach router) as value.
        """
        self.routingTable = dict()
    
    def handle_rx (self, packet, port):
        """
        Generic dispatch function handling the three packet type:
        DiscoveryPacket, RoutingUpdate, and DataPacket.
        """
        if type(packet) is DiscoveryPacket:
            self._handleDiscoveryPacket(packet, port)
        elif type(packet) is RoutingUpdate:
            self._handleRoutingUpdate(packet, port)
        else:
            self._handleDataPacket(packet, port)
    
    def _handleDiscoveryPacket(self, packet, port):
        """
        Function handling DiscoveryPacket.
        """
        if packet.is_link_up:
            "Setup a new key-value pair in the routing table."
            self.routingTable[packet.src] = {packet.src : (1, port)}
            "Announce neighbor since the current routing table changed"
            self._announce()
        else:
            if packet.src in self.routingTable:
                "Delete a key-value pair in the routing table since link to the key goes down"
                self.routingTable.pop(packet.src)
                "Announce neighbor since the current routing table changed"
                self._announce()

    def _handleRoutingUpdate(self, packet, port):
        """
        Function handling RoutingUpdate.
        """
        
        if packet.src in self.routingTable:
            "Deep copy the value(dictionary) has key packet.src"
            slot = self.routingTable[packet.src].copy()
            "Acquire all the routers the update packet updated"
            dests = packet.all_dests()
            
            "Implicit withdrawals"
            for router in self.routingTable[packet.src]:
                if (router not in dests) and (router != packet.src):
                    slot.pop(router)
            
            "Update path to routers through packet.src"
            for dest in dests:
                slot[dest] = (1+packet.get_distance(dest), port)
            
            "Announce neighbors if routing table has changed"
            if slot != self.routingTable[packet.src]:
                self.routingTable[packet.src] = slot.copy()
                self._announce()

    def _handleDataPacket(self, packet, port):
        """
        Function handling DataPacket.
        """
        
        "Get all the ports through which can reach packet.dst and the corresponding distance"
        ports = [dests[packet.dst] for dests in self.routingTable.values() if packet.dst in dests]
        
        "Send through the shortest distance (Secondary key, smaller portID) port."
        if len(ports) != 0:
            ports.sort()
            self.send(packet, ports[0][1], False)
    
    def _announce(self):
        """
        Whenever called, this announce function will announce the current
        routing table to self's neighbors.
        """
        
        "Create dictionary to hold key: router, value: all the distances to it"
        shortestDises = dict()

        "Fill in shortestDises by going through all the values in routing table"        
        for disToDests in self.routingTable.values():
            for dest in disToDests:
                shortestDises[dest] = min(shortestDises.get(dest, (100, 100)), disToDests[dest])
        
        "Send the update packet to self's neighbors"
        for neighbor in self.routingTable:
            updatePacket = RoutingUpdate()
            disPortToNeighbor = self.routingTable[neighbor][neighbor]
                
            "Add destinations(except neighbor) and shortest distances into the update packet"
            for dest in shortestDises:
                if dest != neighbor:
                        
                    "Poison reverse"
                    if shortestDises[dest][1] == disPortToNeighbor[1]:
                        distance = 100
                    else:
                        distance = shortestDises[dest][0]
                            
                    updatePacket.add_destination(dest, distance)
    
            "Sending update packet after construction"
            self.send(updatePacket, disPortToNeighbor[1], False)

