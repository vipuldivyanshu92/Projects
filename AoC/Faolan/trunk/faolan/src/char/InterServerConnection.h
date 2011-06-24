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

#include <boost/asio.hpp>
#include <boost/thread.hpp>
#include "../common/Buffer.h"


/**
 * Connection to the auth server to register the char server
 * @author Albator
 */
class InterServerConnection
{

public:

    InterServerConnection(boost::asio::io_service& IOService, const std::string& loginServerAddress, const std::string& port);



    /**
     * Main function of inter server communication process.
     * This has to be run inside a different thread.
     * This will run until a call to stop() or an error.
     */
    void run();

    /**
     * blocking function to wait the connection to the login server.
     */
    bool waitUntilConnected();

    /**
     * Stop the connection
     */
    void stop();

private:


    void onResolve(const boost::system::error_code& err,
                   boost::asio::ip::tcp::resolver::iterator endpoint_iterator);

    void onConnect(const boost::system::error_code& err,
                   boost::asio::ip::tcp::resolver::iterator endpoint_iterator);

    void onRead(const boost::system::error_code& e,
            std::size_t bytesTransferred);

    void onWrite(const boost::system::error_code& e);


	void AsyncRead();

	void AsyncWrite(Buffer& b);

	void AsyncWrite(Buffer& b, uint32 size);


	void onAuthStatus();

	void onRegistrationStatus();

	void Authentificate();

    boost::asio::io_service& m_IOService;
    boost::asio::ip::tcp::socket m_Socket;
    boost::asio::ip::tcp::resolver m_Resolver;
    Buffer m_readBuffer, m_writeBuffer;
    const std::string& m_loginServerAddress, m_port;
    bool m_connected, m_registered;

    // synchro
    mutable boost::mutex m_mutex;
    boost::condition m_condition;

};
