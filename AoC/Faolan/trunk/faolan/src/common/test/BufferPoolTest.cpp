#include <iostream>
#include "../BufferPool.h"
#include "../Buffer.h"

int main()
{

    std::cout << "BufferPool Test" << std::endl;
    std::cout << "---------------" << std::endl;
    
    
    // allocate 200 buffer of 200Bytes
    BufferPool bufPool(200,200);
    
    Buffer* buf1 = bufPool.allocateBuffer(20);
    Buffer* buf2 = bufPool.allocateBuffer(800);
    Buffer* buf3 = bufPool.allocateBuffer(95);
    
    std::cout << "Buffer1 size: " << buf1->capacity() << std::endl;
    std::cout << "Buffer2 size: " << buf2->capacity() << std::endl;
    std::cout << "Buffer3 size: " << buf3->capacity() << std::endl;
    
    bufPool.disposeBuffer(buf1);
    bufPool.disposeBuffer(buf2);
    bufPool.disposeBuffer(buf3);

    return 0;
}
