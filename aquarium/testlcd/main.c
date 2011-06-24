#include <p18f25k80.h>
#include <timers.h>
#include <delays.h>

#pragma config XINST  = OFF
#pragma config WDTEN  = OFF
#pragma config FOSC   = INTIO2
#pragma config PLLCFG = OFF

#define TRIS_LCD_DATA   TRISC
#define TRIS_LCD_RW     TRISAbits.TRISA0
#define TRIS_LCD_E      TRISAbits.TRISA1
#define TRIS_LCD_RS     TRISAbits.TRISA2

#define TRIS_LED        TRISAbits.TRISA6
#define LED             LATAbits.LATA6

#define LCD_DATA        LATC
#define LCD_RW          PORTAbits.RA0
#define LCD_E           PORTAbits.RA1
#define LCD_RS          PORTAbits.RA2

#define INPUT   1
#define OUTPUT  0

void timer0_isr(void);

volatile unsigned int ms_ticks = 0;

void high_ISR(void)
{
    _asm goto timer0_isr _endasm
}

#pragma interrupt timer0_isr
void timer0_isr(void)
{
    INTCON1bits.TMR0IF = 0;
    WriteTimer0(6);

    ms_ticks++;
}

void lcd_write(unsigned char rs, unsigned char data)
{
    LCD_RS = rs & 1;
    LCD_RW = 0;
    LCD_DATA = data;

    Delay10TCYx(1);
    LCD_E = 1;
    Delay10TCYx(1);
    LCD_E = 0;
    Delay10TCYx(1);
}

void mcu_init(void)
{
    // Set the internal clock to 16mHz
    OSCCONbits.IRCF = 0b111;

    // Set the Latch values to 0
    LCD_DATA = 0;
    LCD_RW = 0;
    LCD_E = 0;
    LCD_RS = 0;
    LED = 0;

    // Set the Data direction registers
    TRIS_LCD_DATA = 0;
    TRIS_LCD_RW = OUTPUT;
    TRIS_LCD_E = OUTPUT;
    TRIS_LCD_RS = OUTPUT;
    TRIS_LED = OUTPUT;

    // init lcd sequence
    ms_ticks = 0;
    while (ms_ticks < 15);
    lcd_write(0, 0b00110000);

    ms_ticks = 0;
    while (ms_ticks < 5);
    lcd_write(0, 0b00110000);

    ms_ticks = 0;
    while (ms_ticks < 2);
    lcd_write(0, 0b00110000);

    ms_ticks = 0;
    while (ms_ticks < 2);
    lcd_write(0, 0b00111000);
    lcd_write(0, 0b00001000);
    lcd_write(0, 0b00000001);
    lcd_write(0, 0b00000110);

    lcd_write(1, 60);
}

void main(void)
{
    // Timers
    OpenTimer0(TIMER_INT_ON & T0_8BIT & T0_SOURCE_INT & T0_PS_1_16);
    WriteTimer0(6);
    RCONbits.IPEN = 1;
    RCONbits.SBOREN = 0;
    INTCON = 0b10000000;
    INTCON2bits.TMR0IP = 1;
    INTCONbits.TMR0IE = 1;

    //
    mcu_init();

    //
    LED = 1;

    for (;;)
    {
    }
}