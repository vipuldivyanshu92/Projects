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

#include "InterServerConnection.h"
#include "CharacterConfiguration.h"
#include "../common/Logger.h"

#include <boost/bind.hpp>



InterServerConnection::InterServerConnection(boost::asio::io_service& IOService,
        const std::string& loginServerAddress,  const std::string& port) :
        m_IOService(IOService),m_Socket(IOService),m_Resolver(IOService), m_readBuffer(1000), m_writeBuffer(1000),
        m_loginServerAddress(loginServerAddress), m_port(port), m_connected(false)
{


}

void InterServerConnection::run()
{

    boost::asio::ip::tcp::resolver::query query(m_loginServerAddress,m_port);

    m_Resolver.async_resolve(query,
                             boost::bind(&InterServerConnection::onResolve, this,
                                         boost::asio::placeholders::error,
                                         boost::asio::placeholders::iterator));

    m_IOService.run();
}

void InterServerConnection::onResolve(const boost::system::error_code& err,
                                      boost::asio::ip::tcp::resolver::iterator endpoint_iterator)
{
    if (!err)
    {
        // Attempt a connection to the first endpoint in the list. Each endpoint
        // will be tried until we successfully establish a connection.
        boost::asio::ip::tcp::endpoint endpoint = *endpoint_iterator;

        m_Socket.async_connect(endpoint,
                               boost::bind(&InterServerConnection::onConnect, this,
                                           boost::asio::placeholders::error, ++endpoint_iterator));

    }
    else
    {
        Logger::log("InterServerConnection error: %s\n",err.message().c_str());
        m_condition.notify_all();
    }
}

void InterServerConnection::onConnect(const boost::system::error_code& err,
                                      boost::asio::ip::tcp::resolver::iterator endpoint_iterator)
{

    if (!err)
    {
        Authentificate();
        AsyncRead();

    }
    else if (endpoint_iterator != boost::asio::ip::tcp::resolver::iterator())
    {
        // The connection failed. Try the next endpoint in the list.
        m_Socket.close();
        boost::asio::ip::tcp::endpoint endpoint = *endpoint_iterator;
        m_Socket.async_connect(endpoint,
                               boost::bind(&InterServerConnection::onConnect, this,
                                           boost::asio::placeholders::error, ++endpoint_iterator));
    }
    else
    {
        Logger::log("InterServerConnection error: %s\n",err.message().c_str());
        m_condition.notify_all();
    }

}

void InterServerConnection::Authentificate()
{
    std::string login = "charserver";
    std::string password = "charserver";
    // we are now connected, request authentification
    uint32 size = login.size() + password.size() + 12;
    uint32 opcode = 0x01;
    m_writeBuffer << size << opcode << login << password;

    AsyncWrite(m_writeBuffer);
    m_writeBuffer.reset();
}

void InterServerConnection::onRead(const boost::system::error_code& e,
                                   std::size_t bytesTransferred)
{
    // Read the incoming buffer and parse the packet
    if (!e && bytesTransferred >= 8)
    {
        uint32 pSize = 0;

        m_readBuffer >> pSize;
        if (pSize == bytesTransferred) // valid size
        {

            uint32 opcode = 0;
            m_readBuffer >> opcode;

            switch (opcode)
            {
            case 0x01:
                onAuthStatus();
                break;
            case 0x02:
                onRegistrationStatus();
                break;
            default:
                Logger::log("Unknown opcode sent auth server : 0x%2x \n",opcode);
                return;
            }

            m_readBuffer.reset();
            AsyncRead();

            return;
        }

    }


    // error code goes here - disconnect
    m_condition.notify_all();

}

void InterServerConnection::onWrite(const boost::system::error_code &e)
{
    if (e)
    {
        std::cout << "writeerror" << std::endl;
        Logger::log("InterServerCommunication: socket write problem \n");
        boost::system::error_code ignored_ec;
        m_Socket.shutdown(boost::asio::ip::tcp::socket::shutdown_both, ignored_ec);
    }
}


bool InterServerConnection::waitUntilConnected()
{
    boost::mutex::scoped_lock lock(m_mutex);
    m_condition.wait(lock);
    return (m_connected & m_registered);
}


void InterServerConnection::onAuthStatus()
{
    uint8 connected;
    m_readBuffer >> connected;

    if (connected == 0x01)
    {
        m_connected = true;

        // we are now connected, request authentification
        uint32 size = CharacterConfiguration::instance().listenPublicAddress.size() + 12 +  CharacterConfiguration::instance().listenPublicPort.size();
        uint32 opcode = 0x02;
        m_writeBuffer << size << opcode << CharacterConfiguration::instance().listenPublicAddress
        << CharacterConfiguration::instance().listenPublicPort;

        AsyncWrite(m_writeBuffer);
        m_writeBuffer.reset();

    }
    else
    {
        m_connected = false;
        m_condition.notify_all();
    }

}

void InterServerConnection::onRegistrationStatus()
{
    uint8 registered;
    m_readBuffer >> registered;

    if (registered == 0x01)
    {
        m_registered = true;
    }
    else
    {
        m_registered = false;
    }


    m_condition.notify_all();

}

void InterServerConnection::AsyncRead()
{
    m_readBuffer.reset();

    m_Socket.async_read_some(boost::asio::buffer(m_readBuffer.mutBuffer()),
                             boost::bind(&InterServerConnection::onRead, this,
                                         boost::asio::placeholders::error,
                                         boost::asio::placeholders::bytes_transferred));
}

void InterServerConnection::AsyncWrite(Buffer& b)
{
    boost::asio::async_write(m_Socket, boost::asio::buffer(b.constBuffer(), b.size()),
                             boost::bind(&InterServerConnection::onWrite, this,
                                         boost::asio::placeholders::error));
}

void InterServerConnection::AsyncWrite(Buffer& b, uint32 size)
{
    boost::asio::async_write(m_Socket, boost::asio::buffer(b.constBuffer(),size),
                             boost::bind(&InterServerConnection::onWrite, this,
                                         boost::asio::placeholders::error));
}

void InterServerConnection::stop()
{
    m_Socket.close();
    m_IOService.stop();
}





