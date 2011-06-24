from ..common import packet
from construct import *

class onPing:
    def __init__(self, handler, ipkt):
        # Parsing
        t = UBInt32("Time").parse(ipkt.data)
        
        # Pong
        opkt = packet.Packet(handler, 0x06, "Game")
        opkt.append_uint32(t)
        opkt.commit()