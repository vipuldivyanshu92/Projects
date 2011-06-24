#include <p18f25k80.h>
#include <delays.h>

#define LED		PORTAbits.RA6

void mcu_init(void)
{
	// Disable the Analog converter
	ANCON1 = 0b00000000;

	// Set PORTA as output
	TRISA = 0x00;

	// Set PORTC as output
	//TRISC = 0x00;
}

void main(void)
{
	mcu_init();

	LED = 1;

	for (;;)
	{
	}
}