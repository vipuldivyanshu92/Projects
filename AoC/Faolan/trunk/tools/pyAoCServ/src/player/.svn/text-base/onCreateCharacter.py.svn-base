from .common import packet
from construct import *

class onCreateCharacter:    
    def __init__(self, handler, ipkt):
        self.handler = handler
        
        CreateCharacterStruct = Struct("CreateCharacter",
            UBInt32("DimID"),
            PascalString("RDBDSN", length_field = UBInt16("length")),
            UBInt32("PlayerInstance"),
        )
       
        self.CreateCharacterData = CreateCharacterStruct.parse(ipkt.data)
        
        self.CSServerConnectReady()
        self.LoginConnectReady()
        
    def LoginConnectReady(self):
        opkt = packet.Packet(self.handler, 2, "Player")
        # GameAddr
        opkt.append_uint8(127)
        opkt.append_uint8(0)
        opkt.append_uint8(0)
        opkt.append_uint8(1)
        opkt.append_uint16(7040)
        
        # ClientAgentAddr
        opkt.append_uint8(127)
        opkt.append_uint8(0)
        opkt.append_uint8(0)
        opkt.append_uint8(1)
        opkt.append_uint16(7038)
        
        opkt.append_uint32(int(self.handler.m_playerInfos["cookie"]))
        opkt.append_uint32(0x0000C350)
        opkt.append_uint32(int(self.handler.m_playerInfos["PlayerInstance"]))
        
        opkt.append_uint32(0x620000c7)
        opkt.append_uint8(0x9e)
        
        opkt.append_uint32(0x00000fa0) #Playfield
        opkt.append_uint64(0) # Suppose to be client id
        
        opkt.append_uint32(2)
        opkt.append_uint32(0x00009c50)
        opkt.append_uint32(0x00158af9)
        
        opkt.commit()
        
        
    def CSServerConnectReady(self):
        # Need configuration to specify CSServer
        opkt = packet.Packet(self.handler, 3, "Player")
        opkt.append_uint8(127)
        opkt.append_uint8(0)
        opkt.append_uint8(0)
        opkt.append_uint8(1)
        opkt.append_uint16(7002)
        opkt.append_uint32(int(self.handler.m_playerInfos["cookie"]))
        opkt.append_uint32(0x0000C350) # Character client id ! (to do)
        opkt.append_uint32(int(self.handler.m_playerInfos["PlayerInstance"]))
        opkt.commit()