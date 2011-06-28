#include "stdafx.h"
#include <iostream>
#include <windows.h>
#include <fstream>
#include <string.h>

using namespace std;

#pragma comment (linker, "/export:FreeAddrInfoEx=ws2_32_.FreeAddrInfoEx,@25")
#pragma comment (linker, "/export:FreeAddrInfoExW=ws2_32_.FreeAddrInfoExW,@26")
#pragma comment (linker, "/export:FreeAddrInfoW=ws2_32_.FreeAddrInfoW,@27")
#pragma comment (linker, "/export:GetAddrInfoExA=ws2_32_.GetAddrInfoExA,@28")
#pragma comment (linker, "/export:GetAddrInfoExW=ws2_32_.GetAddrInfoExW,@29")
#pragma comment (linker, "/export:GetAddrInfoW=ws2_32_.GetAddrInfoW,@30")
#pragma comment (linker, "/export:GetNameInfoW=ws2_32_.GetNameInfoW,@31")
#pragma comment (linker, "/export:InetNtopW=ws2_32_.InetNtopW,@32")
#pragma comment (linker, "/export:InetPtonW=ws2_32_.InetPtonW,@33")
#pragma comment (linker, "/export:SetAddrInfoExA=ws2_32_.SetAddrInfoExA,@34")
#pragma comment (linker, "/export:SetAddrInfoExW=ws2_32_.SetAddrInfoExW,@35")
#pragma comment (linker, "/export:WEP=ws2_32_.WEP,@500")
#pragma comment (linker, "/export:WPUCompleteOverlappedRequest=ws2_32_.WPUCompleteOverlappedRequest,@36")
#pragma comment (linker, "/export:WSAAccept=ws2_32_.WSAAccept,@37")
#pragma comment (linker, "/export:WSAAddressToStringA=ws2_32_.WSAAddressToStringA,@38")
#pragma comment (linker, "/export:WSAAddressToStringW=ws2_32_.WSAAddressToStringW,@39")
#pragma comment (linker, "/export:WSAAdvertiseProvider=ws2_32_.WSAAdvertiseProvider,@40")
#pragma comment (linker, "/export:WSAAsyncGetHostByAddr=ws2_32_.WSAAsyncGetHostByAddr,@102")
#pragma comment (linker, "/export:WSAAsyncGetHostByName=ws2_32_.WSAAsyncGetHostByName,@103")
#pragma comment (linker, "/export:WSAAsyncGetProtoByName=ws2_32_.WSAAsyncGetProtoByName,@105")
#pragma comment (linker, "/export:WSAAsyncGetProtoByNumber=ws2_32_.WSAAsyncGetProtoByNumber,@104")
#pragma comment (linker, "/export:WSAAsyncGetServByName=ws2_32_.WSAAsyncGetServByName,@107")
#pragma comment (linker, "/export:WSAAsyncGetServByPort=ws2_32_.WSAAsyncGetServByPort,@106")
#pragma comment (linker, "/export:WSAAsyncSelect=ws2_32_.WSAAsyncSelect,@101")
#pragma comment (linker, "/export:WSACancelAsyncRequest=ws2_32_.WSACancelAsyncRequest,@108")
#pragma comment (linker, "/export:WSACancelBlockingCall=ws2_32_.WSACancelBlockingCall,@113")
#pragma comment (linker, "/export:WSACleanup=ws2_32_.WSACleanup,@116")
#pragma comment (linker, "/export:WSACloseEvent=ws2_32_.WSACloseEvent,@41")
#pragma comment (linker, "/export:WSAConnect=ws2_32_.WSAConnect,@42")
#pragma comment (linker, "/export:WSAConnectByList=ws2_32_.WSAConnectByList,@43")
#pragma comment (linker, "/export:WSAConnectByNameA=ws2_32_.WSAConnectByNameA,@44")
#pragma comment (linker, "/export:WSAConnectByNameW=ws2_32_.WSAConnectByNameW,@45")
#pragma comment (linker, "/export:WSACreateEvent=ws2_32_.WSACreateEvent,@46")
#pragma comment (linker, "/export:WSADuplicateSocketA=ws2_32_.WSADuplicateSocketA,@47")
#pragma comment (linker, "/export:WSADuplicateSocketW=ws2_32_.WSADuplicateSocketW,@48")
#pragma comment (linker, "/export:WSAEnumNameSpaceProvidersA=ws2_32_.WSAEnumNameSpaceProvidersA,@49")
#pragma comment (linker, "/export:WSAEnumNameSpaceProvidersExA=ws2_32_.WSAEnumNameSpaceProvidersExA,@50")
#pragma comment (linker, "/export:WSAEnumNameSpaceProvidersExW=ws2_32_.WSAEnumNameSpaceProvidersExW,@58")
#pragma comment (linker, "/export:WSAEnumNameSpaceProvidersW=ws2_32_.WSAEnumNameSpaceProvidersW,@59")
#pragma comment (linker, "/export:WSAEnumNetworkEvents=ws2_32_.WSAEnumNetworkEvents,@60")
#pragma comment (linker, "/export:WSAEnumProtocolsA=ws2_32_.WSAEnumProtocolsA,@61")
#pragma comment (linker, "/export:WSAEnumProtocolsW=ws2_32_.WSAEnumProtocolsW,@62")
#pragma comment (linker, "/export:WSAEventSelect=ws2_32_.WSAEventSelect,@63")
#pragma comment (linker, "/export:WSAGetLastError=ws2_32_.WSAGetLastError,@111")
#pragma comment (linker, "/export:WSAGetOverlappedResult=ws2_32_.WSAGetOverlappedResult,@64")
#pragma comment (linker, "/export:WSAGetQOSByName=ws2_32_.WSAGetQOSByName,@65")
#pragma comment (linker, "/export:WSAGetServiceClassInfoA=ws2_32_.WSAGetServiceClassInfoA,@66")
#pragma comment (linker, "/export:WSAGetServiceClassInfoW=ws2_32_.WSAGetServiceClassInfoW,@67")
#pragma comment (linker, "/export:WSAGetServiceClassNameByClassIdA=ws2_32_.WSAGetServiceClassNameByClassIdA,@68")
#pragma comment (linker, "/export:WSAGetServiceClassNameByClassIdW=ws2_32_.WSAGetServiceClassNameByClassIdW,@69")
#pragma comment (linker, "/export:WSAHtonl=ws2_32_.WSAHtonl,@70")
#pragma comment (linker, "/export:WSAHtons=ws2_32_.WSAHtons,@71")
#pragma comment (linker, "/export:WSAInstallServiceClassA=ws2_32_.WSAInstallServiceClassA,@72")
#pragma comment (linker, "/export:WSAInstallServiceClassW=ws2_32_.WSAInstallServiceClassW,@73")
#pragma comment (linker, "/export:WSAIoctl=ws2_32_.WSAIoctl,@74")
#pragma comment (linker, "/export:WSAIsBlocking=ws2_32_.WSAIsBlocking,@114")
#pragma comment (linker, "/export:WSAJoinLeaf=ws2_32_.WSAJoinLeaf,@75")
#pragma comment (linker, "/export:WSALookupServiceBeginA=ws2_32_.WSALookupServiceBeginA,@76")
#pragma comment (linker, "/export:WSALookupServiceBeginW=ws2_32_.WSALookupServiceBeginW,@77")
#pragma comment (linker, "/export:WSALookupServiceEnd=ws2_32_.WSALookupServiceEnd,@78")
#pragma comment (linker, "/export:WSALookupServiceNextA=ws2_32_.WSALookupServiceNextA,@79")
#pragma comment (linker, "/export:WSALookupServiceNextW=ws2_32_.WSALookupServiceNextW,@80")
#pragma comment (linker, "/export:WSANSPIoctl=ws2_32_.WSANSPIoctl,@81")
#pragma comment (linker, "/export:WSANtohl=ws2_32_.WSANtohl,@82")
#pragma comment (linker, "/export:WSANtohs=ws2_32_.WSANtohs,@83")
#pragma comment (linker, "/export:WSAPoll=ws2_32_.WSAPoll,@84")
#pragma comment (linker, "/export:WSAProviderCompleteAsyncCall=ws2_32_.WSAProviderCompleteAsyncCall,@85")
#pragma comment (linker, "/export:WSAProviderConfigChange=ws2_32_.WSAProviderConfigChange,@86")
#pragma comment (linker, "/export:WSARecv=ws2_32_.WSARecv,@87")
#pragma comment (linker, "/export:WSARecvDisconnect=ws2_32_.WSARecvDisconnect,@88")
#pragma comment (linker, "/export:WSARecvFrom=ws2_32_.WSARecvFrom,@89")
#pragma comment (linker, "/export:WSARemoveServiceClass=ws2_32_.WSARemoveServiceClass,@90")
#pragma comment (linker, "/export:WSAResetEvent=ws2_32_.WSAResetEvent,@91")
#pragma comment (linker, "/export:WSASend=ws2_32_.WSASend,@92")
#pragma comment (linker, "/export:WSASendDisconnect=ws2_32_.WSASendDisconnect,@93")
#pragma comment (linker, "/export:WSASendMsg=ws2_32_.WSASendMsg,@94")
#pragma comment (linker, "/export:WSASendTo=ws2_32_.WSASendTo,@95")
#pragma comment (linker, "/export:WSASetBlockingHook=ws2_32_.WSASetBlockingHook,@109")
#pragma comment (linker, "/export:WSASetEvent=ws2_32_.WSASetEvent,@96")
#pragma comment (linker, "/export:WSASetLastError=ws2_32_.WSASetLastError,@112")
#pragma comment (linker, "/export:WSASetServiceA=ws2_32_.WSASetServiceA,@97")
#pragma comment (linker, "/export:WSASetServiceW=ws2_32_.WSASetServiceW,@98")
#pragma comment (linker, "/export:WSASocketA=ws2_32_.WSASocketA,@99")
#pragma comment (linker, "/export:WSASocketW=ws2_32_.WSASocketW,@100")
#pragma comment (linker, "/export:WSAStartup=ws2_32_.WSAStartup,@115")
#pragma comment (linker, "/export:WSAStringToAddressA=ws2_32_.WSAStringToAddressA,@117")
#pragma comment (linker, "/export:WSAStringToAddressW=ws2_32_.WSAStringToAddressW,@118")
#pragma comment (linker, "/export:WSAUnadvertiseProvider=ws2_32_.WSAUnadvertiseProvider,@119")
#pragma comment (linker, "/export:WSAUnhookBlockingHook=ws2_32_.WSAUnhookBlockingHook,@110")
#pragma comment (linker, "/export:WSAWaitForMultipleEvents=ws2_32_.WSAWaitForMultipleEvents,@120")
#pragma comment (linker, "/export:WSApSetPostRoutine=ws2_32_.WSApSetPostRoutine,@24")
#pragma comment (linker, "/export:WSCDeinstallProvider=ws2_32_.WSCDeinstallProvider,@121")
#pragma comment (linker, "/export:WSCEnableNSProvider=ws2_32_.WSCEnableNSProvider,@122")
#pragma comment (linker, "/export:WSCEnumProtocols=ws2_32_.WSCEnumProtocols,@123")
#pragma comment (linker, "/export:WSCGetApplicationCategory=ws2_32_.WSCGetApplicationCategory,@124")
#pragma comment (linker, "/export:WSCGetProviderInfo=ws2_32_.WSCGetProviderInfo,@125")
#pragma comment (linker, "/export:WSCGetProviderPath=ws2_32_.WSCGetProviderPath,@126")
#pragma comment (linker, "/export:WSCInstallNameSpace=ws2_32_.WSCInstallNameSpace,@127")
#pragma comment (linker, "/export:WSCInstallNameSpaceEx=ws2_32_.WSCInstallNameSpaceEx,@128")
#pragma comment (linker, "/export:WSCInstallProvider=ws2_32_.WSCInstallProvider,@129")
#pragma comment (linker, "/export:WSCInstallProviderAndChains=ws2_32_.WSCInstallProviderAndChains,@130")
#pragma comment (linker, "/export:WSCSetApplicationCategory=ws2_32_.WSCSetApplicationCategory,@131")
#pragma comment (linker, "/export:WSCSetProviderInfo=ws2_32_.WSCSetProviderInfo,@132")
#pragma comment (linker, "/export:WSCUnInstallNameSpace=ws2_32_.WSCUnInstallNameSpace,@133")
#pragma comment (linker, "/export:WSCUpdateProvider=ws2_32_.WSCUpdateProvider,@134")
#pragma comment (linker, "/export:WSCWriteNameSpaceOrder=ws2_32_.WSCWriteNameSpaceOrder,@135")
#pragma comment (linker, "/export:WSCWriteProviderOrder=ws2_32_.WSCWriteProviderOrder,@136")
#pragma comment (linker, "/export:WahCloseApcHelper=ws2_32_.WahCloseApcHelper,@137")
#pragma comment (linker, "/export:WahCloseHandleHelper=ws2_32_.WahCloseHandleHelper,@138")
#pragma comment (linker, "/export:WahCloseNotificationHandleHelper=ws2_32_.WahCloseNotificationHandleHelper,@139")
#pragma comment (linker, "/export:WahCloseSocketHandle=ws2_32_.WahCloseSocketHandle,@140")
#pragma comment (linker, "/export:WahCloseThread=ws2_32_.WahCloseThread,@141")
#pragma comment (linker, "/export:WahCompleteRequest=ws2_32_.WahCompleteRequest,@142")
#pragma comment (linker, "/export:WahCreateHandleContextTable=ws2_32_.WahCreateHandleContextTable,@143")
#pragma comment (linker, "/export:WahCreateNotificationHandle=ws2_32_.WahCreateNotificationHandle,@144")
#pragma comment (linker, "/export:WahCreateSocketHandle=ws2_32_.WahCreateSocketHandle,@145")
#pragma comment (linker, "/export:WahDestroyHandleContextTable=ws2_32_.WahDestroyHandleContextTable,@146")
#pragma comment (linker, "/export:WahDisableNonIFSHandleSupport=ws2_32_.WahDisableNonIFSHandleSupport,@147")
#pragma comment (linker, "/export:WahEnableNonIFSHandleSupport=ws2_32_.WahEnableNonIFSHandleSupport,@148")
#pragma comment (linker, "/export:WahEnumerateHandleContexts=ws2_32_.WahEnumerateHandleContexts,@149")
#pragma comment (linker, "/export:WahInsertHandleContext=ws2_32_.WahInsertHandleContext,@150")
#pragma comment (linker, "/export:WahNotifyAllProcesses=ws2_32_.WahNotifyAllProcesses,@152")
#pragma comment (linker, "/export:WahOpenApcHelper=ws2_32_.WahOpenApcHelper,@153")
#pragma comment (linker, "/export:WahOpenCurrentThread=ws2_32_.WahOpenCurrentThread,@154")
#pragma comment (linker, "/export:WahOpenHandleHelper=ws2_32_.WahOpenHandleHelper,@155")
#pragma comment (linker, "/export:WahOpenNotificationHandleHelper=ws2_32_.WahOpenNotificationHandleHelper,@156")
#pragma comment (linker, "/export:WahQueueUserApc=ws2_32_.WahQueueUserApc,@157")
#pragma comment (linker, "/export:WahReferenceContextByHandle=ws2_32_.WahReferenceContextByHandle,@158")
#pragma comment (linker, "/export:WahRemoveHandleContext=ws2_32_.WahRemoveHandleContext,@159")
#pragma comment (linker, "/export:WahWaitForNotification=ws2_32_.WahWaitForNotification,@160")
#pragma comment (linker, "/export:WahWriteLSPEvent=ws2_32_.WahWriteLSPEvent,@161")
#pragma comment (linker, "/export:__WSAFDIsSet=ws2_32_.__WSAFDIsSet,@151")
#pragma comment (linker, "/export:accept=ws2_32_.accept,@1")
#pragma comment (linker, "/export:bind=ws2_32_.bind,@2")
#pragma comment (linker, "/export:closesocket=ws2_32_.closesocket,@3")
#pragma comment (linker, "/export:connect=ws2_32_.connect,@4")
#pragma comment (linker, "/export:freeaddrinfo=ws2_32_.freeaddrinfo,@162")
#pragma comment (linker, "/export:getaddrinfo=ws2_32_.getaddrinfo,@163")
#pragma comment (linker, "/export:gethostbyaddr=ws2_32_.gethostbyaddr,@51")
//#pragma comment (linker, "/export:gethostbyname=ws2_32_.gethostbyname,@52")
#pragma comment (linker, "/export:gethostname=ws2_32_.gethostname,@57")
#pragma comment (linker, "/export:getnameinfo=ws2_32_.getnameinfo,@164")
#pragma comment (linker, "/export:getpeername=ws2_32_.getpeername,@5")
#pragma comment (linker, "/export:getprotobyname=ws2_32_.getprotobyname,@53")
#pragma comment (linker, "/export:getprotobynumber=ws2_32_.getprotobynumber,@54")
#pragma comment (linker, "/export:getservbyname=ws2_32_.getservbyname,@55")
#pragma comment (linker, "/export:getservbyport=ws2_32_.getservbyport,@56")
#pragma comment (linker, "/export:getsockname=ws2_32_.getsockname,@6")
#pragma comment (linker, "/export:getsockopt=ws2_32_.getsockopt,@7")
#pragma comment (linker, "/export:htonl=ws2_32_.htonl,@8")
#pragma comment (linker, "/export:htons=ws2_32_.htons,@9")
#pragma comment (linker, "/export:inet_addr=ws2_32_.inet_addr,@11")
#pragma comment (linker, "/export:inet_ntoa=ws2_32_.inet_ntoa,@12")
#pragma comment (linker, "/export:inet_ntop=ws2_32_.inet_ntop,@165")
#pragma comment (linker, "/export:inet_pton=ws2_32_.inet_pton,@166")
#pragma comment (linker, "/export:ioctlsocket=ws2_32_.ioctlsocket,@10")
#pragma comment (linker, "/export:listen=ws2_32_.listen,@13")
#pragma comment (linker, "/export:ntohl=ws2_32_.ntohl,@14")
#pragma comment (linker, "/export:ntohs=ws2_32_.ntohs,@15")
#pragma comment (linker, "/export:recv=ws2_32_.recv,@16")
#pragma comment (linker, "/export:recvfrom=ws2_32_.recvfrom,@17")
#pragma comment (linker, "/export:select=ws2_32_.select,@18")
#pragma comment (linker, "/export:send=ws2_32_.send,@19")
#pragma comment (linker, "/export:sendto=ws2_32_.sendto,@20")
#pragma comment (linker, "/export:setsockopt=ws2_32_.setsockopt,@21")
#pragma comment (linker, "/export:shutdown=ws2_32_.shutdown,@22")
#pragma comment (linker, "/export:socket=ws2_32_.socket,@23")

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