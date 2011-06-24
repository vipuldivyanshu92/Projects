#include "../Packet.h"
#include "../PacketParser.h"
#include <iostream>

int main()
{

    std::cout << "Packet tests" << std::endl;
    std::cout << "------------" << std::endl;

    const std::string sender("Sender");
    const std::string receiver("Receiver");

    Buffer *buf = new Buffer(300);
    Packet *p = new Packet(200, sender, 1, 2, receiver, 3, 4, 5, buf);

    std::cout << "send packet" << std::endl;
    std::cout << "sender: " << p->sender() << " receiver: " << p->receiver()
            << " opcode: " << p->opcode() << std::endl;

    buf->reset(); // reset packet to consider it as new packet coming
    
    Packet *p2 = new Packet(buf);

    std::cout << "receive packet" << std::endl;
    std::cout << "sender: " << p2->sender() << " receiver: " << p2->receiver()
            << " opcode: " << p2->opcode() << std::endl;
    delete p;
    delete p2;
    delete buf;

    return 0;
}
