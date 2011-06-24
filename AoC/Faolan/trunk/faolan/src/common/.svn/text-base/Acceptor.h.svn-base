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

#ifndef ACCEPTOR_H_
#define ACCEPTOR_H_

#include "Common.h"
#include "BufferPool.h"
#include <boost/asio.hpp>
#include <boost/noncopyable.hpp>


class Acceptor : private boost::noncopyable
{
public:
    
    
    /**
     * Run until stop is called or all the io_service return
     * 
     */
    virtual void run()=0;
    
    /**
     * stop all the running io_services
     */
    virtual void stop()=0;
    
    virtual ~Acceptor()
	{
	}
    
private:
    
    
    /**
     * event call when there is a new connection attempt
     */
    virtual void onAccept(const boost::system::error_code& e)=0;
    
    /**
     * return next available io_service using a round robin for load balancing
     */
	virtual std::pair<boost::asio::io_service*, BufferPool*> IOService()=0;

};
#endif
