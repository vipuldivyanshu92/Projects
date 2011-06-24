#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <SDL/SDL_ttf.h>
#include "widget.h"

static SDL_Surface *screen;
static Uint32 background_color;

/*
 */
void widget_init(SDL_Surface *s, Uint32 bckc)
{
	screen = s;
	background_color = bckc;
}

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
	int rgb, int x, int y)
{
	// Load the font
	s->font = TTF_OpenFont(font, fontsize);
	if (!(s->font))
		return 1;
	s->text = text;

	// Set the color
	s->color.r = (rgb & 0xFF0000) >> 16;
	s->color.g = (rgb & 0x00FF00) >> 8;
	s->color.b = rgb & 0x0000FF;

	s->surface = NULL;

	// Set x y coordinates
	s->x = x;
	s->y = y;

	update_label(s, s->text, 1);

	return 0;
}

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
int init_icon(icon_t *s, char *on_img, char *off_img, int status, int x, int y)
{
	//Load icon image on and image off
	s->surface_on = IMG_Load(on_img);
	s->surface_off = IMG_Load(off_img);

	// Return 1 if unable to load one of the image
	if (!(s->surface_on) || !(s->surface_off))
		return 1;

	// Populate other variables from param
	s->status = status;
	s->x = x;
	s->y = y;

	update_icon(s, 1, 0);

	return 0;
}

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
	int y, int max, int direction)
{
	// Load the image
	s->surface_full = IMG_Load(img_full);
	s->surface_empty = IMG_Load(img_empty);

	// Set the alpha channel
	SDL_SetColorKey(s->surface_full, SDL_RLEACCEL,
		s->surface_full->format->colorkey);
	SDL_SetColorKey(s->surface_empty, SDL_RLEACCEL,
		s->surface_empty->format->colorkey);

	// Set the attributes
	s->maximum_value = max;
	s->current_value = 0;
	s->current_display_level = 0;
	s->x = x;
	s->y = y;
	s->direction = direction;

	// Display the empty graph
	SDL_Rect dst;
	dst.x = s->x;
	dst.y = s->y;
	dst.h = s->surface_empty->clip_rect.h;
	dst.w = s->surface_empty->clip_rect.w;

	SDL_BlitSurface(s->surface_empty, &(s->surface_empty->clip_rect), screen, &dst);

	return 0;
}

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
int update_label(label_t *s, char *text, int update_rect)
{
	SDL_Rect dst;
	SDL_Surface *surface;

	// Render the text with the selected font
	if (text)
	{
		// Update the label structure with the new text
		s->text = text;

		surface = TTF_RenderText_Blended(s->font, s->text, s->color);
	}
		


	// Make sure test surface is not null
	if(!surface && text)
		return 1;

	// Replace the old surface area with the background color to erase previous
	// value
	if(s->surface != NULL)
	{
		dst.x = s->x;
		dst.y = s->y;
		dst.w = s->surface->w;
		dst.h = s->surface->h;
		SDL_FillRect(screen, &dst, background_color);
	}

	// Copy the new text surface to the screen
	dst.x = s->x;
	dst.y = s->y;
	if (text)
	{
		dst.w = surface->w;
		dst.h = surface->h;
		SDL_BlitSurface(surface, &(surface->clip_rect), screen, &dst);

		// Free the unused old surface
		SDL_FreeSurface(s->surface);

		// Associate the new surface
		s->surface = surface;
	}
	else
	{
		dst.w = s->surface->w;
		dst.h = s->surface->h;
		SDL_BlitSurface(s->surface, &(s->surface->clip_rect), screen, &dst);
	}

	// If update_rect is set force the screen update
	if(update_rect)
		SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);

	return 0;
}

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
int update_icon(icon_t *s, int status, int update_rect)
{
	SDL_Rect dst;
	SDL_Surface *surface;

	// Check the status
	if (status >= 0)
		s->status = status;
	
	if (s->status)
            surface = s->surface_on;
	else
            surface = s->surface_off;

	// Create the destination rectangle
	dst.x = s->x;
	dst.y = s->y;
	dst.w = surface->w;
	dst.h = surface->h;

	// Replace the surface with the background color
	SDL_FillRect(screen, &dst, background_color);

	// Copy the new surface to the screen
	SDL_BlitSurface(surface, &(surface->clip_rect), screen, &dst);

	// Force update if required
	if (update_rect)
		SDL_UpdateRect(screen, dst.x, dst.y, dst.w, dst.h);

	return 0;
}




/*
 * Update a bar graph structure
 * PARAMETERS:
 *	s			: bar graph structure to initialise
 *	value		: value to update the bar graph with
 *
 * RETURNS:
 *	0			: Success
 *	1			: Failure
 */
int update_bar_graph(bar_graph_t *s, int value, int update)
{
	double ratio;
	int display_level;
	SDL_Rect src, dst;
	SDL_Surface *surface = NULL;

	// Be sure not to update with a negative value
	if (value < 0)
		value = 0;
	else if (value > s->maximum_value)
		value = s->maximum_value;

	s->current_value = value;

	// Calculate the new ratio to be displayed
	ratio = (double)value / s->maximum_value;

	// Check what direction the bar graph is using
	if (s->direction == 1) //if going up-down direction
		display_level = s->surface_full->h * ratio;
	else //else if going left right
		display_level = s->surface_full->w * ratio;

	// Find out what to update
	if (update)
	{
		// refresh have to be updated with last value
		surface = s->surface_full;

		dst.x = s->x;
		dst.y = s->y;
		dst.h = s->surface_empty->clip_rect.h;
		dst.w = s->surface_empty->clip_rect.w;

		SDL_BlitSurface(s->surface_empty, &(s->surface_empty->clip_rect), screen, &dst);

		src.x = s->x;
		src.y = s->y;

		if (s->direction == 1)
		{
			src.h = display_level;
			src.w = surface->w;
		}
		else
		{
			src.h = surface->h;
			src.w = display_level;
		}
	}
	else if (s->current_display_level == display_level)
	{
		// display has not changed
		return 0;
	}
	else if (s->current_display_level < display_level)
	{
		surface = s->surface_full;

		//if up-down direction
		if (s->direction == 1)
		{
			src.x = 0;
			src.y = surface->h - display_level;
			src.h = abs(display_level - s->current_display_level);
			src.w = surface->w;
		}
		else
		{
			src.x = s->current_display_level;
			src.y = 0;
			src.h = surface->h;
			src.w = abs(display_level - s->current_display_level);

		}

	}
	else
	{
		surface = s->surface_empty;
		if (s->direction == 1)
		{
			src.x = 0;
			src.h = abs(display_level - s->current_display_level);
			src.y = surface->h - s->current_display_level;
			src.w = surface->w;
		}
		else
		{
			src.x = display_level;
			src.y = 0;
			src.h = surface->h;
			src.w = abs(display_level - s->current_display_level);

		}
	}

	// Calculate the source and destination rectangles
	dst.x = src.x + s->x;
	dst.y = src.y + s->y;
	dst.h = src.h;
	dst.w = src.w;

	// Update the buffer
	SDL_FillRect(screen, &dst, background_color);
	SDL_BlitSurface(surface, &src, screen, &dst);

	// Set the current width
	s->current_display_level = display_level;

	return 0;
}