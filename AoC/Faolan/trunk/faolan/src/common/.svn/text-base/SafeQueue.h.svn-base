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

#ifndef SAFEQUEUE_
#define SAFEQUEUE_

#include <boost/thread.hpp>
#include <queue>
#include "Common.h"

/**
 * A thread safe queue based on Boost::Thread lock
 * std::queue like interface
 * @author Albator
 */
template<typename T> class SafeQueue {
public:

    std::size_t size()
    {
        boost::mutex::scoped_lock lock(m_mutex);
        return m_queue.size();
    }

    bool empty() const
    {
        boost::mutex::scoped_lock lock(m_mutex);
        return m_queue.size();
    }

    void push(const T& x)
    {
        boost::mutex::scoped_lock lock(m_mutex);
        const bool empty = m_queue.empty();
        m_queue.push(x);

        lock.unlock();

        if (empty)
        {
            m_condition.notify_one();
        }
    }

    T& front()
    {
        boost::mutex::scoped_lock lock(m_mutex);
        return m_queue.front();
    }

    void pop()
    {
        boost::mutex::scoped_lock lock(m_mutex);
        m_queue.pop();
    }

    /**
     * Usefull in the case of a consumer/producer queue.
     * This will wait until a new element is available in the queue
     */
    void popWait(T& x)
    {
        boost::mutex::scoped_lock lock(m_mutex);
        while (m_queue.empty())
        {
            m_condition.wait(lock);
        }

        x = m_queue.front();
        m_queue.pop();
    }

    void tryPop(T& x)
    {
        boost::mutex::scoped_lock lock(m_mutex);
        if (m_queue.empty())
        {
            x = NULL;
            return;
        }
        
        x = m_queue.front();
        m_queue.pop();        
    }

private:
    std::queue<T> m_queue;
    mutable boost::mutex m_mutex;
    boost::condition m_condition;

};

#endif /*SAFEQUEUE_*/
