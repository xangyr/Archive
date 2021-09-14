// Starter code for the page replacement project
#define _GNU_SOURCE 1
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <signal.h>
#include "473_mm.h"
#include <string.h>

#define READ_FLAG (0)
#define WRITE_FLAG (1)
#define USED (1)
#define UNUSED (0)

// since frame id=0 is used, use -1 as the invalid frame
#define INVALID_FRAME (-1)

// page table info
typedef struct _pt {
    // physical page
    int page;

    // virtual frame
    int frame;

    // 0 for read, 1 for write
    int permission;

    // reference bit, for third chance method use
    int ref;

    // modified bit, for third chance method use
    int modified;

    // chance bit, for third chance method use
    int chance;
}_pt_t;

// circular list
struct pt_t_list {
    _pt_t val;
    struct pt_t_list *next;
};
typedef struct pt_t_list _pt_t_list;

// control info for the circular list
struct _ctrl {
    // actual number of elements within the list
    int size;

    // the preallocated size of the list
    int capacity;

    // head of the actual element
    _pt_t_list *head;

    // tail of the actual element
    _pt_t_list *tail;

    // point to the allocated list
    _pt_t_list *list;
};
typedef struct _ctrl _ctrl_t;

// record parameters for each signal handler calling's use
static void *_vm;
static int _page_size;
static int _n_frames;

// the allocated info for physical frames
static int *_phy_frame_tbl;

// the control info of the circular linked list
static _ctrl_t _ctrl_list_pt;

// init the circular list
static void init(_ctrl_t *ctrl, int capacity) {
    ctrl->size = 0;
    ctrl->capacity = capacity;
    ctrl->list = (_pt_t_list *)malloc(capacity * sizeof(_pt_t_list));

    if (ctrl->list == NULL) {
        fprintf(stderr, "func:%s, line:%d. cannot allocate the list!\n", __func__, __LINE__);
        exit(-1);
    }

    for (int i = 0; i < capacity; i++) {
        ctrl->list[i].val.page = INVALID_FRAME;
    }

    ctrl->head = ctrl->list;
    ctrl->tail = ctrl->list;

    for (int i = 0; i < capacity - 1; i++) {
        ctrl->list[i].next = &ctrl->list[i + 1];
    }
    ctrl->list[capacity - 1].next = &ctrl->list[0];
}

// push an element from the tail
static void push_back(_ctrl_t *ctrl, _pt_t val) {
    if (ctrl->size > ctrl->capacity) {
        fprintf(stderr, "func:%s, line:%d. full size!\n", __func__, __LINE__);
        exit(-1);
    }

    ctrl->tail->val = val;
    ctrl->tail = ctrl->tail->next;
    ctrl->size++;
}

// pop an element from the front
static _pt_t *pop_front(_ctrl_t *ctrl) {
    if (ctrl->size < 1) {
        fprintf(stderr, "func:%s, line:%d. The list is empty!\n", __func__, __LINE__);
        exit(-1);
    }

    _pt_t_list *head_prev = ctrl->head;
    ctrl->head = ctrl->head->next;
    ctrl->size--;

    return &head_prev->val;
}

// get the actual number of element
static int get_size(const _ctrl_t *ctrl) {
    return ctrl->size;
}

// find a specific page within the list
static _pt_t *find(const _ctrl_t *ctrl, int page) {
    if (ctrl->size < 1) {
        return NULL;
    }

    _pt_t_list *p = ctrl->head;
    for (int i = 0; i < ctrl->size; i++) {
        if (p->val.page == page) {
            return &p->val;
        }
        p = p->next;
    }

    return NULL;
}

// replace an element pointed by "pos"
static void replace(_ctrl_t *ctrl, _pt_t *pos, _pt_t val) {
    if (pos == NULL) {
        fprintf(stderr, "func:%s, line:%d. pos is NULL!\n", __func__, __LINE__);
        exit(-1);
    }

    *pos = val;
     ctrl->head = ctrl->head->next;
}

// push an element from the head
static void push_front(_ctrl_t *ctrl, _pt_t val) {
    ctrl->head->val = val;
    ctrl->head = ctrl->head->next;
    ctrl->size++;
}

