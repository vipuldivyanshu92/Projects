#include "FileLogger.h"
#include <boost/assert.hpp>

FileLogger::FileLogger(const std::string& fileName) :
    m_debugFile(fileName.c_str())
{

}

FileLogger::~FileLogger()
{

}

void FileLogger::write(const std::string& msg)
{

    BOOST_ASSERT(m_debugFile.is_open());

    m_debugFile << msg;
}

