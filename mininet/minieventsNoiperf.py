"""
minievents is a Framework over Mininet to introduce an event generator.
Events are changes in mininet network at a specific time. The events are defined in a json document.
Implemented events are traffic generation (iperf) and link variations
(bandwidth, loss, delay) during a mininet launch.
It will launch mininet and perform the events at the specific time of each event
"""

import time
import json
import argparse
import os
#import cmd
from myNetwork import myNetwork
from mininet.util import dumpNodeConnections

from time import sleep

from minisched import scheduler
from mininet.cli import CLI
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel, info, debug
from mininet.net import Mininet
from mininet.node import OVSController, DefaultController, Host, OVSKernelSwitch, RemoteController
from mininet.link import TCLink, Intf, Link

__author__ = 'Carlos Giraldo'
__copyright__ = "Copyright 2014, AtlantTIC - University of Vigo"
__credits__ = ["Carlos Giraldo"]
__license__ = "GPL"
__version__ = "2.2.0"
__maintainer__ = "Carlos Giraldo"
__email__ = "carlos.giraldo@gti.uvigo.es"
__status__ = "Prototype"

class Minievents(Mininet):
    def __init__(self, topo=None, switch=OVSKernelSwitch, host=Host,
                 controller=DefaultController, link=Link, intf=Intf,
                 build=True, xterms=True, cleanup=False, ipBase='10.0.0.0/8',
                 inNamespace=False,
                 autoSetMacs=False, autoStaticArp=False, autoPinCpus=False,
                 listenPort=None, waitConnected=False, events_file=None):
        super(Minievents, self).__init__(topo=topo, switch=switch, host=host, controller=controller,
                                         link=link, intf=intf, build=build, xterms=xterms, cleanup=cleanup,
                                         ipBase=ipBase, inNamespace=inNamespace, autoSetMacs=autoSetMacs,
                                         autoStaticArp=autoStaticArp, autoPinCpus=autoPinCpus,
                                         listenPort=listenPort,
                                         waitConnected=waitConnected)
      
        self.scheduler = scheduler(time.time, time.sleep)
        if events_file:
            json_events = json.load(open(events_file))
            self.load_events(json_events)

    def load_events(self, json_events):
        # event type to function correspondence
        event_type_to_f = {'editLink': self.editLink, 'iperf': self.iperf, 'ping': self.ping, 'stop': self.stop}
        for event in json_events:
            debug("processing event: time {time}, type {type}, params {params}\n".format(**event))
            event_type = event['type']
            self.scheduler.enter(event['time'], 1, event_type_to_f[event_type], kwargs=event['params'])

    # EVENT COMMANDS
    def delLink(self, src, dst):
        # TODO This code should be tested
        info('{time}:deleting link from {src} to {dst}\n'.format(time=time.time(), src=src, dst=dst))
        n1, n2 = self.get(src, dst)
        intf_pairs = n1.connectionsTo(n2)
        for intf_pair in intf_pairs:
            n1_intf, n2_intf = intf_pair
            info('{time}:deleting link from {intf1} and {intf2}\n'.format(time=time.time(), intf1=n1_intf.name,
                                                                          intf2=n2_intf.name))
            n1_intf.link.delete()
            self.links.remove(n1_intf.link)
            del n1.intfs[n1.ports[n1_intf]]
            del n1.ports[n1_intf]
            del n1.nameToIntf[n1_intf.name]

            n2_intf.delete()
            del n2.intfs[n2.ports[n2_intf]]
            del n2.ports[n2_intf]
            del n2.nameToIntf[n2_intf.name]

    def editLink(self, **kwargs):
        """
        Command to edit the properties of a link between src and dst.
        :param kwargs: named arguments
            src: name of the source node.
            dst: name of the destination node.
            bw: bandwidth in Mbps.
            loss: packet loss ratio percentage.
            delay: delay in ms.
        """
        n1, n2 = self.get(kwargs['src'], kwargs['dst'])
        intf_pairs = n1.connectionsTo(n2)
        info('***editLink event at t={time}: {args}\n'.format(time=time.time(), args=kwargs))
        for intf_pair in intf_pairs:
            n1_intf, n2_intf = intf_pair
            n1_intf.config(**kwargs)
            n2_intf.config(**kwargs)
    def ping(self, **kwargs):
        """
        Command to send pings between src and dst.
        :param kwargs: named arguments
            src: name of the source node.
            dst: name of the destination node.
            interval: time between ping packet transmissions.
            count: number of ping packets.
        """
        kwargs.setdefault('count', 3)
        kwargs.setdefault('interval', 1.0)
        info('***ping event at t={time}: {args}\n'.format(time=time.time(), args=kwargs))

        if not os.path.exists("output"):
            os.makedirs("output")
        output = "output/ping-{src}-{dst}.txt".format(**kwargs)
        info('output filename: {output}\n'.format(output=output))

        src, dst = self.get(kwargs['src'], kwargs['dst'])
        ping_cmd = 'ping -c {count} -i {interval} {dst_ip}'.format(dst_ip=dst.IP(), **kwargs)

        info('ping command: {cmd} &>{output} &\n'.format(
            cmd = ping_cmd, output=output))
        src.sendCmd('{cmd} &>{output} &'.format(
            cmd = ping_cmd, output=output))
        # This is a patch to allow sendingCmd while ping is running in background.CONS: we can not know when
        # ping finishes and get its output
        src.waiting = False

    def start(self):
        super(Minievents, self).start()
        s1 = self.get('s1')
        s2 = self.get('s2')
        s3 = self.get('s3')
        s4 = self.get('s4')
        s5 = self.get('s5')
        s6 = self.get('s6')                                
        s7 = self.get('s7')
        s1.cmd( 'ovs-vsctl set Bridges s1 stp_enable=true') 
        s2.cmd( 'ovs-vsctl set Bridges s2 stp_enable=true')
        s3.cmd( 'ovs-vsctl set Bridges s3 stp_enable=true')
        s4.cmd( 'ovs-vsctl set Bridges s4 stp_enable=true')
        s5.cmd( 'ovs-vsctl set Bridges s5 stp_enable=true')
        s6.cmd( 'ovs-vsctl set Bridges s6 stp_enable=true')
        s7.cmd( 'ovs-vsctl set Bridges s7 stp_enable=true')         
        #CLI(self) if self.scheduler.empty() else self.scheduler.run()
        CLI(self)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--events",default="/home/mininet/mininet/mininet/minievents.json", help="json file with event descriptions")
    args = parser.parse_args()
    setLogLevel('info')
    net = Minievents(topo=myNetwork(), link=TCLink, controller=OVSController, events_file=args.events)
    net.start()
    print "Dumping host connections" 
    dumpNodeConnections(net.switches)
    

