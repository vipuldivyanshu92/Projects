/*
 * TODO:
 

 * do the blink too
 *
 * talk about config in report as in menu config
 * check all the warning levels and see if they are working!
 * remove debug prints and silly comments
 */
//TODO entering menu shows some bugs

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <linux/types.h>

#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <SDL/SDL_ttf.h>
#include <SDL/SDL_thread.h>
#include <SDL/SDL_mutex.h>

#include "config.h"
#include "widget.h"
#include "can.h"
#include "canusb.h"
#include "packet_parser.h"
#include "can_packets.h"
#include "logging.h"

#define DELAY               100
#define MAX_BLINK_LENGTH    10

Uint32 background_color;

/* SDL variables */
SDL_mutex   *lock;
SDL_mutex   *logger_lock;
SDL_Surface *screen;
SDL_Event ev;
SDL_Thread *read_thread;
SDL_Thread *input_thread;

/* GUI Widget variables*/
bar_graph_t rpm_graph, fuel_graph, gear_shift_charge;
label_t rpm_value, rpm_label;
label_t spd_value, spd_label;
label_t gear_value, gear_label;
label_t engine_temp, engine_degrees;
label_t engine_temp_label, engine_label;

icon_t engine_light;
icon_t fuel_icon;
icon_t coolant_icon;
icon_t bullet_icon;


/* General global variables */
static int running = 1;
static int in_menu;
static int max_rpm;
static int eng_temp_warn_lev;
static int coolant_temp_warn_lev;
static int fuel_low_warn_lev;
static int oil_temp_warn_lev;
static int speed_source; //{road_speed = 0, wheel_speed = 1, gps_speed = }
static int logenable;
static int can_enabled = 1;
static int canusb;

/* SPI configuration */
static char *device = "/dev/spidev1.1";
static uint8_t mode = 1;
static uint8_t bits = 8;
static uint32_t speed = 100000;
static uint16_t delay;

char *logfile;
config_t config;

/*
 * Initialise SDL modules
 */
int modules_init()
{
    int success = 0;

    // Initialise SDL, SDL_Image, SDL_TTF
    success |= SDL_Init(SDL_INIT_VIDEO | SDL_INIT_NOPARACHUTE) == -1;
    success |= IMG_Init(IMG_INIT_PNG) != IMG_INIT_PNG;
    success |= TTF_Init() == -1;

    return success;
}

/*
 * Unload the SDL modules
 */
void modules_quit()
{
    TTF_Quit();
    IMG_Quit();
    SDL_Quit();
}

/*
 *
 */
int gui_init()
{
    //intialize values
    init_bar_graph(&rpm_graph, "resources/rpm_graph_full.png", "resources/rpm_graph_empty.png", 150, 50, max_rpm, 0);
    init_bar_graph(&fuel_graph, "resources/fuel_full.png", "resources/fuel_empty.png", 0, 50, 100, 1);
        init_bar_graph(&gear_shift_charge, "resources/gear_shift_charge_full.png","resources/gear_shift_charge_empty.png",465,350,255,1);
        
    init_label(&rpm_value, "00000", "resources/DS-DIGI.TTF", 80, 0xDF394B, 550, 75);
    init_label(&rpm_label, "RPM", "resources/DS-DIGI.TTF", 50, 0xDF394B, 675, 160);
    init_label(&spd_value, "000", "resources/DS-DIGI.TTF", 180, 0xB3CE4B, 200, 160);
    init_label(&spd_label, "MPH", "resources/DS-DIGI.TTF", 80, 0xB3CE4B, 520, 230);
    init_label(&gear_value, "N", "resources/DS-DIGI.TTF", 120, 0xB3CE4B, 400, 325);
    init_label(&gear_label, "GEAR", "resources/DS-DIGI.TTF", 50, 0xDF394B, 400, 440);
        init_label(&engine_temp, "00", "resources/DS-DIGI.TTF", 80, 0xDF394B, 0, 390);
        init_label(&engine_degrees, "OC", "resources/DS-DIGI.TTF", 27, 0xDF394B, 80, 400);
        init_label(&engine_label, "ENGINE", "resources/DS-DIGI.TTF", 40, 0xDF394B, 110, 400);
        init_label(&engine_temp_label, "TEMP", "resources/DS-DIGI.TTF", 40, 0xDF394B, 110, 430);
        

    //init icons
    init_icon(&engine_light, "resources/engine_oil_full.png", "resources/engine_oil_empty.png", 1, 700, 375);
    init_icon(&fuel_icon, "resources/fuel_icon_full.png", "resources/fuel_icon_empty.png", 1, 35, 280);
    init_icon(&coolant_icon, "resources/coolant_full.png", "resources/coolant_empty.png",1,640, 375);
    return 0;
}