// mprotect wrapper, the error code is judged
static void mprotect_wrapper(void *addr, size_t len, int prot, const char *func, int line) {
    int ret = mprotect(addr, len, prot);

    if (ret < 0) {
        fprintf(stderr, "func:%s, line:%d. mprotect failed!\n", func, line);
        exit(-1);
    }
}

// evict a page by using third chance method
static _pt_t *evict(_ctrl_t *ctrl) {
    while (1) {
        _pt_t *p = &ctrl->head->val;

        if (p->ref == 0 && p->modified == 0) {
            return p;
        } else if (p->ref == 1 && p->modified == 0) {
            p->ref = 0;
            p->chance++;

            void *vm_start = p->page * _page_size + _vm;
            mprotect_wrapper(vm_start, _page_size, PROT_NONE, __func__, __LINE__);
        } else if (p->ref == 1 && p->modified == 1) {
            p->ref = 0;
            p->chance++;

            void *vm_start = p->page * _page_size + _vm;
            mprotect_wrapper(vm_start, _page_size, PROT_NONE, __func__, __LINE__);
        } else {  // R=0 and M=1
            p->chance++;
            if (p->chance == 3) {
                return p;
            }
        }

        ctrl->head = ctrl->head->next;
    }
}

// allocate a new physical frame
static int alloc_phy_frame() {
    for (int i = 0; i < _n_frames; i++) {
        if (_phy_frame_tbl[i] == UNUSED) {
            _phy_frame_tbl[i] = USED;
            return i;
        }
    }

    return -1;
}

// free a specific physical frame
static void free_phy_frame(int i) {
    _phy_frame_tbl[i] = UNUSED;
}

void signal_handler_fifo(int signal, siginfo_t *siginfo, void * ucontext) {
    unsigned long err = (*(ucontext_t *)ucontext).uc_mcontext.gregs[REG_ERR];
    int permission = (err&0x2)>>1;

    int page = ((unsigned long long)siginfo->si_addr-(unsigned long long)_vm)/_page_size;
    void *vm_start=(void *)(unsigned long long)(page*_page_size+_vm);
    int offset = (unsigned long long)siginfo->si_addr-page*_page_size-(unsigned long long)_vm;

    int evicted_page = -1;
    int write_back = 0;
    _pt_t *p = find(&_ctrl_list_pt, page);
    if (p == NULL) {
        if (get_size(&_ctrl_list_pt) == _n_frames) {
            _pt_t *p_evict = pop_front(&_ctrl_list_pt);
            evicted_page = p_evict->page;
            if (p_evict->permission == WRITE_FLAG) {
                write_back = 1;
            }
            void *vm_start_evict = evicted_page*_page_size+_vm;

            mprotect_wrapper(vm_start_evict, _page_size, PROT_NONE, __func__, __LINE__);

            free_phy_frame(p_evict->frame);
        }

        // when run here there is free space whether it is original free or after eviction
        _pt_t pt;
        pt.frame = alloc_phy_frame();
        if (pt.frame < 0) {
            fprintf(stderr, "func:%s, line:%d. fail to get new physical frame!\n", __func__, __LINE__);
            exit(-1);
        }

        int phy_addr = pt.frame * _page_size + offset;
        pt.permission = permission;
        pt.page = page;
        push_back(&_ctrl_list_pt, pt);

        int prot = permission == READ_FLAG?PROT_READ:PROT_WRITE;
        mprotect_wrapper(vm_start, _page_size, prot, __func__, __LINE__);

        mm_logger(page, permission, evicted_page, write_back, phy_addr);
    } else {
        if (p->permission == READ_FLAG && permission == WRITE_FLAG) {
            p->permission = WRITE_FLAG;
            int phy_addr = p->frame*_page_size+offset;

            mprotect_wrapper(vm_start, _page_size, PROT_WRITE, __func__, __LINE__);

            mm_logger(page, 2, evicted_page, write_back, phy_addr);
        }
    }
}

