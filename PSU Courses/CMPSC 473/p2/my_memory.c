// Include files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define  N_OBJS_PER_SLAB    (64)
#define  N_CHUNK            (11)
#define  HEADER_SZ          (4)
#define  INVALID_TYPE       (-1)

// Functional prototypes
void setup( int malloc_type, int mem_size, void* start_of_memory );
void *my_malloc( int size );
void my_free( void *ptr );

// store the malloc_type
static int _malloc_type;

// all 11 possible sizes in buddy allocation, in bytes unit
const int _chunk_sz_tbl[N_CHUNK] = { 1*1024, 2*1024, 4*1024, 8*1024, 16*1024,
                                  32*1024, 64*1024, 128*1024, 256*1024,
                                  512*1024, 1024*1024};

typedef struct _addr {
    // starting address of current buddy allocation
    // buddy header included
    void *start_addr;

    // end address of the current buddy allocation
    void *end_addr;

    // in bytes units
    int size;
} _addr_t;

struct _addr_list {
    _addr_t addr;
    struct _addr_list *next;
};

typedef struct _addr_list _addr_list_t;

// each point to head of a linked list, each linked list
// maintains a free list corresponds to size in _chunk_sz_tbl[]
static _addr_list_t *_free_lists[N_CHUNK];

#ifndef uint64_t
#define uint64_t unsigned long long
#endif

struct _slab_ptr {
    // bitmap for all N_OBJS_PER_SLAB chunks
    uint64_t bitmap;

    // start address of the current slab
    void *addr;

    struct _slab_ptr *next;
};

typedef struct _slab_ptr _slab_ptr_t;

typedef struct {
    // chunk size as the type, headers not included
    int type;

    // the size of the current slab, in bytes unit
    // buddy's header is not included
    int size;

    // the maximum number of chunks
    int numObj;

    // the number of current occupied chunks
    int usedObj;

    // a linked list, point to the chunk's bitmap structure
    // also the address of each slab is included
    _slab_ptr_t *slab_ptr;
} _slab_dsc_tbl_t;

// point to the slab descriptor table
_slab_dsc_tbl_t *_slab_dsc_tbl;

// generate 64bit mask to abstract the free chunk from the bitmap
static uint64_t mask(int i) {
    return (uint64_t)1 << i;
}

// get the header _addr_list_t of a free linked list
static _addr_list_t *get_head(int id) {
    return _free_lists[id];
}

// insert the input addr into the free linked list
// since after insert, the list is ordered by start_addr, so need a search first
static void insert_elem(int id, _addr_t addr) {
    _addr_list_t *obj = (_addr_list_t *)malloc(sizeof(_addr_list_t));
    if (obj == NULL) {
        fprintf(stderr, "func:%s, line:%d. cannot allocate new object!\n", __func__, __LINE__);
        exit(-1);
    }

    obj->addr.start_addr = addr.start_addr;
    obj->addr.end_addr = addr.end_addr;
    obj->addr.size = addr.size;

    // consider three cases
    // 1. the list is empty
    // 2. the "addr" should be inserted before the head
    // 3. other normal cases
    _addr_list_t *p = get_head(id);
    if (get_head(id) == NULL) {
        obj->next = NULL;
        _free_lists[id] = obj;
    } else if (addr.start_addr < p->addr.start_addr) {
        obj->next = get_head(id);
        _free_lists[id] = obj;
    } else {
        while (p != NULL) {
            _addr_list_t *next = p->next;
            if ((next == NULL)||(addr.start_addr < next->addr.start_addr)) {
                p->next = obj;
                obj->next = next;
                break;
            }

            p = p->next;
        }
    }
}

