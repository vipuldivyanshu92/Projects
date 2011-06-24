#include "../Logger.h"
#include "../ConsoleLogger.h"
#include "../FileLogger.h"


int main()
{
    Logger::setLogger(new ConsoleLogger());
    Logger::log() << "A c++ style console log " << "O.o" << 17;
    Logger::log("A C style log %d %d %d", 1,2,3);
    
    Logger::setLogger(new FileLogger());
    Logger::log() << "A c++ style console log " << "O.o" << 17;
    Logger::log("A C style log %d %d %d", 1,2,3);
    
    return 0;
}
