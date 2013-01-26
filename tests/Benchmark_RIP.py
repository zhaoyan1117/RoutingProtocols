import sys
sys.path.append('.')

from sim.api import *
from sim.basics import *
import sim.topo as topo
from rip_router import RIPRouter
from ls_router import LSRouter
import time

class RIPBenchmark (RIPRouter):
    def __init__(self):
        RIPRouter.__init__(self)
        self.convergencedTable = None
        self.upDone = False
        self.downDone = False
        
    def checklUpConvergened(self, start):
        if not self.upDone:
            converged = False
                
            if self.convergencedTable == self.routingTable:
                converged = True
                        
            if converged:
                timeUsed = time.time() - start
                print "[RIP] " + str(self.name) + " 's routing table is converged: time used is " + str(timeUsed) + " seconds."
                self.upDone = True

    def checklDownConvergened(self, start):
        if not self.downDone:
            converged = False
                
            if self.convergencedTable == self.routingTable:
                converged = True
                        
            if converged:
                timeUsed = time.time() - start
                print "[RIP] " + str(self.name) + " 's routing table is converged: time used is " + str(timeUsed) + " seconds."
                self.downDone = True        


def create(switch_type = RIPBenchmark, host_type = BasicHost):

    switch_type.create('s1')
    switch_type.create('s2')
    switch_type.create('s3')
    switch_type.create('s4')
    switch_type.create('s5')

    host_type.create('h1a')
    host_type.create('h1b')
    host_type.create('h2a')
    host_type.create('h2b')

    topo.link(s1, h1a)
    topo.link(s4, h1b)
    topo.link(s2, h2a)
    topo.link(s5, h2b)

    topo.link(s1, s2)
    topo.link(s2, s5)
    topo.link(s5, s4)
    topo.link(s4, s1)

    topo.link(s3, s1)
    topo.link(s3, s2)
    topo.link(s3, s4)
    topo.link(s3, s5)
    
import sim.core
switch = RIPBenchmark

import sim.api as api
import logging
api.simlog.setLevel(logging.DEBUG)
api.userlog.setLevel(logging.DEBUG)
_DISABLE_CONSOLE_LOG = True

create(switch)

def start():
    print '---------------------------------------'
    print '|Link-up convergence Benchmark for RIP|'
    print '---------------------------------------'
    s1.convergencedTable = {h1a: {h1a: (1, 0)}, s4: {s5: (2, 2), h2b: (3, 2), h2a: (4, 2), s2: (3, 2), h1b: (2, 2), s4: (1, 2), h1a: (101, 2), s3: (2, 2)}, s3: {s5: (2, 3), h2b: (3, 3), h2a: (3, 3), s4: (2, 3), h1b: (3, 3), s2: (2, 3), h1a: (101, 3), s3: (1, 3)}, s2: {s5: (2, 1), h2b: (3, 1), h2a: (2, 1), s2: (1, 1), h1b: (101, 1), s4: (101, 1), h1a: (101, 1), s3: (2, 1)}}
    s2.convergencedTable = {h2a: {h2a: (1, 0)}, s1: {s5: (101, 1), h2b: (101, 1), h2a: (101, 1), s1: (1, 1), h1b: (3, 1), s4: (2, 1), h1a: (2, 1), s3: (2, 1)}, s3: {s5: (2, 3), h2b: (3, 3), h2a: (101, 3), s1: (2, 3), h1b: (3, 3), s4: (2, 3), h1a: (3, 3), s3: (1, 3)}, s5: {s5: (1, 2), h2b: (2, 2), h2a: (101, 2), s1: (101, 2), h1b: (3, 2), s4: (2, 2), h1a: (101, 2), s3: (2, 2)}}
    s3.convergencedTable = {s5: {s5: (1, 3), h2b: (2, 3), s4: (2, 3), s2: (2, 3), s1: (3, 3), h1b: (3, 3), h2a: (3, 3), h1a: (4, 3)}, s2: {s5: (2, 1), h2b: (3, 1), h2a: (2, 1), s1: (2, 1), s4: (3, 1), h1b: (4, 1), s2: (1, 1), h1a: (3, 1)}, s1: {s5: (3, 0), h2b: (4, 0), s4: (2, 0), s2: (2, 0), s1: (1, 0), h1b: (3, 0), h2a: (3, 0), h1a: (2, 0)}, s4: {s5: (2, 2), h2b: (3, 2), h2a: (4, 2), s2: (3, 2), s1: (2, 2), h1b: (2, 2), s4: (1, 2), h1a: (3, 2)}}
    s4.convergencedTable = {h1b: {h1b: (1, 0)}, s1: {s5: (3, 2), h2b: (4, 2), h2a: (3, 2), s1: (1, 2), h1b: (101, 2), s2: (2, 2), h1a: (2, 2), s3: (2, 2)}, s3: {s5: (2, 3), h2b: (3, 3), h2a: (3, 3), s1: (2, 3), h1b: (101, 3), s2: (2, 3), h1a: (3, 3), s3: (1, 3)}, s5: {s5: (1, 1), h2b: (2, 1), h2a: (3, 1), s1: (3, 1), h1b: (101, 1), s2: (2, 1), h1a: (4, 1), s3: (2, 1)}}
    s5.convergencedTable = {h2b: {h2b: (1, 0)}, s4: {h2b: (101, 2), s3: (2, 2), h2a: (101, 2), s1: (2, 2), h1b: (2, 2), s2: (101, 2), s4: (1, 2), h1a: (3, 2)}, s3: {h2b: (101, 3), h1b: (3, 3), h2a: (3, 3), s1: (2, 3), s4: (2, 3), s3: (1, 3), h1a: (3, 3), s2: (2, 3)}, s2: {h2b: (101, 1), s3: (2, 1), h2a: (2, 1), s1: (2, 1), h1a: (3, 1), h1b: (4, 1), s4: (3, 1), s2: (1, 1)}}
    start_time = time.time()
    timer_s1 = create_timer(0.0001, s1.checklUpConvergened, kw = {"start":start_time})
    timer_s2 = create_timer(0.0001, s2.checklUpConvergened, kw = {"start":start_time})
    timer_s3 = create_timer(0.0001, s3.checklUpConvergened, kw = {"start":start_time})
    timer_s4 = create_timer(0.0001, s4.checklUpConvergened, kw = {"start":start_time})
    timer_s5 = create_timer(0.0001, s5.checklUpConvergened, kw = {"start":start_time})
    sim.core.simulate()

