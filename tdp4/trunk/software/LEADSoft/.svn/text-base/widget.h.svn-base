/* 
 * File:   widget.h
 * Author: adraen
 *
 * Created on 15 April 2011, 14:13
 */

#ifndef WIDGET_H
#define	WIDGET_H

#ifdef	__cplusplus
extern "C" {
#endif

/* Bar Graph structure */
typedef struct
{
	SDL_Surface *surface_full;
	SDL_Surface *surface_empty;
	int maximum_value;
        int current_value;
	int current_display_level;
	int direction; //0 = left-right , 1 = down - up
	int x;
	int y;
} bar_graph_t;

/* Label structure */
typedef struct
{
	SDL_Surface *surface;
	TTF_Font *font;
	SDL_Color color;
	char *text;
	int x;
	int y;
} label_t;

/* Icon structure*/
typedef struct
{
	SDL_Surface *surface_on;
	SDL_Surface *surface_off;
	int status;
	int x;
	int y;
} icon_t;

/*
 * Initialise a label structure
 * PARAMETERS:
 *	s			: Label structure to initialise
 *	text		: Text of the label
 *	font		: Path of the font to use
 *	fontsize	: Size of the font
 *	rgb			: Text Color
 *	x			: x coordinate of the top left corner of the label
 *	y			: y coordinate of the top left corner of the label
 *
 * RETURNS:
 *	0			: Success
 *	1			: Failure
 */
int init_label(label_t *s, char *text, char* font, int fontsize,
	int rgb, int x, int y);

/*
 * Initialise an icon structure
 * PARAMETERS:
 *	s			: Label structure to initialise
 *	on_img		: Path to the on_image picture
 *	off_img		: Path to the off_image picture
 *	status		: 0 for off_image, 1 for on_image
 *	x			: x coordinate of the top left corner of the label
 *	y			: y coordinate of the top left corner of the label
 *
 * RETURNS:
 *	0			: Success
 *	1			: Failure
 */
int init_icon(icon_t *s, char *on_img, char *off_img, int status, int x, int y);

/*
 * Init a bar graph structure
 * PARAMETERS:
 *	s			: bar graph structure to update
 *	img_full	: Path to the image full file
 *	img_empty	: Path to the image empty file
 *	x			: x top left corner coordinate
 *	y			: y top left corner coordinate
 *	max			: maximum value of the bar graph
 *	direction	: 0 left - right, 1 up - down
 *
 * RETURNS:
 *	0			: Success
 *	1			: Failure
 */
int init_bar_graph(bar_graph_t *s, char *img_full, char *img_empty, int x,
	int y, int max, int direction);

/*
 * Update a label structure
 * PARAMETERS:
 *	s			: Label structure to update
 *	text		: string to display on the label
 *	update_rect : 1 to force screen refresh
 *
 * RETURNS:
 *	0			: Success
 *	1			: Failure
 */
int update_label(label_t *s, char *text, int update_rect);

/*
 * Update an icon structure
 * PARAMETERS:
 *	s			: Icon structure to initialise
 *	status		: 0 display surface off else surface on
 *	update_rect : 1 to force screen refresh
 *
 * RETURNS:
 *	0			: Success
 *	1			: Failure
 */
int update_icon(icon_t *s, int status, int update_rect);




/*
 * Update a bar graph structure
 * PARAMETERS:
 *	s			: bar graph structure to initialise
 *	value                   : value to update the bar graph with
 *      update                  : force update of the screen
 *
 * RETURNS:
 *	0			: Success
 *	1			: Failure
 */
int update_bar_graph(bar_graph_t *s, int value, int update);

#ifdef	__cplusplus
}
#endif

#endif	/* WIDGET_H */

