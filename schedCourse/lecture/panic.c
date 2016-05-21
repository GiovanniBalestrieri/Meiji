#include "beagleboneblack.h"

static inline void panic(int l1)
{
	leds_mask(l1 & 0xf);
	for (;;) {
		loop_delay(3000000u);
		leds_toggle_mask(0xf);
	}
}

void panic0(void)
{
	panic(5);
}

void panic1(void)
{
	panic(6);
}

void panic2(void)
{
	panic(3);
}
