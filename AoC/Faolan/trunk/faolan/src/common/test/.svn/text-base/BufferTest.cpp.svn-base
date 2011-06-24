#include "../Buffer.h"
#include "../Common.h"
#include <iostream>
#include <boost/asio.hpp>

int main()
{
    
    std::cout << "Buffer test read/write" << std::endl;
    std::cout << "----------------------" << std::endl;
    Buffer buf(80);
    
    uint32 a = 15;
    uint64 b = 12;
    uint16 c = 47;

    buf << a << b << c << std::string("my string");

    uint32 d;
    uint64 e;
    uint16 f;
    std::string x;
    
    buf >> d >> e >> f >> x;
    std::cout << "Results should be 15-12-47-my string" << std::endl;
    std::cout << d << "-" << e << "-" << f << "-" << x << std::endl;
    
    
    std::cout << "Buffer test boost::asio" << std::endl;
   
    
    boost::asio::const_buffers_1 test = boost::asio::buffer(buf.rawBuffer(), buf.size());
    
    return 0;
}