/*
 *
 */
void gui_refresh()
{
    update_bar_graph(&rpm_graph, -1, 1);
    update_bar_graph(&fuel_graph, -1, 1);
        update_bar_graph(&gear_shift_charge, -1, 1);

    update_label(&rpm_value, NULL, 0);
    update_label(&rpm_label, NULL, 0);
    update_label(&spd_value, NULL, 0);
    update_label(&spd_label, NULL, 0);
    update_label(&gear_value, NULL, 0);
    update_label(&gear_label, NULL, 0);
        update_label(&engine_temp, NULL, 0);
        update_label(&engine_degrees, NULL, 0);
        update_label(&engine_label, NULL, 0);
        update_label(&engine_temp_label, NULL, 0);

    update_icon(&engine_light, -1, 0);
    update_icon(&fuel_icon, -1, 0);
    update_icon(&coolant_icon, -1, 0);
}

/*
 * Fill a rectangle with the background color
 * PARAMETERS:
 *    x            : x top left corner
 *    y            : y top left corner
 *    w            : width of the rectangle
 *    h            : height of the rectangle
 */
void fill_with_bgcolor(int x, int y, int w, int h)
{
    SDL_Rect dst;
    dst.x = x;
    dst.y = y;
    dst.w = w;
    dst.h = h;

    SDL_FillRect(screen, &dst, background_color);
    SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);
}

int draw_menu_box(int x, int y, int w, int h)
{
    SDL_Rect dst;

    //create a white rectangle on screen
    dst.x = x-1;
    dst.y = y-1;
    dst.w = w+2;
    dst.h = h+2;

    SDL_FillRect(screen, &dst, 0xFFFFFF);
    SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);

    //place black rectangle inside of white one
    dst.x = x;
    dst.y = y;
    dst.w = w;
    dst.h = h;

    SDL_FillRect(screen, &dst, background_color);
    SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);

    return 0;
}

void change_speed_source()
{
    int x = 450;
    int y = 147;

    char c[2];
    sprintf(c, "%d", speed_source);
    label_t digit;
    init_label(&digit, c, "resources/DS-DIGI.TTF", 30, 0xDF394B, x, y);

    SDL_PumpEvents();
    while(SDL_WaitEvent(&ev))
    {
        switch(ev.type)
        {
        case SDL_KEYUP:
            if(ev.key.keysym.sym == SDLK_RETURN || ev.key.keysym.sym == SDLK_RIGHT)
            {
                            config_set_dword(config, "speed_source", speed_source);
                            return;
                            
            }
            else if(ev.key.keysym.sym == SDLK_UP)
            {
                if (speed_source >= 2)
                {
                    speed_source = 0; //rollover
                }
                else
                {
                    speed_source++;
                }

                if (speed_source == 1)
                {
                    SDL_Rect dst;

                    dst.x = x;
                    dst.y = y;
                    dst.w = 30;
                    dst.h = 30;
                    SDL_FillRect(screen, &dst, background_color);
                    SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);
                }
                sprintf(c,"%d",speed_source);
                update_label(&digit,c,1);

            }
            else if(ev.key.keysym.sym == SDLK_DOWN)
            {
                if (speed_source <= 0)
                {
                    speed_source = 2; //rollover
                }
                else
                {
                    speed_source--;
                }

                if (speed_source == 1)
                {
                    SDL_Rect dst;

                    dst.x = x;
                    dst.y = y;
                    dst.w = 30;
                    dst.h = 30;
                    SDL_FillRect(screen, &dst, background_color);
                    SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);
                }
                sprintf(c,"%d",speed_source);
                update_label(&digit,c,1);

            }
            else if(ev.key.keysym.sym == SDLK_LEFT)
            {
                            
                            config_set_dword(config, "speed_source", speed_source);
                            return ;

            }
            break;
        case SDL_KEYDOWN: break;
        default:
                        //todo save before return
            return ;
        }
    }
    
        config_set_dword(config, "speed_source", speed_source);
    return ;

}