// delete a specific element from the linked list
static int remove_elem(int id, void *start_addr) {
    _addr_list_t *p = get_head(id);

    if (p == NULL) {
        fprintf(stderr, "func:%s, line:%d. _free_lists[%d] is empty!\n", __func__, __LINE__, id);
        exit(-1);
    }

    if (p->addr.start_addr == start_addr) {
        _free_lists[id] = p->next;
        free(p);
        return 0;
    } else {
        _addr_list_t *prev = p;
        p = p->next;

        while (p != NULL) {
            if (p->addr.start_addr == start_addr) {
                prev->next = p->next;
                free(p);
                return 0;
            }

            prev = p;
            p = p->next;
        }
    }

    return -1;
}

// delete the first head element from the linked list
static void pop(int id) {
    _addr_list_t *p = get_head(id);

    if (p == NULL) {
        fprintf(stderr, "func:%s, line:%d. _free_lists[%d] is empty!\n", __func__, __LINE__, id);
        exit(-1);
    }

    remove_elem(id, p->addr.start_addr);
}

// returns the previous element to the input
static _addr_list_t *find_prev(int id, void *start_addr) {
    _addr_list_t *p = _free_lists[id];

    if (p == NULL) {
        fprintf(stderr, "func:%s, line:%d. _free_lists[%d] is empty!\n", __func__, __LINE__, id);
        exit(-1);
    }

    if (p->addr.start_addr == start_addr) {
        // if "start_addr" is the head of the linked list, then
        // return NULL
        return NULL;
    } else {
        _addr_list_t *prev = p;
        p = p->next;

        while (p != NULL) {
            if (p->addr.start_addr == start_addr) {
                return prev;
            }

            prev = p;
            p = p->next;
        }

        // if there is no matching "start_addr" within the linked list
        // also return NULL
        return NULL;
    }
}

// returns the next element to the input
_addr_list_t *find_next(int id, void *start_addr) {
    _addr_list_t *p = _free_lists[id];

    if (p == NULL) {
        fprintf(stderr, "func:%s, line:%d. _free_lists[%d] is empty!\n", __func__, __LINE__, id);
        exit(-1);
    }

    return p->next;
}

// get the index of _chunk_sz_tbl from input size
static int chunksz2id(int size) {
    for (int i = 0; i < N_CHUNK; i++) {
        if (_chunk_sz_tbl[i] == size) {
            return i;
        }
    }

    fprintf(stderr, "func:%s, line:%d. size=%d is not found in _chunk_sz_tbl!\n", __func__, __LINE__, size);
    return INVALID_TYPE;
}

////////////////////////////////////////////////////////////////////////////
//
// Function     : setup
// Description  : initialize the memory allocation system
//
// Inputs       : malloc_type - the type of memory allocation method to be used [0..3] where
//                (0) Buddy System
//                (1) Slab Allocation

void setup( int malloc_type, int mem_size, void* start_of_memory ) {
    _malloc_type = malloc_type;

    for (int i = 0; i < N_CHUNK; i++) {
        _free_lists[i]= NULL;
    }

    _addr_t addr;
    addr.start_addr = start_of_memory;
    addr.end_addr = start_of_memory + mem_size - 1;
    addr.size = mem_size;
    insert_elem(N_CHUNK - 1, addr);

    _slab_dsc_tbl = NULL;
}

// round the input to the closest values in _chunk_sz_tbl
// the input "size_wo_header" does not contains the header size
static int round2chunkid(int size_wo_header) {
    int size = size_wo_header + HEADER_SZ;

    // even the largest value in _chunk_sz_tbl is smaller than "size"
    if (size > _chunk_sz_tbl[N_CHUNK - 1]) {
        return -1;
    }

    // even the smallest value in _chunk_sz_tbl is larger than "size"
    if (size <= _chunk_sz_tbl[0]) {
        return 0;
    }

    for (int i = 1; i < N_CHUNK; i++) {
        if (size <= _chunk_sz_tbl[i]) {
            // if runs here, it must be larger than _chunk_sz_tbl[i-1]
            return i;
        }
    }

    fprintf(stderr, "func:%s, line:%d. should not run here!\n", __func__, __LINE__);
    exit(-1);
}

