#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

#define NULL	((void *)0)

#define MAX_NUM_TASKS	32

#define MAXUINT	(0xffffffffu)

typedef void (*isr_t) (void);
typedef void (*job_t) (void *);

struct task {
	int valid;		/* this descriptor is associated with a valid task */
	job_t job;		/* job function to be executed at any activation */
	void *arg;		/* arguments to be passed to the job function */
	unsigned long releasetime;	/* next release time */
	unsigned long released;	/* number of released, pending jobs */
	unsigned long period;	/* period of the task in ticks */
	unsigned long priority;	/* priority of the task (FPR) or job (EDF) */
	unsigned long deadline; /* relative deadline of the job (EDF), zero for FPR */
	const char *name;	/* task name */
	unsigned long sp;	/* saved value for r13/sp */
	unsigned long regs[8];	/*storage area for registers r4-r11 */
};

/* The types of task known to the scheduler */
#define FPR 0
#define EDF 1

extern volatile unsigned long ticks;
extern int num_tasks;
extern struct task taskset[MAX_NUM_TASKS];

extern volatile unsigned long trigger_schedule;
extern struct task *current;	/* the task of the job in execution */

void main(void);
void panic0(void);
void panic1(void);
void panic2(void);
int putc(int ch);
int puts(const char *st);
int putnl(void);
int puth(unsigned long v);
int putu(unsigned long v);
int putd(long v);
int putf(double v, int prec);
int putcn(int ch, int n);
int register_isr(int n, isr_t func);
void init_ticks(void);
void check_periodic_tasks(void);
struct task *schedule(void);
void _sys_schedule(void);
void init_taskset(void);
void run_periodic_tasks(void);
void init_watchdog(void);
int create_task(job_t job, void *arg, unsigned long period,
		       unsigned long delay, unsigned long priority,
			   int type, const char *name);
void calibrate_udelay(void);
void udelay(unsigned int usec);

static inline void loop_delay(unsigned long d)
{
	while (d-- > 0)
		__memory_barrier();
}

#define time_after(a,b)		((long)((b)-(a))<0)
#define time_before(a,b)	time_after(b,a)
#define time_after_eq(a,b)	((long)((a)-(b))>=0)
#define time_before_eq(a,b)	time_after_eq(b,a)
