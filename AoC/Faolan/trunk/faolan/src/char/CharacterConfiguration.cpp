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

#include "CharacterConfiguration.h"
#include <iostream>
#include <fstream>


CharacterConfiguration::CharacterConfiguration() : Singleton<CharacterConfiguration>(), m_description("Character server options")
{


	m_description.add_options()
		("listenAddress",boost::program_options::value<std::string>(&listenAddress)->default_value("127.0.0.1"),"Address to listen to")
		("listenPort", boost::program_options::value<std::string>(&listenPort)->default_value("7000"),"Port to listen to")
		("listenPublicAddress",boost::program_options::value<std::string>(&listenPublicAddress)->default_value("127.0.0.1"),"Public Address to send to client")
		("listenPublicPort", boost::program_options::value<std::string>(&listenPublicPort)->default_value("7000"),"public port to send to client")
		("authServerAddress",boost::program_options::value<std::string>(&authServerAddress)->default_value("127.0.0.1"),"Auth server address")
		("authServerPort", boost::program_options::value<std::string>(&authServerPort)->default_value("12000"),"Auth server port")
		("configFile", boost::program_options::value<std::string>(&configFile)->default_value("CharacterConfig.cfg"),"Character server configuration file")
		("DBUsername", boost::program_options::value<std::string>(&DBUsername)->default_value("faolan"),"DB username")
		("DBPassword", boost::program_options::value<std::string>(&DBPassword)->default_value("faolan"),"DB password")
		("DBPort", boost::program_options::value<uint32>(&DBPort)->default_value(3306),"DB port")
		("DBHost", boost::program_options::value<std::string>(&DBHost)->default_value("127.0.0.1"),"DB Host")
		("DBName", boost::program_options::value<std::string>(&DBName)->default_value("faolandb"),"shema name")
		("demuxerCount", boost::program_options::value<uint32>(&demuxerCount)->default_value(2),"Count of network demuxer thread")
		("DBConnectionCount", boost::program_options::value<uint32>(&DBConnectionCount)->default_value(2),"Number of active connection to the DB server")
        ("logType", boost::program_options::value<std::string>(&logType)->default_value("console"),"Console or file base logging")
		("logFilename", boost::program_options::value<std::string>(&logFilename)->default_value("CharacterConfiguration.log"),"File name of the log");


}

void CharacterConfiguration::parseCommandLine(int argc, char *argv[])
{

	boost::program_options::store(boost::program_options::parse_command_line(argc,argv,m_description),m_variableMap);
	boost::program_options::notify(m_variableMap);


	if (argc < 2 || (!strcmp(argv[1], "-?") || !strcmp(argv[1], "--?") || !strcmp(argv[1], "/?") || !strcmp(argv[1], "/h") || !strcmp(argv[1], "-h") || !strcmp(argv[1], "--h") || !strcmp(argv[1], "--help") || !strcmp(argv[1], "/help") || !strcmp(argv[1], "-help") || !strcmp(argv[1], "help") ))
	{
		printConfiguration();

	}

}


void CharacterConfiguration::parseConfigFile()
{

	std::ifstream ifs;
	if(!m_variableMap.count("configFile"))
	{
		ifs.open("CharacterConfig.cfg");
	}
	else
	{
		ifs.open(configFile.c_str());
	}


	if(!ifs.fail())
	{
		boost::program_options::store(boost::program_options::parse_config_file(ifs,m_description),m_variableMap);
		boost::program_options::notify(m_variableMap);
		ifs.close();
	}
	else
	{
		std::cout << "Can't open the configuration file" << std::endl;
	}





}

void CharacterConfiguration::generateFinalOptions()
{


}

void CharacterConfiguration::printConfiguration()
{
	//std::cout << m_description << std::endl;
}