// segment from level=id to level id-1. Use the recursive method.
static int segment(int id) {
    if (id > N_CHUNK - 1) {
        // id = N_CHUNK - 1 is the last level chunk
        // if runs here, mean all low level chunk is full
        return -1;
    } else if (get_head(id) == NULL) {
        int ret = segment(id + 1);
        if (ret < 0) {
            return ret;
        }
    }

    // it still needs to run here, if 1) the first call of segment runs here
    //                       2) returns from higher level chunk calls
    _addr_t *high = &get_head(id)->addr;

    int size = high->size / 2;
    _addr_t low_left;
    low_left.start_addr = high->start_addr;
    low_left.end_addr = high->start_addr + size - 1;
    low_left.size = size;

    _addr_t low_rht;
    low_rht.start_addr = high->start_addr + size;
    low_rht.end_addr = high->end_addr;
    low_rht.size = size;

    pop(id);
    insert_elem(id - 1, low_left);
    insert_elem(id - 1, low_rht);

    return 0;
}

static void *my_malloc_buddy( int size ) {
    int id = round2chunkid(size);

    if (id < 0 || size <= 0) {
        return NULL;
    }

    if (get_head(id) == NULL) {
        int ret = segment(id + 1);
        if (ret < 0) {
            return NULL;
        }
    }

    int *start_addr = get_head(id)->addr.start_addr;
    *start_addr = _chunk_sz_tbl[id];

    pop(id);

    return (unsigned char *)start_addr + HEADER_SZ;
}

// allocate the slab descriptor table of "size"
static _slab_dsc_tbl_t *alloc_dsc_tbl(size_t size) {
    _slab_dsc_tbl_t *p = (_slab_dsc_tbl_t *)malloc(size * sizeof(_slab_dsc_tbl_t));

    if (p == NULL) {
        fprintf(stderr, "func:%s, line:%d. cannot allocate new alloc_dsc_tbl!\n", __func__, __LINE__);
        exit(-1);
    }

    for (int i = 0; i < size; i++) {
        p[i].type = INVALID_TYPE;
        p[i].size = 0;
        p[i].numObj = 0;
        p[i].usedObj = 0;
        p[i].slab_ptr = NULL;
    }

    return p;
}

// return an entry corresponds to "type"
// return an empty one if it does not exist
// re-allocate a larger chunk of memory if the current one size
// cannot accomodate all the entries
static _slab_dsc_tbl_t *get_dsc_tbl(int type) {
    static size_t init_size = 128;

    // if it is the very first time to call
    if (_slab_dsc_tbl == NULL) {
        _slab_dsc_tbl = alloc_dsc_tbl(init_size);
    }

    // try to find one corresponds to "type"
    for (size_t i = 0; i < init_size; i++) {
        if (_slab_dsc_tbl[i].type == type) {
            return &_slab_dsc_tbl[i];
        }
    }

    // try to allocate a new empty entry
    for (size_t i = 0; i < init_size; i++) {
        if (_slab_dsc_tbl[i].type == INVALID_TYPE) {
            return &_slab_dsc_tbl[i];
        }
    }

    // enlarge the allocated memory size by 2
    size_t old_size = init_size;
    size_t new_size = init_size * 2;

    _slab_dsc_tbl_t *p = alloc_dsc_tbl(new_size);
    if (p == NULL) {
        fprintf(stderr, "func:%s, line:%d. cannot allocate new descriptor table!\n", __func__, __LINE__);
        exit(-1);
    }

    // copy the original contents into the new memory
    memcpy(p, _slab_dsc_tbl, old_size*sizeof(_slab_dsc_tbl_t));
    init_size = new_size;

    return &_slab_dsc_tbl[old_size];
}

// the "p"'s previous HEADER_SZ bytes with value "size"
static void set_header(void *p, int size) {
    int *p_int = (int *)((unsigned char *)p - HEADER_SZ);
    *p_int = size;
}

