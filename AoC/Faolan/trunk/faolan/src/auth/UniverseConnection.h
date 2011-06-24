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

#ifndef UNIVERSECONNECTION_H_
#define UNIVERSECONNECTION_H_

#include <boost/enable_shared_from_this.hpp>
#include "../common/Connection.h"
#include "../common/Query.h"

#include <gmpxx.h>


class UniverseConnection : public Connection
{
public:

	UniverseConnection(boost::asio::io_service& IOService, BufferPool* hp);

	void start();

	~UniverseConnection();


private:


	enum State {
		WAITING_INITIATE_AUTH,
		INITIATE_AUTH,
		ANSWER_CHALLENGE
	};

	void onRead(const boost::system::error_code& e,
            std::size_t bytesTransferred);

    void onWrite(const boost::system::error_code& e);

	void onInitiateAuthentification();

	void onAnswerChallenge();

	void onRequestUniverseManager();

	void writePacketHeader(Buffer* dest, uint32 size, uint32 opcode);

	void checkLogin(Query* q);


	// Big number - gmp
	mpz_class m_serverHash;
	gmp_randclass m_gmpRand;
	mpz_t m_commonKey;


	std::string m_username,m_password,m_hash;
	uint64 m_userID;

	bool m_registered;

	State m_state;


	// Static var
	static uint32 connectionCount;
	static const uint32 PACKET_HEADER_SIZE = 54; // header size - 4, because the size in the packet is the overall packet size - 4


};

#endif
