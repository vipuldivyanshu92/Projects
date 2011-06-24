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

#include "Buffer.h"

////////////////////////////////////////////////////////
//
// Buffer methods implementation
//
////////////////////////////////////////////////////////
Buffer::Buffer(std::size_t chunkSize) :
    m_rawBuffer(chunkSize), m_writeCursor(0), m_readCursor(0), m_size(0)
{

}

void Buffer::write(const uint8* data, std::size_t length)
{
    BOOST_ASSERT((m_writeCursor+length) <= m_rawBuffer.size());
    memcpy(&(m_rawBuffer[m_writeCursor]), data, length);
    m_writeCursor+=length;
    m_size+= length;
}

void Buffer::resize(std::size_t size)
{
    m_rawBuffer.resize(size);
}

std::size_t Buffer::capacity()
{
    return m_rawBuffer.size();
}

void Buffer::reset()
{
    m_size=0;
    m_writeCursor=0;
    m_readCursor=0;
}

std::size_t Buffer::size()
{
    return m_size;
}

const std::vector<uint8>& Buffer::constBuffer() const
{
    return m_rawBuffer;
}

std::vector<uint8>& Buffer::mutBuffer()
{
    return m_rawBuffer;
}

std::string Buffer::read()
{

    BOOST_ASSERT((m_readCursor+sizeof(uint16)) <= m_rawBuffer.size());
    uint16 stringSize = read<uint16>();

    BOOST_ASSERT((m_readCursor+stringSize) <= m_rawBuffer.size());
    std::string ret(&(m_rawBuffer[m_readCursor]),
            &(m_rawBuffer[m_readCursor+stringSize]));
    
    m_readCursor+=stringSize;
    return ret;

}

void Buffer::write(const std::string& data)
{
    BOOST_ASSERT((m_writeCursor+data.size()+sizeof(uint16)) <= m_rawBuffer.size());
    write<uint16>(data.size());
    write((const uint8*) &(data[0]),data.size());
}

void Buffer::debugPrint()
{

	printf("packet size:%d\n",m_size);
	
	uint32 size = *(reinterpret_cast<uint32*>(&m_rawBuffer[0]));
	SwapByte::Swap<uint32>(size);
	printf("writen size %d\n",size);
	for(uint32 i=0; i < m_size; i++)
	{
		printf("%2x ",static_cast<int>(m_rawBuffer[i]));
	}

	std::cout << std::endl;
}

void Buffer::debugPrint(uint32 offset)
{

	printf("packet size:%d\n",m_size);
	
	uint32 size = *(reinterpret_cast<uint32*>(&m_rawBuffer[0]));
	SwapByte::Swap<uint32>(size);
	printf("writen size %d\n",size);
	for(uint32 i=offset; i < m_size; i++)
	{
		printf("%2x ",static_cast<int>(m_rawBuffer[i]));
	}

	std::cout << std::endl;
}

