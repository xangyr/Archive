/* 
 * CS:APP Data Lab 
 * 
 * <Please put your name and userid here>
 * Author: Xiangyu Ren
 * Email: xvr5040@psu.edu
 * bits.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, although you might get a compiler warning. In general,
 * it's not good practice to ignore compiler warnings, but in this
 * case it's OK.  
 */

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to the Data Lab by
editing the collection of functions in this source file.

INTEGER CODING RULES:
 
  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code 
  must conform to the following style:
 
  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. Unary integer operations ! ~
  4. Binary integer operations & ^ | + << >>
    
  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, -, or ?:
  6. Use any form of casting.
  7. Use any data type other than int.  This implies that you
     cannot use arrays, structs, or unions.

 
  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting if the shift amount
     is less than 0 or greater than 31.


EXAMPLES OF ACCEPTABLE CODING STYLE:
  /*
   * pow2plus1 - returns 2^x + 1, where 0 <= x <= 31
   */
  int pow2plus1(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     return (1 << x) + 1;
  }

  /*
   * pow2plus4 - returns 2^x + 4, where 0 <= x <= 31
   */
  int pow2plus4(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     int result = (1 << x);
     result += 4;
     return result;
  }

FLOATING POINT CODING RULES

For the problems that require you to implement floating-point operations,
the coding rules are less strict.  You are allowed to use looping and
conditional control.  You are allowed to use both ints and unsigneds.
You can use arbitrary integer and unsigned constants. You can use any arithmetic,
logical, or comparison operations on int or unsigned data.

You are expressly forbidden to:
  1. Define or use any macros.
  2. Define any additional functions in this file.
  3. Call any functions.
  4. Use any form of casting.
  5. Use any data type other than int or unsigned.  This means that you
     cannot use arrays, structs, or unions.
  6. Use any floating point data types, operations, or constants.


NOTES:
  1. Use the dlc (data lab checker) compiler (described in the handout) to 
     check the legality of your solutions.
  2. Each function has a maximum number of operations (integer, logical,
     or comparison) that you are allowed to use for your implementation
     of the function.  The max operator count is checked by dlc.
     Note that assignment ('=') is not counted; you may use as many of
     these as you want without penalty.
  3. Use the btest test harness to check your functions for correctness.
  4. Use the BDD checker to formally verify your functions
  5. The maximum number of ops for each function is given in the
     header comment for each function. If there are any inconsistencies 
     between the maximum ops in the writeup and in this file, consider
     this file the authoritative source.

/*
 * STEP 2: Modify the following functions according the coding rules.
 * 
 *   IMPORTANT. TO AVOID GRADING SURPRISES:
 *   1. Use the dlc compiler to check that your solutions conform
 *      to the coding rules.
 *   2. Use the BDD checker to formally verify that your solutions produce 
 *      the correct answers.
 */


#endif
/* Copyright (C) 1991-2012 Free Software Foundation, Inc.
   This file is part of the GNU C Library.

   The GNU C Library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   The GNU C Library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with the GNU C Library; if not, see
   <http://www.gnu.org/licenses/>.  */
/* This header is separate from features.h so that the compiler can
   include it implicitly at the start of every compilation.  It must
   not itself include <features.h> or any other header that includes
   <features.h> because the implicit include comes before any feature
   test macros that may be defined in a source file before it first
   explicitly includes a system header.  GCC knows the name of this
   header in order to preinclude it.  */
/* We do support the IEC 559 math functionality, real and complex.  */
/* wchar_t uses ISO/IEC 10646 (2nd ed., published 2011-03-15) /
   Unicode 6.0.  */
/* We do not support C11 <threads.h>.  */
/* 
 * allEvenBits - return 1 if all even-numbered bits in word set to 1
 *   where bits are numbered from 0 (least significant) to 31 (most significant)
 *   Examples allEvenBits(0xFFFFFFFE) = 0, allEvenBits(0x55555555) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 2
 */
/*
 * set an 8 bit variable, expand to 0x55555555 and check
 */
int allEvenBits(int x) {
  int t = 85;
  t = t << 8 | t;
  t = t << 16 | t;
  return 0 | !(t ^ (t & x));
}
/* 
 * bang - Compute !x without using !
 *   Examples: bang(3) = 0, bang(0) = 1
 *   Legal ops: ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 4 
 */
/*
 * by shifting non-negative leads to 0, neg leads to -1
 * just make 1 become -1, then plus 1 to whole ret
 */
int bang(int x) {
  return (x >> 31 | (~x + 1) >> 31) + 1;
}
/* 
 * floatIsEqual - Compute f == g for floating point arguments f and g.
 *   Both the arguments are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representations of
 *   single-precision floating point values.
 *   If either argument is NaN, return 0.
 *   +0 and -0 are considered equal.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 25
 *   Rating: 2
 */