void signal_handler_3rdchance(int signal, siginfo_t *siginfo, void * ucontext) {
    unsigned long err = (*(ucontext_t *)ucontext).uc_mcontext.gregs[REG_ERR];
    int permission = (err&0x2)>>1;

    int page = ((unsigned long long)siginfo->si_addr - (unsigned long long)_vm) / _page_size;
    void *vm_start = (void *)(unsigned long long)(page * _page_size+_vm);
    int offset = (unsigned long long)siginfo->si_addr - page * _page_size - (unsigned long long)_vm;

    int evicted_page = -1;
    int write_back = 0;
    _pt_t *p_evict = NULL;
    _pt_t *p = find(&_ctrl_list_pt, page);
    if (p == NULL) {
        if (get_size(&_ctrl_list_pt) == _n_frames) {
            p_evict = evict(&_ctrl_list_pt);
            evicted_page = p_evict->page;
            if (p_evict->modified == 1) {
                write_back = 1;
            }
            void *vm_start_evict = evicted_page * _page_size + _vm;

            mprotect_wrapper(vm_start_evict, _page_size, PROT_NONE, __func__, __LINE__);

            free_phy_frame(p_evict->frame);
        }

        // when run here there is free space whether it is original free or after eviction
        _pt_t pt;
        pt.page = page;
        pt.frame = alloc_phy_frame();
        if (pt.frame < 0) {
            fprintf(stderr, "func:%s, line:%d. fail to get new physical frame!\n", __func__, __LINE__);
            exit(-1);
        }

        pt.permission = permission;
        pt.ref = 1;
        pt.modified = permission == WRITE_FLAG?1:0;
        pt.chance = 0;
        int phy_addr = pt.frame * _page_size + offset;

        if (p_evict == NULL) {
            push_front(&_ctrl_list_pt, pt);
        } else {
            replace(&_ctrl_list_pt, p_evict, pt);
        }

        int prot = permission == READ_FLAG?PROT_READ:PROT_WRITE;
        mprotect_wrapper(vm_start, _page_size, prot, __func__, __LINE__);
        mm_logger(page, permission, evicted_page, write_back, phy_addr);
    } else {
        int phy_addr = p->frame*_page_size+offset;
        if (permission == READ_FLAG) {
            p->ref = 1;
            p->chance = 0;
            mprotect_wrapper(vm_start, _page_size, PROT_READ, __func__, __LINE__);
            mm_logger(page, 3, evicted_page, write_back, phy_addr);
        } else {
            // write access
            p->modified = 1;
            p->chance = 0;
            p->ref = 1;
            if (p->permission == READ_FLAG) {
                p->permission = WRITE_FLAG;
                mprotect_wrapper(vm_start, _page_size, PROT_WRITE, __func__, __LINE__);
                mm_logger(page, 2, evicted_page, write_back, phy_addr);
            } else {
                mprotect_wrapper(vm_start, _page_size, PROT_WRITE, __func__, __LINE__);
                mm_logger(page, 4, evicted_page, write_back, phy_addr);
            }
        }
    }
}

void mm_init(void* vm, int vm_size, int n_frames, int page_size, int policy) {
    init(&_ctrl_list_pt, n_frames);

    _vm = vm;
    _n_frames = n_frames;
    _page_size = page_size;

    mprotect_wrapper(vm, vm_size, PROT_NONE, __func__, __LINE__);

    struct sigaction act;
    memset(&act, 0, sizeof(struct sigaction));

    sigemptyset(&act.sa_mask);
    switch (policy) {
        case 1:
            act.sa_sigaction = signal_handler_fifo;
            break;
        case 2:
            act.sa_sigaction = signal_handler_3rdchance;
            break;
        default:
            fprintf(stderr, "func:%s, line:%d. policy should be 1 or 2!\n", __func__, __LINE__);
            exit(-1);
    }

    act.sa_flags = SA_SIGINFO;

    sigaction(SIGSEGV, &act, NULL);

    _phy_frame_tbl = (int *) malloc(sizeof(int) * n_frames);
    if (_phy_frame_tbl == NULL) {
        fprintf(stderr, "func:%s, line:%d. cannot allocate _phy_frame_tbl!\n", __func__, __LINE__);
        exit(-1);
    }

    for (int i = 0; i < n_frames; i++) {
        _phy_frame_tbl[i] = UNUSED;
    }
}