def drop():
    print '-----------------------------------------'
    print '|Link-down convergence Benchmark for RIP|'
    print '-----------------------------------------'
    print '######remove link between s1 and s2######'
    s1.convergencedTable = {h1a: {h1a: (1, 0)}, s4: {s5: (2, 2), h2b: (3, 2), h2a: (4, 2), s2: (3, 2), h1b: (2, 2), s4: (1, 2), h1a: (101, 2), s3: (2, 2)}, s3: {s5: (2, 3), h2b: (3, 3), h2a: (3, 3), s4: (2, 3), h1b: (3, 3), s2: (2, 3), h1a: (101, 3), s3: (1, 3)}}
    s2.convergencedTable = {h2a: {h2a: (1, 0)}, s3: {s5: (2, 3), h2b: (3, 3), h2a: (101, 3), s1: (2, 3), h1b: (3, 3), s4: (2, 3), h1a: (3, 3), s3: (1, 3)}, s5: {s5: (1, 2), h2b: (2, 2), h2a: (101, 2), s1: (3, 2), h1b: (3, 2), s4: (2, 2), h1a: (4, 2), s3: (2, 2)}}
    s3.convergencedTable = {s5: {s5: (1, 3), h2b: (2, 3), s4: (2, 3), s2: (2, 3), s1: (3, 3), h1b: (3, 3), h2a: (3, 3), h1a: (4, 3)}, s2: {s5: (2, 1), h2b: (3, 1), h2a: (2, 1), s1: (101, 1), h1b: (4, 1), s2: (1, 1), s4: (3, 1), h1a: (101, 1)}, s1: {s5: (3, 0), h2b: (4, 0), s4: (2, 0), s1: (1, 0), h1b: (3, 0), s2: (101, 0), h2a: (101, 0), h1a: (2, 0)}, s4: {s5: (2, 2), h2b: (3, 2), h2a: (4, 2), s2: (3, 2), s1: (2, 2), h1b: (2, 2), s4: (1, 2), h1a: (3, 2)}}
    s4.convergencedTable = {h1b: {h1b: (1, 0)}, s1: {s5: (101, 2), h2b: (101, 2), h2a: (4, 2), s1: (1, 2), h1b: (101, 2), s2: (3, 2), h1a: (2, 2), s3: (2, 2)}, s3: {s5: (2, 3), h2b: (3, 3), h2a: (3, 3), s1: (2, 3), h1b: (101, 3), s2: (2, 3), h1a: (3, 3), s3: (1, 3)}, s5: {s5: (1, 1), h2b: (2, 1), h2a: (3, 1), s1: (101, 1), h1b: (101, 1), s2: (2, 1), h1a: (101, 1), s3: (2, 1)}}
    s5.convergencedTable = {h2b: {h2b: (1, 0)}, s4: {h2b: (101, 2), s3: (2, 2), h2a: (101, 2), s1: (2, 2), h1b: (2, 2), s2: (101, 2), s4: (1, 2), h1a: (3, 2)}, s3: {h2b: (101, 3), h1b: (3, 3), h2a: (3, 3), s1: (2, 3), s4: (2, 3), s3: (1, 3), h1a: (3, 3), s2: (2, 3)}, s2: {h2b: (101, 1), s3: (2, 1), h2a: (2, 1), s1: (3, 1), h1a: (4, 1), h1b: (101, 1), s4: (101, 1), s2: (1, 1)}}
    topo.unlink(s1, s2)
    start_time = time.time()
    timer_s1 = create_timer(0.0001, s1.checklDownConvergened, kw = {"start":start_time})
    timer_s2 = create_timer(0.0001, s2.checklDownConvergened, kw = {"start":start_time})
    timer_s3 = create_timer(0.0001, s3.checklDownConvergened, kw = {"start":start_time})
    timer_s4 = create_timer(0.0001, s4.checklDownConvergened, kw = {"start":start_time})
    timer_s5 = create_timer(0.0001, s5.checklDownConvergened, kw = {"start":start_time})


start()
time.sleep(5)
drop()
time.sleep(5)


