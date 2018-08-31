#!/usr/bin/env python3
"""Simple DNS Server to make DNS over TLS connection"""

from dnslib import *
from dnslib.server import DNSServer
from time import sleep
import getdns
import logging
import sys

class MyResolver:

    # Setup Context
    cntx = getdns.Context()
    extensions = {}
    desired_addr_type = "IPv4"

    # Setup Upstream to cloudflare DNS on TLS
    upstream =  [ {
            'address_data': '1.1.1.1',
            'address_type': 'IPv4',
            'tls_pubkey_pinset': ['pin-sha256="yioEpqeR4WtDwE9YxNVnCEkTxIjx6EEIwFSQW+lJsbc="']
            }
    ]

    cntx.resolution_type = getdns.RESOLUTION_STUB
    cntx.dns_transport_list = [ getdns.TRANSPORT_TLS ]
    cntx.upstream_recursive_servers = upstream

    def get_rrtype(self,qtype):
        try:
            rrtype = eval("getdns.RRTYPE_%s" % qtype.upper())
        except AttributeError:
            print("Unknown DNS record type: {0}".format(qtype))
            sys.exit(1)
        else:
            return rrtype

    def resolve(self, request, handler):
        reply = request.reply()
        name = str(DNSLabel(request.q.qname))
        qtype = self.get_rrtype(QTYPE[request.q.qtype])

        try:
            results = self.cntx.address(name=name, extensions=self.extensions)
        except getdns.error as e:
            print (str(e))
            sys.exit(1)

        status = results.status
        # Parse results for A record (can be extended for other record types too)
        if status == getdns.RESPSTATUS_GOOD:
            for address in results.just_address_answers:
                if address['address_type'] == self.desired_addr_type:
                    addr = address['address_data']
                    zone =  "{name} {qtype} {addr}".format(name=name, qtype=request.q.qtype,addr=addr)
                    reply.add_answer(RR(name,QTYPE.A,rdata=A(addr),ttl=60))
            return reply
    

if __name__ == '__main__':
    
    # Setup listening port and address
    # defaults to 53 and 0.0.0.0
    port = int(os.getenv('DNS_PORT', 53))
    address = os.getenv('DNS_LISTEN_ADDRESS', "")

    resolver = MyResolver()

    # Start TCP and UDP listeners
    udp_server = DNSServer(resolver,port=port,address=address)
    tcp_server = DNSServer(resolver,port=port,address=address,tcp=True)
    udp_server.start_thread()
    tcp_server.start_thread()

    while udp_server.isAlive() or tcp_server.isAlive():
        sleep(1)
    udp_server.stop()
    tcp_server.stop()
