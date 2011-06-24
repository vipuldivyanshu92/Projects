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

const std::vector<uint8>& Buffer::rawBuffer() const
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
