"""
Faolan Project, a free Age of Conan server emulator made for educational purpose
Copyright (C) 2008 Project Faolan team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

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
