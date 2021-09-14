// Author: Xiangyu Ren
// Email: xvr5040@psu.edu
#include <stdlib.h>
// rotate the values pointed to by three pointers
// so values move from xp to yp, yp to zp and zp to xp

// 
// set a temp val equal to *xp since interface would change value directly
// then rotate using 4 variables
void rotate(int *xp, int *yp, int *zp) {
  int val = *xp;
  *xp = *zp;
  *zp = *yp;
  *yp = val;
  return;
}

// Write a function that returns 0 if x is 0, returns -1 
// if x < 0, returns 1 if x > 0
// Your code must follow the Bit-Level Integer Coding Rules
// on the textbook (located between hw 2.60 and 2.61).
// You can assume w = 32. 
// The only allowed operations in your code are:
// ! ~ & ^ | + << >>
// This requirement is more restrictive than the coding rules. 

//
// my orig return is (x>>31)-(-x>>31) can't pass int_min and wrong op
// right shift 31 bits can determine neg or non-neg
// so use | to make sure -1 won't be changed
// want to get 0|0 or 0|1 for non-neg
// to 0, 0_not is -1, so will end up with 0
// to pos, just make sure after shifting will always be -1
int sign(int x) {
  return (x>>31) | (~((~x+1)>>31)+1);
}

// Given a source string, and a destination string, write the
// reversed source string into destination. Make sure you terminate
// the reversed string properly with an integer value 0.
// You may assume that the destination array is big enough to hold
// the reversed string. 

// 
// since in the argv are pointers of array
// if source is empty, set dest to empty with \0
// then jump to the end of the src, using i to count the steps
// src jump backwards while dest jump forwards
// when i reach 0 set the end of dest to \0
void reverse(const char source[], char destination[]) {
  if (*source == '\0') {
    *destination = '\0';
  }
  else {
    int i = 0;
    while (*source) {
      source++;
      i++;
    }
    while (i >= 0) {
      source--;
      i--;
      *destination = *source;
      destination++;
    }
    *destination = '\0';
  }
  return;
}
