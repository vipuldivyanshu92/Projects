#ifndef LOGGER_H_
#define LOGGER_H_

#include <string>
#include <sstream>

class Logger {

public:

    /**
     * Change logger instance by a new one
     * @param logger logger instance
     */
    static void setLogger(Logger* logger);

    /**
     * C style message logging
     */
    static void log(const char* format, ...);

    /**
     * C++ style message logging
     */
    static Logger& log();
    template<class T> Logger& operator <<(const T& message);

    /**
     * Destructor
     */
    virtual ~Logger();

private:

    /**
     * pure virtual method to overload on each logger
     */
    virtual void write(const std::string& msg)=0;

    /**
     * Destroy the current logger instance
     */
    static void destroy();

    static Logger* m_loggerInstance;

};

template <class T> Logger& Logger::operator <<(const T& message)
{
    std::ostringstream stream;
    stream << message;
    write(stream.str());

    return log();
}

#endif /*LOGGER_H_*/
