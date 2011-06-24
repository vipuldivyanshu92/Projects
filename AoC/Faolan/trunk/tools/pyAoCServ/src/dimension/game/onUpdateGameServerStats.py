from ..common import packet
from construct import *

class onUpdateGameServerStats:
    def __init__(self, handler, ipkt):        
        # GameServerStats
        opkt = packet.Packet(handler, 0x0a, "Game")
        opkt.append("42c66ccd00431cdb00000002".decode("hex"))
        opkt.commit()