static void *my_malloc_slab( int size ) {
    if (size <= 0) {
        return NULL;
    }

    _slab_dsc_tbl_t *slab_dsc_tbl = get_dsc_tbl(size);

    if ((slab_dsc_tbl->type == INVALID_TYPE)||(slab_dsc_tbl->numObj == slab_dsc_tbl->usedObj)) {
        int slab_size = (size + HEADER_SZ) * N_OBJS_PER_SLAB;

        unsigned char *slab_addr = my_malloc_buddy(slab_size);

        if (slab_addr == NULL) {
            return NULL;
        }

        for (int i = 0; i < N_OBJS_PER_SLAB; i++) {
            set_header(slab_addr + HEADER_SZ + i * (size + HEADER_SZ), size + HEADER_SZ);
        }

        _slab_ptr_t *slab_ptr = (_slab_ptr_t *)malloc(sizeof(_slab_ptr_t));
        if (slab_ptr == NULL) {
            fprintf(stderr, "func:%s, line:%d. cannot allocate a new slab!\n", __func__, __LINE__);
            exit(-1);
        }

        slab_ptr->bitmap = 0;
        slab_ptr->addr = slab_addr;
        slab_ptr->next= NULL;

        if (slab_dsc_tbl->type == INVALID_TYPE) {
            slab_dsc_tbl->type = size;
            slab_dsc_tbl->size = slab_size;
            slab_dsc_tbl->numObj = N_OBJS_PER_SLAB;
            slab_dsc_tbl->usedObj = 0;

            slab_dsc_tbl->slab_ptr = slab_ptr;
        } else {
            slab_dsc_tbl->numObj += N_OBJS_PER_SLAB;

            // add to the end of the linked list
            _slab_ptr_t *p = slab_dsc_tbl->slab_ptr;
            while (p->next != NULL) {
                p = p->next;
            }
            p->next = slab_ptr;
        }
    }

    // traverse to find one chunk
    _slab_ptr_t *slab_ptr = slab_dsc_tbl->slab_ptr;
    while (slab_ptr!= NULL) {
        for (int i = 0; i < N_OBJS_PER_SLAB; i++) {
            if ((slab_ptr->bitmap&mask(i)) == 0) {
                slab_ptr->bitmap |= mask(i);
                slab_dsc_tbl->usedObj++;

                unsigned char *p = (unsigned char *)slab_ptr->addr + i * (size + HEADER_SZ);
                return p + HEADER_SZ;
            }
        }

        slab_ptr = slab_ptr->next;
    }

    fprintf(stderr, "func:%s, line:%d. should not run here!\n", __func__, __LINE__);
    exit(-1);
}

////////////////////////////////////////////////////////////////////////////
//
// Function     : my_malloc
// Description  : allocates memory segment using specified allocation algorithm
//
// Inputs       : size - size in bytes of the memory to be allocated
// Outputs      : -1 - if request cannot be made with the maximum mem_size requirement

void *my_malloc( int size ) {
    switch (_malloc_type) {
        case 0:
            return my_malloc_buddy(size);
        case 1:
            return my_malloc_slab(size);
        default:
            fprintf(stderr, "func:%s, line:%d. _malloc_type should be in the range 0 or 1!\n", __func__, __LINE__);
            exit(-1);
    }
}