/* changes the value in the variable that corresponds to a corrdinate in the GUI*/
int change_value(char* config_name,int *variable,int y)
{
    int x = 450;
    int val = *variable;       //shallow copy of value
    int val_arr[6];            // array of the individual config digits
    label_t flex_arr [6];      // label for the individual digits
    int index = 0;             //current index of the value being changed
        char* c = malloc(2);    //temp variable for storing conversion from int to string

    val_arr[0] = val/100000;
    val %= 100000;
    val_arr[1] = val/10000;
    val %= 10000;
    val_arr[2] = val/1000;
    val %= 1000;
    val_arr[3] = val/100;
    val %= 100;
    val_arr[4] = val/10;
    val %= 10;
    val_arr[5] = val;

    int spacing = 30;
    int i;
    for(i = 0; i < 6; i++)
    {
        sprintf(c, "%d", val_arr[i]);
        init_label(&(flex_arr[i]), c, "resources/DS-DIGI.TTF", 30, 0xDF394B, x+(i*spacing), y);
    }

    SDL_PumpEvents();
    while(SDL_WaitEvent(&ev))
    {
        switch(ev.type)
        {
        case SDL_KEYUP:
            if(ev.key.keysym.sym == SDLK_RETURN || ev.key.keysym.sym == SDLK_RIGHT)
            {
                if (index >= 5)
                {
                    //TODO save the new value
                    *variable = val_arr[0]*100000 + val_arr[1]*10000 + val_arr[2]*1000 + val_arr[3]*100 + val_arr[4]*10 + val_arr[5];
                                        config_set_dword(config, config_name, *variable);
                    return 0;
                }
                index++;
            }
            else if(ev.key.keysym.sym == SDLK_UP)
            {
                if (val_arr[index] >= 9)
                {
                    val_arr[index] = 0; //rollover
                }
                else
                {
                    val_arr[index] ++;
                }

                if (val_arr[index] == 1)
                {
                    SDL_Rect dst;

                    dst.x = flex_arr[index].x;
                    dst.y = flex_arr[index].y;
                    dst.w = spacing;
                    dst.h = 30;
                    SDL_FillRect(screen, &dst, background_color);
                    SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);
                }
                sprintf(c,"%d",val_arr[index]);
                update_label(&(flex_arr[index]),c,1);

            }
            else if(ev.key.keysym.sym == SDLK_DOWN)
            {
                if (val_arr[index] <= 0)
                {
                    val_arr[index] = 9; //rollover
                }
                else
                {
                    val_arr[index] --;
                }

                if (val_arr[index] == 1)
                {
                    SDL_Rect dst;

                    dst.x = flex_arr[index].x;
                    dst.y = flex_arr[index].y;
                    dst.w = spacing;
                    dst.h = 30;
                    SDL_FillRect(screen, &dst, background_color);
                    SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);
                }
                sprintf(c,"%d",val_arr[index]);
                update_label(&(flex_arr[index]),c,1);

            }
            else if(ev.key.keysym.sym == SDLK_LEFT)
            {
                                *variable = val_arr[0]*100000 + val_arr[1]*10000 + val_arr[2]*1000 + val_arr[3]*100 + val_arr[4]*10 + val_arr[5];
                                config_set_dword(config, config_name, *variable);
                return 0;
                //TODO go back to prev screen
                //modules_quit();
                //exit(1);
            }
            break;
        case SDL_KEYDOWN: break;

        }
    }

        // TODO before returning save to file
        *variable = val_arr[0]*100000 + val_arr[1]*10000 + val_arr[2]*1000 + val_arr[3]*100 + val_arr[4]*10 + val_arr[5];
        config_set_dword(config, config_name, *variable);
    return 0;

}

