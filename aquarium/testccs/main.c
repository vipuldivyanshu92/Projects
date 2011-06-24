#include <18F25K80.h>
#fuses INTRC_IO,NOWDT,NOPROTECT,PUT,BROWNOUT
#use delay(clock=8MHZ)

#include "ecan.h"

#define BUZZER		PIN_A7
#define LED			PIN_A6

/*
// Frequency of interrupt (clock/(4*divisor)) / (256-reload)
#INT_TIMER0
void timer0_isr()
{
	output_toggle(BUZZER);
}
*/

void buzzer_enable()
{
	// Setup the TIMER0 Interrupt
	set_timer0(0);
	setup_timer_0(RTCC_INTERNAL | RTCC_8_BIT | RTCC_DIV_4);
	enable_interrupts(INT_TIMER0);
	enable_interrupts(GLOBAL);
}

void mcu_init()
{
	setup_oscillator(OSC_8MHZ);
	setup_adc_ports(NO_ANALOGS);
	setup_adc(ADC_OFF);
	setup_comparator(NC_NC_NC_NC);

	//buzzer_enable()

	output_a(0);
	set_tris_a(0);
}

void main()
{
	mcu_init();

	output_high(LED);

	while (1)
	{
	}
}