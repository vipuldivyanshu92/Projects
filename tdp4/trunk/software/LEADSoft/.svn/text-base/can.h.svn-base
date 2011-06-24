/* 
 * File:   can.h
 * Author: adraen
 *
 * Created on 20 April 2011, 12:34
 */

#ifndef CAN_H
#define	CAN_H

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

enum spi_status
{
	CMD,
	D11,
	D29,
};

int can_data_read();

int can_init(char *dev, uint8_t m, uint8_t b, uint32_t s, uint16_t d,
        void (*callback)(packet_info_t *p));

void can_abort();

#ifdef	__cplusplus
}
#endif

#endif	/* CAN_H */

