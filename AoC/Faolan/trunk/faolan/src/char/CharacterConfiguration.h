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

#ifndef CHARACTERCONFIGURATION_H_INCLUDED
#define CHARACTERCONFIGURATION_H_INCLUDED

#include "../common/Singleton.h"
#include "../common/Common.h"

#include <boost/program_options.hpp>
#include <boost/thread.hpp>

/**
 * Character server configuration manager
 * @author Albator
 */
class CharacterConfiguration : public Singleton<CharacterConfiguration>
{
	friend class Singleton<CharacterConfiguration>;

public:


	void parseCommandLine(int argc, char* argv[]);

	void parseConfigFile();

	void printConfiguration();

	void generateFinalOptions();

	////////////////////////////////////////////////////////
	// Public configuration data
	//
	///////////////////////////////////////////////////////

	std::string listenAddress, configFile, listenPort;
	std::string listenInterAddress, listenInterPort;
	uint32 demuxerCount;

	std::string DBUsername, DBPassword, DBName, DBHost;
	uint32 DBPort,DBConnectionCount;

	std::string logType, logFilename;

    std::string listenPublicAddress, listenPublicPort;

    std::string authServerAddress, authServerPort;



private:

	CharacterConfiguration();

	boost::program_options::options_description m_description;
	boost::program_options::variables_map m_variableMap;

	boost::mutex m_mutex;


};

#endif // CHARACTERCONFIGURATION_H_INCLUDED
