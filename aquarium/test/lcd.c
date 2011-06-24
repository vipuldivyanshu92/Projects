#include <delays.h>
#include "lcd.h"

#define LCD_DB4	PORTAbits.RC4
#define LCD_DB5	PORTAbits.RC5
#define LCD_DB6	PORTAbits.RC6
#define LCD_DB7	PORTAbits.RC7

#define LCD_E	PORTCbits.RA0
#define LCD_RS	PORTCbits.RA2
#define LCD_RW	PORTCbits.RA1

#define LED	   PORTAbits.RA6

#define LCD_TYPE		2
#define	LCD_LINE_TWO	0x40

char const LCD_INIT_STRING[4] = {
	0x20 | (LCD_TYPE << 2),
	0x0C,
	1,
	6
};

void delay_us(unsigned char t)
{
	char i;
	for (i = 0; i < t; i++)
	{
		Delay10TCYx(1);
		Delay1TCY();
		Delay1TCY();
		Delay1TCY();
		Delay1TCY();
		Delay1TCY();
		Delay1TCY();
	}
}

void delay_ms(unsigned char t)
{
	char i;
	for (i = 0; i < t; i++)
		Delay1KTCYx(16);
}

void delay_sec(unsigned char t)
{
	char i;
	for (i = 0; i < t * 1000; i++)
		delay_ms(1);
}

void lcd_send_nibble(char nibble)
{
	LCD_DB4 = !!(nibble & 1);
	LCD_DB5 = !!(nibble & 2);
	LCD_DB6 = !!(nibble & 4);
	LCD_DB7 = !!(nibble & 8);

	Delay1TCY();
	LCD_E = 1;
	delay_us(2);
	LCD_E = 0;
}

/*
char lcd_read_nibble(void)
{
	char retval = 0;

	LCD_E = 1;
	Delay1TCY();

	retval |= LCD_DB4;
	retval |= LCD_DB5 << 1;
	retval |= LCD_DB6 << 2;
	retval |= LCD_DB7 << 3;

	LCD_E = 0;

	return retval;
}
*/

/*
char lcd_read_byte(void)
{
	char low;
	char high;

	LCD_RW = 1;
	Delay1TCY();
	
	high = lcd_read_nibble();
	low = lcd_read_nibble();

	return ((high << 4) | low);
}
*/

void lcd_send_byte(char address, char n)
{
	LCD_RS = 0;

	LED = 0;
	delay_us(60);
	LED = 1;

	if (address)
		LCD_RS = 1;
	else
		LCD_RS = 0;

	Delay1TCY();

	//LCD_RW = 0;
	//Delay1TCY();

	LCD_E = 0;

	lcd_send_nibble(n >> 4);
	lcd_send_nibble(n & 0x0F);
}

void lcd_init(void)
{
	/*char i;

	LCD_RS = 0;
	//LCD_RW = 0;
	LCD_E = 0;

	delay_ms(15);

	for (i = 0; i < 3; i++)
	{
		lcd_send_nibble(0x03);
		delay_ms(5);
	}

	lcd_send_nibble(0x02);

	for (i = 0; i < sizeof(LCD_INIT_STRING); i++)
	{
		lcd_send_byte(0, LCD_INIT_STRING[i]);
		delay_ms(5);
	}*/

//	LCD_RS = 0;
	LCD_E = 0;
	LED = 1;
	//delay_sec(2);
	//LED = 0;
	//LCD_E = 1;
}

void lcd_gotoxy(char x, char y)
{
	char address;

	if (y != 1)
		address = LCD_LINE_TWO;
	else
		address = 0;

	address += x-1;
	lcd_send_byte(0, 0x80 | address);
}

void lcd_putc(char c)
{
	switch(c)
	{
		case '\f':
			lcd_send_byte(0, 1);
			delay_ms(2);
			break;

		case '\n':
			lcd_gotoxy(1, 2);
			break;

		case '\b':
			lcd_send_byte(0, 0x10);
			break;

		default:
			lcd_send_byte(1, c);
			break;
	}
}

/*
char lcd_getc(char x, char y)
{
	char value;

	lcd_gotoxy(x, y);

	// Wait until busy flag is low.
	while(!!(lcd_read_byte() & 0x80))
		;

	LCD_RS = 1;
	value = lcd_read_byte();
	LCD_RS = 0;

	return value;
}
*/