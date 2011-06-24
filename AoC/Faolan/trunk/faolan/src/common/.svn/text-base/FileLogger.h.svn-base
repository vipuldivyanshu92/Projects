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
