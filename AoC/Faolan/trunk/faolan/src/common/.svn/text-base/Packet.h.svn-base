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

#ifndef PACKET_H_
#define PACKET_H_

#include <string>
#include "Common.h"
#include "Buffer.h"

/**
 * class representing a network message
 * Packet is not inheriting from Buffer to make things easier while working with boost::asio or the BufferPool
 * @author Albator
 */
class Packet {

public:

    /**
     * Build a packet from an existing buffer containing data
     * used for receiving packet
     */
    Packet(Buffer* buf);

    /**
     * Create a new packet.
     * usefull for packet to send. 
     */
    Packet(uint32 size, const std::string& sender, uint32 unknown1,
            uint32 unknown2, const std::string& receiver, uint32 unknown3,
            uint32 unknown4, uint32 opcode, Buffer* buf);
    
    //////////////////////////////////////////////
    // Getters
    /////////////////////////////////////////////
    Buffer* buffer();
    
    uint32 opcode();
    uint32 unknown1();
    uint32 unknown2();
    uint32 unknown3();
    uint32 unknown4();
    uint32 size();
    
    
    std::string sender();
    std::string receiver();

protected:
    Buffer* m_buffer;

    std::string m_sender, m_receiver;
    uint32 m_size;
    uint32 m_opcode;
    uint32 m_unknown1, m_unknown2, m_unknown3, m_unknown4;
};

#endif /*PACKET_H_*/
