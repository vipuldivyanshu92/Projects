#!/usr/bin/env python

import struct

"""
    uint32 : RealmCount
    for i in range(RealmCount):
        uint32 : RealmNumber
        uint32 : unk1
        uint32 : unk2
        uint32 : unk3
        uint16 : RealmNameLength
        string : RealmName
        uint32 : unk4
        uint32 : unk5
        uint32 : unk6
        uint32 : unk7
        uint32 : unk8
        uint32 : unk9
        uint16 : unk10
        uint32 : unk11
"""

class realmEnum:
    def ReadFromBuffer(self, buffer):
        self.realms = {}
        pointer = 0
        self.realmcount = struct.unpack('!I', buffer[pointer:+4])[0]
        pointer += 4
        for i in range(self.realmcount):
            RealmNumber, RealmStatus, unk2, unk3, RealmNameLength = struct.unpack('!IIIIH', buffer[pointer:pointer+18])
            pointer += 18
            RealmName, unk4, unk5, unk6, unk7, unk8, unk9, RealmType, unk11 = struct.unpack('!%dsIIIIIIHI' % (RealmNameLength), buffer[pointer:pointer+RealmNameLength+30])
            pointer += RealmNameLength+30
            self.realms[RealmNumber] = {'RealmStatus':RealmStatus, 'unk2':unk2, 'unk3':unk3, 'RealmNameLength':RealmNameLength, 'RealmName':RealmName, 'unk4':unk4, 'unk5':unk5, 'unk6':unk6, 'unk7':unk7, 'unk8':unk8, 'unk9':unk9, 'RealmType':RealmType, 'unk11':unk11}
        
    def GetBuffer(self):
        pass