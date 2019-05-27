#!/usr/bin/env python -B
# -*- coding: utf-8 -*-

import logging
import binascii
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from scapy.utils import PcapWriter

msg = []
pcap_file = "steg.pcap"
pkts = PcapWriter(pcap_file, append=True, sync=True)

def decode(lst):
    data = int("".join(['{:08b}'.format(i)[:2] for i in lst]),2)
    return binascii.unhexlify('%x' % data)

def callback(packet):
    global pkts
    pkts.write(packet)
    msg.append(packet.getlayer(IP).ttl)

def sniffer():
    try:
        # change interface and IP accordingly...
        sniff(prn=callback, iface="en0" ,\
             filter="icmp and ip host 192.168.10.15",\
             store=0, count=44) # count is equal with the total number of packets
    except Exception, e:
        print e
        exit(0)

if __name__ == '__main__':
    print '\n[+] Decoder started...'
    try:
        sniffer()
        print '[+] Writing pcap file: {}'.format(pcap_file)
        print "[+] The hidden message is -->  {}\n".format(''.join(decode(msg)))
    except KeyboardInterrupt:
        exit(0)