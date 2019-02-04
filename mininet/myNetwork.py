#!/usr/bin/python
#import os
#os.system("gnome-terminal -e 'bash -c \"sudo ~/pox/pox.py forwarding.l2_pairs info.packet_dump samples.pretty_log log.level --DEBUG   ; exec bash\"'")
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.topo import Topo

class myNetwork( Topo ):

#    def __init__( self ):
#        net = Mininet( topo=None,
#                       build=False,
#                       ipBase='10.0.0.0/8')
#    

    def build(self):
        info( '*** Adding controller\n' )
#        c0=self.addController(name='c0',
#                           controller=Controller,
#                           ip='127.0.0.1',
#                           protocol='tcp',
#                           port=6633)
    
        info( '*** Add switches\n')
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch)
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch)
        s5 = self.addSwitch('s5', cls=OVSKernelSwitch)
        s6 = self.addSwitch('s6', cls=OVSKernelSwitch)
        s7 = self.addSwitch('s7', cls=OVSKernelSwitch)
       # s8 = self.addSwitch('s8', cls=OVSKernelSwitch)
    
        info( '*** Add hosts\n')
        #h1 = self.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
        #h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')


        info( '*** Add links\n')
        self.addLink(s1, s2)
        self.addLink(s1, s5)
        self.addLink(s1, s6)
        self.addLink(s2, s3)
        self.addLink(s2, s5)
        self.addLink(s2, s6)
        self.addLink(s2, s7)
        self.addLink(s3, s6)
        self.addLink(s3, s4)
        self.addLink(s3, s5)
        self.addLink(s3, s7)
        self.addLink(s4, s7)
        self.addLink(s5, s6)
        self.addLink(s6, s7)


      #  self.addLink(s8, s7)
      #  self.addLink(s8, s1)
      #  self.addLink(s8, s2)
      #  self.addLink(s8, s3)
      #  self.addLink(s8, s4)
      #  self.addLink(s7, s1)
      #  self.addLink(s7, s2)
      #  self.addLink(s7, s3)
      #  self.addLink(s7, s4)
      #  self.addLink(s7, s6)
      #  self.addLink(s6, s5)
      #  self.addLink(s6, s4)
      #  self.addLink(s6, s3)
      #  self.addLink(s6, s2)
      #  self.addLink(s6, s1)
      #  self.addLink(s5, s4)
      #  self.addLink(s5, s3)
      #  self.addLink(s5, s2)
      #  self.addLink(s5, s1)
      #  self.addLink(s2, s3)
      #  self.addLink(s3, s4)
        self.addLink(h1, s1)
        # self.addLink(h2, s2) # TODO change to h2 <==> s4
        self.addLink(s4, h2)
    
#        info( '*** Starting network\n')
#        self.build()
#        c0.start()
#        info( '*** Starting controllers\n')
#       # for controller in net.controllers:
#       #     controller.start()
#    
#        info( '*** Starting switches\n')
#        s5.start([c0])
#        s2.start([c0])
#        s8.start([c0])
#        s1.start([c0])
#        s4.start([c0])
#        s7.start([c0])
#        s3.start([c0])
#        s6.start([c0])
    
    
       # s5.cmd('ovs-vsctl set bridge s5 rstp-enable=true')
       # s2.cmd('ovs-vsctl set bridge s2 rstp-enable=true')
       # s8.cmd('ovs-vsctl set bridge s8 rstp-enable=true')
       # s1.cmd('ovs-vsctl set bridge s1 rstp-enable=true')
       # s4.cmd('ovs-vsctl set bridge s4 rstp-enable=true')
       # s7.cmd('ovs-vsctl set bridge s7 rstp-enable=true')
       # s3.cmd('ovs-vsctl set bridge s3 rstp-enable=true')
       # s6.cmd('ovs-vsctl set bridge s6 rstp-enable=true')
        info( '*** Post configure switches and hosts\n')
    
        #CLI(self)
    #net.stop()

#if __name__ == '__main__':
#    setLogLevel( 'info' )
#    myNetwork()

