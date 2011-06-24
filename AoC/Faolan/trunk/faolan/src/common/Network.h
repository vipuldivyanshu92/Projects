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

#ifndef NETWORK_H_
#define NETWORK_H_

#include "Common.h"
#include <boost/asio.hpp>
#include <boost/thread.hpp>
#include <boost/noncopyable.hpp>
#include <boost/bind.hpp>
#include <vector>

#include "Acceptor.h"
#include "ConnectionAcceptor.h"
/**
 * Network class
 * @author Albator, Doron
 */
class Network : private boost::noncopyable {
public:
    Network();

    /**
     * Create a new connection acceptor and run it in a separate thread
     */
    template<typename ConnectionType> void createConnectionAcceptor(
            const std::string& address, const std::string& port,
            std::size_t poolSize)
	{
		ConnectionAcceptor<ConnectionType>* ca = new ConnectionAcceptor<ConnectionType>(address, port, poolSize);
		m_acceptors.push_back(ca);
		m_threadGroup.create_thread(boost::bind(&ConnectionAcceptor<ConnectionType>::run, ca));

	}



    /**
     * shut down all the running acceptor
     */
    void stop();


	/**
	 * Wait acceptors until they stop
	 */
	void wait();

    ~Network();

private:
    std::vector<Acceptor*> m_acceptors;
    boost::thread_group m_threadGroup;

};

#endif /*NETWORK_H_*/
