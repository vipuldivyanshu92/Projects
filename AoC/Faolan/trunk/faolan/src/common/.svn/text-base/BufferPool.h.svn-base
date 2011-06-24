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
    std::stack<Buffer*> m_bufferStack;

};



#endif /*BUFFERPOOL_H_*/

