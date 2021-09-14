/**
 * 
 * File             : scheduler.c
 * Description      : This is a stub to implement all your scheduling schemes
 *
 * Author(s)        : @Zihang Xu, Xiangyu Ren
 * Last Modified    : @10/12/2020
*/

// Include Files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <assert.h>
#include <time.h>

#include <math.h>
#include <pthread.h>
#include <semaphore.h>

float get_global_time();

void init_scheduler( int sched_type );
int schedule_me( float currentTime, int tid, int remainingTime, int tprio );
int P( float currentTime, int tid, int sem_id);
int V( float currentTime, int tid, int sem_id);

#define FCFS    0
#define SRTF    1
#define PBS     2
#define MLFQ    3
#define SEM_ID_MAX 50

#define INVAL_THREAD_ID     (-1)
#define INVAL_QUEUE_ID      (-1)
#define MAX_NUM_THREAD      (128)
#define MAX_QUEUE_SIZE      (64)

#define N_LEVEL             (5)
#define HIGHEST_LVL         (0)
#define LOWEST_LVL          (N_LEVEL-1)

// semaphore used for wakeup/block a thread from the scheduler
static sem_t _block_from_sche[MAX_NUM_THREAD];

// semaphore used for wakeup/block a thread from the P/V
static sem_t _block_from_sem[MAX_NUM_THREAD];

// number of waiters for a specific semaphore
static sem_t _num_waiter[SEM_ID_MAX];

// the mutex to protect scheduling related variables
static pthread_mutex_t _sche_lock;

// the mutex to rotect semaphore related variables
static pthread_mutex_t _sem_lock;

// stores the thread ID of currently running
static int _running_thread;

// stores which scheduling method should use
static int _sched_type;

struct _queue_ctrl {
    int size;
    int head;
    int free;
    int *data;
};

typedef struct _queue_ctrl _queue_ctrl_t;

// queue's control info, for FCFS only
static _queue_ctrl_t _q_fcfs;

// queue's control info, for MLFQ only
static _queue_ctrl_t _q_mlfq[N_LEVEL];

// queue's control info, used as each semaphore's waiting list
static _queue_ctrl_t _q_sem[SEM_ID_MAX];

// stores the necessary info of a thread, used to decide which thread to
// schedule
struct _thread_sche {
    int id;
    int remTime;
    float curTime;

    int tprio;

    int queue_id;
    int burst;
};

typedef struct _thread_sche _thread_sche_t;

// an array to store each thread's info. _thread_sche_info[index] is for thread
// id = index
static _thread_sche_t _thread_sche_info[MAX_NUM_THREAD];

typedef int (*judge_func_ptr)(const _thread_sche_t *);

/* initialize a queue, the data to store each element's value is input as a
 parameter The queue is using head and free to circularly reuse a linear array.
*/
static void init_queue(_queue_ctrl_t *ctrl, int data[]) {
    ctrl->size = 0;
    ctrl->head = 0;
    ctrl->free = 0;
    ctrl->data = data;
}

/* push an element into the queue */
static void push_queue(_queue_ctrl_t *ctrl, int val) {
    if (ctrl->size > MAX_QUEUE_SIZE) {
        printf("push_queue: full size!\n");
        exit(-1);
    }

    ctrl->data[ctrl->free] = val;
    ctrl->free = (ctrl->free + 1) % MAX_QUEUE_SIZE;
    ctrl->size++;
}

/* pop an element from the queue */
static int pop_queue(_queue_ctrl_t *ctrl) {
    if (ctrl->size < 1) {
        printf("pop_queue: The queue is empty!\n");
        exit(-1);
    }

    int ret = ctrl->data[ctrl->head];
    ctrl->head = (ctrl->head + 1) % MAX_QUEUE_SIZE;
    ctrl->size--;

    return ret;
}

/* get the size of the queue */
static int get_size(const _queue_ctrl_t *ctrl) {
    return ctrl->size;
}

/* get the head element from the queue. Compared with push_queue,
   this function does not change head/free. */
static int get_head(const _queue_ctrl_t *ctrl) {
    if (ctrl->size < 1) {
        printf("get_head: The queue is empty!\n");
        exit(-1);
    }

    return ctrl->data[ctrl->head];
}

/* delete a specific element from the queue. In this particular file, the thread
   id is stored as the value and there is not overlapped value. 
   return 0 if succesful, -1 otherwise*/
