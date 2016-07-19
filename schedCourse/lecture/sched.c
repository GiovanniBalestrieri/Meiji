#include "beagleboneblack.h"

struct task *current;

volatile unsigned long globalreleases = 0;	/* used as a status changed flag */

volatile unsigned long trigger_schedule = 0;	/* force rescheduling */

void check_periodic_tasks(void)
{
	unsigned long now = ticks;
	struct task *f;
	int i;

	for (i = 0, f = taskset + 1; i < num_tasks; ++f) {	/* skip task 0 (idle task) */
		if (f - taskset >= MAX_NUM_TASKS)
			panic0();	/* Should never happen */
		if (!f->valid)
			continue;
		if (time_after_eq(now, f->releasetime)) { // se è già stato rilasciato
			f->releasetime += f->period;
			++f->released;
			trigger_schedule = 1;	/* force scheduler invocation */
			++globalreleases;
		}
		++i;
	}
}

static inline struct task *select_best_task(void)
{
	unsigned long maxprio;
	int i, edf;
	struct task *best, *f;

	maxprio = MAXUINT;
	edf = 0;
	best = &taskset[0];
	for (i = 0, f = taskset + 1; i < num_tasks; ++f) {
		if (f - taskset >= MAX_NUM_TASKS)
			panic0();	/* Should never happen */
		if (!f->valid)
			continue;
		++i;
		if (f->released == 0)
			continue;
		if (edf) {
			/* fixed-priority tasks have lower priority than EDF ones */
			if (f->deadline == 0)
				continue;
			/* priority in EDF tasks is basically a time instant */
			if (time_before(f->priority, maxprio)) {
				maxprio = f->priority;
				best = f;
			}
			continue;
		} 
		if (f->deadline != 0) {
			edf = 1;
			maxprio = f->priority;
			best = f;
			continue;
		}
		if (f->priority < maxprio) {
			maxprio = f->priority;
			best = f;
		}
	}
	return best;
}

struct task *schedule(void)
{
	static int do_not_enter = 0;
	struct task *best;
	unsigned long oldreleases;
	irq_disable();
	if (do_not_enter != 0) {
		irq_enable();
		return NULL;
	}
	do_not_enter = 1;
	do {
		oldreleases = globalreleases;
		irq_enable();
		best = select_best_task();
		irq_disable();
	} while (oldreleases != globalreleases);
	trigger_schedule = 0;
	best = (best != current ? best : NULL);
	do_not_enter = 0;
	irq_enable();
	return best;
}

#define save_regs(regs) \
    __asm__ __volatile__("stmia %0,{r4-r11}" \
    : : "r" (regs) : "memory");

#define load_regs(regs) \
    __asm__ __volatile__("ldmia %0,{r4-r11}" \
            : : "r" (regs) : "r4", "r5", "r6", "r7", "r8", \
            "r9", "r10", "r11", "memory");

#define switch_stacks(from, to) \
    __asm__ __volatile__("str sp,%0\n\t" \
                         "ldr sp,%1" \
    : : "m" ((from)->sp), "m" ((to)->sp) \
    : "sp", "memory");

#define naked_return() __asm__ __volatile__("bx lr");

void _switch_to(struct task *) __attribute__ ((naked));

void _switch_to(struct task *to)
{
	irq_disable();
	save_regs(current->regs);
	load_regs(to->regs);
	switch_stacks(current, to);
	current = to;
	irq_enable();
	naked_return();
}
