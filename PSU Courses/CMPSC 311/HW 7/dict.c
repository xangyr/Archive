/*
 * author: Xiangyu Ren
 * email: xvr5040@psu.edu
 * dict.c for CMPSC 311 Fall 2019
 * last updated: 10/23/2019
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dict.h"

// count number of keys in a dict.

// create a variable to count the number
// TODO
//    create a const dictNode current or use dict instead
//    might change the ptr pointing the head node
// use while loop to stop when the node is NULL
int countKeys(const dictNode *dict) {
  int count = 0;
  //dictNode *current = dict;

  while (dict) {
    count++;
    dict = dict->next;
  }
  return count;
}

// given a key, look up its corresponding value in the
// dictionary, returns -1 if the value is not in the dictionary.
// your search for key should end when the key in the next node
// is bigger than the lookup key or you reached the end of the
// list.

// use while loop to check thru every node in the dict
// TODO
//    if current node key bigger than the look up key, break
//    return the value when reach the look up key
//    return -1 when the current node reach NULL (not found)
//        or the dict is NULL
int lookupKey(const dictNode *dict, const char *key) {
  //dictNode *current = dict;

  while (dict) {
    if (strcmp(dict->key, key) > 0) {
      break;
    }
    if (strcmp(dict->key, key) == 0) {
      return dict->value;
    }
    dict = dict->next;
  }
  return -1;
}

// delete the node in a dict with given key, return the value of
// the deleted node if it was found, return -1 if it wasn't found.

// create a dictNode current pointing the head of the dict
// create temp to store the delete node and val to store the value of the node
// TODO 
//    check if the dict is NULL, or will segmentation fail
//    then handle 2 cases: delete the head node or others
//    use while loop to check the next node 
//
// if the head node, ptr point to the next node
// if other nodes return -1 when disordered linked list or not found
//                return value of next node, current->next = current->next->next
// free node when found
int deleteKey(dictNode **dictPtr, const char *key) {
  dictNode *current = *dictPtr;
  dictNode *temp = NULL;
  int val = 0;
  
  if (!current) {
    return -1;
  }
  if (strcmp(current->key, key) == 0) { 
    val = current->value;
    *dictPtr = current->next;
    freeNode(current);
    return val;
  }
  while (current->next) {
    if (strcmp(current->key, key) > 0) {
      return -1;
    }
    if (strcmp(current->next->key, key) == 0) {
      temp = current->next;
      val = temp->value;
      current->next = temp->next;
      freeNode(temp);
      return val;
    }
    current = current->next;
  }

  return -1;
}

// given a key/value pair, first lookup the key in the dictionary,
// if it is already there, update the dictionary with the new
// value; if it is not in the dictionary, insert a new node into
// the dictionary, still make sure that the key is in alphabetical
// order.
// IMPORTANT: When creating a new node, make sure you dynamically
// allocate memory to store a copy of the key in the memory. You
// may use strdup function. DO NOT STORE the input key from the 
// argument directly into the node. There is no guarantee that key
// pointer's value will stay the same. 
// YOU MUST KEEP THE ALPHABETICAL ORDER OF THE KEY in the dictionary.

// create 3 dictNode:
//    current point to the dict
//    temp to store the new node
//    prev point to the previous node which prev->next is current
//    using method in dict_support.c to create a new node and store in temp
//    set next default to NULL and k nd v
// 
// TODO
//    handle cases:
//    1. dict is NULL
//    2. dict maked, no key matches
//        a. new node key smaller than the current key
//            i. new node be the new head of the dict
//            ii. new node insert in the middle of dict
//        b. new node key bigger than the current key
//    3. dict maked, keys match
//
//    free node temp (don't know if necessary)
//
// case 1:    set ptr pointing to temp, temp->next = NULL (default)
// case 2ai:  set ptr pointing to temp, temp->next = current
// case 2aii: set prev->next = temp, temp->next = current
// case 2b:   set current->next = temp, temp->next = null
// case 3:    set current value, free temp

void addKey(dictNode **dictPtr, const char *key, int value) {
  dictNode *current = *dictPtr;
  dictNode *temp = NULL;
  dictNode *prev = NULL;
  
  temp = malloc(sizeof(dictNode));
  temp->key = strdup(key);
  temp->value = value;
  temp->next = NULL;
// case 1
  if (!current) {
    *dictPtr = temp;
    return;
  }
  while (current) {
// case 2a
    if (strcmp(current->key, key) > 0) {
      temp->next = current;
// case i
      if (!prev) {
        *dictPtr = temp;
        return;
      }
// case ii
      prev->next = temp;
      return;
    }
// case 3
    else if (strcmp(current->key, key) == 0) {
      current->value = value;
      freeNode(temp);
      return;
    }
    prev = current;
    current = current->next;
  }
// case 2b
  current = temp;
  prev->next = current;
  return;
}