static int delete_queue(_queue_ctrl_t *ctrl, int val) {
    int index = ctrl->head;
    for (int i = 0; i < ctrl->size; i++) {
        if (ctrl->data[(index + i) % MAX_QUEUE_SIZE] == val) {
            if (i == ctrl->size - 1) {
                ctrl->free = (ctrl->free - 1) % MAX_QUEUE_SIZE;
            } else if (i == 0) {
                ctrl->head = (ctrl->head + 1) % MAX_QUEUE_SIZE;
            } else {
                for (int j = i; j < ctrl->size; j++) {
                    ctrl->data[(index + j) % MAX_QUEUE_SIZE] = ctrl->data[(index + j + 1) % MAX_QUEUE_SIZE];
                }
                ctrl->free=(ctrl->free - 1) % MAX_QUEUE_SIZE;
            }
            ctrl->size--;
            return 0;
        }
    }

    return -1;
}

void init_scheduler( int sched_type ) {
    static int queue_sem_raw_data[SEM_ID_MAX][MAX_NUM_THREAD];
    static int queue_sche_raw_data[N_LEVEL][MAX_QUEUE_SIZE];

    pthread_mutex_init(&_sche_lock, NULL);
    pthread_mutex_init(&_sem_lock, NULL);

    _running_thread = INVAL_THREAD_ID;

    _sched_type = sched_type;

    for (int i = 0; i < MAX_NUM_THREAD; i++) {
        sem_init(&_block_from_sche[i], 0, 0);
        sem_init(&_block_from_sem[i], 0, 0);
    }

    for (int i = 0; i < SEM_ID_MAX; i++) {
        sem_init(&_num_waiter[i], 0, 0);
        init_queue(&_q_sem[i], queue_sem_raw_data[i]);
    }

    switch (_sched_type) {
        case FCFS:
            init_queue(&_q_fcfs, queue_sche_raw_data[0]);
            break;

        case SRTF:
        case PBS:
            for (int i = 0; i < MAX_NUM_THREAD; i++) {
                _thread_sche_info[i].id = INVAL_THREAD_ID;
            }
            break;

        case MLFQ:
            for (int i = 0; i < MAX_NUM_THREAD; i++) {
                _thread_sche_info[i].id = INVAL_THREAD_ID;
                _thread_sche_info[i].queue_id = INVAL_QUEUE_ID;
            }
            for (int i = 0; i < N_LEVEL; i++) {
                init_queue(&_q_mlfq[i], queue_sche_raw_data[i]);
            }
            break;

        default:
            printf("init_scheduler: sched_type should be in the range 0~3!\n");
            exit(-1);
    }
}

/* scheduling method for FCFS */
static int schedule_me_fcfs( float currentTime, int tid, int remainingTime, _queue_ctrl_t *ctrl) {
    pthread_mutex_lock(&_sche_lock);

    if (remainingTime == 0) {
        // delete from the queue
        // print_queue(ctrl);
        pop_queue(ctrl);

        if (get_size(ctrl) > 0) {
            int index = get_head(ctrl);

            sem_post(&_block_from_sche[index]);
        }

        pthread_mutex_unlock(&_sche_lock);

        return 0;
    }

    if (_running_thread == INVAL_THREAD_ID) {
        _running_thread = tid;
        push_queue(ctrl, tid);
        pthread_mutex_unlock(&_sche_lock);
        return currentTime;
    } else if (_running_thread == tid) {
        pthread_mutex_unlock(&_sche_lock);
        return currentTime;
    } else {
        push_queue(ctrl, tid);
        pthread_mutex_unlock(&_sche_lock);
        sem_wait(&_block_from_sche[tid]);

        pthread_mutex_lock(&_sche_lock);
        _running_thread = tid;
        pthread_mutex_unlock(&_sche_lock);
        return get_global_time();
    }
}

/* return the index whose element has the minimum remTime. If two elements
   share the same remTime, return the one with the minimum curTime. */
static int find_min_srtf(const _thread_sche_t *p) {
    int index = -1, i;
    for (i = 0; i < MAX_NUM_THREAD; i++) {
        if (p[i].id != INVAL_THREAD_ID) {
            index = i;
            break;
        }
    }

    for (; i < MAX_NUM_THREAD; i++) {
        if (p[i].id != INVAL_THREAD_ID) {
            if (p[i].remTime < p[index].remTime) {
                index = i;
            } else if (p[i].remTime == p[index].remTime) {
                if (p[i].curTime < p[index].curTime) {
                    index = i;
                }
            }
        }
    }

    return index;
}

