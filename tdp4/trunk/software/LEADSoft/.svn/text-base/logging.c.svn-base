#include <stdio.h>

#include "logging.h"

static FILE* logger;

int logger_init(char *path, int append)
{
	if (append)
		logger = fopen(path, "a");
	else
		logger = fopen(path, "w");
	if(logger)
		return 0;
	return 1;	
}

void logger_log(void *data, size_t l)
{	
	fwrite(data, l, 1, logger);
}

int logger_read(void *buffer, size_t l)
{
        fread(buffer, l ,1,logger);
}

int logger_seek(long offset, int origin)
{
        return fseek(logger, offset, origin);
}

void logger_abort()
{
	fclose(logger);
}
