#include <boost/assert.hpp>
#include "Logger.h"

Logger* Logger::m_loggerInstance= NULL;

void Logger::setLogger(Logger* logger)
{
    destroy();
    m_loggerInstance = logger;
}

void Logger::destroy()
{
    delete m_loggerInstance;
    m_loggerInstance = NULL;
}

void Logger::log(const char* Format, ...)
{
    BOOST_ASSERT(m_loggerInstance != NULL);

    char sBuffer[512];
    va_list Params;
    va_start(Params, Format);
    vsprintf(sBuffer, Format, Params);
    va_end(Params);

    m_loggerInstance->write(sBuffer);
}

Logger& Logger::log()
{
    return *m_loggerInstance;
}

Logger::~Logger()
{
}

