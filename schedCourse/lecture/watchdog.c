#include "beagleboneblack.h"

#define	WDT_Ticks		(HZ*30)
#define WDT_RelDeadline	(WDT_Ticks-1)

static void rearm_watchdog(void *arg __attribute__ ((unused)))
{
	iomem(WDT1_WTGR)++;
}

void init_watchdog(void)
{
	if (create_task(rearm_watchdog, NULL, WDT_Ticks, 1, WDT_RelDeadline, EDF, "watchdog") == -1) {
		puts("ERROR: cannot create task \"watchdog\"\n");
		panic0();
	}
}
