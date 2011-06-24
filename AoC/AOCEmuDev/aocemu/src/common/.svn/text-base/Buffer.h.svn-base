#ifndef BUFFER_H_
#define BUFFER_H_

#include <vector>
#include <memory>
#include <string>
#include <boost/assert.hpp>
#include <boost/asio.hpp>

#include "Common.h"

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

    template <typename T> void write(const T data)
    {
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
        return ret;
    }

    /**
     * Read Aoc string <uint16,size><string>
     */
    std::string read();

    ///////////////////////////////////////////////////
    // Asio const buffer impl
    ///////////////////////////////////////////////////
    const std::vector<uint8>& rawBuffer() const;

private:

    std::vector<uint8> m_rawBuffer;
    uint32 m_writeCursor;
    uint32 m_readCursor;
    std::size_t m_size;
};


#endif /*BUFFER_H_*/
