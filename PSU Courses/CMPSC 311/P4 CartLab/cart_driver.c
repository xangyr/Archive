////////////////////////////////////////////////////////////////////////////////
//
//  File           : cart_driver.c
//  Description    : This is the implementation of the standardized IO functions
//                   for used to access the CART storage system.
//
//  Author         : Xiangyu Ren
//  PSU email      : xvr5040@psu.edu
//  Failed: can't pass test6, may be something wrong with allocating new frame
//          don't think the data structure is built wrongly

// Includes
#include <stdlib.h>
#include <string.h>

// Project Includes
#include "cart_driver.h"
#include "cart_controller.h"

//Maximum frames a file can access
#define CART_MAX_FRAME 100
//create for rt1
typedef unsigned char uint1_t;
//file counters: how many in he sys
int file_cnt = 0;
/*
 to help find static location in sys
 */
struct frame{
  CartridgeIndex IC;
  CartFrameIndex IF;
};
/*
 create struct inode to store info for a file
 name: 128 byts file name
 size: size of the file
 pos: current position in the file
 isopen: -1 unintialized, 0 closed, 1 opened
 frame_cnt: numbers of frames the file access
 struct frames: to allocate the physical location in sys, has frameid and cartid
 */
struct inode{
  char name[CART_MAX_PATH_LENGTH];
  int size;
  int pos;
  int isopen;
  int frame_cnt;
  struct frame id[CART_MAX_FRAME];
};
//declaration for global variables
//array to store files' meta
struct inode filehandle[CART_MAX_TOTAL_FILES];
//for allocating frame
struct frame next;

/*
 implement create_op to setup opcodes, 8|8|1|16|16|unused
 variable type is uint64, left shift to the response location
 */
CartXferRegister create_op (CartXferRegister ky1, CartXferRegister ky2, CartXferRegister rt1, CartXferRegister ct1, CartXferRegister fm1) {
  return (((ky1&0xff) << 56)|((ky2&0xff) << 48)|((rt1&0x1) << 47)|((ct1&0xffff) << 31)|((fm1&0xffff) << 15)|0x0);
}

/*
 implement extract_op to get bits for each register
 */
void extract_op (CartXferRegister opcode, uint8_t *ky1, uint8_t *ky2, uint1_t * rt1, uint16_t *ct1, uint16_t *fm1) {
  *ky1 = (uint8_t)(opcode >> 56);
  *ky2 = (uint8_t)((opcode << 8) >> 56);
  *rt1 = (uint1_t)((opcode << 9) >> 63);
  *ct1 = (uint16_t)((opcode << 17) >> 48);
  *fm1 = (uint16_t)((opcode << 33) >> 48);
  return;
}
/*
 implement check_rt1 to check rt1, 0 is successful, -1 is failed
 */
int check_rt1(CartXferRegister oregstate) {
  uint8_t ky1, ky2;
  uint1_t rt1;
  uint16_t ct1, fm1;
  extract_op(oregstate, &ky1, &ky2, &rt1, &ct1, &fm1);
  if (rt1 == -1) {
    return (-1);
  }
  return (0);
}
/*
 implement 3 op_helper functions for opcode
 */
/*
 helper_ky1 when opcode is initms, bzero, or powoff, since only need ky1 changed
 */
int op_helper_ky1(CartOpCodes opcode) {
  CartXferRegister regstate = 0, oregstate = 0;
  
  //if (opcode == CART_OP_INITMS || opcode == CART_OP_BZERO || opcode == CART_OP_POWOFF)
  regstate = create_op(opcode, 0, 0, 0, 0);
  oregstate = cart_io_bus(regstate, NULL);
  
  return (check_rt1(oregstate));
}
/*
 helper_ky1_ct1 when opcode is ldcart
 index: the cart index need to be loaded
 */
int op_helper_ky1_ct1(CartOpCodes opcode, uint16_t index) {
  CartXferRegister regstate = 0, oregstate = 0;
  
  //if (opcode == CART_OP_LDCART)
  regstate = create_op(opcode, 0, 0, index, 0);
  oregstate = cart_io_bus(regstate, NULL);
  return (check_rt1(oregstate));
}
/*
 helper_ky1_fm1 when opcode is rdfrme or wrfrme
 index: the frame index need to be accessed
 buf: to store the data
 */
int op_helper_ky1_fm1(CartOpCodes opcode, uint16_t index, char *buf) {
  CartXferRegister regstate = 0, oregstate = 0;
  
  //if (opcode == CART_OP_RDFRME || opcode == CART_OP_WRFRME)
  regstate = create_op(opcode, 0, 0, 0, index);
  oregstate = cart_io_bus(regstate, buf);
  
  return (check_rt1(oregstate));
}

