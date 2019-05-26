#!/usr/bin/env python -B
# -*- coding: utf-8 -*-

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

WH = '\033[0m'
FG = '\033[0;32m'

conf.verb = 0
msg = 's3cr3tfl@g!'

bin_data = [bin(int(hex(ord(i))[2:],16))[2:].zfill(8) for i in msg]
chunks = [[j[i:i+2] for i in range(0, len(j), 2)] for j in bin_data]

# the total number of packets is not used in the encoder
# but it's useful for the listener to know how many packets to expect...
print '\n[*] Total packets to be send:{}'.format(len(chunks)*4)

for i in range(len(msg)):
    for j in range(4):
        # change the IPs accordingly...
        packet = IP(src = '192.168.10.15', dst='192.168.10.123')/ICMP()
        packet.ttl = int(chunks[i][j]+'111111',2) 
        send(packet)

print '[+] Data transmitted:\n'
print '{}{}{}\n'.format(FG, "".join([item for sublist in chunks for item in sublist]), WH)