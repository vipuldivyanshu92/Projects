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


#include "InterConnection.h"
#include "UniverseConfiguration.h"
#include "../common/BufferPool.h"
#include "../common/MysqlDatabase.h"
#include "../common/MysqlQuery.h"
#include "../common/Logger.h"
#include <iostream>
#include <sstream>
#include <boost/bind.hpp>






InterConnection::InterConnection(boost::asio::io_service& IOService, BufferPool* hp) : Connection(IOService,hp),m_charServerRegistered(false)
{}

void InterConnection::start()
{

    AsyncRead();
    Logger::log("New connection from char server\n");
}

void InterConnection::onRead(const boost::system::error_code &e, std::size_t bytesTransferred)
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
                onRequestAuth();
                break;
            case 0x02:
                onRegisterCharServer();
                break;
            default:
                Logger::log("Unknown opcode %d\n",opcode);
                return;
            }

            m_readBuffer.reset();
            AsyncRead();

            return;
        }

        Logger::log("Incorrect packet size \n");

    }

    Logger::log("Char server disconnected (client:%d)\n",m_connectionID);
    // error code goes here - disconnect
}

void InterConnection::onWrite(const boost::system::error_code &e)
{
    if (e)
    {
        Logger::log("socket write problem \n");
        boost::system::error_code ignored_ec;
        m_socket.shutdown(boost::asio::ip::tcp::socket::shutdown_both, ignored_ec);
    }

}

void InterConnection::onRequestAuth()
{

    m_readBuffer >> m_username >> m_password;

    MysqlDatabase* db = MysqlDatabase::instance();
    MysqlQuery* q = new MysqlQuery(MysqlQuery::SYNCHRONOUS,MysqlQuery::HAS_RESULT);
    q->setCallbackFunction(boost::bind(&InterConnection::checkLogin, this, q ));
    q->setQueryText("SELECT account_id FROM Accounts WHERE username='%s' AND password='%s'",m_username.c_str(),m_password.c_str());
    db->executeSynchronousQuery(q);
    delete q;

    Buffer* b = m_bufferPool->allocateBuffer(1000);
    b->write<uint32>(9);
    b->write<uint32>(0x01);

    if (m_registered)
    {
        b->write<uint8>(0x01);
    }
    else
    {
        b->write<uint8>(0x00);
    }

    AsyncWrite(b);
    m_bufferPool->disposeBuffer(b);


}



void InterConnection::checkLogin(Query* q)
{

    if (q->fetchRow()) // registered char server
    {

        m_registered=true;
        m_userID = q->getUint64();
        Logger::log("Char server sucessfully login (ID:%d) \n",m_userID);
    }
    else // unregistered user
    {
        Logger::log("Fail to login with username: %s \n",m_username.c_str());
    }
}


void InterConnection::onRegisterCharServer()
{

    if (m_registered)
    {
        m_readBuffer >> m_charServerPublicIP >> m_charServerPort;

        std::ostringstream os;
        os << m_charServerPublicIP << ":" << m_charServerPort;
        m_completeCharServerAddress = os.str();

        UniverseConfiguration::instance().addCharServer(m_completeCharServerAddress);

        m_charServerRegistered = true;

        Buffer* b = m_bufferPool->allocateBuffer(1000);
        b->write<uint32>(9); //size
        b->write<uint32>(0x02);

        if (m_registered)
        {
            b->write<uint8>(0x01);
        }
        else
        {
            b->write<uint8>(0x00);
        }

        AsyncWrite(b);
        m_bufferPool->disposeBuffer(b);
    }
    else
    {
        disconnect();
    }
}



InterConnection::~InterConnection()
{
    // remove char server from list.
    if (m_charServerRegistered)
    {
        UniverseConfiguration::instance().removeCharServer(m_completeCharServerAddress);
    }
}

