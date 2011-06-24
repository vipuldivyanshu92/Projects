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

#ifndef INTERCONNECTION_H_
#define INTERCONNECTION_H_

#include "../common/Connection.h"
#include "../common/Query.h"

class InterConnection : public Connection
{
public:

	InterConnection(boost::asio::io_service& IOService, BufferPool* hp);

	void start();

	~InterConnection();


private:



	void onRead(const boost::system::error_code& e,
            std::size_t bytesTransferred);

    void onWrite(const boost::system::error_code& e);

	void onRequestAuth();

	void onRegisterCharServer();

	void checkLogin(Query* q);


    uint64 m_userID;

	std::string m_username,m_password, m_charServerPublicIP, m_completeCharServerAddress;
	std::string m_charServerPort;
	bool m_registered, m_charServerRegistered;

};

#endif
