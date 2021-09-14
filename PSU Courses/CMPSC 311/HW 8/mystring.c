/*
 * author: Xiangyu Ren
 * email: xvr5040@psu.edu
 * main.c for CMPSC 311 Fall 2019
 * last updated: 10/29/2019
 */
#include <string.h>
#include "mystring.h"
#include <stdlib.h>
#include <errno.h>
/*
 * to implement strcmp, tried to get all possible return values
 * but compiler would have optimization when inputs are two constant strings, both gcc and clang
 * 
 * get the index of first different char, using while loop, break when string get to the end
 * simply return the difference of two char ascii codes, using minus
 */
int mystrcmp(const char *s1, const char *s2) {
  int i = 0;
  
  while (s1[i] == s2[i]) {
    i++;
    if (s1[i] == '\0'){
      break;
    }
  }
/*  
  if (s1[i]<s2[i]) {
    return -1;
  }
  if (s1[i]>s2[i]) {
    return 1;
  }
  return 0;
*/
return s1[i]-s2[i];
//return strcmp(s1, s2);
}

/*
 * first get the size or length of the string, then malloc
 * according manual, malloc size+1
 * then if malloc failed, return null, may need casting to (char *)
 * or define another ptr pointing to the memory
 * set the values: char
 * return dup
 */
char *mystrdup(const char *s) {
  int size = 0;
  char *dup;
  while (s[size]) {
    size++;
  }
  dup = (char *)malloc(size * sizeof(char) + 1);
  if (!dup) {
    errno = ENOMEM;
    return (char *)NULL;
  }
  char *set = dup;
  while(*s != '\0') {
    *set = *s;
    set++;
    s++;
  }
  *set = '\0';
  return dup;
//return strdup(s);
}
