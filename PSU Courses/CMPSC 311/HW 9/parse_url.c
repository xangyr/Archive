/*
 * author: Xiangyu Ren
 * email: xvr5040@psu.edu
 * parse_url.c for CMPSC 311 Fall 2019
 * last updated: 11/20/2019
 */
#include "parse_url.h"
#include <string.h>
#define MAXBUF 8096
// returns 1 if the url starts with http:// (case insensitive)
// and returns 0 otherwise
// If the url is a proper http scheme url, parse out the three
// components of the url: host, port and path and copy
// the parsed strings to the supplied destinations.
// Remember to terminate your strings with 0, the null terminator.
// If the port is missing in the url, copy "80" to port.
// If the path is missing in the url, copy "/" to path.
int parse_url(const char *url, char *host, char *port, char *path) {
  /*
   check the first 7 characters of url to see if proper
   add return 1 at the end of the if statement
   add return 0 outside the statement
   */
  if (!strncasecmp(url, "http://", 7)) {
    /*
     create variables:
     'temp' to store the string of url
        since url is 'const char', and arguments of strtok need to be 'char'
     'token' to split
     'rest' to store the rest string
     */
    char temp[MAXBUF];
    strcpy(temp, url);
    char *token;
    char *rest = temp;
    
    /*
     after testing, by using 2 time strtok(string,"/")
     host:port is stored in 'token' and the path is stored in 'rest'
     so split 'token' by ":" again and copy to host
     */
    token = strtok_r(rest, "/", &rest);
    token = strtok_r(NULL, "/", &rest);
    
    strcpy(host, strtok_r(token, ":", &token));
    
    /*
     check if strtok return NULL meaning there is no ':port_#' so copy 80 to port
     else copy 'token' to port
     */
    if((token = strtok(token, ":")) == NULL) {
      strcpy(port, "80");
    } else {
      strcpy(port, token);
    }
    
    /*
     by requirement the path should contain "/", so copy to path first
     then use strcat to append the string to the dest
     don't need to care if the 'rest' is empty
     */
    strcpy(path, "/");
    strcat(path, rest);
    
    return 1;
  }
  return 0;
}
