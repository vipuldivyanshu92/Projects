/* 
 * File:   canusb.h
 * Author: adraen
 *
 * Created on 28 April 2011, 09:42
 */

#ifndef CANUSB_H
#define	CANUSB_H

#ifdef	__cplusplus
extern "C" {
#endif

#ifndef PACKET_INFO_T
#define PACKET_INFO_T
typedef struct
{
	unsigned char op;
	unsigned int can_id;
	unsigned char dlc;
	unsigned char data[8];
} packet_info_t;
#endif


int canusb_data_read();
void canusb_queue_packet(packet_info_t *p);
int canusb_init(char *dev, void (*callb)(packet_info_t *p));
void canusb_abort();


#ifdef	__cplusplus
}
#endif

#endif	/* CANUSB_H */

