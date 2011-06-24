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

#ifndef CONNECTION_H_
#define CONNECTION_H_

#include "Common.h"
#include <boost/asio.hpp>
#include <boost/noncopyable.hpp>
#include <boost/enable_shared_from_this.hpp>


#include "BufferPool.h"



/**
 * Abstract connection class
 * @author Albator, Doron
 */
class Connection : private boost::noncopyable,  public boost::enable_shared_from_this<Connection>
{
public:
    
    Connection(boost::asio::io_service& IOService, BufferPool* bp);
    
    boost::asio::ip::tcp::socket& socket();
    
    /**
     * First operation executed after establishing a connection
     */
    virtual void start() = 0;
protected:
    
    virtual void onRead(const boost::system::error_code& e,
            std::size_t bytesTransferred) = 0;
    
    virtual void onWrite(const boost::system::error_code& e) = 0;
    
    void disconnect();

	void AsyncRead();

	void AsyncWrite(Buffer* b);

	void AsyncWrite(Buffer* b, uint32 size);
	
	boost::asio::ip::tcp::socket m_socket;
	BufferPool* m_bufferPool;
	Buffer m_readBuffer;
	uint32 m_connectionID;


    
};


#endif /*CONNECTION_H_*/
