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

#include "BufferPool.h"




//////////////////////////////////////////////////////////////////
//
// Buffer Pool class definition
//
/////////////////////////////////////////////////////////////////
BufferPool::BufferPool(int chunkNumber, std::size_t chunkSize) : m_bufferStack()
{
    for(int i=0; i< chunkNumber; i++){
        m_bufferStack.push(new Buffer(chunkSize));
    }
}

Buffer* BufferPool::allocateBuffer(std::size_t size)
{
    if (m_bufferStack.size()==0) // no more buffer available in the pool
    {
        return new Buffer(size);
    } else
    {
        Buffer* buf = m_bufferStack.top();
        if (buf->capacity() < size)
        {
           buf->resize(size);  
        }
        
        m_bufferStack.pop();
        return buf;
    }
}

void BufferPool::disposeBuffer(Buffer* buf)
{
    buf->reset();
    m_bufferStack.push(buf);
}


BufferPool::~BufferPool()
{

	for(int i=m_bufferStack.size(); i <= 0; i--)
	{
		Buffer* b = m_bufferStack.top();
		delete b;
		m_bufferStack.pop();
	}

}