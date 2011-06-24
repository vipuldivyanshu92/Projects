#include <p18f25k80.h>

#pragma config XINST  = OFF
#pragma config WDTEN  = OFF
#pragma config FOSC   = INTIO2
#pragma config CANMX  = PORTC
#pragma config PLLCFG = OFF

#define TRIS_CAN_TX TRISCbits.TRISC6
#define TRIS_CAN_RX TRISCbits.TRISC7

#define TRIS_LED TRISAbits.TRISA6
#define LED      LATAbits.LATA6

#define CAN_CONFIG_MODE 0b100
#define CAN_NORMAL_MODE 0b000

#define INPUT   1
#define OUTPUT  0

void mcu_init(void)
{
    // Set the internal clock to 16mHz
    OSCCONbits.IRCF = 0b111;

    // Set the PORTA 
    LED = 0;
    TRIS_LED = OUTPUT;
}

void can_init(void)
{
    // Set initial LAT and TRIS bits for RX Can
    LATC = 0;
    TRIS_CAN_RX = INPUT;

    // Set ECAN module in configuration mode
    CANCONbits.REQOP = CAN_CONFIG_MODE;
    while (CANCONbits.REQOP != CAN_CONFIG_MODE)
        ;

    // Set ECAN module
    ECANCONbits.MDSEL = 0b10;
    ECANCONbits.FIFOWM = 1;
    ECANCONbits.EWIN = 0b10010;

    // Setup the Baud Rate
    BRGCON1 = 0xc3;
    BRGCON2 = 0x9e;
    BRGCON3 = 0x03;
    /*BRGCON1 = 0b11001001;
    BRGCON2 = 0b10011110;
    BRGCON3 = 0b00000011;*/

    //
    RXB0CON = 0;
    RXB0CONbits.RXM1 = 1;

    RXB1CON = 0;
    RXB1CONbits.RXM1 = 1;

    CIOCONbits.ENDRHI = 0;
    CIOCONbits.CANCAP = 1;
    CIOCON |= 0x01;

    // Set ECAN module in normal mode
    CANCONbits.REQOP = CAN_NORMAL_MODE;
    while (CANCONbits.REQOP != CAN_NORMAL_MODE)
        ;
}

void main(void)
{
    mcu_init();
    can_init();

    // Send a CAN packet

    TXB0CONbits.TXREQ = 0;
    TXB0SIDH = 0x1A;
    TXB0SIDLbits.SID = 3;
    TXB0DLCbits.DLC = 0;
    TXB0CONbits.TXREQ = 1;

    LED = 1;
    while (1)
    {
    }
}