//
// Implementation

////////////////////////////////////////////////////////////////////////////////
//
// Function     : cart_poweron
// Description  : Startup up the CART interface, initialize filesystem
//
// Inputs       : none
// Outputs      : 0 if successful, -1 if failure

int32_t cart_poweron(void) {
  CartXferRegister i;
  //initialize mem system
  if (op_helper_ky1(CART_OP_INITMS) == -1) {
    return (-1);
  }
  //through out the sys and zero out every cart
  for (i = 0; i < CART_MAX_CARTRIDGES; i++) {
    if (op_helper_ky1_ct1(CART_OP_LDCART, i) == -1) {
      return (-1);
    }
    if (op_helper_ky1(CART_OP_BZERO) == -1) {
      return (-1);
    }
  }
  //initialize files
  for (i = 0; i < CART_MAX_TOTAL_FILES; i++) {
    filehandle[i].name[0] = '\0';
    filehandle[i].pos = 0;
    filehandle[i].size = 0;
    filehandle[i].isopen = -1;
    filehandle[i].frame_cnt = -1;
  }
  //set to zeros for allocating frame
  next.IC = 0;
  next.IF = 0;
  // Return successfully
  return(0);
}

////////////////////////////////////////////////////////////////////////////////
//
// Function     : cart_poweroff
// Description  : Shut down the CART interface, close all files
//
// Inputs       : none
// Outputs      : 0 if successful, -1 if failure

int32_t cart_poweroff(void) {
  CartXferRegister i;
  //close all files
  for (i = 0; i < CART_MAX_TOTAL_FILES; i++) {
    filehandle[i].isopen = 0;
  }
  //poweroff mem system
  if (op_helper_ky1(CART_OP_POWOFF) == -1) {
    return (-1);
  }
  //set to zeros for allocating
  next.IC = 0;
  next.IF = 0;
  // Return successfully
  return(0);
}

////////////////////////////////////////////////////////////////////////////////
//
// Function     : cart_open
// Description  : This function opens the file and returns a file handle
//
// Inputs       : path - filename of the file to open
// Outputs      : file handle if successful, -1 if failure

int16_t cart_open(char *path) {
  if (path == NULL) {
    return (-1);
  }
  int i;
  //go through filehandle to check if is opened
  //and detect current input path
  for (i = 0; i < file_cnt; i++) {
    if (filehandle[i].isopen != -1 && strcmp(path, filehandle[i].name) == 0) {
      filehandle[i].isopen = 1;
      filehandle[i].pos = 0;
      return i;
    }
  }
  //if not found, initialize a filehandle and open file
  //update meta for the file
  //file counter + 1
  strncpy(filehandle[i+1].name, path, sizeof(filehandle[i].name));
  filehandle[i+1].size = 0;
  filehandle[i+1].pos = 0;
  filehandle[i+1].isopen = 1;
  filehandle[i+1].frame_cnt = -1;
  file_cnt += 1;
  
  // THIS SHOULD RETURN A FILE HANDLE
  return (file_cnt);
}

////////////////////////////////////////////////////////////////////////////////
//
// Function     : cart_close
// Description  : This function closes the file
//
// Inputs       : fd - the file descriptor
// Outputs      : 0 if successful, -1 if failure

int16_t cart_close(int16_t fd) {
  //check if fd is valid or file is closed
  if (fd < 0 || fd > CART_MAX_TOTAL_FILES || filehandle[fd].isopen != 1) {
    return (-1);
  }
  //if not, close the file
  filehandle[fd].isopen = 0;
  
  // Return successfully
  return (0);
}

////////////////////////////////////////////////////////////////////////////////
//
// Function     : cart_read
// Description  : Reads "count" bytes from the file handle "fh" into the 
//                buffer "buf"
//
// Inputs       : fd - filename of the file to read from
//                buf - pointer to buffer to read into
//                count - number of bytes to read
// Outputs      : bytes read if successful, -1 if failure

