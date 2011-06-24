/* 
 * File:   main.c
 * Author: adraen
 *
 * Created on 20 April 2011, 15:41
 */

#include <stdio.h>
#include <stdlib.h>

typedef struct
{
	unsigned char op;
	unsigned int can_id;
	unsigned char dlc;
	unsigned char data[8];
} packet_info_t;

/*
 * 
 */
int main(int argc, char** argv)
{
	packet_info_t packet;
	FILE *fp;
	int i;

	if (argc != 2)
	{
		printf("Usage: %s can.log\n", argv[0]);
		return (EXIT_FAILURE);
	}

	if (!(fp = fopen(argv[1], "r")))
	{
		perror("Error opening ");
		return (EXIT_FAILURE);
	}

	while (fread(&packet, sizeof(packet_info_t), 1, fp))
	{
		printf("ID: %02X\tDLC: %d\tDATA: ", packet.can_id, packet.dlc);
		for (i = 0; i < packet.dlc; i++)
			printf("%02X ", packet.data[i]);
		printf("\n");
	}


	return (EXIT_SUCCESS);
}

