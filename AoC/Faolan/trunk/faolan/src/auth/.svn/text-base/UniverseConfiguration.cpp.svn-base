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

#include "UniverseConfiguration.h"
#include <iostream>
#include <fstream>


UniverseConfiguration::UniverseConfiguration() : Singleton<UniverseConfiguration>(), m_description("Universe server options"), m_addressCounter(0)
{


	m_description.add_options()
		("listenAddress",boost::program_options::value<std::string>(&listenAddress)->default_value("127.0.0.1"),"Address to listen to")
		("listenPort", boost::program_options::value<std::string>(&listenPort)->default_value("7000"),"Port to listen to")
		("listenInterAddress",boost::program_options::value<std::string>(&listenInterAddress)->default_value("127.0.0.1"),"Address to listen to")
		("listenInterPort", boost::program_options::value<std::string>(&listenInterPort)->default_value("12000"),"Port to listen to")
		("configFile", boost::program_options::value<std::string>(&configFile)->default_value("UniverseConfig.cfg"),"Universe server configuration file")
		("DBUsername", boost::program_options::value<std::string>(&DBUsername)->default_value("faolan"),"DB username")
		("DBPassword", boost::program_options::value<std::string>(&DBPassword)->default_value("faolan"),"DB password")
		("DBPort", boost::program_options::value<uint32>(&DBPort)->default_value(3306),"DB port")
		("DBHost", boost::program_options::value<std::string>(&DBHost)->default_value("127.0.0.1"),"DB Host")
		("DBName", boost::program_options::value<std::string>(&DBName)->default_value("faolandb"),"shema name")
		("demuxerCount", boost::program_options::value<uint32>(&demuxerCount)->default_value(2),"Count of network demuxer thread")
		("DBConnectionCount", boost::program_options::value<uint32>(&DBConnectionCount)->default_value(5),"Number of active connection to the DB server")
		("serverPrivateKey",boost::program_options::value<std::string>(&serverPrivateKey)->default_value("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"),"Server key")
		("clientKey", boost::program_options::value<std::string>(&clientKey)->default_value("9c32cc23d559ca90fc31be72df817d0e124769e809f936bc14360ff4bed758f260a0d596584eacbbc2b88bdd410416163e11dbf62173393fbc0c6fefb2d855f1a03dec8e9f105bbad91b3437d8eb73fe2f44159597aa4053cf788d2f9d7012fb8d7c4ce3876f7d6cd5d0c31754f4cd96166708641958de54a6def5657b9f2e92"), "public client key")
		("dhPrimeStr", boost::program_options::value<std::string>(&dhPrimeStr)->default_value("eca2e8c85d863dcdc26a429a71a9815ad052f6139669dd659f98ae159d313d13c6bf2838e10a69b6478b64a24bd054ba8248e8fa778703b418408249440b2c1edd28853e240d8a7e49540b76d120d3b1ad2878b1b99490eb4a2a5e84caa8a91cecbdb1aa7c816e8be343246f80c637abc653b893fd91686cf8d32d6cfe5f2a6f"), "Diffie-Hellman prime number")
		("dhBase", boost::program_options::value<std::string>(&dhBase)->default_value("5"),"Diffie Hellman base")
		("logType", boost::program_options::value<std::string>(&logType)->default_value("console"),"Console or file base logging")
		("logFilename", boost::program_options::value<std::string>(&logFilename)->default_value("UniverseConfiguration.log"),"File name of the log");


}

void UniverseConfiguration::parseCommandLine(int argc, char *argv[])
{

	boost::program_options::store(boost::program_options::parse_command_line(argc,argv,m_description),m_variableMap);
	boost::program_options::notify(m_variableMap);


	if (argc < 2 || (!strcmp(argv[1], "-?") || !strcmp(argv[1], "--?") || !strcmp(argv[1], "/?") || !strcmp(argv[1], "/h") || !strcmp(argv[1], "-h") || !strcmp(argv[1], "--h") || !strcmp(argv[1], "--help") || !strcmp(argv[1], "/help") || !strcmp(argv[1], "-help") || !strcmp(argv[1], "help") ))
	{
		printConfiguration();

	}

}


void UniverseConfiguration::parseConfigFile()
{

	std::ifstream ifs;
	if(!m_variableMap.count("configFile"))
	{
		ifs.open("UniverseConfig.cfg");
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

void UniverseConfiguration::generateFinalOptions()
{
	mpz_init_set_str(clientPublicKey,clientKey.c_str(),16);
	mpz_init_set_str(dhPrimeNum, dhPrimeStr.c_str(),16);
	mpz_init_set_str(mpzdhBase,dhBase.c_str(),10);
	mpz_init_set_str(mpzserverPrivateKey,serverPrivateKey.c_str(),16);
	mpz_init(serverPublicKey);
	mpz_powm(serverPublicKey,mpzdhBase,mpzserverPrivateKey,dhPrimeNum);


}

void UniverseConfiguration::printConfiguration()
{
	//std::cout << m_description << std::endl;
}

std::string UniverseConfiguration::getCharServerAddress()
{
	boost::mutex::scoped_lock lock(m_mutex);

	m_addressCounter++;
	if(m_addressCounter >=  m_charServers.size())
	{
		m_addressCounter = 0;
	}

	return m_charServers[m_addressCounter];


}

void UniverseConfiguration::addCharServer(std::string charServerAddress)
{
    boost::mutex::scoped_lock lock(m_mutex);
	m_charServers.push_back(charServerAddress);
}

void UniverseConfiguration::removeCharServer(std::string charServerAddress)
{
    boost::mutex::scoped_lock lock(m_mutex);

    std::vector<std::string>::iterator it;
    for ( it=m_charServers.begin() ; it < m_charServers.end(); it++ )
    {
        if(*it == charServerAddress)
        {
            m_charServers.erase(it);
            return;
        }
    }

}