/* return the index whose element has the maximum priority. If two elements
   share the same remTime, return the one with the minimum curTime. */
static int find_max_tprio(const _thread_sche_t *p) {
    int index = -1, i;
    for (i = 0; i < MAX_NUM_THREAD; i++) {
        if (p[i].id != INVAL_THREAD_ID) {
            index = i;
            break;
        }
    }

    for (; i < MAX_NUM_THREAD; i++) {
        if (p[i].id != INVAL_THREAD_ID) {
            if (p[i].tprio < p[index].tprio) {
                index = i;
            } else if (p[i].tprio == p[index].tprio) {
                if (p[i].curTime < p[index].curTime) {
                    index = i;
                }
            }
        }
    }

    return index;
}

/* scheduling method for SRTF and PBS */
static int schedule_me_srtf_pbs( float currentTime, int tid, int remainingTime, int tprio, judge_func_ptr func_ptr) {
    pthread_mutex_lock(&_sche_lock);

    if (remainingTime == 0) {
        _thread_sche_info[tid].id = INVAL_THREAD_ID;

        int index = func_ptr(_thread_sche_info);

        if (index >= 0) {
            sem_post(&_block_from_sche[index]);
        }

        pthread_mutex_unlock(&_sche_lock);
        return 0;
    }

    if (_thread_sche_info[tid].id == INVAL_THREAD_ID) {
        _thread_sche_info[tid].id = tid;
    }

    _thread_sche_info[tid].remTime = remainingTime;
    _thread_sche_info[tid].curTime = currentTime;
    _thread_sche_info[tid].tprio = tprio;

    // if the currentTime is not multiples of ms, delay the scheduling decision.
    if (fabs(currentTime-floor(currentTime)) > 0.0001f) {
        pthread_mutex_unlock(&_sche_lock);
        sem_wait(&_block_from_sche[tid]);

        pthread_mutex_lock(&_sche_lock);
        _running_thread = tid;
        pthread_mutex_unlock(&_sche_lock);

        return get_global_time();
    }

    if (_running_thread == INVAL_THREAD_ID) {
        _running_thread = tid;
        pthread_mutex_unlock(&_sche_lock);
        return currentTime;
    } else {
        int _tid = func_ptr(_thread_sche_info);

        if (_tid == tid) {
            _running_thread = _tid;

            pthread_mutex_unlock(&_sche_lock);
            return get_global_time();

        } else {
            if (_tid != _running_thread) {
                sem_post(&_block_from_sche[_tid]);
            }

            pthread_mutex_unlock(&_sche_lock);
            sem_wait(&_block_from_sche[tid]);

            pthread_mutex_lock(&_sche_lock);
            _running_thread = tid;
            pthread_mutex_unlock(&_sche_lock);

            return get_global_time();
        }
    }
}

