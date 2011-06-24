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

#include "../common/Network.h"
#include "UniverseConnection.h"
#include "InterConnection.h"
#include <boost/bind.hpp>
#include <boost/function.hpp>
#include <boost/thread.hpp>

#include "UniverseConfiguration.h"
#include "InterConnection.h"
#include "../common/MysqlDatabase.h"
#include "../common/MysqlQuery.h"
#include "../common/Logger.h"
#include "../common/ConsoleLogger.h"
#include "../common/FileLogger.h"



boost::function0<void> console_ctrl_function;

BOOL WINAPI console_ctrl_handler(DWORD ctrl_type)
{
	switch (ctrl_type)
	{
	case CTRL_C_EVENT:
	case CTRL_BREAK_EVENT:
	case CTRL_CLOSE_EVENT:
	case CTRL_SHUTDOWN_EVENT:
		console_ctrl_function();
		return TRUE;
	default:
		return FALSE;
	}
}



int main(int argc, char* argv[])
{
	try
	{
		// Parse config
		UniverseConfiguration::instance().parseCommandLine(argc,argv);
		UniverseConfiguration::instance().parseConfigFile();
		UniverseConfiguration::instance().generateFinalOptions();

		
		// set the logger
		if(UniverseConfiguration::instance().logType == "console")
		{
			Logger::setLogger(new ConsoleLogger());
		}
		else
		{
			Logger::setLogger(new FileLogger(UniverseConfiguration::instance().logFilename));
		}

		// Setup database
		MysqlDatabase* db = MysqlDatabase::createInstance(UniverseConfiguration::instance().demuxerCount,
			UniverseConfiguration::instance().DBUsername,
			UniverseConfiguration::instance().DBHost,
			UniverseConfiguration::instance().DBPassword,
			UniverseConfiguration::instance().DBName,
			UniverseConfiguration::instance().DBPort);
    
		if(!db->start())
		{
			throw std::exception("Can't start the DB");
		}



		// Create listening server
		Network n;
		n.createConnectionAcceptor<UniverseConnection>(UniverseConfiguration::instance().listenAddress,
			UniverseConfiguration::instance().listenPort,
			UniverseConfiguration::instance().demuxerCount);
		
		n.createConnectionAcceptor<InterConnection>(UniverseConfiguration::instance().listenInterAddress,
                UniverseConfiguration::instance().listenInterPort,
                1);

		
		// Set console control handler to allow server to be stopped.
		console_ctrl_function = boost::bind(&Network::stop, &n);
		SetConsoleCtrlHandler(console_ctrl_handler, TRUE);

		// Run the server until stopped.
		n.wait();
		

	}
	catch (std::exception& e)
	{
		std::cerr << "unhandled exception: " << e.what() << "\n";
	}

			
	MysqlDatabase::destroy();
	UniverseConfiguration::destroy();
	
	return 0;
}
