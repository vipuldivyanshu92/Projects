#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

#include "url.h"

#define BUF_SIZE    4096

int establish_connection(URL_t url)
{
    struct addrinfo hints, *ai, *ai0;
    int fd, i;
    
    // Create the address info structure
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    
    // Resolve the domain name
    if ((i = getaddrinfo(url.domain, url.port, &hints, &ai0)) != 0)
        return -1;
        
    // Loop through the linked list of addressinfo returned by getaddrinfo
    for (ai = ai0; ai != NULL; ai = ai->ai_next)
    {
        // create the socket
        fd = socket(ai->ai_family, ai->ai_socktype, ai->ai_protocol);
        
        // check if it has been properly created or try next addrinfo
        if (fd == -1)
            continue;

        // try to connect or try next addrinfo
        if (connect(fd, ai->ai_addr, ai->ai_addrlen) == -1)
        {
            close(fd);
            continue;
        }

        return fd;
    }
    
    return -1;
}

void post_form(int fd)
{
}

int main(int argc, char *argv[])
{
/*
    //www.fileserve.com/file/u8xEmG8/how.i.met.your.mother.s06e12.hdtv.xvid-fqm.avi
    char *path = "/file/u8xEmG8/how.i.met.your.mother.s06e12.hdtv.xvid-fqm.avi";
    char *domain = "www.fileserve.com";
    char *port = "80";
    
    char *remote, *request;
    char buffer[BUF_SIZE];
    struct addrinfo hints, *ai, *ai0;
    int fd, i;

    // Resolve the domain name
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    // Create the request with respect to the presence of a proxy
    //request = malloc(strlen("GET  HTTP/1.1\r\nHost: \r\n\r\n") + strlen(path) + strlen(domain) + 1);
    request = "POST /login.php HTTP/1.1\r\n"
        "Host: www.fileserve.com\r\n"
        "Content-Length: 164\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
        "loginUserName=adraen&loginUserPassword=N3YL9RL5&autoLogin=on&recaptcha_response_field=&recaptcha_challenge_field=&recaptcha_shortencode_field=&loginFormSubmit=Login";
    remote = domain;
    port = port;
    //sprintf(request, "GET %s HTTP/1.1\r\nHost: %s\r\n\r\n", path, domain);

    // try to resolve the dns
    if ((i = getaddrinfo(remote, port, &hints, &ai0)) != 0)
    {
        //free(request);
        return EXIT_FAILURE;
    }

    // Loop through the linked list of addressinfo returned by getaddrinfo
    for (ai = ai0; ai != NULL; ai = ai->ai_next)
    {
        // create the socket
        fd = socket(ai->ai_family, ai->ai_socktype, ai->ai_protocol);
        // check if it has been properly created or try next addrinfo
        if (fd == -1)
            continue;

        // try to connect or try next addrinfo
        if (connect(fd, ai->ai_addr, ai->ai_addrlen) == -1)
        {
            close(fd);
            continue;
        }

        // Send the request
        if(write(fd, request, strlen(request)) == -1)
        {
            return 0;
        }
        //free(request);

        // Read the header from the socket
        ssize_t rcount = 0;
        char *eoh; // End of Header
        do
        {
            rcount = read(fd, buffer + rcount, BUF_SIZE - rcount);
            if (rcount == -1)
            {
                return EXIT_FAILURE;
            }
        } while (((eoh = strstr(buffer, "\r\n\r\n")) == NULL) && (rcount != 0));
        printf(buffer);
        
        //retrieve the cookie from the header
        char *socookie = strstr(buffer, "Set-Cookie: ") + 12;
        socookie = strstr(socookie, "Set-Cookie: ") + 12;
        char *eocookie = strstr(socookie, "\r\n");
        int len = eocookie - socookie;
        char *cookie = malloc(len + 1);
        strncpy(cookie, socookie, len);
        cookie[len] = 0;
        
        printf("\n%s\n", cookie);
        
        // purge the read
        do
        {
            rcount = read(fd, buffer, BUF_SIZE);
        } while (rcount > 0);

        // write the get request
        request = malloc(strlen("GET  HTTP/1.1\r\nHost: \r\nCookie: \r\n\r\n") + strlen(path) + strlen(domain) + strlen(cookie) + 1);
        sprintf(request, "GET %s HTTP/1.1\r\nHost: %s\r\nCookie: %s\r\n\r\n", path, domain, cookie);
        write(fd, request, strlen(request));
        
        read(fd, buffer, BUF_SIZE);
        printf(buffer);

        close(fd);
        return EXIT_SUCCESS;
    }

    // At this point the connection has been unsuccesfull
    return EXIT_FAILURE;
    */
    char *addr = "http://www.fileserve.com/login.php";
    URL_t url;
    int fd;
    
    // Parse the input url
    if (url_parse(addr, &url) != 0)
    {
        fprintf(stderr, "Unable to connect to <url>");
        return EXIT_FAILURE;
    }
    
    if ((fd = establish_connection(url)) == -1)
    {
        fprintf(stderr, "Unable to connect to <url>");
        return EXIT_FAILURE;
    }
        
    return EXIT_SUCCESS;
}