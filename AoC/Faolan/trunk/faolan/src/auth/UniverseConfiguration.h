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

#ifndef UNIVERSECONFIGURATION_H_
#define UNIVERSECONFIGURATION_H_


#include "../common/Singleton.h"
#include "../common/Common.h"

#include <boost/program_options.hpp>
#include <boost/thread.hpp>
#include <gmp.h>

/**
 * Universe server configuration manager
 * @author Albator
 */
class UniverseConfiguration : public Singleton<UniverseConfiguration>
{
	friend class Singleton<UniverseConfiguration>;

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

	std::string serverPrivateKey, clientKey, dhPrimeStr,dhBase;
	mpz_t serverPublicKey, clientPublicKey, dhPrimeNum, mpzdhBase, mpzserverPrivateKey;

	std::string logType, logFilename;

	/**
     * Return the char server adress/ use a round robin algorithm for load balancing in case
	 * of multiple char servers
	 * Thread safe
	 * @return <address>:<port>
	 */
	std::string getCharServerAddress();

	/**
	 * Add a char server to the list of connected char servers
	 * support many char servers for load balancing purpose
	 * Thread Safe
	 */
	void addCharServer(std::string charServerAddress);


    /**
     * Remove a registered char server from the global list.
     * Thread Safe
     */
	void removeCharServer(std::string charServerAddress);



private:

	UniverseConfiguration();

	boost::program_options::options_description m_description;
	boost::program_options::variables_map m_variableMap;

	boost::mutex m_mutex;
	uint32 m_addressCounter;
	std::vector<std::string> m_charServers;


};

#endif
