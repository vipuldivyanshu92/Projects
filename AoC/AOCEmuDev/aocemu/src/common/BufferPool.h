#ifndef BUFFERPOOL_H_
#define BUFFERPOOL_H_

#include "Buffer.h"
#include <stack>
#include <boost/foreach.hpp>

/**
 * BufferPool class to read and write data on raw buffer.
 * @author Albator
 * 
 */
class BufferPool {

public:

    BufferPool(int chunkNumber, std::size_t chunkSize);

    /**
     * Request a buffer from the pool.
     * This system avoid memory allocation for each packets created and focus on memory reuse
     * These buffers have to be manually released by releaseBuffer.
     * @param size size of the requested buffer in byte.
     */
    Buffer* allocateBuffer(std::size_t size);

    /**
     * release a previously requested buffer.
     * This method signal to BufferPool that the space allocated in previously is free again.
     * The buffer cursors are reseted.
     * @param buffer the allocated space to release
     */
    void disposeBuffer(Buffer* buf);
    
    /**
     * Delete all buffer in the pool for clean shutdown.
     */
    ~BufferPool();

private:
    std::stack<Buffer*> bufferStack;

};

//////////////////////////////////////////////////////////////////
//
// Buffer Pool class definition
//
/////////////////////////////////////////////////////////////////
BufferPool::BufferPool(int chunkNumber, std::size_t chunkSize) : bufferStack()
{
    for(int i=0; i< chunkNumber; i++){
        bufferStack.push(new Buffer(chunkSize));
    }
}

Buffer* BufferPool::allocateBuffer(std::size_t size)
{
    if (bufferStack.size()==0) // no more buffer available in the pool
    {
        return new Buffer(size);
    } else
    {
        Buffer* buf = bufferStack.top();
        if (buf->capacity() < size)
        {
           buf->resize(size);  
        }
        
        bufferStack.pop();
        return buf;
    }
}

void BufferPool::disposeBuffer(Buffer* buf)
{
    buf->reset();
    bufferStack.push(buf);
}


BufferPool::~BufferPool()
{
    BOOST_FOREACH(Buffer* b, bufferStack)
    {
        delete b;
    }
}

#endif /*BUFFERPOOL_H_*/

