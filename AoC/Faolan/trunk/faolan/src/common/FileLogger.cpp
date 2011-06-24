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

#include "FileLogger.h"
#include <boost/assert.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>


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

	m_debugFile << "[" <<  boost::posix_time::to_simple_string(boost::posix_time::second_clock::local_time()) << "] " << msg;
	m_debugFile.flush();
}


