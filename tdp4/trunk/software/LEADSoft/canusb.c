#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <net/if.h>
#include <stdio.h>
#include "canusb.h"

#define MAX_STRING_LEN    6

static int running;
static void (*callback)(packet_info_t*);
static char *device;
static int s;
struct ifreq ifr;
struct sockaddr_can addr;

void canusb_queue_packet(packet_info_t *p)
{
	struct can_frame frame;

	frame.can_id = p->can_id;
	frame.can_dlc = p->dlc;
	memcpy(&(frame.data[0]), &(p->data[0]), 8);

	write(s, &frame, sizeof(frame));
}


/* thread function reads data from CAN */
int canusb_data_read()
{
    ssize_t n;
    struct can_frame frame;
	packet_info_t packet;

	//int fuel_blink = 0
	printf("can_packet: variables declared and initialized\n");
    while (running && (n = read(s, &frame, sizeof(frame))) != 0 )
    {
		packet.can_id = frame.can_id;
		memcpy(&(packet.data[0]), &(frame.data[0]), 8);
		packet.dlc = frame.can_dlc;
		callback(&packet);
    }
   	printf("can_packet: while loop terminated\n");
    // Close the connection
	
    return 0;//EXIT_SUCCESS;
}

int canusb_init(char *dev, void (*callb)(packet_info_t *p))
{
	int ret;

	callback = callb;
	device = dev;

	running = 1;

    // Establish the connection to the virtual can adapter
    s = socket(PF_CAN, SOCK_RAW, CAN_RAW);

    strcpy(ifr.ifr_name, device);
    ioctl(s, SIOCGIFINDEX, &ifr);

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) != 0)
    {
        perror("Unable to bind to can interface");
        running = 0;
		exit(EXIT_FAILURE);
    }
	printf("can_packet: bound success\n");

	return ret;
}

void canusb_abort()
{
	running = 0;

    close(s);
	printf("can_packet: closed the scoket s, exit function\n");
}