from sim.api import *
from sim.basics import *
import Queue
import random

"""
Link State Router.
Global state with LSpacket transmission.
Local computation with Breadth First Search.
"""
class LSRouter (Entity):
    def __init__(self):
        """
        self.routingTable(dict): key: router, value: through which port sends packet to the key(router).
        self.topology(dict): key: router(including self), value: tuple value (neighbor, port to neighbor).
        self.forwardedPacketIDs(list): list of IDs of all the LSpackets that have been forwarded.
        """
        self.routingTable = dict()
        self.topology = {self : list()}
        self.forwardedPacketIDs = list()

    def handle_rx(self, packet, port):
        """
        Generic dispatch function handling the three packet type:
        DiscoveryPacket, LSpacket, and DataPacket.
        """
        if type(packet) is DiscoveryPacket:
            self._handleDiscoveryPacket(packet, port)
        elif type(packet) is LSpacket:
            self._handleLSpacket(packet, port)
        else:
            self._handleDataPacket(packet, port)
            
    def _handleDiscoveryPacket(self, packet, port):
        """
        Function handling Discovery Packet.
        Three functionalities:
            1. Change self's topology and calculate new routing table.
            2. Broadcast signalPacket to inform other routers that the topology has changed.
            3. Broadcast self's new (neighbor, port) tuples to other routers.
        """
        
        "Create signalPacket and updatePacket with LSpackets."
        signalPacket = LSpacket(random.random(), True)
        updatePacket = LSpacket(random.random(), False)
        
        "Change self's topology (self's neighbors) based on link_up or link_down."
        if packet.is_link_up:
            self.topology[self].append((packet.src, port))
        else:
            for neighborPort in self.topology[self]:
                if neighborPort[0] == packet.src:
                    self.topology[self].remove(neighborPort)
        
        "Calculating new routing table."
        self._updateRoutingTable()

        "Adding self's (neighbor, port) tuples into the update packet."
        for neighborPort in self.topology[self]:
            updatePacket.add_neighbor(neighborPort)

        "Broadcast update packet."
        self.send(updatePacket, None, True)
        "Broadcast signal packet."
        self.send(signalPacket, port, True)
        
    def _handleLSpacket(self, packet, port):
        """
        Function handling LSpacket.
        Big Ideas:
            1. Avoid forwarding forwarded LSpackets.
            2. Handle signal packet:
                a. Keep flooding signal packet.
                b. Broadcasting self's (neighbor, port) tuples to other routers.
            3. Handle update packet:
                a. Adding update information of topology into self's topology.
                b. Update routing table.
                b. Keep flooding update packet.
        """
        
        "Check if forwarded packet before."
        forwarded = False
        for id in self.forwardedPacketIDs:
            if packet.id == id:
                forwarded = True
                
        "If not, process the packet handling."
        if not forwarded:
            
            if packet.isSignal:
                "For signal packet"
                
                "Construct update Packet."
                updatePacket = LSpacket(random.random(), False)
                for neighborPort in self.topology[self]:
                    updatePacket.add_neighbor(neighborPort)
    
                "Broadcast self's update packet."    
                self.send(updatePacket, None, True)
                "Keep flooding signal packet."
                self.send(packet, port, True)
            
            else:
                "For update packet."
                
                "Update self's topology."
                self.topology[packet.src] = [neighborPort for neighborPort in packet.get_neighbors()]
                "Update routing table."
                self._updateRoutingTable()
                "Keep flooding update packet."
                self.send(packet, port, True)
            "Add packet's id into forwarded list."
            self.forwardedPacketIDs.append(packet.id)
        
    def _handleDataPacket(self, packet, port):
        """
        Function handling DataPacket.
        Functionality: 
            1. Retrieve out going port from routing table with key of packet.dst.
            2. Send it.
        """
        self.send(packet, self.routingTable[packet.dst], False)

    def _updateRoutingTable(self):
        """
        Breadth First Search updating routing table.
        Since this project's background does not have a cost on each link, 
        that each link costs 1, we can use the special edition of Dijkstra's algorithm - Breadth first search.
        P.S. We are using a special edition of Uniform cost search, Breadth first search.
        
        Special Idea:
            We do a special handling when visit a router in bfs.
            Since our routing table maps the router to the port, through which we can go to the router with shortest path from self,
            we need to map router to self's port, not the router's parent's port.
            Note this two concepts are the same when the router is self's neighbors.
            
            Thus, we have a rootPort dictionary,
                if the router is self's neighbor, its root port is the self's port to itself.
                else, the router's self port its its parent's root port.
        """
        
        "Initialization."
        visited = list()
        fringe = Queue.Queue()
        fringe.put(self)
        visited.append(self)
        "Initialize root port dictionary."
        rootPort = dict()
        
        "Loop."
        while not fringe.empty():
            router = fringe.get()
            if router in self.topology:
                neighborPorts = [neighborPort for neighborPort in self.topology[router]]
                neighborPorts.sort(key=lambda x:x[1])
                for neighborPort in neighborPorts:
                    
                    if neighborPort[0] not in visited:
                        
                        "Map router to neighbor's port to itself or it's parent's root port."
                        if router == self:
                            rootPort[neighborPort[0]] = neighborPort[1]
                        else:
                            rootPort[neighborPort[0]] = rootPort[router]
                            
                        self.routingTable[neighborPort[0]] = rootPort[neighborPort[0]]
                        fringe.put(neighborPort[0])
                        visited.append(neighborPort[0])

