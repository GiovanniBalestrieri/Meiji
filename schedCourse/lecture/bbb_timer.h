#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

#include "bbb_dmtimer0.h"
#include "bbb_dmtimer1.h"

/* AM33x TRM says that DMTimer0 runs at ~32768 Hz (20.1.2.2),
 * however instead of 1024 Hz we got a 1256 Hz tick frequency
 * on a rev.B board, and 1310 Hz on a rev.C board.
 * The issue is explained at 8.1.6.12 ("Timer Clock Structure"):
 * "DMTIMER1 is implemented using the DMTimer_1ms module which is capable of
 * generating an accurate 1ms tick using a 32.768 KHz clock. [...]
 * in low power modes DMTIMER1 in the WKUP domain can use the 32K
 * RC oscillator for generating the OS (operating system) 1ms tick generation
 * and timer based wakeup. Since most applications expect an accurate 1ms OS
 * tick which the inaccurate 32K RC (16-60 KHz) oscillator cannot provide, a
 * separate 32768 Hz oscillator (32K Osc) is provided as another option."
 * It turns out that DMTimer0 makes use of the inaccurate 32K RC oscillator,
 * while DMTimer1 (when not in power mode) can be configure so as to exploit
 * the accurate 32K Osc oscillator. Go for it, then. */
 
#define HZ          1000	/* Tick frequency (Hz) */
#define TICK_TLDR       (0xffffffffu-(Timer1_Freq/HZ)+1)

#define CONFIG_TICK_ADJUST 0

#define TICK_V0			(Timer1_Freq/HZ)
#define TICK_V1			(Timer1_Freq*1000*(1000/HZ))
#define TICK_TPIR		(((TICK_V0+1)*1000000ul)-TICK_V1)	/* 232000 -- AM335x TRM 20.2.3.1.1 */
#define TICK_TNIR		((TICK_V0*1000000ul)-TICK_V1)		/* -768000 -- AM335x TRM 20.2.3.1.1 */
