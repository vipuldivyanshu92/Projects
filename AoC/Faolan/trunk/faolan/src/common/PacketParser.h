/*
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
*/

#ifndef PACKETPARSER_H_
#define PACKETPARSER_H_

#include "Common.h"
#include <map>

#include "Packet.h"
#include "Buffer.h"

///////////////////////////////////////////////////
// Macro to register a new packet
// a : callbackObject type
// b : packet class name
// c : opcode
//////////////////////////////////////////////////

#define REGISTER_PACKET_HANDLER(packetClassName, opcode, callbackObjectType) \
    template<class T > class packetClassName ## Factory : \
    public PacketParser<T>::PacketFactory { \
public: \
    packetClassName ## Factory() : \
        PacketParser<T>::PacketFactory(opcode) \
    { \
    } \
 \
    virtual void create(T * cbo, Buffer* buf) \
    { \
        cbo->onPacket(packetClassName(buf) ); \
    } \
}; \
static packetClassName ## Factory<callbackObjectType> packetClassName ## Fact

/**
 * Parse incoming packet.
 * Create packet object if data are valid.
 * PacketFactories then call a method in the callBackObject
 */
template<class T> class PacketParser
{

public:

    PacketParser(T* callbackObject) :
    m_callbackObject(callbackObject)
    {

    }

    /**
     * Parse a received buffer and create the right packet if the packet is valid
     * and the opcode included in the std::map.
     */
    void AOCParse(Buffer* buf, uint32 readedSize)
    {
        uint32 size;
        uint32 unknown1,unknown2,unknown3,unknown4,opcode;
        std::string sender, receiver;

        // can we hardcode the position of the opcode ?
        
        (*buf) >> size >>  sender >> unknown1 >> unknown2 >> receiver >> unknown3 >> unknown4  >> opcode;

        if (size == (readedSize-4))
        {
            Iter iter = MapPacketFactory().find(opcode);
            if(iter==MapPacketFactory().end())
            {
                //packet isn't registered, send an event to callbackObject

            }
            else
            {
                //legitimate packet
                buf->reset();
                (*iter).second->create(m_callbackObject,buf);
            }
        } else
        {
            // send an event to the callbackObject ?
        }

    }

    class PacketFactory
    {
    public:

        /**
         * Instantiate a new Packet from the given buffer
         * and call a specific method from callbackObject with the packet for processing
         */
        virtual void create(T* callbackObject, Buffer* buf) = 0;

    protected:

        /**
         * Register the factory into the parser
         */
        PacketFactory(uint32 opcode)
        {
            PacketParser::MapPacketFactory().insert(std::make_pair(opcode, this));
        }

        virtual ~PacketFactory()
        {

        }
    };

    /**
     * Packet factories container
     */
    static std::map<uint32, PacketFactory*>& MapPacketFactory()
    {
        static std::map<uint32, PacketFactory*> m_mapPacketFatories;
        return m_mapPacketFatories;
    }

private:

    T* m_callbackObject;
    typedef typename std::map<uint32, PacketFactory*>::iterator Iter;

};

#endif /*PACKETPARSER_H_*/
