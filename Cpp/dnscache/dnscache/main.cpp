#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>

// link with ws2_32.lib
#pragma comment(lib, "Ws2_32.lib")

int __cdecl main(int argc, char **argv)
{

    //-----------------------------------------
    // Declare and initialize variables
    WSADATA wsaData = {0};
    int iResult = 0;

    DWORD dwRetval;

    struct sockaddr_in saGNI;
    char hostname[NI_MAXHOST];
    char servInfo[NI_MAXSERV];
    u_short port = 27015;

    // Validate the parameters
    if (argc != 2) {
        printf("usage: %s IPv4 address\n", argv[0]);
        printf("  to return hostname\n");
        printf("       %s 127.0.0.1\n", argv[0]);
        return 1;
    }
    // Initialize Winsock
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
        printf("WSAStartup failed: %d\n", iResult);
        return 1;
    }
    //-----------------------------------------
    // Set up sockaddr_in structure which is passed
    // to the getnameinfo function
    saGNI.sin_family = AF_INET;
    saGNI.sin_addr.s_addr = inet_addr(argv[1]);
    saGNI.sin_port = htons(port);

    //-----------------------------------------
    // Call getnameinfo
    dwRetval = getnameinfo((struct sockaddr *) &saGNI,
                           sizeof (struct sockaddr),
                           hostname,
                           NI_MAXHOST, servInfo, NI_MAXSERV, NI_NUMERICSERV);

    if (dwRetval != 0) {
        printf("getnameinfo failed with error # %ld\n", WSAGetLastError());
        return 1;
    } else {
        printf("getnameinfo returned hostname = %s\n", hostname);
        return 0;
    }
}
