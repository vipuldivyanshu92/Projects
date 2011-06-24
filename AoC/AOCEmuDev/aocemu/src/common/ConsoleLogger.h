#ifndef CONSOLELOGGER_H_
#define CONSOLELOGGER_H_

#include <string>
#include "Logger.h"

class ConsoleLogger : public Logger {
private:
    virtual void write(const std::string& msg);
};

#endif /*CONSOLELOGGER_H_*/
