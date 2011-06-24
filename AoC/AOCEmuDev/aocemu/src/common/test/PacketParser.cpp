#include <iostream>
#include "../PacketParser.h"
#include "../Packet.h"
#include "../Common.h"
#include "../SafeQueue.h"

class TestPacket : public Packet {
public:
    TestPacket(uint32 size, const std::string& sender, uint32 unknown1,
            uint32 unknown2, const std::string& receiver, uint32 unknown3,
            uint32 unknown4, uint32 opcode, Buffer* buf) :
        Packet(size, sender, unknown1, unknown2, receiver, unknown3, unknown4,
                opcode, buf)
    {

    }
    
    TestPacket(Buffer *buf) : Packet(buf)
    {
        
    }

};




class CallbackObject {
public:
    CallbackObject() :
        m_parser(this)
    {
        
    }

    void onPacket(const TestPacket& p)
    {
        std::cout << "Handle new packet!" << std::endl;
    }

    
    void testParse(Buffer* buf)
    {
        m_parser.AOCParse(buf,42);
    }
    ~CallbackObject()
    {

    }
private:
    PacketParser<CallbackObject> m_parser;

};


// Register packet in the parser.
REGISTER_PACKET_HANDLER(TestPacket ,5, CallbackObject);


int main()
{

    
    //TestPacketFactory<CallbackObject> tpf;
    const std::string sender("Sender");
    const std::string receiver("Receiver");

    Buffer *buf = new Buffer(300);
    Packet *p = new TestPacket(42, sender, 1, 2, receiver, 3, 4, 5 , buf);

    std::cout << "send packet" << std::endl;
    std::cout << "===========" << std::endl;
    std::cout << "sender: " << p->sender() << " receiver: " << p->receiver()
            << " opcode: " << p->opcode() << " size:" << p->size() << std::endl;

    buf->reset();
    ///////////////////////////////////
    // Packet Parser
    CallbackObject* obj = new CallbackObject();
    obj->testParse(buf);

    delete obj;
    delete p;
    delete buf;

    return 0;
}
