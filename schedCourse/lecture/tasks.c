#include "beagleboneblack.h"

/* Allocate the stacks in the .bss.stack subsection
 * (init_bss() ignores them so that it does not overwrite
 * its own return address)
 * Each stack is 4096 byte long and aligned
 * There is one stack per each task */

#define STACK_SIZE 4096
char stacks[MAX_NUM_TASKS * STACK_SIZE]
    __attribute__ ((aligned(STACK_SIZE)))
    __attribute__ ((section(".bss.stack")));;
const char *stack0_top = stacks + MAX_NUM_TASKS * STACK_SIZE;

struct task taskset[MAX_NUM_TASKS];

int num_tasks;

void init_taskset(void)
{
	int i;
	num_tasks = 0;
	for (i = 0; i < MAX_NUM_TASKS; ++i)
		taskset[i].valid = 0;

	/* Task 0 is special: it is the idle (or kernel) task,
	 * which runs whenever no other job is runnable.
	 * Actually, taskset[0] is only used as an address
	 * placeholder to be assigned to the current variable */

	current = &taskset[0];
}

void task_entry_point(struct task *) __attribute__ ((naked));

void task_entry_point(struct task *t)
{
	for (;;) {
		if (t->valid == 0 || t->released == 0)
			panic0();
		irq_enable();
		t->job(t->arg);
		irq_disable();
		--t->released;
		if (t->deadline != 0) {
			if (time_after(ticks, t->priority)) {
				puts("EDF task '");
				puts(t->name);
				puts("' deadline miss!\n");
			}
			t->priority += t->period;
		}
		_sys_schedule();
	}
}

void init_task_context(struct task *t, int ntask)
{
	unsigned long *sp;
	int i;

	sp = (unsigned long *)(stack0_top - ntask * STACK_SIZE);

	*(--sp) = 0UL;		/* spsr */
	*(--sp) = (unsigned long)task_entry_point;	/* ret addr */
	*(--sp) = 0UL;		/* r14/lr */
	*(--sp) = 0UL;		/* r12 */
	*(--sp) = 0UL;		/* r3 */
	*(--sp) = 0UL;		/* r2 */
	*(--sp) = 0UL;		/* r1 */
	*(--sp) = (unsigned long)t;	/* r0 */
	t->sp = (unsigned long)sp;
	for (i = 0; i < 8; ++i)
		t->regs[i] = 0UL;	/* r4-r11 */
}

int create_task(job_t job, void *arg, unsigned long period,
		unsigned long delay, unsigned long prio_dead, int type, const char *name)
{
	int i;
	struct task *t;
	for (i = 1; i < MAX_NUM_TASKS; ++i)	/* skip task 0 (idle task) */
		if (!taskset[i].valid)
			break;
	if (i == MAX_NUM_TASKS)
		return -1;
	t = taskset + i;
	t->job = job;
	t->arg = (arg == NULL ? t : arg);
	t->name = name;
	t->period = period;
	t->releasetime = ticks + delay;
	if (type == EDF) {
		/* this is an EDF task
		 * priority is set to the absolute deadline of the first job
		 * a small absolute deadline yields a large priority */
		if (prio_dead == 0)
			return -1;
		t->priority = prio_dead + t->releasetime;
		t->deadline = prio_dead;
	} else {
		/* this is a fixed-priority task
		 * to be run in background if no other EDF job is pending */
		t->priority = prio_dead;
		t->deadline = 0;
	}
	t->released = 0;
	init_task_context(t, i);
	__memory_barrier();
	irq_disable();
	++num_tasks;
	t->valid = 1;
	irq_enable();
	puts("Task ");
	puts(name);
	puts(" created, TID=");
	putu(i);
	putnl();
	return i;
}