int32_t cart_read(int16_t fd, void *buf, int32_t count) {
  /*
   buffer: temp buf holded each frame, since read frame by frame
   rest_cnt: the rest counter
   pos: position in the file
   size: size of the file
   bytes_n: numbers of bytes to read
   buf_ptr: the postion in the buffer
   */
  char *buffer = (char *)malloc(CART_FRAME_SIZE);
  int32_t rest_cnt;
  int pos, size;
  int bytes_n;
  int buf_ptr = 0;
  //check if fd is valid, buf is setted, count is valid
  //also check file is not closed
  if (fd < 0 || fd > CART_MAX_TOTAL_FILES || buf == NULL || count < 0 || filehandle[fd].isopen != 1) {
    free(buffer);
    return (-1);
  }
  
  pos = filehandle[fd].pos;
  size = filehandle[fd].size;
  //set file metas
  if (count > (size - pos)) {
    count = size - pos;
    filehandle[fd].pos = size;
  } else {
    filehandle[fd].pos += count;
  }
  //create variables offset, logical frame location
  rest_cnt = count;
  int offset = pos % CART_FRAME_SIZE;
  int frame_log = pos / CART_FRAME_SIZE;
  //load the cart with location IC in file with index frame_log
  if (op_helper_ky1_ct1(CART_OP_LDCART, filehandle[fd].id[frame_log].IC) == -1) {
    free(buffer);
    return (-1);
  }
  //read frame with location IF in file wiht index frame_log
  if (op_helper_ky1_fm1(CART_OP_RDFRME, filehandle[fd].id[frame_log].IF, buffer) == -1) {
    free(buffer);
    return (-1);
  }
  //if count > rest space in frame, first read rest data in frame
  //if not, just read count bytes data
  if (rest_cnt > (CART_FRAME_SIZE - offset)) {
    bytes_n = CART_FRAME_SIZE - offset;
  } else {
    bytes_n = rest_cnt;
  }
  //copy data to buf
  //update pointer of buffer and rest counter
  memcpy(buf, &buffer[offset], bytes_n);
  buf_ptr += bytes_n;
  rest_cnt -= bytes_n;
  //now in the new frame, just read and update
  while (rest_cnt > 0) {
    frame_log = (pos + bytes_n) / CART_FRAME_SIZE;
    //load the cart with location IC in file with index frame_log
    if (op_helper_ky1_ct1(CART_OP_LDCART, filehandle[fd].id[frame_log].IC) == -1) {
      free(buffer);
      return (-1);
    }
    //read frame with location IF in file wiht index frame_log
    if (op_helper_ky1_fm1(CART_OP_RDFRME, filehandle[fd].id[frame_log].IF, buffer) == -1) {
      free(buffer);
      return (-1);
    }
    //read rest counter bytes not 1024 bytes
    if (rest_cnt > CART_FRAME_SIZE) {
      bytes_n = CART_FRAME_SIZE;
    } else {
      bytes_n = rest_cnt;
    }
    //copy data to buf
    //update pointer and rest counter
    buf += buf_ptr;
    memcpy(buf, buffer, bytes_n);
    buf_ptr += bytes_n;
    rest_cnt -= bytes_n;
  }
  free(buffer);
  // Return successfully
  return (count);
}

////////////////////////////////////////////////////////////////////////////////
//
// Function     : cart_write
// Description  : Writes "count" bytes to the file handle "fh" from the 
//                buffer  "buf"
//
// Inputs       : fd - filename of the file to write to
//                buf - pointer to buffer to write from
//                count - number of bytes to write
// Outputs      : bytes written if successful, -1 if failure

