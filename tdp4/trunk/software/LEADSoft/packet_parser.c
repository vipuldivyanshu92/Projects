#include <stdint.h>
#include "packet_parser.h"

int16_t get_int16(uint8_t *data, int offset)
{
	return (data[offset] << 8 | data[offset + 1]);
}

uint16_t get_uint16(uint8_t *data, int offset)
{
	return (data[offset] << 8 | data[offset + 1]);
}

int32_t get_int32(uint8_t *data, int offset)
{
	return (data[offset] << 24)
			| (data[offset + 1] << 16)
			| (data[offset + 2] << 8)
			| (data[offset + 3]);
}

double get_small_decimal(uint8_t *data, int offset)
{
	int ipart = get_int16(data, offset);
	double fpart = get_int16(data, offset + 2) / 10000;

	return ipart + fpart;
}

double get_large_decimal(uint8_t *data, int offset)
{
	int ipart = get_int32(data, offset);
	double fpart = get_int32(data, offset + 4);

	return ipart + fpart;
}