#ifndef __URL_H
#define __URL_H

typedef struct
{
    char *res_type;
    char *username;
    char *password;
    char *domain;
    char *port;
    char *path;
} URL_t;

/* Parse a url string and return a URL_t structure */
int url_parse(char *u, URL_t *dest);

/* Free the memory allocated by a URL structure */
void url_destroy(URL_t *url);

/* Convert a URL_t to a string, if res_type not specified http is used by by default. */
char *url_to_string(URL_t *url);

#endif
