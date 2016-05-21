#include "beagleboneblack.h"

static isr_t ISR[NUM_IRQ_LINES];
unsigned long irqcount[NUM_IRQ_LINES] = { 0, };;

void _bsp_irq(void)
{
	isr_t isr;
	u32 v;

	/* Cancel any soft irq */
	iomem(INTC_ISR_CLEAR_BASE + 0) = 0xffffffffUL;
	iomem(INTC_ISR_CLEAR_BASE + 8) = 0xffffffffUL;
	iomem(INTC_ISR_CLEAR_BASE + 16) = 0xffffffffUL;
	iomem(INTC_ISR_CLEAR_BASE + 24) = 0xffffffffUL;

	for (;;) {
		if (iomem(INTC_PENDING_IRQ_BASE + 0) == 0 &&
		    iomem(INTC_PENDING_IRQ_BASE + 8) == 0 &&
		    iomem(INTC_PENDING_IRQ_BASE + 16) == 0 &&
		    iomem(INTC_PENDING_IRQ_BASE + 24) == 0)
			return;

		/* there are pending unmasked IRQs on some IC */

		/* read the (highest-priority) IRQ line number */
		v = iomem(INTC_SIR_IRQ);

		/* Do nothing if a spurious interrupt is detected 
		   (see AM335x TRM, 6.2.5) */
		if (v < NUM_IRQ_LINES) {
			isr = ISR[v];
			if (!isr)
				panic0();
			/* invoke the ISR (with IRQ disabled) */
			isr();
			++irqcount[v];
			/* just to be sure, in case the ISR has left enabled the IRQs */
			irq_disable();
		}

		/* (TRM 6.2.2) "After the return of the subroutine, the ISR sets the
		 * NEWIRQAGR/NEWFIQAGR bit to enable the processing of subsequent pending
		 * IRQs/FIQs and to restore ARM context [...] Because the writes are
		 * posted on an Interconnect bus, to be sure that the preceding writes
		 * are done before enabling IRQs/FIQs, a Data Synchronization Barrier is
		 * used. This operation ensure that the IRQ/FIQ line is de-asserted before
		 * IRQ/FIQ enabling. After that, the INTC processes any other pending
		 * interrupts or deasserts the IRQ/FIQ signal if there is no interrupt. */

		iomem(INTC_CONTROL) = NEWIRQAGR;
		data_sync_barrier();
	}
}

int register_isr(int n, isr_t func)
{
	if (ISR[n] != NULL) {
		puts("ERROR in register_isr(): line ");
		putu(n);
		puts(" already registered\n");
		return 1;
	}
	ISR[n] = func;
	return 0;
}

int deregister_isr(int n)
{
	if (ISR[n] == NULL) {
		puts("ERROR in deregister_isr(): line ");
		putu(n);
		puts(" is not registered\n");
		return 1;
	}
	ISR[n] = NULL;
	return 0;
}
