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

#include "UniverseConnection.h"
#include "UniverseConfiguration.h"
#include "../common/BufferPool.h"
#include "../common/AoCCrypto.h"
#include "../common/MysqlDatabase.h"
#include "../common/MysqlQuery.h"
#include "../common/Logger.h"
#include <iostream>
#include <boost/bind.hpp>
#include <boost/algorithm/string.hpp>
#include <gmpxx.h>

uint32 UniverseConnection::connectionCount = 0;


//unknown packet 0x05, raw packet until we figure out what does it contain
uint8 rawPacket[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x3f, 0x80, 0x00,0x00,
0x3f, 0x80, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x08 };




UniverseConnection::UniverseConnection(boost::asio::io_service& IOService, BufferPool* hp) : Connection(IOService,hp), m_gmpRand(gmp_randinit_default),
m_registered(false), m_state(UniverseConnection::WAITING_INITIATE_AUTH)
{
	m_gmpRand.seed(connectionCount);
	m_serverHash = m_gmpRand.get_z_bits(16*8);
	mpz_init(m_commonKey);
}

void UniverseConnection::start()
{

	AsyncRead();

	m_connectionID = connectionCount;

	Logger::log("New connection accepted ID: %d \n",m_connectionID);
	connectionCount++;

}

void UniverseConnection::onRead(const boost::system::error_code &e, std::size_t bytesTransferred)
{

	// Read the incoming buffer and parse the packet
	if(!e && bytesTransferred >= 4)
	{
		uint32 pSize = 0;

		m_readBuffer >> pSize;
		if(pSize == (bytesTransferred-4)) // valid size
		{
			uint32 unknown1= 0,unknown2 = 0,unknown3= 0,unknown4= 0,opcode = 0;
			std::string sender, receiver;
			m_readBuffer >> sender >> unknown1>> unknown2>> receiver>> unknown3>> unknown4>> opcode;

			switch(opcode)
			{
			case 0x00: // initiate authentification
				onInitiateAuthentification();
				break;
			case 0x01: // Answer challenge
				onAnswerChallenge();
				break;
			case 0x02: // Request Universe Manager
				onRequestUniverseManager();
				break;
			default:   // Unknown opcode
				Logger::log("Unknown opcode sent by the client : 0x%2x \n",opcode);
				return;

			}

			m_readBuffer.reset();
			AsyncRead();

			return;
		}

		Logger::log("Incorrect packet size \n");

	}

	Logger::log("Client disconnected (client:%d)\n",m_connectionID);
	// error code goes here - disconnect
}

void UniverseConnection::onWrite(const boost::system::error_code &e)
{
	if (e)
	{
		Logger::log("socket write problem \n");
		boost::system::error_code ignored_ec;
		m_socket.shutdown(boost::asio::ip::tcp::socket::shutdown_both, ignored_ec);
	}

}

void UniverseConnection::onInitiateAuthentification()
{

	if(m_state!=UniverseConnection::WAITING_INITIATE_AUTH)
	{
		disconnect();
	}

	// is there anything interesting to do with the data of this packet?!
	std::string username;
	uint16 unk;
	m_readBuffer >> unk >> username;

	// Send the server hash
	uint32 size = PACKET_HEADER_SIZE+2+32;
	Buffer* b = m_bufferPool->allocateBuffer(size);
	writePacketHeader(b,size,0x00);

	(*b) << m_serverHash.get_str(16);

	AsyncWrite(b);

	m_state = UniverseConnection::INITIATE_AUTH;
	m_bufferPool->disposeBuffer(b);



}



void UniverseConnection::checkLogin(Query* q)
{

	if(q->fetchRow()) // registered user
	{

		m_registered=true;
		m_userID = q->getUint64();
		Logger::log("%s sucessfully login (ID:%d) \n",m_username.c_str(),m_userID);
	}
	else // unregistered user
	{
		Logger::log("Fail to login with username: %s \n",m_username.c_str());
	}
}

