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

#ifndef BUFFER_H_
#define BUFFER_H_

#include "Common.h"

#include <vector>
#include <memory>
#include <string>
#include <boost/assert.hpp>
#include <boost/asio.hpp>

#include "SwapByte.h"



/**
 *  A simple byte buffer with C++ convenient methods
 *  Support asio const buffer by using boost::asio::buffer(buf.rawBuffer(), buf.size());
 *  @author Albator
 */
class Buffer {

public:
    Buffer(std::size_t chunkSize);

    /**
     *  Used size 
     */
    std::size_t size();

    /**
     * Capacity of the buffer
     */
    std::size_t capacity();

    /**
     * Resize the buffer to the given size
     */
    void resize(std::size_t size);

    /**
     * Reset buffer to re-use
     */
    void reset();

    ////////////////////////////////////////////////
    // Write op
    ////////////////////////////////////////////////
    template <typename T> Buffer& operator<<(const T data)
    {

        write(data);
        return *this;
    }

    /**
     *  Write data to the buffer
     */
    void write(const uint8* data, std::size_t length);

    template <typename T> void write(T data)
    {
		SwapByte::Swap<T>(data);
        write(reinterpret_cast<const uint8*>(&data), sizeof(data));
    }
    
    /**
     * Write an AoC string <uint16,size><string>
     */
    void write(const std::string& data);

    /////////////////////////////////////////////////
    // Read op
    //////////////////////////////////////////////////
    template <typename T> Buffer& operator>>(T& data)
    {
        data = read<T>();
        return *this;
    }
    
    Buffer& operator>>(std::string& data)
    {
        data = read();
        return *this;
    }

    template <typename T> T read()
    {
        BOOST_ASSERT((m_readCursor+sizeof(T)) <= m_rawBuffer.size());
        T ret = *(reinterpret_cast<T*>(&m_rawBuffer[m_readCursor]));
        m_readCursor+=sizeof(T);
		SwapByte::Swap<T>(ret);
		return ret;
    }
    
    /**
     * Read a native type from a position ignoring the real position of readCursor
     * This doesn't change the position of the read cursor.
     */
    template <typename T> T read(uint32 pos)
    {
        BOOST_ASSERT((pos+sizeof(T)) <= m_rawBuffer.size());
        T ret = *(reinterpret_cast<T*>(&m_rawBuffer[pos]));		
		SwapByte::Swap<T>(ret);
        return ret;
    }

    /**
     * Read Aoc string <uint16,size><string>
     */
    std::string read();

	void debugPrint();

	void debugPrint(uint32 offset);

    ///////////////////////////////////////////////////
    // Asio const buffer impl
    ///////////////////////////////////////////////////
    const std::vector<uint8>& constBuffer() const;
	std::vector<uint8>& mutBuffer();




private:

    std::vector<uint8> m_rawBuffer;
    uint32 m_writeCursor;
    uint32 m_readCursor;
    std::size_t m_size;
};


#endif /*BUFFER_H_*/
