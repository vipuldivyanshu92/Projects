#include "stdafx.h"
#include <iostream>
#include <windows.h>
#include <fstream>

using namespace std;

#pragma comment (linker, "/export:AcceptEx=wsock32_.AcceptEx,@1141")
#pragma comment (linker, "/export:EnumProtocolsA=wsock32_.EnumProtocolsA,@1111")
#pragma comment (linker, "/export:EnumProtocolsW=wsock32_.EnumProtocolsW,@1112")
#pragma comment (linker, "/export:GetAcceptExSockaddrs=wsock32_.GetAcceptExSockaddrs,@1142")
#pragma comment (linker, "/export:GetAddressByNameA=wsock32_.GetAddressByNameA,@1109")
#pragma comment (linker, "/export:GetAddressByNameW=wsock32_.GetAddressByNameW,@1110")
#pragma comment (linker, "/export:GetNameByTypeA=wsock32_.GetNameByTypeA,@1115")
#pragma comment (linker, "/export:GetNameByTypeW=wsock32_.GetNameByTypeW,@1116")
#pragma comment (linker, "/export:GetServiceA=wsock32_.GetServiceA,@1119")
#pragma comment (linker, "/export:GetServiceW=wsock32_.GetServiceW,@1120")
#pragma comment (linker, "/export:GetTypeByNameA=wsock32_.GetTypeByNameA,@1113")
#pragma comment (linker, "/export:GetTypeByNameW=wsock32_.GetTypeByNameW,@1114")
#pragma comment (linker, "/export:MigrateWinsockConfiguration=wsock32_.MigrateWinsockConfiguration,@24")
#pragma comment (linker, "/export:NPLoadNameSpaces=wsock32_.NPLoadNameSpaces,@1130")
#pragma comment (linker, "/export:SetServiceA=wsock32_.SetServiceA,@1117")
#pragma comment (linker, "/export:SetServiceW=wsock32_.SetServiceW,@1118")
#pragma comment (linker, "/export:TransmitFile=wsock32_.TransmitFile,@1140")
#pragma comment (linker, "/export:WEP=wsock32_.WEP,@500")
#pragma comment (linker, "/export:WSAAsyncGetHostByAddr=wsock32_.WSAAsyncGetHostByAddr,@102")
//#pragma comment (linker, "/export:WSAAsyncGetHostByName=wsock32_.WSAAsyncGetHostByName,@103")
#pragma comment (linker, "/export:WSAAsyncGetProtoByName=wsock32_.WSAAsyncGetProtoByName,@105")
#pragma comment (linker, "/export:WSAAsyncGetProtoByNumber=wsock32_.WSAAsyncGetProtoByNumber,@104")
#pragma comment (linker, "/export:WSAAsyncGetServByName=wsock32_.WSAAsyncGetServByName,@107")
#pragma comment (linker, "/export:WSAAsyncGetServByPort=wsock32_.WSAAsyncGetServByPort,@106")
#pragma comment (linker, "/export:WSAAsyncSelect=wsock32_.WSAAsyncSelect,@101")
#pragma comment (linker, "/export:WSACancelAsyncRequest=wsock32_.WSACancelAsyncRequest,@108")
#pragma comment (linker, "/export:WSACancelBlockingCall=wsock32_.WSACancelBlockingCall,@113")
#pragma comment (linker, "/export:WSACleanup=wsock32_.WSACleanup,@116")
#pragma comment (linker, "/export:WSAGetLastError=wsock32_.WSAGetLastError,@111")
#pragma comment (linker, "/export:WSAIsBlocking=wsock32_.WSAIsBlocking,@114")
#pragma comment (linker, "/export:WSARecvEx=wsock32_.WSARecvEx,@1107")
#pragma comment (linker, "/export:WSASetBlockingHook=wsock32_.WSASetBlockingHook,@109")
#pragma comment (linker, "/export:WSASetLastError=wsock32_.WSASetLastError,@112")
#pragma comment (linker, "/export:WSAStartup=wsock32_.WSAStartup,@115")
#pragma comment (linker, "/export:WSAUnhookBlockingHook=wsock32_.WSAUnhookBlockingHook,@110")
#pragma comment (linker, "/export:WSApSetPostRoutine=wsock32_.WSApSetPostRoutine,@1000")
#pragma comment (linker, "/export:__WSAFDIsSet=wsock32_.__WSAFDIsSet,@151")
#pragma comment (linker, "/export:accept=wsock32_.accept,@1")
#pragma comment (linker, "/export:bind=wsock32_.bind,@2")
#pragma comment (linker, "/export:closesocket=wsock32_.closesocket,@3")
#pragma comment (linker, "/export:connect=wsock32_.connect,@4")
#pragma comment (linker, "/export:dn_expand=wsock32_.dn_expand,@1106")
#pragma comment (linker, "/export:gethostbyaddr=wsock32_.gethostbyaddr,@51")
#pragma comment (linker, "/export:gethostbyname=wsock32_.gethostbyname,@52")
#pragma comment (linker, "/export:gethostname=wsock32_.gethostname,@57")
#pragma comment (linker, "/export:getnetbyname=wsock32_.getnetbyname,@1101")
#pragma comment (linker, "/export:getpeername=wsock32_.getpeername,@5")
#pragma comment (linker, "/export:getprotobyname=wsock32_.getprotobyname,@53")
#pragma comment (linker, "/export:getprotobynumber=wsock32_.getprotobynumber,@54")
#pragma comment (linker, "/export:getservbyname=wsock32_.getservbyname,@55")
#pragma comment (linker, "/export:getservbyport=wsock32_.getservbyport,@56")
#pragma comment (linker, "/export:getsockname=wsock32_.getsockname,@6")
#pragma comment (linker, "/export:getsockopt=wsock32_.getsockopt,@7")
#pragma comment (linker, "/export:htonl=wsock32_.htonl,@8")
#pragma comment (linker, "/export:htons=wsock32_.htons,@9")
#pragma comment (linker, "/export:inet_addr=wsock32_.inet_addr,@10")
#pragma comment (linker, "/export:inet_network=wsock32_.inet_network,@1100")
#pragma comment (linker, "/export:inet_ntoa=wsock32_.inet_ntoa,@11")
#pragma comment (linker, "/export:ioctlsocket=wsock32_.ioctlsocket,@12")
#pragma comment (linker, "/export:listen=wsock32_.listen,@13")
#pragma comment (linker, "/export:ntohl=wsock32_.ntohl,@14")
#pragma comment (linker, "/export:ntohs=wsock32_.ntohs,@15")
#pragma comment (linker, "/export:rcmd=wsock32_.rcmd,@1102")
#pragma comment (linker, "/export:recv=wsock32_.recv,@16")
#pragma comment (linker, "/export:recvfrom=wsock32_.recvfrom,@17")
#pragma comment (linker, "/export:rexec=wsock32_.rexec,@1103")
#pragma comment (linker, "/export:rresvport=wsock32_.rresvport,@1104")
#pragma comment (linker, "/export:s_perror=wsock32_.s_perror,@1108")
#pragma comment (linker, "/export:select=wsock32_.select,@18")
#pragma comment (linker, "/export:send=wsock32_.send,@19")
#pragma comment (linker, "/export:sendto=wsock32_.sendto,@20")
#pragma comment (linker, "/export:sethostname=wsock32_.sethostname,@1105")
#pragma comment (linker, "/export:setsockopt=wsock32_.setsockopt,@21")
#pragma comment (linker, "/export:shutdown=wsock32_.shutdown,@22")
#pragma comment (linker, "/export:socket=wsock32_.socket,@23")