/* scheduling method for MLFQ */
static int schedule_me_mlfq( float currentTime, int tid, int remainingTime) {
    static const int quantum[N_LEVEL] = {5, 10, 15, 20, 25};

    pthread_mutex_lock(&_sche_lock);

    if (remainingTime == 0) {
        // delete from the queue
        int queue_id = _thread_sche_info[tid].queue_id;
        if ((unsigned int)queue_id > MAX_QUEUE_SIZE) {
            printf("schedule_me_mlfq: Invalid queue_id=%d, should be 0~%d.\n", queue_id, MAX_QUEUE_SIZE - 1);
            exit(-1);
        }

        // cannot use pop_queue, since now the head of queue may be some other alternating thread
        delete_queue(&_q_mlfq[queue_id], tid);

        // delete from the global variable
        _thread_sche_info[tid].id = INVAL_THREAD_ID;

        for (int i = 0; i < N_LEVEL; i++) {
            if (get_size(&_q_mlfq[i]) > 0) {
                 int index = get_head(&_q_mlfq[i]);
                 sem_post(&_block_from_sche[index]);
                 break;
            }
        }

        pthread_mutex_unlock(&_sche_lock);

        return 0;
    }

    // maintain the 5 level queues
    if (_thread_sche_info[tid].id == INVAL_THREAD_ID) {
        _thread_sche_info[tid].id = tid;
        _thread_sche_info[tid].queue_id = HIGHEST_LVL;  // starting from the highest level
        _thread_sche_info[tid].burst = 0;  // initial value, need to increase by 1 if scheduled

        push_queue(&_q_mlfq[HIGHEST_LVL], tid);
    } else {
        int queue_id = _thread_sche_info[tid].queue_id;
        if (queue_id < LOWEST_LVL) {
            if (_thread_sche_info[tid].burst >= quantum[queue_id]) {
                // need to move to the next level of queue
                pop_queue(&_q_mlfq[queue_id]);
                push_queue(&_q_mlfq[queue_id + 1], tid);

                _thread_sche_info[tid].queue_id++;
                _thread_sche_info[tid].burst = 0;
            }
        } else {
            if (_thread_sche_info[tid].burst >= quantum[queue_id] && get_size(&_q_mlfq[LOWEST_LVL]) > 1) {
                pop_queue(&_q_mlfq[LOWEST_LVL]);
                push_queue(&_q_mlfq[LOWEST_LVL], tid);

                _thread_sche_info[tid].burst = 0;
            }
        }
    }

    // if the currentTime is not multiples of ms, delay the scheduling result.
    if (fabs(currentTime-floor(currentTime)) > 0.0001f) {
        pthread_mutex_unlock(&_sche_lock);
        sem_wait(&_block_from_sche[tid]);

        pthread_mutex_lock(&_sche_lock);
        _running_thread = tid;
        _thread_sche_info[tid].burst++;
        pthread_mutex_unlock(&_sche_lock);

        return get_global_time();
    }

    // 1st schedule when power on
    if (_running_thread == INVAL_THREAD_ID) {
        _thread_sche_info[tid].burst = 1;
        _running_thread = tid;
        pthread_mutex_unlock(&_sche_lock);
        return currentTime;
    }

    // pick up one thread from the first four queues (if any), then use the FCFS.
    for (int i = HIGHEST_LVL; i < LOWEST_LVL; i++) {
        if (get_size(&_q_mlfq[i]) > 0) {
            // since the queues have been adjusted in the above codes,
            // just pick up the head from the current level queue.
            int _tid = get_head(&_q_mlfq[i]);
            if (_tid == tid) {
                _running_thread = _tid;
                _thread_sche_info[tid].burst++;
                pthread_mutex_unlock(&_sche_lock);
                return get_global_time();
            } else {
                if (_tid != _running_thread) {
                    sem_post(&_block_from_sche[_tid]);
                }

                pthread_mutex_unlock(&_sche_lock);
                sem_wait(&_block_from_sche[tid]);

                pthread_mutex_lock(&_sche_lock);
                _running_thread = tid;
                _thread_sche_info[tid].burst++;
                pthread_mutex_unlock(&_sche_lock);
                return get_global_time();
            }
        }
    }

    // if runs here, it is the last level queue. Use the round robin.
    if (get_size(&_q_mlfq[LOWEST_LVL]) < 1) {
        printf("Don't have a thread to schedule even in the lowest queue!\n");
    }
    
    int _tid = get_head(&_q_mlfq[LOWEST_LVL]);

    if (_tid == tid) {
        _running_thread = _tid;
        _thread_sche_info[tid].burst++;
        pthread_mutex_unlock(&_sche_lock);
        return get_global_time();
    } else {
        if (_tid != _running_thread) {
            sem_post(&_block_from_sche[_tid]);
        }

        pthread_mutex_unlock(&_sche_lock);
        sem_wait(&_block_from_sche[tid]);

        pthread_mutex_lock(&_sche_lock);
        _running_thread = tid;
        _thread_sche_info[tid].burst++;
        pthread_mutex_unlock(&_sche_lock);
        return get_global_time();
    }
}

int schedule_me( float currentTime, int tid, int remainingTime, int tprio ) {
    if ((unsigned int)tid > MAX_NUM_THREAD - 1) {
        printf("schedule_me: The supported tid=0~%d, current input=%d.\n", MAX_NUM_THREAD - 1, tid);
        exit(-1);
    }

    switch (_sched_type) {
        case FCFS:
            return schedule_me_fcfs(currentTime, tid, remainingTime, &_q_fcfs);
        case SRTF:
            return schedule_me_srtf_pbs(currentTime, tid, remainingTime, tprio, find_min_srtf);
        case PBS:
            return schedule_me_srtf_pbs(currentTime, tid, remainingTime, tprio, find_max_tprio);
        case MLFQ:
            return schedule_me_mlfq(currentTime, tid, remainingTime);
        default:
            printf("schedule_me: _sched_type should be in the range 0~3!\n");
            exit(-1);
    }
}