static void my_free_buddy( void *ptr ) {
    void *start_addr = (unsigned char *)ptr - HEADER_SZ;
    int chunksz = *(int *)start_addr;

    if (chunksz == INVALID_TYPE) {
        return;
    }

    void *end_addr = (unsigned char *)start_addr + chunksz - 1;

    int *start_addr_int = (int *)start_addr;
    *start_addr_int = INVALID_TYPE;

    int id = chunksz2id(chunksz);
    if (id == INVALID_TYPE) {
        return;
    }

    _addr_t addr;
    addr.start_addr = start_addr;
    addr.end_addr = end_addr;
    addr.size = chunksz;
    insert_elem(id, addr);

    // no need to combine the segments if it is the last level
    if (id != N_CHUNK - 1) {
        for (int i = id; i < N_CHUNK - 1; i++) {
            if (get_head(i) == NULL) {
                break;
            }

            _addr_list_t *prev = find_prev(i, start_addr);
            if ((prev != NULL)&&(prev->addr.end_addr + 1 == start_addr)) {
                _addr_t addr;
                addr.start_addr = prev->addr.start_addr;
                addr.end_addr = end_addr;
                addr.size = 2 * _chunk_sz_tbl[i];

                insert_elem(i + 1, addr);

                remove_elem(i, prev->addr.start_addr);
                remove_elem(i, start_addr);

                // for next round of loop use, only need to update start_addr
                start_addr =(unsigned char *)start_addr - _chunk_sz_tbl[i];

                continue;
            }

            _addr_list_t *next = find_next(i, start_addr);
            if ((next!= NULL) && (end_addr + 1 == next->addr.start_addr)) {
                _addr_t addr;
                addr.start_addr = start_addr;
                addr.end_addr = next->addr.end_addr;
                addr.size = 2 * _chunk_sz_tbl[i];

                insert_elem(i + 1, addr);

                remove_elem(i, start_addr);
                remove_elem(i, next->addr.start_addr);

                // for next round of loop use, only need to update end_addr
                end_addr = (unsigned char *)end_addr + _chunk_sz_tbl[i];

                continue;
            }

            // if runs here, cannot combine with the previous or next, just break
            break;
        }
    }
}

static void my_free_slab( void *ptr ) {
    int *chunksz_addr = (int *)((unsigned char *)ptr - HEADER_SZ);
    int chunksz = *chunksz_addr;

    if (chunksz == INVALID_TYPE) {
        return;
    }

    int *chunksz_addr_int = (int *)chunksz_addr;
    *chunksz_addr_int = INVALID_TYPE;

    _slab_dsc_tbl_t *slab_dsc_tbl = get_dsc_tbl(chunksz-HEADER_SZ);

    if (slab_dsc_tbl->type == INVALID_TYPE) {
        fprintf(stderr, "func:%s, line:%d. cannot find slab of type=%d!\n", __func__, __LINE__, chunksz - HEADER_SZ);
        exit(-1);
    }

    _slab_ptr_t *slab_ptr = slab_dsc_tbl->slab_ptr;

    while (slab_ptr != NULL) {
        for (int i = 0; i < N_OBJS_PER_SLAB; i++) {
            if ((unsigned char *)slab_ptr->addr + i * chunksz == (unsigned char *)chunksz_addr) {
                slab_ptr->bitmap &= ~mask(i);
                slab_dsc_tbl->usedObj--;

                void *slab_addr_to_free = slab_ptr->addr;

                if (slab_ptr->bitmap == 0) {
                    if (slab_dsc_tbl->usedObj == 0) {
                        // the empty slab is the first slab
                        slab_dsc_tbl->type = INVALID_TYPE;
                    } else {
                        // the empty slab is in between, then need to main the slab_ptr list
                        _slab_ptr_t *p = slab_dsc_tbl->slab_ptr;
                        while (p->next != slab_ptr) {
                            p = p->next;
                        }
                        p->next = slab_ptr->next;
                    }

                    my_free_buddy(slab_addr_to_free);
                }

                return;
            }
        }

        slab_ptr = slab_ptr->next;
    }

    fprintf(stderr, "func:%s, line:%d. cannot find slab of type=%d!\n", __func__, __LINE__, chunksz - HEADER_SZ);
}

////////////////////////////////////////////////////////////////////////////
//
// Function     : my_free
// Description  : deallocated the memory segment being passed by the pointer
//
// Inputs       : ptr - pointer to the memory segment to be free'd
// Outputs      :

void my_free( void *ptr ) {
    switch (_malloc_type) {
        case 0:
            my_free_buddy(ptr);
            break;
        case 1:
            my_free_slab(ptr);
            break;
        default:
            fprintf(stderr, "func:%s, line:%d. _malloc_type should be in the range 0 or 1!\n", __func__, __LINE__);
            exit(-1);
    }
}

