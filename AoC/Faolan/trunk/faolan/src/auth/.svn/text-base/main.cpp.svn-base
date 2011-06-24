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
#include "../common/MysqlDatabase.h"
#include "../common/MysqlQuery.h"
#include "../common/Logger.h"
#include "../common/ConsoleLogger.h"
#include "../common/FileLogger.h"

#include <pthread.h>
#include <signal.h>


int main(int argc, char* argv[])
{
    try
    {
        // Parse config
        UniverseConfiguration::instance().parseCommandLine(argc,argv);
        UniverseConfiguration::instance().parseConfigFile();
        UniverseConfiguration::instance().generateFinalOptions();


        // set the logger
        if (UniverseConfiguration::instance().logType == "console")
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

        if (!db->start())
        {
            throw std::exception();
        }



        // Create listening server
        Network n;
        n.createConnectionAcceptor<UniverseConnection>(UniverseConfiguration::instance().listenAddress,
                UniverseConfiguration::instance().listenPort,
                UniverseConfiguration::instance().demuxerCount);

        n.createConnectionAcceptor<InterConnection>(UniverseConfiguration::instance().listenInterAddress,
                UniverseConfiguration::instance().listenInterPort,
                1);

        // Restore previous signals.
      //  pthread_sigmask(SIG_SETMASK, &old_mask, 0);

        // Wait for signal indicating time to shut down.
        sigset_t wait_mask;
        sigemptyset(&wait_mask);
        sigaddset(&wait_mask, SIGINT);
        sigaddset(&wait_mask, SIGQUIT);
        sigaddset(&wait_mask, SIGTERM);
        pthread_sigmask(SIG_BLOCK, &wait_mask, 0);
        int sig = 0;
        sigwait(&wait_mask, &sig);

        n.stop();

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
