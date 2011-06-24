/*
 * File:   widget.h
 * Author: adraen
 *
 * Created on 15 April 2011, 14:13
 */

#ifndef LOGGING_H
#define	LOGGING_H

#ifdef	__cplusplus
extern "C" {
#endif
int  logger_init(char *logfile, int append);

void logger_log(void *data, size_t s);

int logger_read(void *buffer, size_t l);

int logger_seek(long offset, int origin);

void logger_abort();

#ifdef	__cplusplus
}
#endif

#endif	/* LOGGING_H */

