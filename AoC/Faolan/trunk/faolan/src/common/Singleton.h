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

#ifndef SINGLETON_H_
#define SINGLETON_H_

#include "Common.h"


template <typename T>
class Singleton {

public:
	static T& instance()
	{
		if(!m_instance)
			m_instance = new T();

		return *m_instance;
	}

	static void destroy()
	{
		if(m_instance)
			delete m_instance;
	}

protected:

	Singleton()
	{
	}

	~Singleton()
	{
	}
private:

	static T* m_instance;

	Singleton(Singleton&);
	void operator =(Singleton&);

};

template<typename T> T* Singleton<T>::m_instance = NULL;

#endif
