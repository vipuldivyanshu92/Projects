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

#ifndef CHARACTERCONNECTION_H_
#define CHARACTERCONNECTION_H_


#include <boost/enable_shared_from_this.hpp>
#include "../common/Connection.h"
#include "../common/PacketParser.h"
#include "../common/Query.h"


class CharacterConnection : public Connection, public boost::enable_shared_from_this<CharacterConnection>
{
public:

	CharacterConnection(boost::asio::io_service& IOService, BufferPool* hp);

	void start();

	~CharacterConnection();

	
private:


	enum State {
	};

	
	void onRead(const boost::system::error_code& e,
            std::size_t bytesTransferred);
    
    void onWrite(const boost::system::error_code& e);
	
	void writePacketHeader(Buffer* dest, uint32 size, uint32 opcode);

	void onAuthentification();

	void onGetStartupData();


	
	uint32 m_userID[2];
	uint32 m_smallUserId, m_cookie;
	State m_state;
		
	// Static var
	static const uint32 PACKET_HEADER_SIZE = 50; // header size - 4, because the size in the packet is the overall packet size - 4
	

};

#endif