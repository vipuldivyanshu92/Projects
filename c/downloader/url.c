/* resource_type://username:password@domain:port/path?query_string#anchor */

#include <regex.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "url.h"

#define NMATCH  10

/* return a string from a regmatch */
static char *regmatch_to_string(char *fs, regmatch_t rm)
{
    int length = rm.rm_eo-rm.rm_so;
    char *s = (char *)malloc(length + 1);
    memcpy(s, fs+rm.rm_so, length);
    s[length] = 0;

    return s;
}

/* Parse a url string and return a URL_t structure */
int url_parse(char *u, URL_t *dest)
{
    const int nmatch = 10;
    regmatch_t pmatch[nmatch];
    regex_t re;
    memset(dest, 0, sizeof(URL_t));

    // URL  regular expression pattern
    char *pattern = "((.*)://)?((.*):(.*)@)?([A-Za-z0-9.-]*)(:([0-9]+))?(.+)?$";

    // the regular expression evaluation failed return NULL
    if (regcomp(&re, pattern, REG_EXTENDED) != 0)
    {
        return EXIT_FAILURE;
    }

    if (regexec(&re, u, NMATCH, pmatch, 0) != 0)
    {
        return EXIT_FAILURE;
    }

    // Ressource Type
    if (pmatch[2].rm_eo != -1)
        dest->res_type = regmatch_to_string(u, pmatch[2]);
    else
    {
        dest->res_type = malloc(5);
        strcpy(dest->res_type, "http");
    }

    if (pmatch[4].rm_eo != -1)
        dest->username = regmatch_to_string(u, pmatch[4]);

    if (pmatch[5].rm_eo != -1)
        dest->password = regmatch_to_string(u, pmatch[5]);

    if (pmatch[6].rm_eo != -1)
        dest->domain = regmatch_to_string(u, pmatch[6]);

    if (pmatch[8].rm_eo != -1)
        dest->port = regmatch_to_string(u, pmatch[8]);
    else
    {
        dest->port = malloc(3);
        strcpy(dest->port, "80");
    }

    if (pmatch[9].rm_eo != -1)
        dest->path = regmatch_to_string(u, pmatch[9]);
    else
    {
        dest->path = malloc(2);
        strcpy(dest->path, "/");
    }

    // free the regular expression
    regfree(&re);

    return EXIT_SUCCESS;
}

/* Free the memory allocated by a URL structure */
void url_destroy(URL_t *url)
{
    free(url->res_type);
    free(url->username);
    free(url->password);
    free(url->domain);
    free(url->port);
    free(url->path);
}

/* Convert a URL_t to a string, if res_type not specified http is used by by default. */
char *url_to_string(URL_t *url)
{
    char *s = malloc(
        strlen(url->res_type) +
        ((url->password && url->username) ? strlen(url->password) + strlen(url->username) + 2 : 0) +
        strlen(url->domain) +
        strlen(url->port) +
        strlen(url->path) +
        6
    );
    size_t offset = 0;

    // set the ressource type
    offset += sprintf(s, "%s://", url->res_type);

    // set username and password only if both are present
    if ((url->username != NULL) && (url->password != NULL))
        offset += sprintf(s+offset, "%s:%s@", url->username, url->password);

    // set the domain
    offset += sprintf(s+offset, "%s", url->domain);

    // set the port
    if (url->port != NULL)
        offset += sprintf(s+offset, ":%s", url->port);

    // set the path
    offset += sprintf(s+offset, "%s", url->path);

    // null terminate the string
    s[offset] = 0;

    return s;
}
