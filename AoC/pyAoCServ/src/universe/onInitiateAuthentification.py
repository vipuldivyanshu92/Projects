import random
from .common import packet

class onInitiateAuthentification:
    def __init__(self, handler, ipkt):
        handler.server_hash = "%x" % (random.getrandbits(8*16))

        opkt = packet.Packet(handler, 0, "Universe")
        opkt.append_string(handler.server_hash)
        opkt.commit()