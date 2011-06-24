#include <pic.h>

__CONFIG(WDTDIS & PWRTEN & MCLRDIS & BORDIS & HS & LVPDIS);

unsigned char transmit = 'a';

interrupt isr(void)
{
	/* RCIF = 0, buffer full
	 * RCIF = 1, buffer empty
	 */
	if (RCIF)
	{
		TXREG = RCREG;
	}

	/* TXIF = 0, buffer is empty
	 * TXIF = 1, buffer is full
	 */
	if (!TXIF)
	{
		// buffer is empty send something
	}		
	//TXREG = transmit++;
}

void reset(void)
{
	// Disable comparator and enable pins for I/O
	CMCON = 0x07;

	//
	OPTION = 0b11000000;

	// 
	INTCON = 0b11000000;
	PIE1 = 0b0011000;

	//
	PORTA = 0;
	PORTB = 0;
	TRISA = 0b11111110;
	TRISB = 0b11111011;

	// UART configuration
	/*TXREG = 0;
	SPBRG = 129;
	TXSTA = 0b00100110;
	RCSTA = 0b10010000;*/
}

void main(void)
{
	reset();
	TRISA = 0;
	RA0 = 1;
	//RA0 = 1;
	//TXREG = transmit;
	for (;;)
	{
		
	}
}