int open_config_menu()
{
    //you would have a config struct to store all the entered figures duhh! TODO
    draw_menu_box(151, 101, 498, 298);
    label_t config_title, speed_source, rpm_level, eng_level, cool_level, fuel_level, oil_level;
    icon_t bullet_icon;
    //TODO when speed source is chosen , it should then put a small label beside the mph saying 'gps'..
    int begin_y = 147;
    int scale = 43;
    int x = 190;
    init_label(&config_title, "CONFIGURATION MENU", "resources/DS-DIGI.TTF", 30, 0xDF394B, 300, 108);
    init_label(&speed_source, "speed source:", "resources/DS-DIGI.TTF", 30, 0xDF394B, x, begin_y);
    init_label(&rpm_level, "max rpm:", "resources/DS-DIGI.TTF", 30, 0xDF394B, x, begin_y+scale);
    init_label(&eng_level, "eng temp warn lev:", "resources/DS-DIGI.TTF", 30, 0xDF394B, x, begin_y+(2*scale));
    init_label(&cool_level, "coolant warn lev: ", "resources/DS-DIGI.TTF", 30, 0xDF394B, x, begin_y+(3*scale));
    init_label(&fuel_level, "fuel low warn lev:", "resources/DS-DIGI.TTF", 30, 0xDF394B, x, begin_y+(4*scale));
        init_label(&oil_level, "oil low warn lev:", "resources/DS-DIGI.TTF", 30, 0xDF394B, x, begin_y+(5*scale));

    init_icon(&bullet_icon, "resources/bullet_on.png", "resources/bullet_off.png", 1, 160, begin_y+10);
    update_icon(&bullet_icon, 1,1);
    //follow by list of labels.. TODO
    int max = 5, index = 0;

    SDL_PumpEvents();
    while(SDL_WaitEvent(&ev))
    {
        switch(ev.type)
        {
        case SDL_KEYUP:
            if(ev.key.keysym.sym == SDLK_RETURN || ev.key.keysym.sym == SDLK_RIGHT)
            {
                update_icon(&bullet_icon,0,1);

                switch (index)
                {
                                       
                    case 0:
                                                change_speed_source();
                        break;
                    case 1: //max rpm
                        change_value("max_rpm",&max_rpm,begin_y+scale);
                        break;
                    case 2: //eng lev
                        change_value("eng_temp_warn_level",&eng_temp_warn_lev,begin_y+(2*scale));
                        break;
                    case 3: //coolant lev
                        change_value("coolant_temp_warn_level",&coolant_temp_warn_lev,begin_y+(3*scale));
                        break;
                    case 4: // fuel lev
                        change_value("fuel_low_warn_level",&fuel_low_warn_lev,begin_y+(4*scale));
                        break;
                                        case 5: // oil lev
                                                change_value("oil_temp_warn_level",&oil_temp_warn_lev,begin_y+(5*scale));
                                                break;
                }

                update_icon(&bullet_icon,1,1);
                //TODO now focus on values of each stuff
            }
            else if(ev.key.keysym.sym == SDLK_UP) // if 'up' was pressed then move the bullet up
            {
                if (index >0)
                {
                    fill_with_bgcolor(bullet_icon.x,bullet_icon.y,20,20);
                    bullet_icon.y -= scale;
                    index--;
                    update_icon(&bullet_icon,1,1);
                }
            }
            else if(ev.key.keysym.sym == SDLK_DOWN) // if 'down' was pressed then move the bullet down
            {
                if (index < max)
                {
                    fill_with_bgcolor(bullet_icon.x,bullet_icon.y,20,20);
                    bullet_icon.y += scale;
                    index++;
                    update_icon(&bullet_icon,1,1);
                }
            }
            else if(ev.key.keysym.sym == SDLK_LEFT)
            {
                return 0;
                //TODO go back to prev screen
                //modules_quit();
                //exit(1);
            }
            break;
        case SDL_KEYDOWN: break;
        default:
            return 0;
        }
    }

    //TODO before exiting, you remove yourself, then where you are retuirning to will put themselves back
    return 0;
}

int draw_menu_option()
{
    label_t diagnostic_menu, config_menu, config_title, exit_menu, shutdown;
    int begin_y = 147;
    int scale = 43;

    draw_menu_box(151,101,498,298);

    init_label(&config_title, "MENU", "resources/DS-DIGI.TTF", 30, 0xDF394B, 300, 108);
    init_label(&config_menu, "configuration menu:", "resources/DS-DIGI.TTF", 30, 0xDF394B, 200, begin_y);
    init_label(&diagnostic_menu, "diagnostic menu:", "resources/DS-DIGI.TTF", 30, 0xDF394B, 200, begin_y + scale);
    init_label(&exit_menu, "close application", "resources/DS-DIGI.TTF", 30, 0xDF394B, 200, begin_y + 2*scale);
        init_label(&shutdown, "shutdown system", "resources/DS-DIGI.TTF", 30, 0xDF394B, 200, begin_y + 3*scale);
    init_icon(&bullet_icon, "resources/bullet_on.png", "resources/bullet_off.png", 1, 160, begin_y+10);
    update_icon(&bullet_icon, 1,1);

    return 0;
}


