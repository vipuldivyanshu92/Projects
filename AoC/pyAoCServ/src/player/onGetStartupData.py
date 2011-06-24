from .common import packet
from construct import *

class onGetStartupData:
    def __init__(self, handler, ipkt):
        # Nothing to do with this packet ?
        
        self.handler = handler
        
        self.UpdateClientPlayerData()
        self.SetDimensionList()
        self.PlayerSetupComplete()
    
    def UpdateClientPlayerData(self):
        NB_SLOTS = 8 # Each player can have up to 8 slots
        
        # character enumeration
        characterStruct = Struct("Character",
            UBInt32("CharInstance"),
            UBInt32("PlayerInstance"),
            UBInt32("CharInstance"),
            PascalString("name", length_field = UBInt16("length")),
            UBInt32("dimension_id"),
            UBInt32("sex"),
            PascalString("last_connection", length_field = UBInt16("length")),
            UBInt32("unk1"),
            UBInt32("playfield"),
            UBInt32("level"),
            UBInt32("cclass"),
            UBInt32("unk2"),
            UBInt32("unk3"),
            UBInt32("unk4"),
            UBInt32("race"),
        )
        
        # Getting Chars from DataBase
        self.handler.server.db.query("SELECT * FROM `characters` WHERE `account_id` = '%s'" % (self.handler.m_playerInfos["account_id"]))
        r = self.handler.server.db.store_result()
        characters = r.fetch_row(NB_SLOTS, how=1)
        
        opkt = packet.Packet(self.handler, 4, "Player")
        
        opkt.append_uint32(self.handler.m_playerInfos["PlayerInstance"])
        opkt.append_uint32((len(characters)+1)*1009)

        for i in range(len(characters)):
            opkt.append(characterStruct.build(Container(
                    CharInstance = int(characters[i]["character_id"]),
                    PlayerInstance = self.handler.m_playerInfos["PlayerInstance"] ,
                    CharInstance2 = int(characters[i]["character_id"]),
                    name = characters[i]["name"],
                    dimension_id = int(characters[i]["dimension_id"]),
                    sex = int(characters[i]["sex"]),
                    last_connection = characters[i]["last_connection"],
                    unk1 = 0,
                    playfield = int(characters[i]["playfield"]),
                    level = int(characters[i]["level"]),
                    cclass = int(characters[i]["class"]),
                    unk2 = 0,
                    unk3 = 0x97207ff8,
                    unk4 = 2,
                    race = int(characters[i]["race"]),
                )
            ))

        opkt.append_uint32(NB_SLOTS)
        opkt.commit()
        
    def SetDimensionList(self):
        dimensionStruct = Struct("Dimension",
            UBInt32("dimension_id"),
            UBInt32("status"),
            UBInt32("unk1"),
            UBInt32("unk2"),
            PascalString("name", length_field = UBInt16("length")),
            UBInt32("unk3"),
            UBInt32("unk4"),
            UBInt32("unk5"),
            UBInt32("unk6"),
            UBInt32("unk7"),
            UBInt32("unk8"),
            UBInt16("type"),
            UBInt32("unk9"),
        )
        
        opkt = packet.Packet(self.handler, 5, "Player")
        opkt.append_uint32(len(self.handler.server.dimensions))
        for d in self.handler.server.dimensions:
            opkt.append(dimensionStruct.build(Container(
                    dimension_id = int(self.handler.server.dimensions[d]["dimension_id"]),
                    status = int(self.handler.server.dimensions[d]["status"]),
                    unk1 = 8,
                    unk2 = 100000,
                    name = self.handler.server.dimensions[d]["name"],
                    unk3 = 0,
                    unk4 = 0,
                    unk5 = 0,
                    unk6 = 0,
                    unk7 = 0,
                    unk8 = 0,
                    type = int(self.handler.server.dimensions[d]["type"]),
                    unk9 = 0,
                )
            ))
        
        opkt.commit()
		
    def PlayerSetupComplete(self):
        opkt = packet.Packet(self.handler, 8, "Player")
        opkt.append_uint32(1)
        opkt.append_uint64(long(self.handler.m_playerInfos["account_id"]))
        opkt.commit()