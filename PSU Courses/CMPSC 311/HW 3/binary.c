#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int main(int argc, char *argv[]) {
  unsigned long int i;
  // checking there is a command line argument
  if (argc != 2) {
    printf("Usage: %s number\n", argv[0]);
    return 0;
  }
  // converting the command line argument to a unsigned long
  // and exit program if there is an error during the conversion.
  errno = 0;
  i = strtoul(argv[1], NULL, 0);
  if (errno != 0) {
    perror("Failed to convert number");
    return 0;
  }
  // write your solutions below this line

  // define variables needed & use a loop which ends when i is 0
  // save numbers into array backwards then print from the front
  int base2[64];
  // printf("%lu\n", i);
  int j = 63;

  do { 
    base2[j] = i % 2;
    i /= 2;
    j--;
  } while(i != 0);
  
  for(j += 1;j < 64;j++) {
    printf("%d", base2[j]);
  }
  
  printf("\n");
  // write your solutions above this line
  return 0;
}