int P( float currentTime, int tid, int sem_id) {
    pthread_mutex_lock(&_sem_lock);

    int sem_val;
    sem_getvalue(&_num_waiter[sem_id], &sem_val);

    // firstly judge whether the value of semaphore is larger than zero,
    // if so, just "substract" it and return. No need to wait.
    if (sem_val>0) {
        sem_wait(&_num_waiter[sem_id]);
        pthread_mutex_unlock(&_sem_lock);

        return (int)currentTime;
    } else {
        push_queue(&_q_sem[sem_id], tid);

        // delete tid from the corresponding queue_thread_sche_info
        // select the new thread to run
        pthread_mutex_lock(&_sche_lock);
        int _tid;
        int queue_id;

        switch (_sched_type) {
            case FCFS:
                {
                    int ret = delete_queue(&_q_fcfs, tid);
                    if (ret < 0) {
                        printf("delete_queue: cannot find tid=%d\n", tid);
                        exit(-1);
                    };
                    _tid = get_head(&_q_fcfs);
                    break;
                }

            case SRTF:
            case PBS:
                if (_thread_sche_info[tid].id == INVAL_THREAD_ID) {
                    printf("already INVAL_THREAD_ID for _thread_sche_info[%d].id\n", tid);
                    exit(-1);
                }
                _thread_sche_info[tid].id = INVAL_THREAD_ID;

                if (_sched_type == SRTF) {
                    _tid = find_min_srtf(_thread_sche_info);
                } else {
                    _tid = find_max_tprio(_thread_sche_info);
                }

                break;

            case MLFQ:
                {
                    queue_id = _thread_sche_info[tid].queue_id;
                    delete_queue(&_q_mlfq[queue_id], tid);

                    int i;
                    for (i = HIGHEST_LVL; i < LOWEST_LVL; i++) {
                        if (get_size(&_q_mlfq[i]) > 0) {
                            _tid = get_head(&_q_mlfq[i]);
                            break;
                        }
                    }

                    if (i == LOWEST_LVL) {
                        _tid = pop_queue(&_q_mlfq[LOWEST_LVL]);
                        push_queue(&_q_mlfq[LOWEST_LVL], _tid);
                    }
                    break;
                }
            default:
                printf("P: _sched_type should be in the range 0~3!\n");
                exit(-1);
        }

        pthread_mutex_unlock(&_sche_lock);
        sem_post(&_block_from_sche[_tid]);  //  wake up the blocked thread

        pthread_mutex_unlock(&_sem_lock);

        sem_wait(&_block_from_sem[tid]);

        pthread_mutex_lock(&_sche_lock);

        switch (_sched_type) {
            case FCFS:
                push_queue(&_q_fcfs, tid);
                break;

            case SRTF:
            case PBS:
                _thread_sche_info[tid].id = tid;
                break;

            case MLFQ:
                push_queue(&_q_mlfq[queue_id], tid);
                _thread_sche_info[tid].id = tid;
                break;
            default:
                printf("P: _sched_type should be in the range 0~3!\n");
                exit(-1);
        }

        pthread_mutex_unlock(&_sche_lock);
        return get_global_time();
    }
}

int V( float currentTime, int tid, int sem_id) {
    pthread_mutex_lock(&_sem_lock);

    int sem_val;
    sem_getvalue(&_num_waiter[sem_id], &sem_val);

    // means there is no thread waiting for this semaphore
    if (sem_val>0) {
        sem_post(&_num_waiter[sem_id]);
        pthread_mutex_unlock(&_sem_lock);

        return (int)currentTime;
    } else {
        // choose the thread that is the head of the semaphore's waiting list
        if (get_size(&_q_sem[sem_id])>0) {
            int _tid = pop_queue(&_q_sem[sem_id]);
            sem_post(&_block_from_sem[_tid]);
        }

        sem_post(&_num_waiter[sem_id]);
        pthread_mutex_unlock(&_sem_lock);

        return (int)currentTime;
    }
}
