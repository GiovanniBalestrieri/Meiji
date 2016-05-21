#include "beagleboneblack.h"

static void banner(void)
{
	putcn('=', 65);
	putnl();
	puts("SERT: System Environment for Real-Time, version ");
	putf(2015.11, 2);	/* just for trying the floating-point unit */
	puts("\nMarco Cesati, SPRG, DICII, University of Rome Tor Vergata\n");
	putcn('=', 65);
	putnl();
}

static void led_cycle(void *arg __attribute__ ((unused)))
{
	static int state = 1;
	state = (2 * state + 1) % 30;
	leds_toggle_mask(state);
}

static void show_ticks(void *arg __attribute((unused)))
{
	puts("\nCurrent ticks: ");
	putu(ticks);
	putnl();
}

const unsigned long small_primes[] = 
	{ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
		53, 59, 61, 67, 71, 73, 79, 83, 89, 97 };

void factor_ticks(void *arg)
{
	unsigned long v = ticks;
	int i;
	gpio1_on(3);
	arg = arg;
	putu(v);
	puts(": ");
	i = 0;
	while (v > 1 && i < 25) {
		unsigned long w = v / small_primes[i];
		putc('{');
		putu(w);
		putc('}');
		putc(' ');
		if (v == w * small_primes[i]) {
			putu(small_primes[i]);
			putc(' ');
			v = w;
			continue;
		}
		++i;
	}
	if (v > 1) {
		putc('[');
		putu(v);
		putc(']');
	}
	putnl();
	gpio1_off(3);
}

int raise(int n)
{
	return n;
}

void main(void)
{
	banner();

	if (create_task(led_cycle, NULL, HZ, 5, HZ, FPR, "led_cycle") == -1) {
		puts("ERROR: cannot create task led_cycle\n");
		panic1();
	}
	if (create_task(show_ticks, NULL, 10 * HZ, 5, 10 * HZ, FPR, "show_ticks") == -1) {
		puts("ERROR: cannot create task show_ticks\n");
		panic1();
	}
	if (create_task(factor_ticks, NULL, 17, 1, 1, FPR, "factor_ticks") == -1) {
		puts("ERROR: cannot create task factor_ticks\n");
		panic1();
	}
	for (;;)
		cpu_wait_for_interrupt();
}
