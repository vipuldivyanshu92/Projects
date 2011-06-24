#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <linux/can.h>
#include <net/if.h>

#define BUFFER_SIZE 4096

int id_table[100][2];
int id_table_count = 0;

void read_packets(char *filename)
{
    int fp;
    char buffer[BUFFER_SIZE];
    char *pchr;
    
    fp = open(filename, O_RDONLY);
    if (fp == -1)
        perror("Unable to open file");

    // Read the entire content of the file, buggy if file bigger than 4k
    read(fp, &buffer, BUFFER_SIZE);
    buffer[BUFFER_SIZE - 1] = 0;

    // Parse the content of the file
    int id;
    int count;
    pchr = strtok(&buffer, "\n");
    while (pchr != NULL)
    {
        if (!(strlen(pchr) == 0 || pchr[0] == '#'))
        {
            sscanf(pchr, "%d %d", &id, &count);
            id_table[id_table_count][0] = id;
            id_table[id_table_count][1] = count;
            id_table_count++;
        }
        pchr = strtok(NULL, "\n");
    }    
}

int main(int argc, char *argv[])
{
    int s;
    int pid;
    int i;
    unsigned int delay;
    ssize_t n;
    struct sockaddr_can addr;
    struct can_frame frame;
    struct ifreq ifr;

    if (argc != 3)
    {
        printf("Usage:\n");
        printf("\t ./cansend <filename> <packets per second>\n");
        return EXIT_SUCCESS;
    }

    // Establish the connection to the virtual can adapter
    s = socket(PF_CAN, SOCK_RAW, CAN_RAW);

    strcpy(ifr.ifr_name, "vcan0");
    ioctl(s, SIOCGIFINDEX, &ifr);

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) != 0)
        perror("Unable to bind to vcan0");

    // Init the random number generator
    srand(stime(NULL));

    // Load the id definitions
    read_packets(argv[1]);

    // Calculate delay
	int pps = atoi(argv[2]);
    delay = 1000000 / pps;

    // Send random packets
    printf("Sending packet press ^C to quit, verbose disabled\n");
    while (1)
    {
        // generate a random packet
        pid = rand() % id_table_count;
        frame.can_id = id_table[pid][0];
        frame.can_dlc = id_table[pid][1];
        for (i = 0; i < frame.can_dlc; i++)
            frame.data[i] = rand() % 256;

        // write the packet to the stream
        n = write(s, &frame, sizeof(frame));
//        printf("Sent ID %d DLC %d\n", frame.can_id, frame.can_dlc);
        usleep(delay);
    }
    
    // Close the connection
    close(s);

    return EXIT_SUCCESS;
}