/*
 * set variables for essential shifting mask and fractions part
 * catch special cases like NaN or +0 -0
 * otherwise just cmp uf and ug
 */
int floatIsEqual(unsigned uf, unsigned ug) {
  unsigned m1 = ~(1 << 31);
  unsigned m2 = ~0 + (1 << 23);

  unsigned frac_f = uf & m1;
  unsigned frac_g = ug & m1;

  if (!frac_f && !frac_g) {
    return 1;
  }
  if (((frac_f >> 23) == 0xFF && (uf & m2)) || ((frac_g >> 23) == 0xFF && (ug & m2))) {
    return 0;
  }
  return uf == ug;
}

/* 
 * floatUnsigned2Float - Return bit-level equivalent of expression (float) u
 *   Result is returned as unsigned int, but
 *   it is to be interpreted as the bit-level representation of a
 *   single-precision floating point values.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
/*
 * know where bits start using while loop
 * set exp to 31, don't know why 32 doesn't work
 * 
 * then check if in fraction bits part ,if..else then shl or shr
 * bias 127, 1+8+23
 * round to nearest even if needed (use constant 55 : 24+31)
 * TODO 
 * 1)round, check if carry on, check if needed 
 * 2)decrese 1 # of operator
 * (just found that in c can write nothing in if statement and use else, saving ops) 
 */
unsigned floatUnsigned2Float(unsigned u) {
  unsigned e, exp;
  if (!u) {
    return 0;
  }
  e = 31;
  while ((u & (1 << e)) == 0) {
    e--;
  }
  if (e < 24) {
    u = u << (23 - e);
  } 
  else {
    u += (1 << (e - 24));

    if (u << (55 - e)) {
      
    }
    else {
      u = u & (~0 << (e - 22));
    }
    if (u & (1 << e)) {

    } 
    else { 
      e++; 
    }
    u = u >>(e - 23);
  }
  exp = (e + 127) << 23;
  return exp | (u & ((~0) + (1 << 23)));
}
/* 
 * isLess - if x < y  then return 1, else return 0 
 *   Example: isLess(4,5) = 1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 24
 *   Rating: 3
 */
/*
 * to return 1, either diff sign which x < 0,
 * or same sign bit x-y is negative
 */
int isLess(int x, int y) {
  return ((x & ~y) | (~(x ^ y) & (x + (~y + 1)))) >> 31 & 1;
}
/* 
 * isNonNegative - return 1 if x >= 0, return 0 otherwise 
 *   Example: isNonNegative(-1) = 0.  isNonNegative(0) = 1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 6
 *   Rating: 2
 */
/*
 * non-negative shift right 31 bits is 0
 * plus 1 handles
 */
int isNonNegative(int x) {
  return (x >> 31) + 1;
}
/*
 * isTmax - returns 1 if x is the maximum, two's complement number,
 *     and 0 otherwise 
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 10
 *   Rating: 1
 */
/*
 * 2's complement max is 1 bit of 0 with 31 bits of 1s
 * to tmax x+1 is also ~x
 */
int isTmax(int x) {
  return (!!(x + 1)) & !(~ ((x + 1) ^ x));
}
/* 
 * rotateLeft - Rotate x to the left by n
 *   Can assume that 0 <= n <= 31
 *   Examples: rotateLeft(0x87654321,4) = 0x76543218
 *   Legal ops: ~ & ^ | + << >> !
 *   Max ops: 25
 *   Rating: 3 
 */
/*
 * shift to left to get extra bits of 0
 * shift to right to get bits that are lost
 * then use |
 */
int rotateLeft(int x, int n) {
  return (x << n) | ((~(~0 << n)) & (x >> (32 + (~n + 1))));
}
/* 
 * signMag2TwosComp - Convert from sign-magnitude to two's complement
 *   where the MSB is the sign bit
 *   Example: signMag2TwosComp(0x80000005) = -5.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 4
 */
/*
 * remove the sign bit, then 2 cases
 * to positive, keep
 * to negative ~x+1
 */
int signMag2TwosComp(int x) {
  return (x & ~(x >> 31)) | ((~(~(1 << 31) & x) + 1) & (x >> 31));
}
/* 
 * thirdBits - return word with every third bit (starting from the LSB) set to 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 8
 *   Rating: 1
 */
/*
 * create an 8bits variable
 * then shift left to expand and follow the path
 */
int thirdBits(void) {
  int x = 73;
  x = x << 9 | x;
  return x << 18 | x;
}
