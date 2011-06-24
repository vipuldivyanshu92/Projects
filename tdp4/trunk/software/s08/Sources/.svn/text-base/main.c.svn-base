#include <hidef.h> /* for EnableInterrupts macro */
#include <string.h>
#include "derivative.h" /* include peripheral declarations */

/*
 * Configuration
 */

#define SPI_BUFFER_SIZE 255

/*
 * Macros
 */
 
#define CANRID_11 (CANRIDR0 << 3) | (CANRIDR1 >> 5)
#define SPI_send(x)  (void)SPI_trans(x)  // Ignore return
#define SPI_rcv()    SPI_trans(0)        // Send dummy byte

/*
 * Global Variables
 */

static char SPI_Tx_buff[SPI_BUFFER_SIZE][11];
static volatile unsigned int read = 0;   //read index
static volatile unsigned int write = 0;  //write index

static int 		totalSent = 0;
static int 		size = 0;
static char *	dataptr;
static int 		index;
static int 		totalRecvd = 0;

/*
 * Interrupts
 */

//CAN receive interrupt handler
interrupt VectorNumber_Vcanrx void CAN_receive_interrupt(void)
{  
    //Set the values with respect to the specifications   
    /* packet[0][7-6] = STATUS
     * packet[0][5-0] = CAN_ID[11-5]
     * packet[1][7-3] = CAN_ID[4-0]
     * packet[1][2-0] = Don't care
     * packet[2][3-0] = CAN_DLC
     * packet[3-10]   = CAN_DATA
     */
    
    //get pointer to next write position in storage buffer 
    char *packet = &SPI_Tx_buff[write][0];
    
    //Light up!
    PTBD_PTBD0 = 1;
    
    //break CAN packet down to fit our protocol
    //Please see 'spi_timing.pdf' file for a full description of the protocol used  
    packet[0] = (1 << 6) | (((CANRID_11) >> 5) & 0x3F);
    packet[1] = (CANRID_11 & 0x1F) << 3;
    packet[2] = CANRDLR_DLC;
     
    (void)memcpy(&packet[3], &CANRDSR0, CANRDLR_DLC);
  
    // change the write position pointer
    write = (write + 1) % SPI_BUFFER_SIZE;
  
    // Reset CAN receive flag to receive next CAN packet
    // msCAN interrupts flags are cleared by writing a 1
    CANRFLG_RXF = 1;
    
    PTBD_PTBD0 = 0;
} 

/*
  Functions
*/


/*
  Name:	
  	initialiseCAN
  	
  Description:
  	Function to enable and set up the MSCAN module for use

*/
void initialiseCAN()
{
	//Initialise the CAN module
	CANCTL1_CANE = 1; //Enable CAN module
	CANCTL0_INITRQ = 1; //Start initialisation mode
	while(!CANCTL1_INITAK){} // Wait for acknowledgement of initalisiation
	//Entering initialisation mode
	CANCTL1 = 0xc0; //MSCAN clock is as the bus clock source
	CANBTR0 = 0x03; /* SJW = 1 Tq clock cycle, baud rate prescaler = 4 - CHECK THESE VALUES*/
	CANBTR1 = 0x58; /* SAMP = 0, TSEG2 = 6, TSEG1 = 9, 16 Tq per bit */
	CANIDAR0 = 0xFF; //Identifier acceptance register
	CANIDMR0 = 0xFF; //Not masking off the input identifier codes. Accept anything.
	CANIDMR1 = 0xFF;
	CANCTL0_INITRQ = 0; // Leave Initialisation mode
	while(CANCTL1_INITAK){} /* wait for ack of init mode exit */
	CANTBSEL = 0x01; //Select TX buffer 0
	CANRFLG = 0x40;  //Wake in interrupt
	CANRIER_RXFIE = 1; //Receive interrupt enable (RXF)
	CANTARQ = 0; // No abort request 
	CANTIER = 0; //Transmit interupt disabled
	while (!CANCTL0_SYNCH){}
		    
}

/**
Transmits data over the CAN bus.

can_id	     -  The CAN ID of this subsystem.
priority     -  CAN message priority (within the internal buffers)
data_length  -  Length of data being transmitted in bytes
data         -  A pointer to the data to be transmitted.

*/
void transmitCAN(unsigned long can_id, unsigned char priority,
  unsigned char data_length, unsigned char * data) {

  	//Local index variable
  	unsigned int i;
  	
  	//Light up!
  	PTBD_PTBD1 = 1;

  	//Set up CAN ID
  	CANTIDR0 = can_id >> 3;
    CANTIDR1 = can_id << 5;

    //Choose next free transmit buffer
    CANTBSEL = CANTFLG;

    //Set up data register
    for (i=0; i<data_length; ++i) {
      *(&CANTDSR0+i) = *(data+i);
    }

    //Set up length register
    CANTDLR = data_length;

	//Set up priority register
	CANTTBPR = priority;

    //Start transmission
    CANTFLG = 0x01;

    //Wait for transmission complete
    while(!CANTFLG_TXE0);
    
    PTBD_PTBD1 = 0;


}

/*
  Name:	
  	initialiseSPI
  	
  Description:
  	Function to enable and set up the SPI module for use
  	
  Paramaters:
  	enable_receive_int: 	boolean to enable or disable SPI receive interrupt (1 to enable)
  	enable_transmit_int:	boolean to enable or disable SPI transmit interrupt (1 to enable)
  	enable_master:			boolean to say what role this device plays. (1 for master, 0 for slave)
  	SPIClock_mode:			Specify Clock Mode value between 0 and 3, inclusive.
  							See SPI documentation on CPOL and CPHA for more info
*/

