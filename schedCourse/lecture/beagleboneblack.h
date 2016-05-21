#ifndef _BEAGLEBONEBLACK_H_
#define  _BEAGLEBONEBLACK_H_

typedef unsigned int u32;

static volatile u32 *const _iomem = (u32 *) 0;

#define iomemdef(N,V) enum { N = (V)/sizeof(u32) };
#define iomem(N) _iomem[N]

static inline void iomem_high(unsigned int reg, u32 mask)
{
	iomem(reg) |= mask;
}

static inline void iomem_low(unsigned int reg, u32 mask)
{
	iomem(reg) &= ~mask;
}

#include "bbb_cpu.h"
#include "bbb_vectors.h"
#include "bbb_cm.h"
#include "bbb_gpio.h"
#include "bbb_led.h"
#include "bbb_uart.h"
#include "bbb_intc.h"
#include "bbb_timer.h"
#include "bbb_watchdog.h"

#include "comm.h"

#endif