void lookup (char** string, char ** can_val,packet_info_t *p)
{

    switch(p->can_id)
    {
        case FL_WHEEL_SPEED: 
            strcpy(*string, "FL wheel speed");
            sprintf(*can_val,"%d",get_int16(p->data, 0)) ;
            break;

        case FR_WHEEL_SPEED: 
            strcpy(*string, "FR wheel speed");
            sprintf(*can_val,"%d",get_int16(p->data, 0)) ;
            break;

        case RL_WHEEL_SPEED:
            strcpy(*string, "RL wheel speed");
            sprintf(*can_val,"%d",get_int16(p->data, 0)) ;
            break;

        case RR_WHEEL_SPEED: 
            strcpy(*string, "RR wheel speed");
            sprintf(*can_val,"%d",get_int16(p->data, 0)) ;
            break;

        case  GPS_SPEED: 
            strcpy(*string,  "GPS speed");
            sprintf(*can_val,"%d",get_int16(p->data, 0)) ;
            break;

        case ROAD_SPEED: 
            strcpy(*string, "road speed");
            sprintf(*can_val,"%d",get_int16(p->data, 0)) ;
            break;

        case GEAR_CHANGE :
            strcpy(*string,  "gear change");
            sprintf(*can_val,"%d",p->data[0]); 
            break;
            
        case ENGINE_REVS:
            strcpy(*string, "engine revs");
            sprintf(*can_val,"%d",get_uint16(p->data, 0));
            break;
            
        case FUEL_LEVEL: 
            strcpy(*string, "fuel level");
            sprintf(*can_val,"%d",p->data[0]);
            break;
            
        case OIL_TEMP:
            strcpy(*string, "oil temperature");
            sprintf(*can_val,"%d",get_int16(p->data, 0));
            break;
            
        case COOLANT_TEMP:
            strcpy(*string, "coolant temperature");
            sprintf(*can_val,"%d",get_int16(p->data, 0));
            break;

        case GEAR_SHIFT_CHARGE_STATE : 
            strcpy(*string, "gear shift charge state");
            sprintf(*can_val,"%d",p->data[0]); break;
            
        case ENGINE_TEMP_S1:
            strcpy(*string, "engine temperature (S1)");
            sprintf(*can_val,"%d",get_int16(p->data,0));
            break;

        case ENGINE_TEMP_S2:
            strcpy(*string, "engine temperature (S2)");
            sprintf(*can_val,"%d",get_int16(p->data,0));
            break;

        case ENGINE_TEMP_S3:
            strcpy(*string, "engine temperature (S3)");
            sprintf(*can_val,"%d",get_int16(p->data,0));
            break;

        case ENGINE_TEMP_S4:
            strcpy(*string, "engine temperature (S4)");
            sprintf(*can_val,"%d",get_int16(p->data,0));
            break;
            
        default: 
            strcpy(*string, "---");
            sprintf(*can_val,"%0x.0x.0x.0x.0x.0x.0x.0x",p->data[0],p->data[1],p->data[2],p->data[3],
                    p->data[4],p->data[5],p->data[6],p->data[7]);
    }

}