int32_t cart_write(int16_t fd, void *buf, int32_t count) {
  /*
   buffer: temp buf holded each frame, since read frame by frame
   rest_cnt: the rest counter
   pos: position in the file
   size: size of the file
   bytes_n: numbers of bytes to read
   buf_ptr: the postion in the buffer
   */
  char *buffer = (char *)malloc(CART_FRAME_SIZE);
  int32_t rest_cnt;
  int pos, size;
  int bytes_n;
  int buf_ptr = 0;
  //check if fd is valid, buf is setted, count is valid
  //also if file is not closed
  if (fd < 0 || fd > CART_MAX_TOTAL_FILES || buf == NULL || count < 0 || filehandle[fd].isopen != 1) {
    free(buffer);
    return (-1);
  }
  //create variables offset, logical frame location
  rest_cnt = count;
  pos = filehandle[fd].pos;
  size = filehandle[fd].size;
  int offset = pos % CART_FRAME_SIZE;
  int frame_log = pos / CART_FRAME_SIZE;
  //update metas for filehandle
  if ((pos + count) > size) {
    filehandle[fd].size = pos + count;
  }
  filehandle[fd].pos = pos + count;
  //if offset is not zero, position is not multiple of 1024
  //first read 1024 bytes, then overwrite
  if (offset > 0) {
    //need to allocate new frame
    if (frame_log > filehandle[fd].frame_cnt) {
      filehandle[fd].id[frame_log].IC = next.IC;
      filehandle[fd].id[frame_log].IF = next.IF;
      if (next.IC >= (CART_CARTRIDGE_SIZE - 1)) {
        next.IC++;
        next.IF = 0;
      } else {
        next.IF++;
      }
      filehandle[fd].frame_cnt++;
    }
    //load the cart with location IC in file with index frame_log
    if (op_helper_ky1_ct1(CART_OP_LDCART, filehandle[fd].id[frame_log].IC) == -1) {
      free(buffer);
      return (-1);
    }
    //read from frame with location IF in file with index frame_log
    if (op_helper_ky1_fm1(CART_OP_RDFRME, filehandle[fd].id[frame_log].IF, buffer) == -1) {
      free(buffer);
      return (-1);
    }
    //update bytes number
    if (rest_cnt > (CART_FRAME_SIZE - offset)) {
      bytes_n = CART_FRAME_SIZE - offset;
    } else {
      bytes_n = rest_cnt;
    }
    //copy data to buf
    //update pointer and rest counter
    memcpy(&buffer[offset], buf + buf_ptr, bytes_n);
    buf_ptr += bytes_n;
    rest_cnt -= bytes_n;
    //write to frame with location IF in file with index frame_log
    if (op_helper_ky1_fm1(CART_OP_WRFRME, filehandle[fd].id[frame_log].IF, buffer) == -1) {
      free(buffer);
      return (-1);
    }
    //update frame location
    frame_log++;
  }
  //temp: hold full write frame numbers
  int temp = rest_cnt / CART_FRAME_SIZE;
  //when position is multiple of 1024
  while (temp) {
    memcpy(buffer, buf + buf_ptr, CART_FRAME_SIZE);
    buf_ptr += CART_FRAME_SIZE;
    //if space is not enough, allocate new frame
    if (frame_log > filehandle[fd].frame_cnt) {
      filehandle[fd].id[frame_log].IC = next.IC;
      filehandle[fd].id[frame_log].IF = next.IF;
      if (next.IC >= (CART_CARTRIDGE_SIZE - 1)) {
        next.IC++;
        next.IF = 0;
      } else {
        next.IF++;
      }
      filehandle[fd].frame_cnt++;
    }
    //have enough frame space, first read out data in frame then write in a whole
    if (op_helper_ky1_ct1(CART_OP_LDCART, filehandle[fd].id[frame_log].IC) == -1) {
      free(buffer);
      return (-1);
    }
    if (op_helper_ky1_fm1(CART_OP_WRFRME, filehandle[fd].id[frame_log].IF, buffer) == -1) {
      free(buffer);
      return (-1);
    }
    //update frame location
    frame_log++;
    temp--;
  }
  rest_cnt %= CART_FRAME_SIZE;
  //has data left to write in, read 1024 bytes first
  if (rest_cnt > 0) {
    if (frame_log > filehandle[fd].frame_cnt) {
      filehandle[fd].id[frame_log].IC = next.IC;
      filehandle[fd].id[frame_log].IF = next.IF;
      if (next.IC >= (CART_CARTRIDGE_SIZE - 1)) {
        next.IC++;
        next.IF = 0;
      } else {
        next.IF++;
      }
      filehandle[fd].frame_cnt++;
    }

    if (op_helper_ky1_ct1(CART_OP_LDCART, filehandle[fd].id[frame_log].IC) == -1) {
      free(buffer);
      return (-1);
    }
    if (op_helper_ky1_fm1(CART_OP_RDFRME, filehandle[fd].id[frame_log].IF, buffer) == -1) {
      free(buffer);
      return (-1);
    }
    memcpy(&buffer[offset], buf + buf_ptr, rest_cnt);
    if (op_helper_ky1_fm1(CART_OP_WRFRME, filehandle[fd].id[frame_log].IF, buffer) == -1) {
      free(buffer);
      return (-1);
    }
    //update frame location
    frame_log++;
  }
  
  // Return successfully
  free(buffer);
  return (count);
}

////////////////////////////////////////////////////////////////////////////////
//
// Function     : cart_read
// Description  : Seek to specific point in the file
//
// Inputs       : fd - filename of the file to write to
//                loc - offset of file in relation to beginning of file
// Outputs      : 0 if successful, -1 if failure

int32_t cart_seek(int16_t fd, uint32_t loc) {
  //check if fd is valid
  if (fd < 0 || fd > CART_MAX_TOTAL_FILES) {
    return (-1);
  }
  //check if offset is valid
  if (filehandle[fd].size < loc) {
    return (-1);
  }
  //if not update the location
  filehandle[fd].pos = loc;
  
  // Return successfully
  return (0);
}
