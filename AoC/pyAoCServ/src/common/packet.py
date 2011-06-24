from construct import *
from interfaces import *

PACKET_STRUCT = Struct("HEADER_STRUCT",
    UBInt32("size"),
    PascalString("receiver", length_field = UBInt16("length")),
    UBInt32("unk1"),
    UBInt32("unk2"),
    PascalString("sender", length_field = UBInt16("length")),
    UBInt32("unk3"),
    UBInt32("unk4"),
    UBInt32("opcode"),
    MetaField("data", lambda ctx: ctx["size"]-(24 + len(ctx["sender"]) + len(ctx["receiver"]))),
)

class Packet:
    """
        Create a packet object, /!\ only for writing !
    """
    def __init__(self, handler, opcode, interface):
        self.opcode = opcode
        self.data = ""
        self.handler = handler
        
        self.CLIENT_INTERFACE_NAME, self.SERVER_INTERFACE_NAME = interfaces[interface]        
        
    def append(self, v):
        self.data += v
        
    def append_string(self, v):
        self.data += PascalString("string", length_field = UBInt16("length")).build(v)
        
    def append_uint8(self, v):
        self.data += UBInt8("uint8").build(v)
        
    def append_uint16(self, v):
        self.data += UBInt16("uint16").build(v)
        
    def append_uint32(self, v):
        self.data += UBInt32("uint32").build(v)
        
    def append_uint64(self, v):
        self.data += UBInt64("uint64").build(v)
    
    def commit(self):
        self.handler.write_buffer.append(
            PACKET_STRUCT.build(Container(
                size = 24 + len(self.CLIENT_INTERFACE_NAME) + len(self.SERVER_INTERFACE_NAME) + len(self.data),
                receiver = self.CLIENT_INTERFACE_NAME,
                unk1 = 1,
                unk2 = 0,
                sender = self.SERVER_INTERFACE_NAME,
                unk3 = 0,
                unk4 = 0,
                opcode = self.opcode,
                data = self.data)
            )
        )