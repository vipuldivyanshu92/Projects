#include <linux/spi/spidev.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <SDL/SDL_mutex.h>
#include <time.h>
#include "LinkedList.h"
#include "can.h"

static char *device;
static uint8_t mode;
static uint8_t bits;
static uint32_t speed;
static uint16_t delay;
static LinkedList *store = NULL;
static SDL_mutex  *store_lock;
static int fd;
static int running;
static void (*callback)(packet_info_t*);
uint8_t rx, tx;

enum spi_commands
{
	CMD_NULL,
	CMD_START,
	CMD_STOP,
	CMD_EOS,
};

enum spi_write_states
{
	START_WRITE,
	D11_WRITE_ID,
	WRITE_DLC,
	WRITE_DATA,
	WRITE_EOS,
	WRITE_DONE
};

enum spi_read_states
{
	START_READ,
	D11_READ_ID,
	READ_DLC,
	READ_DATA,
	READ_DONE
};

static void pabort(const char *s)
{
	perror(s);
	abort();
}

static void transfer(int fd, uint8_t *tx_buffer, uint8_t *rx_buffer, size_t size)
{
	int ret;

	struct spi_ioc_transfer tr = {
		.tx_buf = (unsigned long)tx_buffer,
		.rx_buf = (unsigned long)rx_buffer,
		.len = size,
		.delay_usecs = delay,
		.speed_hz = speed,
		.bits_per_word = bits,
	};

	ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
	if (ret < 1)
		pabort("can't send spi message");
}

int can_data_read()
{
	// variables to hold the current state of the transfer process
	enum spi_write_states write_state = START_WRITE;
	enum spi_read_states read_state = START_READ;

	int data_written = 0; // holds the amount of data that has been transfered given a dlc
	int data_read = 0;		/* holds the amount of data that has been transfered given a dlc */

	packet_info_t *write_packet_info = NULL;
	packet_info_t read_packet_info;

	/* send a command start byte */
	tx = CMD_START;
	transfer(fd, &tx, &rx, 1);

	while(running)
	{
                switch(write_state)
		{
			case(START_WRITE):
				//get data from the store to be read
				SDL_mutexP(store_lock);
				write_packet_info = ll_get(store);
				SDL_mutexV(store_lock);

				if(!write_packet_info)
				{
					//leave the state as state start_write;
					tx = CMD_NULL;
				}
				else if(write_packet_info->op == CMD)
				{
					// Not used at the moment
				}
				else if(write_packet_info->op == D11)
				{
					//package the command and 6 bits of CAN_ID
					tx = (((write_packet_info->op) << 6) | ((write_packet_info->can_id) >> 5) & 0x3F);
					write_state = D11_WRITE_ID;
				}
				break;

			case(D11_WRITE_ID): // specific to D11. D29 would need to have another state(s) for fully writing its CAN_ID bytes
				tx = (write_packet_info->can_id) << 3; //take the can_id lower order 5 bits and shift 3
				write_state = WRITE_DLC;
				break;

			case(WRITE_DLC):
				//tx = the dlc of the struct
				tx = write_packet_info->dlc;
				write_state = WRITE_DATA;
				break;

			case(WRITE_DATA):
				tx = ((char *) write_packet_info->data)[data_written];
				if(data_written + 1 == write_packet_info->dlc)
					write_state = WRITE_DONE; //write_state = write_EOS;
				else
					data_written ++;
				break;

			case(WRITE_DONE):
				free(write_packet_info);
				data_written = 0;
				tx = CMD_NULL;
				write_state = START_WRITE;
				break;
		}

		transfer(fd, &tx, &rx, 1);

		switch(read_state)
		{
			case(START_READ):
				// if the command was a D11
				if((rx >> 6) == D11)
				{
					read_packet_info.can_id = (rx & 0x3F) << 5;
					read_state = D11_READ_ID;
				}
				break;
			case(D11_READ_ID): // special to D11. D29 would need to have another state(s) for fully writing its CAN_ID bytes
				read_packet_info.can_id |= rx >> 3;
				read_state = READ_DLC;
				break;

			case(READ_DLC):
				read_packet_info.dlc = rx;
				read_state = READ_DATA;
				break;

			case(READ_DATA):
				read_packet_info.data[data_read] = rx;
				if(data_read + 1 == read_packet_info.dlc)
				{
					read_state = START_READ;
					data_read = 0;
					
					callback(&read_packet_info);
					/*
					switch(read_packet_infocan_id)
					{
						case 0x1A0:
							value = data_buff[0];// << 8 | frame.data[1];
							sprintf(text,"%d", value);
							update_label(&gear_value,text,0);
							break;
					}
					*/
				}
				else
					data_read++;

				break;
		}
	}

	tx = CMD_STOP;
	transfer(fd, &tx, &rx, 1);
	return 0;

}

void can_queue_packet(packet_info_t *p)
{
	SDL_mutexP(store_lock);
	ll_add(store, p);
	SDL_mutexV(store_lock);
}

int can_init(char *dev, uint8_t m, uint8_t b, uint32_t s, uint16_t d,
	void (*callb)(packet_info_t *p))
{
	int ret;

	// Initialise SPI specifications
	device = dev;
	mode = m;
	bits = b;
	speed = s;
	delay = d;
	callback = callb;

	store_lock = SDL_CreateMutex();

	//
	running = 1;
        

	// Create the link list containing output datas
	store = ll_create();

	if(!store)
		pabort("could not create linked list");

	fd = open(device, O_RDWR);
	if (fd < 0)
		pabort("can't open device");

	/*
	 * spi mode
	 */
	ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
	if (ret == -1)
		pabort("can't set spi mode");

	ret = ioctl(fd, SPI_IOC_RD_MODE, &mode);
	if (ret == -1)
		pabort("can't get spi mode");

	/*
	 * bits per word
	 */
	ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
	if (ret == -1)
		pabort("can't set bits per word");

	ret = ioctl(fd, SPI_IOC_RD_BITS_PER_WORD, &bits);
	if (ret == -1)
		pabort("can't get bits per word");

	/*
	 * max speed hz
	 */
	ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
	if (ret == -1)
		pabort("can't set max speed hz");

	ret = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
	if (ret == -1)
		pabort("can't get max speed hz");

	return ret;
}

void can_abort()
{
	running = 0;
}

