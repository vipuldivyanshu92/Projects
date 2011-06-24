#include <18F25K80.h> 
#fuses INTRC_IO,NOWDT,NOPROTECT,PUT 
#use delay(clock=16MHZ) 

/*
 * LCD Configuration
 */
#define LCD_DB4      PIN_B4
#define LCD_DB5      PIN_B5 
#define LCD_DB6      PIN_B6
#define LCD_DB7      PIN_B7

#define LCD_E        PIN_C2
#define LCD_RS       PIN_C5
#define LCD_RW       PIN_C4

#define LCD_TYPE     2        // 0=5x7, 1=5x10, 2=2 lines 
#define LCD_LINE_TWO 0x40 // LCD RAM address for the 2nd line 

/*
 *
 */
#define BUZZER      PIN_A7 
#define LED         PIN_A6 

/*
 *
 */
#define DEVID1_ADDR 0x3FFFFEL
#define DEVID2_ADDR 0x3FFFFFL

/*
 *
 */


int8 const LCD_INIT_STRING[4] = 
{ 
   0x20 | (LCD_TYPE << 2), // Func set: 4-bit, 2 lines, 5x8 dots 
   0xc,                    // Display on 
   1,                      // Clear display 
   6                       // Increment cursor 
}; 

void lcd_send_nibble(int8 nibble) 
{ 
   // Note:  !! converts an integer expression 
   // to a boolean (1 or 0). 
   output_bit(LCD_DB4, !!(nibble & 1)); 
   output_bit(LCD_DB5, !!(nibble & 2));  
   output_bit(LCD_DB6, !!(nibble & 4));    
   output_bit(LCD_DB7, !!(nibble & 8));    
    
   delay_cycles(1); 
   output_high(LCD_E); 
   delay_us(2); 
   output_low(LCD_E); 
} 

void lcd_send_byte(int8 address, int8 n) 
{ 
   output_low(LCD_RS); 
   delay_us(60);  
    
   if(address) 
      output_high(LCD_RS); 
   else 
      output_low(LCD_RS); 
         
   delay_cycles(1); 
    
   output_low(LCD_E); 
    
   lcd_send_nibble(n >> 4); 
   lcd_send_nibble(n & 0xf); 
} 

void lcd_init(void) 
{ 
   int8 i; 

   output_low(LCD_RS); 
   output_low(LCD_E); 

   delay_ms(15); 

   for(i=0 ;i < 3; i++) 
   { 
      lcd_send_nibble(0x03); 
      delay_ms(5); 
   } 

   lcd_send_nibble(0x02); 

   for(i=0; i < sizeof(LCD_INIT_STRING); i++) 
     { 
       lcd_send_byte(0, LCD_INIT_STRING[i]); 
       
       delay_ms(5); 
   } 
} 

void lcd_gotoxy(int8 x, int8 y) 
{ 
   int8 address; 
    
   if(y != 1) 
      address = LCD_LINE_TWO; 
   else 
      address=0; 
    
   address += x-1; 
   lcd_send_byte(0, 0x80 | address); 
} 

void lcd_putc(char c) 
{ 
    switch(c) 
   { 
       case '\f': 
         lcd_send_byte(0,1); 
         delay_ms(2); 
         break; 
       
       case '\n': 
          lcd_gotoxy(1,2); 
          break; 
       
       case '\b': 
          lcd_send_byte(0,0x10); 
          break; 
       
       default: 
          lcd_send_byte(1,c); 
          break; 
   } 
} 


#INT_TIMER0 
void timer0_isr() 
{ 
   output_toggle(BUZZER); 
}


// Frequency of interrupt (clock/(4*divisor)) / (256-reload) 
void mcu_init() 
{ 
   setup_oscillator(OSC_16MHZ); 
   setup_adc_ports(NO_ANALOGS); 
   setup_adc(ADC_OFF); 
   setup_comparator(NC_NC_NC_NC); 

 
   // Setup the TIMER0 Interrupt 
   set_timer0(0); 
   setup_timer_0(RTCC_INTERNAL | RTCC_8_BIT | RTCC_DIV_4); 
   enable_interrupts(INT_TIMER0); 
   enable_interrupts(GLOBAL); 

   set_tris_a(0);
   set_tris_b(0);
   set_tris_c(0);
}

void main() 
{
    char devid1, devid2; 
    int16 unique_id;

    mcu_init();    
    //output_high(BUZZER);
    
    output_high(LED); 
    
    //lcd_init();
    /*    
    devid1 = read_program_eeprom(DEVID1_ADDR);
    devid2 = read_program_eeprom(DEVID2_ADDR);
    unique_id = ((devid1 & 0xE0) >> 5) | ((int16)devid2 << 3);*/

    //printf(lcd_putc, "\f%Lu", unique_id);

    //
   while (1) 
   {
        /*printf(lcd_putc, "\f\xc7Hello \nCharles");
        delay_ms(1000);
        printf(lcd_putc, "\fPGM !!!!");
        delay_ms(1000);
        printf(lcd_putc, "\f J'aime \n");
        delay_ms(1000);
        printf(lcd_putc, "\f les \n FRITES");
        delay_ms(1000);*/

      enable_interrupts(INT_TIMER0); 
   } 
} 