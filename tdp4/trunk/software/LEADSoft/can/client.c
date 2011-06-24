/*
created by Simon Jouet and Esiri Igbako
client.c
This file test the can adpter.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <net/if.h>

int main(int argc, char *argv[])
{
    int s;
    ssize_t n;
    struct sockaddr_can addr;
    struct can_frame frame;
    struct ifreq ifr;
    
    // Establish the connection to the virtual can adapter
    s = socket(PF_CAN, SOCK_RAW, CAN_RAW);

    strcpy(ifr.ifr_name, "vcan0");
    ioctl(s, SIOCGIFINDEX, &ifr);

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) != 0)
        perror("Unable to bind to vcan0");


    // Receive can packets
    while ((n = read(s, &frame, sizeof(frame))) != 0)
    {
        printf("Bytes received %d\n", n);
    }
    
    // Close the connection
    close(s);

    return EXIT_SUCCESS;
}