void diagnose()
{

    draw_menu_box(151,101,498,298);

    label_t data_read;
    icon_t diag_icon;
    init_icon(&diag_icon, "resources/diag.png", "resources/diag.png", 1, 250, 144);
    update_icon(&diag_icon,1,1);

    FILE* log_read = fopen(logfile, "r");

    if(!log_read)
    {
        perror("coudnt open file for read: ");
        //return;
    }
    printf("file \'%s\' open succesfull\n", logfile);
    init_label(&data_read, "  System        CAN ID(HEX)        DATA", "resources/DS-DIGI.TTF", 20, 0xDF394B, 260, 108);

    //display the firs 13 packets
    packet_info_t p ;
    int i;
    int max = 13;
    int read;
    int scale = 20;
    char str_format[100];

    char * can_name = malloc(40);
    char * can_val = malloc (10);

    if(log_read)
    {
        for(i = 1; i <= max; i++)
        {
            SDL_mutexP(logger_lock);
            read = fread(&p, sizeof(packet_info_t) ,1,log_read);
            SDL_mutexV(logger_lock);

            if (read == 0)
            {
                printf("round %d: read nothing from the CAN\n", i);
                break;
            }

            lookup(&can_name,&can_val,&p);
            //printf("can_name:%s   can_val:%s\n",can_name,can_val);
            sprintf(str_format, "  %-10X             %-20s     %-15s",p.can_id, can_name, can_val);
            printf("1:can_name:%s   can_val:%s\n",can_name,can_val);
            printf("2: %s\n", str_format);
            init_label(&data_read, str_format, "resources/DS-DIGI.TTF", 16, 0xFF, 275, 108 +(i*scale));
        }

    }
    
    int index = 1;
    SDL_PumpEvents();
    while(running && SDL_WaitEvent(&ev))
    {
        switch(ev.type)
        {
            case SDL_KEYUP:
                if(ev.key.keysym.sym == SDLK_RETURN || ev.key.keysym.sym == SDLK_RIGHT)
                {
                    //do nothing
                }
                else if(ev.key.keysym.sym == SDLK_UP)
                {
                    if(index == 1)
                    {
                        //scroll up
                        if(log_read)
                        {


                            SDL_mutexP(logger_lock);
                            read = fseek(log_read,-(sizeof(packet_info_t)*14),SEEK_CUR);
                            SDL_mutexV(logger_lock);
                            printf("scrolling up: fseek= %d\n", read);

                            if(read)
                                continue;
                            
                            fill_with_bgcolor(275,125,350,270);
                            for(i = 1; i <= max; i++)
                            {
                                SDL_mutexP(logger_lock);
                                read = fread(&p, sizeof(packet_info_t) ,1,log_read);
                                SDL_mutexV(logger_lock);

                                if(read == 0)
                                    break;

                                lookup(&can_name,&can_val,&p);
                                sprintf(str_format, "  %-10X             %-20s     %-15s",p.can_id, can_name, can_val);
                                init_label(&data_read, str_format, "resources/DS-DIGI.TTF", 16, 0xFF, 275, 108 +(i*scale));
                            }
                        }
                        
                    }
                    else if (index > 1)
                    {
                        fill_with_bgcolor(diag_icon.x,diag_icon.y,10,10);
                        diag_icon.y -= scale;
                        index--;
                        update_icon(&diag_icon,1,1);
                    }

                }
                else if(ev.key.keysym.sym == SDLK_DOWN)
                {
                    if(index == max)
                    {
            //scroll down
                        if(log_read)
                        {

                            SDL_mutexP(logger_lock);
                            read = fseek(log_read,-(sizeof(packet_info_t))*12,SEEK_CUR);
                            SDL_mutexV(logger_lock);

                            printf("scrolling down: fseek = %d\n", read);
                            if (read)
                                continue;
                            
                            fill_with_bgcolor(275,125,350,270);

                            for(i = 1; i <= max; i++)
                            {
                                SDL_mutexP(logger_lock);
                                read = fread(&p, sizeof(packet_info_t) ,1,log_read);
                                SDL_mutexV(logger_lock);
                                
                                if(read == 0)
                                    break;

                                lookup(&can_name,&can_val,&p);
                                sprintf(str_format, "  %-10X             %-20s     %-15s",p.can_id, can_name, can_val);
                                init_label(&data_read, str_format, "resources/DS-DIGI.TTF", 16, 0xFF, 275, 108 +(i*scale));
                            }

                        }

                    }
                    else if(index < max)
                    {
                        //move bullet down
            fill_with_bgcolor(diag_icon.x,diag_icon.y,10,10);
            diag_icon.y += scale;
            index++;
            update_icon(&diag_icon,1,1);
                    }

                }
                else if(ev.key.keysym.sym == SDLK_LEFT)
                {
                    fclose(log_read);
                    return;
                }
                break;
        }
    }
}


int open_menu_option()
{
    in_menu = 1;
    draw_menu_option();

    int scale = 43;
    int index = 0, max = 3;
    SDL_PumpEvents();
    while(running && SDL_WaitEvent(&ev))
    {
        switch(ev.type)
        {
        case SDL_KEYUP:
            if(ev.key.keysym.sym == SDLK_RETURN || ev.key.keysym.sym == SDLK_RIGHT)
            {
                switch (index)
                {
                    case 0:
                        open_config_menu();
                        break;
                    case 1:
                        diagnose();
                        break;
                    case 2:
                        running = 0;
						if (canusb)
							canusb_abort();
						else
							can_abort();
                        break;
                    case 3:
                        running = 0;
						if (canusb)
							canusb_abort();
						else
							can_abort();
                        system("halt");
                        break;

                }
				draw_menu_option();
				index = 0;
            }
            else if(ev.key.keysym.sym == SDLK_UP)
            {
                if (index > 0)
                {
                    fill_with_bgcolor(bullet_icon.x,bullet_icon.y,20,20);
                    bullet_icon.y -= scale;
                    index--;
                    update_icon(&bullet_icon,1,1);
                }
            }
            else if(ev.key.keysym.sym == SDLK_DOWN)
            {
                if (index < max)
                {
                    fill_with_bgcolor(bullet_icon.x,bullet_icon.y,20,20);
                    bullet_icon.y += scale;
                    index++;
                    update_icon(&bullet_icon,1,1);
                }
            }
            else if(ev.key.keysym.sym == SDLK_LEFT)
            {
                in_menu = 0;
                return 0;
            }
        case SDL_KEYDOWN: break;
            break;
        default:
            in_menu = 0;
            return 0; //TODO remove this when the program is in proper shape and the ones in other switch statements as well
        }
    }
    //TODO before exiting, you remove yourself
    //TODO put the bullet in a struct or put an array of thing the bullet can point to,
    //or just put the array in the menu fucntion
    in_menu = 0;
    return 0;
}

