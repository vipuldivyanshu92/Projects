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

#include "Connection.h"
#include <boost/bind.hpp>
#include <boost/asio.hpp>

Connection::Connection(boost::asio::io_service& IOService, BufferPool* bp) : m_socket(IOService), m_bufferPool(bp), m_readBuffer(2000)
{
    
}

boost::asio::ip::tcp::socket& Connection::socket()
{
    return m_socket;
}

void Connection::disconnect()
{
	m_socket.shutdown(boost::asio::socket_base::shutdown_both);
}

void Connection::AsyncRead()
{
	m_readBuffer.reset();

	m_socket.async_read_some(boost::asio::buffer(m_readBuffer.mutBuffer()),
				boost::bind(&Connection::onRead, shared_from_this(),
				boost::asio::placeholders::error,
				boost::asio::placeholders::bytes_transferred));
}

void Connection::AsyncWrite(Buffer* b)
{
	boost::asio::async_write(m_socket, boost::asio::buffer(b->constBuffer(), b->size()),
		boost::bind(&Connection::onWrite, shared_from_this(),
            boost::asio::placeholders::error));
}

void Connection::AsyncWrite(Buffer* b, uint32 size)
{
	boost::asio::async_write(m_socket, boost::asio::buffer(b->constBuffer(),size),
		boost::bind(&Connection::onWrite, shared_from_this(),
            boost::asio::placeholders::error));
}