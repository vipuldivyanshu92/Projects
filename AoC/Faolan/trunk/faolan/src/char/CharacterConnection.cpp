#include "CharacterConnection.h"
#include "../common/BufferPool.h"
#include "../common/MysqlDatabase.h"
#include "../common/MysqlQuery.h"
#include "../common/Logger.h"
#include <iostream>
#include <boost/bind.hpp>
#include <boost/algorithm/string.hpp>





CharacterConnection::CharacterConnection(boost::asio::io_service& IOService, BufferPool* hp) : Connection(IOService,hp),
m_smallUserId(0),m_cookie(0)
{

}

void CharacterConnection::start()
{

	AsyncRead();

	Logger::log("New connection accepted\n");

}

void CharacterConnection::onRead(const boost::system::error_code &e, std::size_t bytesTransferred)
{

	// Read the incoming buffer and parse the packet
	if(!e && bytesTransferred >= 4)
	{
		uint32 pSize = 0;

		m_readBuffer >> pSize;
		if(pSize == (bytesTransferred-4)) // valid size
		{
			uint32 unknown1= 0,unknown2 = 0, playerID = 0,unknown3= 0,opcode = 0;
			std::string sender, receiver;
			m_readBuffer >> sender >> unknown1>> unknown2>> receiver>> playerID >> unknown3>> opcode;

			switch(opcode)
			{
			case 0x00:
				onAuthentification(); // check if the client is already logged
				break;

			case 0x06:
				onGetStartupData();
				break;
			default:
				Logger::log("Unknown opcode sent by the client : 0x%2x \n",opcode);
				return;

			}

			m_readBuffer.reset();
			AsyncRead();

			return;
		}

	}


	// error code goes here - disconnect
}



void CharacterConnection::onWrite(const boost::system::error_code &e)
{
	if (e)
	{
		Logger::log("socket write problem \n");
		boost::system::error_code ignored_ec;
		m_socket.shutdown(boost::asio::ip::tcp::socket::shutdown_both, ignored_ec);
	}

}

void inline CharacterConnection::writePacketHeader(Buffer* dest, uint32 size,uint32 opcode)
{
	uint32 uknown1=1;
	uint32 uknown2=0;
	static const std::string receiver("PlayerAgent");
	static const std::string sender("PlayerInterface");
	(*dest) << size << receiver << uknown1 << uknown2 << sender
		<< uknown2 << uknown2 << opcode;
}

void CharacterConnection::onAuthentification()
{

	m_readBuffer >> m_smallUserId >> m_cookie;

	uint32 size = PACKET_HEADER_SIZE+4;
	Buffer* b = m_bufferPool->allocateBuffer(size);
	writePacketHeader(b, size, 0x00);

	if(m_cookie == 0x62b53841) // if cookie valid
	{
		b->write<uint32>(0x00000001);
	}
	else
	{
		b->write<uint32>(0xffffffff);
	}

	AsyncWrite(b);
	m_bufferPool->disposeBuffer(b);
}

void CharacterConnection::onGetStartupData()
{
	m_readBuffer >> m_userID[0] >> m_userID[1];

	uint32 size = PACKET_HEADER_SIZE+12;
	Buffer* b = m_bufferPool->allocateBuffer(size);
	writePacketHeader(b,size,0x04);

	b->write(m_userID[1]);
	b->write<uint32>(0x000003f1); // base 10 : (nb_chars + 1) * 1009
	b->write<uint32>(0x00000008); // Number of Char Slots

	AsyncWrite(b);




	// now send realm list
	m_bufferPool->disposeBuffer(b);

	size=PACKET_HEADER_SIZE+60;
	b = m_bufferPool->allocateBuffer(size);

	writePacketHeader(b,size,0x05);
	b->write<uint32>(0x01);
	b->write<uint32>(1);
	b->write<uint32>(2);
	b->write<uint32>(8);
	b->write<uint32>(100000);
	(*b) << std::string("Atlantis");
	b->write<uint32>(0);
	b->write<uint32>(0);
	b->write<uint32>(0);
	b->write<uint32>(0);
	b->write<uint32>(0);
	b->write<uint32>(0);
	b->write<uint16>(1);
	b->write<uint32>(0);

	b->debugPrint(50);
	AsyncWrite(b);
	m_bufferPool->disposeBuffer(b);

	size = PACKET_HEADER_SIZE+12;
	b = m_bufferPool->allocateBuffer(size);
	writePacketHeader(b,size,0x08);
	b->write<uint32>(0x01);
	b->write<uint32>(m_userID[0]);
	b->write<uint32>(m_userID[1]);

	AsyncWrite(b);
	m_bufferPool->disposeBuffer(b);


}


CharacterConnection::~CharacterConnection()
{

}
