#include "beagleboneblack.h"

unsigned int loops_per_usec;

#define LOOPS_PER_USEC_SHIFT 10
#define CALIBRATE_LOOP_DELAY 10000000ul

void calibrate_udelay(void)
{
	unsigned long t, d = CALIBRATE_LOOP_DELAY;
	irq_disable();
	/* start clocking the DMTimer1 module */
	iomem(CM_WKUP_TIMER1_CLKCTRL) = 0x2;
	__memory_barrier();
	loop_delay(10000); /* give enough time to hardware circuits */
	iomem(CM_DPLL_CLKSEL_TIMER1MS_CLK) = 4; /* select high precision 32768 Hz oscillator */
	__memory_barrier();
	iomem(DMTIMER1_TIOCP_CFG) = 0x2; /* soft reset the module */
	while ((DMTIMER1_TISTAT & 0x1) == 0) /* wait for reset completed */
		__memory_barrier(); 
	iomem(DMTIMER1_TIER) = 0; /* disable interrupts */
	__memory_barrier();
	iomem(DMTIMER1_TCLR) = 0x1; /* start the TIMER counter */
	__memory_barrier();
	while (d-- > 0)
		__memory_barrier();
	/* TCRR was just reset to zero, and it wraps around in approx 36 hours. 
	 * There should be no risk of overflow here */
	t = iomem(DMTIMER1_TCRR);
	__memory_barrier();
	irq_enable();
	loops_per_usec = (((CALIBRATE_LOOP_DELAY / 1000000ul) * Timer1_Freq)<<LOOPS_PER_USEC_SHIFT) / (float) t;
	puts("Calibration: loops_per_usec=");
	putf(loops_per_usec/(float)(1u<<LOOPS_PER_USEC_SHIFT), 2);
	putnl();
}

void udelay(unsigned int usec)
{
	unsigned long loops = (usec * loops_per_usec) >> LOOPS_PER_USEC_SHIFT;
	loop_delay(loops);
}

void mdelay(unsigned int msec)
{
	unsigned int tckd = (msec * HZ) / 1000;
	u32 expire = ticks + tckd + 1;
	while (time_before(ticks, expire))
		cpu_wait_for_interrupt();
}
