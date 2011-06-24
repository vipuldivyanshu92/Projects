/*
Faolan Project, a free Age of Conan server emulator made for educational purpose
Copyright (C) 2008 Project Faolan team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

#include <boost/assert.hpp>
#include <stdio.h>
#include <stdarg.h>

#include "Logger.h"

Logger* Logger::m_loggerInstance= NULL;

void Logger::setLogger(Logger* logger)
{
    destroy();
    m_loggerInstance = logger;
}

void Logger::destroy()
{
    if(m_loggerInstance!=NULL)
	{
		delete m_loggerInstance;
		m_loggerInstance = NULL;
	}

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

