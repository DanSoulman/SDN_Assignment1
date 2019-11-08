# Dan Coleman R00151926 SDN Assignment 1
#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, RemoteController
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

# GLOBALS
CORE_SWITCH_COUNT = 2    #No of Core Switches in Topology
AGGREGATE_COUNT = 6      #No of Aggregate Switches in Topology
HOST_PER_AGGREGATE = 2   #No of Switches in each host


class CustomTopo(Topo):

    def __init__(self, NO_OF_CORE_SWITCHES = 2, NO_OF_AGGREGATES = 6, NO_OF_HOSTS_PER_AGGREGATE = 2, **opts):
        #Note NO_OF_AGGREGATES and NO_OF_HOSTS_PER_AGGREGATE are defaults if value is no declared

        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        #Variables 
        switch_list = []#Holds list of Switches
        host_track = 1 #Counts host number

        #Creates a list of all the switches and numbers them
        for i in xrange(0, NO_OF_AGGREGATES + NO_OF_CORE_SWITCHES):
            switch_list.append(self.addSwitch('S%s' % str(i + 1)))
            
            if i == 1: #Links Core Switches (1 and 2) 
                self.addLink(switch_list[i - 1], switch_list[i])
            
            #Creates the Aggregation Switches and adds them to Core Switches
            elif i > NO_OF_CORE_SWITCHES - 1:
                
                #Adds the first half (3 - 5 by default) to switch 1 and the second half (6 - 8) to switch 2
                if (i - NO_OF_CORE_SWITCHES) < (NO_OF_AGGREGATES / 2):
                    self.addLink(switch_list[i], switch_list[0])

                else:
                    self.addLink(switch_list[i], switch_list[1])


                #Adds as many hosts as set in HOST_PER_AGGREGATE to the switch in the current index 
                for j in range(NO_OF_HOSTS_PER_AGGREGATE):
                    host = self.addHost('H%s' % host_track)
                    host_track += 1
                    self.addLink(switch_list[i], host)

        
if __name__ == '__main__':
    setLogLevel('info')

    topo = CustomTopo(NO_OF_CORE_SWITCHES = CORE_SWITCH_COUNT, NO_OF_AGGREGATES=AGGREGATE_COUNT, NO_OF_HOSTS_PER_AGGREGATE=HOST_PER_AGGREGATE)

    net = Mininet(topo=topo, controller=None)# Removed default controller (Thanks Jonathan)
    # Create Controller C0 on port 6653 with IP 192.168.254.202
    controller = net.addController("C0", port=6653, ip="192.168.254.202", controller=RemoteController)
    
    net.start()
    
    print "Pumping host connections"
    dumpNodeConnections(net.hosts)
    
    print "Testing network connectivity"
    net.pingAll()
    
    CLI(net)  # Opens CLI info
    net.stop() # Ends mininet
