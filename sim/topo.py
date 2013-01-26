"""
Provides an API for connecting and disconnecting Entities.
You should only use this to build your own test scenarios
"""

from core import topoOf

def link (entity1, entity2):
  """ Connects the two nodes on a free port """
  return topoOf(entity1).linkTo(entity2)

def unlink (entity1, entity2):
  """ Disconnects two connected nodes """
  return topoOf(entity1).unlinkTo(entity2)

def disconnect (entity):
  """ Disconnects this entity from everything """
  return topoOf(entity).disconnect()

def show_ports (entity):
  ports = topoOf(entity).get_ports()
  print "Ports for %s:" % (entity,)
  for p in ports:
    p1 = "%s:%i" % (p[0],p[1])
    p2 = "%s:%i" % (p[2],p[3])
    print "%14s <-> %-14s" % (p1,p2)
