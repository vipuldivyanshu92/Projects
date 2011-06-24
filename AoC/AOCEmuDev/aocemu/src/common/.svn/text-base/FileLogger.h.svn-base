#ifndef FILELOGGER_H_
#define FILELOGGER_H_

#include <string>
#include <fstream>
#include "Logger.h"

class FileLogger : public Logger {
public:

    FileLogger(const std::string& filemane = "aocemu.log");

private:
    ~FileLogger();

    virtual void write(const std::string& msg);

    std::ofstream m_debugFile;
};

#endif /*FILELOGGER_H_*/
