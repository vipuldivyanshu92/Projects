#include <p18f25k80.h>
#include <delays.h>

#include "lcd.h"

#pragma config XINST = OFF
#pragma config WDTEN = OFF

#define LED PORTAbits.RA6

void mcu_init(void)
{
	// Disable the Analog converter
	ANCON1 = 0x00;

	// Set PORTA as output
    LATA = 0;
	TRISA = 0x00;

	// Set PORTC as output
    LATC = 0;
	TRISC = 0x00;
}

void main(void)
{
	// Initialise the mcu
	mcu_init();

	//
	lcd_init();

	// Switch on the LED
	LED = 1;

	while (1)
	{
		lcd_putc('t');
	}
}