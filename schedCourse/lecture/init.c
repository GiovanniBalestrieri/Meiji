#include "beagleboneblack.h"

static void init_vectors(void)
{
	extern void _reset(void);
	extern void _irq_handler(void);
	volatile u32 *vectors = get_vectors_address();

#define LDR_PC_PC 0xe59ff018

	vectors[0] = LDR_PC_PC;	/* Reset / Reserved */
	vectors[1] = LDR_PC_PC;	/* Undefined instruction */
	vectors[2] = LDR_PC_PC;	/* Software interrupt */
	vectors[3] = LDR_PC_PC;	/* Prefetch abort */
	vectors[4] = LDR_PC_PC;	/* Data abort */
	vectors[5] = LDR_PC_PC;	/* Hypervisor trap */
	vectors[6] = LDR_PC_PC;	/* Interrupt request (IRQ) */
	vectors[7] = LDR_PC_PC;	/* Fast interrupt request (FIQ) */

	vectors[8] = (u32) _reset;	/* Reset / Reserved */
	vectors[9] = (u32) panic0;	/* Undefined instruction */
	vectors[10] = (u32) panic0;	/* Software interrupt */
	vectors[11] = (u32) panic0;	/* Prefetch abort */
	vectors[12] = (u32) panic1;	/* Data abort */
	vectors[13] = (u32) panic0;	/* Hypervisor trap */
	vectors[14] = (u32) _irq_handler;	/* Interrupt request (IRQ) */
	vectors[15] = (u32) panic0;	/* Fast interrupt request (FIQ) */

#undef LDR_PC_PC
}

static void init_gpio1(void)
{
	/* Select pins 21-24 of GPIO1 (USR LED) */
	u32 mask = (1 << 21) | (1 << 22) | (1 << 23) | (1 << 24);
	/* Also select pins 2 (P8-5), 3 (P8-6), 6 (P8-3), 7 (P8-4) */
	mask |= (1 << 6) | (1 << 7) | (1 << 2) | (1 << 3);
	/* Set clock, TRM 8.1.12.1.29 */
	iomem(CM_PER_GPIO1_CLKCTRL) = 0x40002;
	/* Set direction for pins in mask, TRM 25.3.4.3 */
	/* "If the application uses a pin as an output and does not
	 * want interrupt generation from this pin, the application
	 * must properly configure the interrupt enable registers." */
	iomem_low(GPIO1_OE, mask);
	iomem_high(GPIO1_IRQSTATUS_CLR_0, mask);
	iomem_high(GPIO1_IRQSTATUS_CLR_1, mask);
	/* Set pin mux so as to export gpio1[2,3,6,7] signals to header P8 */
	/* Fast slew rate, receiver buffer disabled, internal pull-up resistor
	 * disabled, mode 0b111 (P8[3,4,5,6] <--> gpio1[6,7,2,3])
	 * "If a pad is always configured in output mode, it is recommended for
	 * user software to disable any internal pull resistor tied to it, to avoid
	 * unnecessary consumption."  TRM 9.2.2.2 */
	iomem(CM_CONF_GPMC_AD2) = 0x0f;
	iomem(CM_CONF_GPMC_AD3) = 0x0f;
	iomem(CM_CONF_GPMC_AD6) = 0x0f;
	iomem(CM_CONF_GPMC_AD7) = 0x0f;
	/* Set all lines to ground */
	gpio1_off(2);
	gpio1_off(3);
	gpio1_off(6);
	gpio1_off(7);
}

static void fill_bss(void)
{
	extern u32 _bss_start, _bss_end;
	u32 *p;

	for (p = &_bss_start; p < &_bss_end; ++p)
		*p = 0UL;
}

static void init_intc(void)
{
	/* We globally disabled all interrupts in _reset() */
	/* Now we disable each interrupt individually */
	iomem(INTC_MIR_SET_BASE + 0) = 0xffffffffUL;
	iomem(INTC_MIR_SET_BASE + 8) = 0xffffffffUL;
	iomem(INTC_MIR_SET_BASE + 16) = 0xffffffffUL;
	iomem(INTC_MIR_SET_BASE + 24) = 0xffffffffUL;

	/* Disable the threshold mechanism */
	iomem(INTC_THRESHOLD) = 0xff;

	irq_enable();
}

/* "If an ARMv7-A core includes VFP hardware, it must be explicitly
   enabled before applications can make use of it.
   Several steps are required to do this:
   * The EN bit in the FPEXC register must be set.
   * If access to VFP is required in the Normal world, access to CP10
	 and CP11 must be enabled in the Non-Secure Access Control Register
	 (CP15.NSACR). This would normally be done inside the Secure bootloader.
   * Access to CP10 and CP11 must be enabled in the Coprocessor
	 Access Control Register (CP15.CACR). This can be done on demand by
	 the operating system." (ARM Cortex-A Programming Guide, 6.1.3) */

static void init_vfp(void)
{
	u32 v = read_coprocessor_access_control_register();
	v |= (1u << 20) | (1u << 22);	/* ARM Cortex-A8 TRM, 3.2.27 */
	write_coprocessor_access_control_register(v);
	__memory_barrier();
	set_en_bit_in_fpexc();
}

void _init(void)
{
	init_vfp();
	init_vectors();
	init_gpio1();
	fill_bss();
	init_intc();
	init_taskset();
	calibrate_udelay();
	init_ticks();
	init_watchdog();
	main();
}