HINSTANCE	handle = 0;		//Handle to the original winsock library.
FARPROC		function = {0};	//Pointer for original address.
ofstream	myfile;			//Output stream for log file.

BOOL WINAPI DllMain(HINSTANCE hInst,DWORD reason,LPVOID)
{
	//This code is executed when the DLL is loaded.
	if (reason == DLL_PROCESS_ATTACH)
	{
		//Load the original library.
		handle = LoadLibraryA("wsock32_.dll");
		//Did we get a handle to the library?
		if (!handle || handle == 0) 
			return false;
		//Get a pointer to the original 'gethostbyname' function.
		function = GetProcAddress(handle,"gethostbyname");
		//Open the URL logging file for append.
		myfile.open ("activity.log", ios::out | ios::app);
	}
	//This code is executed when the DLL is unloaded.
	if (reason == DLL_PROCESS_DETACH) 
	{
		//Free memory and handles associated with the original winsock library.
		FreeLibrary(handle);
		//If the output stream for log is open, close the stream.
		if (myfile.is_open())
			myfile.close();
	}
	return true;
}

extern "C" struct hostent* __stdcall mygethostbyname(__in const char *name)
{
	typedef hostent* (__stdcall *pS)(const char*);
	//Forward call to original library.
	pS pps = (pS)function;
	hostent* rv = pps(name);
	//If the log file stream is open, write the URL to file.
	if (myfile.is_open())
		myfile << name << "\r\n";
	//Return data from original library.
	return rv;
}