/* function to detect the pressing of keys on the device */
int read_user_input()
{
    SDL_PumpEvents();
    while(running && SDL_WaitEvent(&ev))
    {
        switch(ev.type)
        {
        case SDL_KEYUP:
            if(ev.key.keysym.sym == SDLK_RETURN || ev.key.keysym.sym == SDLK_RIGHT)
            {
                //SDL_Delay(2*DELAY);
                open_menu_option();
                //set the screen back to background color and redraw all the widgets back
                SDL_FillRect(screen, &screen->clip_rect, background_color);
                SDL_Flip(screen);
                gui_refresh();
                //redraw_all(1);
                //update all that cannot move or just update all actually TODO
            }
            else if(ev.key.keysym.sym == SDLK_UP)
            {
                //packet the gear_up CAN packet into a struct

                packet_info_t *p_info = malloc(sizeof(packet_info_t));
                p_info->op = D11;
                p_info->can_id = 0x1A1;
                p_info->dlc = 1;
                p_info->data[0] = 1;

                //add the gear up CAN packet struct to a queue of packets waiting to be sent
				if (canusb)
					canusb_queue_packet(p_info);
				else
					can_queue_packet(p_info);
            }
            else if(ev.key.keysym.sym == SDLK_DOWN)
            {
                //packet the gear down CAN packet into a struct
                packet_info_t *p_info = malloc(sizeof(packet_info_t));
                p_info->op = D11;
                p_info->can_id = 0x1A1;
                p_info->dlc = 1;
                p_info->data[0] = 0;

                //add the gear down CAN packet struct to a queue of packets waiting to be sent
				if (canusb)
					canusb_queue_packet(p_info);
				else
					can_queue_packet(p_info);
            }
                        else if(ev.key.keysym.sym == SDLK_LEFT)
                        {
                                running = 0;
								if (canusb)
									canusb_abort();
								else
									can_abort();
                        }
            break;
        }
    }
    return 0;
}

void can_callback(packet_info_t *p)
{
    int value;
    char text[10];

        static int blink = 0;   /* blinking light counter for all icons */
        static int on_off = 1 ; /* boolean to determine which state the blinking is in */
        static int coolant_blink = 0;
        static int oil_blink = 0;
        static int fuel_blink = 0;

    switch(p->can_id)
    {
        // Gear
        case GEAR_CHANGE:
            //printf("GEAR_CHANEG \n");
            value = p->data[0];
            if (value == 0)
                sprintf(text, "N");
            else
                sprintf(text, "%d", value);
            update_label(&gear_value, text, 0);
            break;

        // Front left wheel speed
        case FL_WHEEL_SPEED:

			if(speed_source == SOURCE_WHEEL_SPEED)
			{
				//printf("FL_WHEEL_SPEED\n");
				value = get_int16(p->data, 0);
				sprintf(text, "%03d", value);
				update_label(&spd_value, text, 0);
			}
            break;
                        
		case ROAD_SPEED:
                    
			if(speed_source == SOURCE_ROAD_SPEED)
			{
				//printf("ROAD_SPEED \n");
				value = get_int16(p->data, 0);
				sprintf(text, "%03d", value);
				update_label(&spd_value, text, 0);
			}
            break;
                        
		case GPS_SPEED:

			if(speed_source == SOURCE_GPS_SPEED)
			{
				//printf("GPS_SPEED\n");
				value = get_int16(p->data, 0);
				sprintf(text, "%03d", value);
				update_label(&spd_value, text, 0);
			}
            break;

        // RPM
        case ENGINE_REVS:
            value = get_uint16(p->data, 0);
            sprintf(text, "%05d", value);
            update_label(&rpm_value, text, 0);
            update_bar_graph(&rpm_graph, value, 0);
            break;

        // Fuel gauge
        case FUEL_LEVEL:
                        value = p->data[0];
                        update_bar_graph(&fuel_graph, value, 0);

                        if(value <= fuel_low_warn_lev)
                                fuel_blink = 1;
                        else
                                fuel_blink = 0;
                        break;

                // Oil temperature
                case OIL_TEMP:
                        value = get_int16(p->data, 0);
            if (value <= oil_temp_warn_lev) // TODO change this
                oil_blink = 1;
            else
                oil_blink = 0;

                        break;

                // coolant temperature
                case COOLANT_TEMP:
                        value = get_int16(p->data, 0);
            if (value <= coolant_temp_warn_lev) // TODO change this
                coolant_blink = 1;
            else
                coolant_blink = 0;
                        break;

                case GEAR_SHIFT_CHARGE_STATE:
                        value = p->data[0];
                        update_bar_graph(&gear_shift_charge, value, 0);
                        break;

                case ENGINE_TEMP_S1:
                    
                        value = get_int16(p->data, 0);
                        printf("recieved engine temp value %d\n", value);
                        sprintf(text, "%02d", value);
                        update_label(&engine_temp, text, 0);
                        break;

    }

        if(blink >= MAX_BLINK_LENGTH)
        on_off = 0;
    else if(blink <= 0)
        on_off = 1;

    if(on_off)
        blink++;
    else
        blink --;

    if(coolant_blink)
        update_icon(&coolant_icon,on_off,0);

    if(oil_blink)
        update_icon(&engine_light,on_off,0);

        if(fuel_blink)
                update_icon(&fuel_icon,on_off,0);

        
    if (logenable)
        {
                SDL_mutexP(logger_lock);
                logger_log(p, sizeof(packet_info_t));
                SDL_mutexV(logger_lock);
        }

}