void UniverseConnection::onAnswerChallenge()
{

	if(m_state!=UniverseConnection::INITIATE_AUTH)
	{
		disconnect();
	}

	std::string cryptedString;

	m_readBuffer >> cryptedString;

	std::vector<std::string> tok;
	boost::algorithm::split(tok,cryptedString,boost::is_any_of("-"));

	if(tok.size() != 2)
	{
		Logger::log("Error on packet formatting answerChallenge\n");
		return; // packet formatting is wrong
	}

	mpz_t publicClientKey;
	mpz_init_set_str(publicClientKey,tok[0].c_str(),16);

	char *publicClientKey_s=NULL;
	publicClientKey_s = mpz_get_str(publicClientKey_s, 16, publicClientKey);
	Logger::log("public Client Key : %s\n", publicClientKey_s);

	mpz_powm(m_commonKey,publicClientKey,UniverseConfiguration::instance().mpzserverPrivateKey,UniverseConfiguration::instance().dhPrimeNum);
	char *common_key_s=NULL;
	common_key_s = mpz_get_str(common_key_s, 16, m_commonKey);
	Logger::log("Common Key : %s\n", common_key_s);


	Logger::log("Encrypted Message : %s", tok[1].c_str());

	std::string decrypt;
	AoCCrypto::AoCDecrypt(decrypt,tok[1],common_key_s);

	if(decrypt.size() >= 32)
	{

		uint16 loginDataSize = *(reinterpret_cast<uint16*>(&decrypt[10]));
		SwapByte::Swap<uint16>(loginDataSize);


		if(loginDataSize <= (decrypt.size() - 12))
		{
			// parse the username, hash and pass
			std::string loginData = decrypt.substr(12,12+loginDataSize);

			std::vector<std::string> loginTokens;
			boost::algorithm::split(loginTokens,loginData,boost::is_any_of("|"));

			if(loginTokens.size() == 3)
			{
				if(loginTokens[1] == m_serverHash.get_str(16)) // check the server hash
				{
					m_username = loginTokens[0];
					//now check in the DB
					MysqlDatabase* db = MysqlDatabase::instance();
					MysqlQuery* q = new MysqlQuery(MysqlQuery::SYNCHRONOUS,MysqlQuery::HAS_RESULT);
					q->setCallbackFunction(boost::bind(&UniverseConnection::checkLogin, this, q ));
					q->setQueryText("SELECT account_id,username, password FROM accounts WHERE username='%s' AND password='%s'",m_username.c_str(),loginTokens[2].c_str());
					db->executeSynchronousQuery(q);
					delete q;
					if(m_registered) // send the OK packet
					{

						// send a first unknown packet
						uint32 size = PACKET_HEADER_SIZE+31;
						Buffer* b = m_bufferPool->allocateBuffer(size);
						writePacketHeader(b,size,0x05);
						b->write(rawPacket, 31);

						AsyncWrite(b);


						b->reset();
						// send ack packet + char server address
						std::string charServerAddress = UniverseConfiguration::instance().getCharServerAddress();

						size = PACKET_HEADER_SIZE+charServerAddress.size()+2+20;
						writePacketHeader(b,size,0x01);
						b->write<uint32>(0x01); // auth status
						(*b) << m_userID << charServerAddress; // userid + char server address
						b->write<uint32>(0x62b53841); // cookie
						b->write<uint32>(0x00); // reason

						AsyncWrite(b);

						m_bufferPool->disposeBuffer(b);

					}
					else
					{
						uint32 size = PACKET_HEADER_SIZE+22;
						Buffer* b = m_bufferPool->allocateBuffer(size);
						writePacketHeader(b,size,0x01);
						b->write<uint32>(0xffffffff);
						b->write<uint32>(0x00);
						b->write<uint32>(0x00);
						b->write<uint32>(0x00);
						b->write<uint32>(0x00);
						b->write<uint16>(0x01);

						AsyncWrite(b);
						m_bufferPool->disposeBuffer(b);

					}

				}
				else
				{
					Logger::log("invalid server hash sent by the client \n");
				}
			}
			else
			{
				Logger::log("invalid number of token in the login data sent by the client \n");
				return;
			}

		}
		else
		{
			Logger::log("Incorrect packet size (Answerchallenge 1)\n");
			return;
		}


	}
	else
	{
		Logger::log("Incorrect packet size (Answerchallenge 2)\n");
		return;
	}


}

void UniverseConnection::onRequestUniverseManager() // deprecated
{


	// set universe manager
	std::ostringstream os;
	os << UniverseConfiguration::instance().listenAddress
		<< UniverseConfiguration::instance().listenPort;


	uint32 size = UniverseConnection::PACKET_HEADER_SIZE+2+os.str().size();
	Buffer* b = m_bufferPool->allocateBuffer(size);
	writePacketHeader(b,size,0x03);

	(*b) << os.str();

	AsyncWrite(b);

	m_bufferPool->disposeBuffer(b);

}

void inline UniverseConnection::writePacketHeader(Buffer* dest, uint32 size,uint32 opcode)
{
	uint32 uknown1=1;
	uint32 uknown2=0;
	static const std::string receiver("UniverseAgent");
	static const std::string sender("UniverseInterface");

	(*dest) << size << receiver << uknown1 << uknown2 <<
		sender << m_connectionID << uknown2 << opcode;
}


UniverseConnection::~UniverseConnection()
{

}