void initialiseSPI(int enable_receive_int, int enable_transmit_int, int enable_master, int SPIClock_mode){
 
 	//Initialise the SPI Module
	SPIC1_SPE = 1;  //Enable SPI module
	SPIC1_SPIE = enable_receive_int & 1; //Interrupts for receive buffer full enabled
	SPIC1_SPTIE = enable_transmit_int & 1;//Interrupts for transmit buffer empty enabled
	SPIC1_MSTR = enable_master & 1;
	SPIC1_SSOE = 1;
	SPIC2_MODFEN = 1;
	SPIC2_SPC0 = 0;
		
	SPIC1_CPOL = (SPIClock_mode >> 1) & 1;
	SPIC1_CPHA = SPIClock_mode & 1;
}

/*
  Name:	
  	SPI_trans
  	
  Description:
  	Function to simultaneously receive and send a byte over SPI
  	Use defined macros if you need to only receive or only send
  	
  Paramaters:
  	val: byte of data to be sent
  
  Return Value:
  	received SPI byte from SPID register
  */
byte SPI_trans(byte val)
{
   while(!(SPIS & SPIS_SPTEF_MASK)); // Wait until ready to send
   SPID = val;                         // Send SPI byte 
   while(!(SPIS & SPIS_SPRF_MASK) ); // Wait for transfer complete   
   return SPID;                        // Also clears flag
}

void main(void)
{
  unsigned char data = 0x00;
  unsigned char status = 0x00;
  int transmit = 1;  		//Boolean to indicate if the master wishes to receive
  int packetComplete = 0;   //Boolean to make sure at least a full packet is sent before tranmission is stopped
  int CAN11 = 0;	  		//Boolean to indiacte if a CAN11 packet is being received
  int stream = 0;
  //Variables to hold incoming CAN11 values before transmission
  unsigned long RxID;
  unsigned char RxDLC;
  unsigned char RxData[8];
  (void)memset(RxData, 0, 8); 
  
  //Initialise send SPI data pointer to 0
  *dataptr = 0;
  
  EnableInterrupts;
  SOPT1_COPT = 0;	//Disable Watchdog because it's useless
  PTDDD = 1;
  PTDD = 0;
  PTBDD = 0xFF;
   
  PTBD_PTBD0 = 0;
  PTBD_PTBD1 = 0;
  
  initialiseCAN();
  initialiseSPI(0,0,0,1);
  /* include your code here */
  
  for(;;) {
 
    //check for CAN buffer data first
    if ((read != write) && (transmit || (!packetComplete)))
    {
        //Send one byte (char) at a time, using static global vars instead of while loop         
        dataptr = (&SPI_Tx_buff[read][0]) + totalSent;
        stream = 1;        
        if (size == 0)
        {
        	packetComplete = 0;
             size = 3 + dataptr[2];
        }        
        if (totalSent < size)
        {
            totalSent++;
        } 
        if (totalSent == size)
        {
            //Reached the end of the struct, reset global statics.
            read = (read + 1) % SPI_BUFFER_SIZE;
            totalSent = 0;
            size = 0;
            packetComplete = 1;
        }
    }
    else
    {
        *dataptr = 0;
        if (stream)
        {
        	*dataptr = 0x03;  	//Send EOS byte after last packet if there are no more packets to send
        					    //This is highly unlikely to execute though....
        	stream = 0;
        }
    }
       
    data = SPI_trans(*dataptr);  //Simultaneously send and receive a byte over SPI

    //Handle SPI Receive
    //received data can be found in data variable
    //Please see 'spi_timing.pdf' file for a full description of the protocol used 
    if (!CAN11)
    {   
        status = (data & 0xC0)>>6;
        if (status == 0x00)
        {
            //Status = 00 means Command (CMD) packet recived
            if ((data & 0x3F) == 0x01)
            {
                //CMD Start
                transmit = 1;
            }
            else if ((data & 0x3F) == 0x02)
            {
                //CMD Stop
                transmit = 0;
            }
            CAN11 = 0;
        }
        else if (status == 0x01)
        {	
        	//Status = 01 means CAN packet incoming for outbound transmission over CAN bus
            CAN11 = 1;
            totalRecvd = 1; 
        }
    }
    if (CAN11)
    {
        if (totalRecvd == 1)
        {
        	//First CAN11 byte [7:6] = Status
        	//First CAN11 byte [5:0] = CAN11ID [10:5]
            RxID = ((data & 0x3F) << 5);            
            totalRecvd++;
        }
        else if(totalRecvd == 2)
        {
        	//Second CAN11 byte [7:3] = CAN11ID[4:0]
        	RxID |= ((data & 0xF8)>> 3);
            totalRecvd++;
        }
        else if(totalRecvd == 3)
        {
        	//Third CAN11 byte [3:0] = CAN_DLC
        	RxDLC = data & 0x0F;
        	totalRecvd++;	
        }
        else if(totalRecvd <= (RxDLC+3))
        {
        	//Add DLC incoming bytes to Data array before transmission
            RxData[index] = data;
            totalRecvd++;
            index++;
        }
        else
        {
        	//CAN packet has been fully received... Chocks away!!
            transmitCAN(RxID, 0, RxDLC, RxData);
            //reset variables to allow reading of more command packets
            CAN11 = 0;
            totalRecvd = 0;
            RxDLC = 0;
            RxID = 0;
            index = 0;
            (void)memset(RxData, 0, 8);   
        }
    }
    //__RESET_WATCHDOG();	/* feeds the dog woof woof bark*/
  } /* loop forever */
  /* please make sure that you never leave main */
}