int main()
{
    unsigned int ret, video_mode, screen_width, screen_height, screen_bpp, logappend;
	char *canusbdev;

    // Try to load the SDL modules, print on stderr if loading fails
    if (modules_init())
    {
        fprintf(stderr, "Error loading SDL Modules.\n");
        exit(EXIT_FAILURE);
    }

    // Initialise mutex
    lock = SDL_CreateMutex();
    logger_lock = SDL_CreateMutex();

    // Configuration
    config = config_init();

    // Retrieve the configuration
    config_get_dword(config, "speed_source", &speed_source);
    config_get_dword(config, "max_rpm", &max_rpm);
    config_get_dword(config, "eng_temp_warn_level", &eng_temp_warn_lev);
    config_get_dword(config, "oil_temp_warn_level", &oil_temp_warn_lev);
    config_get_dword(config, "coolant_temp_warn_level", &coolant_temp_warn_lev);
    config_get_dword(config, "fuel_low_warn_level", &fuel_low_warn_lev);

    config_get_string(config, "spi_device", &device);
    config_get_dword(config, "spi_mode", &ret);
    mode = (uint8_t)ret;
    config_get_dword(config, "spi_bits", &ret);
    bits = (uint8_t)ret;
    config_get_dword(config, "spi_speed", &ret);
    speed = (uint16_t)ret;
    config_get_dword(config, "spi_delay", &ret);
    delay = (uint16_t)delay;

    config_get_dword(config, "screen_width", &screen_width);
    config_get_dword(config, "screen_height", &screen_height);
    config_get_dword(config, "screen_bpp", &screen_bpp);
    config_get_dword(config, "fullscreen", &ret);
    config_get_dword(config, "canusb", &canusb);
	config_get_string(config, "canusbdevice", &canusbdev);

    video_mode = 0;
    if (ret)
        video_mode |= SDL_FULLSCREEN;

    config_get_dword(config, "double_buffering", &ret);
    if (ret)
        video_mode |= SDL_DOUBLEBUF;
    video_mode |= SDL_SWSURFACE;

    config_get_dword(config, "background_color", &background_color);

    config_get_string(config, "logfile", &logfile);

    config_get_dword(config, "logenable", &logenable);
    config_get_dword(config, "logappend", &logappend);

    // Initialise the screen mode
    screen = SDL_SetVideoMode(screen_width, screen_height, screen_bpp, video_mode);
    if (screen == NULL)
    {
        fprintf(stderr, "Unable to set the video mode.\n");
        exit(EXIT_FAILURE);
    }

    // Set the background color
    SDL_FillRect(screen, &screen->clip_rect, background_color);
    SDL_Flip(screen);

    // Init the widgets
    widget_init(screen, background_color);

    // Init the logging
    if (logenable)
        logger_init(logfile, logappend);

    // Initialise the CAN
    if (canusb)
        canusb_init(canusbdev, can_callback);
    else
        can_init(device, mode, bits, speed, delay, can_callback);

    // Initialise the GUI
    gui_init();

    // Hide the mouse cursor
    SDL_ShowCursor(0);

    // Create the threads
    if (canusb)
        read_thread = SDL_CreateThread(canusb_data_read, NULL);
    else
        read_thread = SDL_CreateThread(can_data_read, NULL);
    input_thread = SDL_CreateThread(read_user_input, NULL);

    // Main thread also acts as the GUI updating thread after all initilalization
    while(running)
    {
        if(in_menu == 0)
        {
            SDL_mutexP(lock);
            SDL_Flip(screen);
            SDL_mutexV(lock);
        }

                SDL_Delay(DELAY);
    }

    SDL_WaitThread(read_thread, NULL);
    SDL_WaitThread(input_thread, NULL);
    config_save(config);
    modules_quit();
        
        return EXIT_SUCCESS;
}