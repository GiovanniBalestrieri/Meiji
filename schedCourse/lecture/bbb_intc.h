#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

/*** Interrupt Controller ***/

#define INTC_BASE           0x48200000

iomemdef(INTC_SYSCONFIG, INTC_BASE + 0x10);
iomemdef(INTC_SIR_IRQ, INTC_BASE + 0x40);
iomemdef(INTC_CONTROL, INTC_BASE + 0x48);
iomemdef(INTC_THRESHOLD, INTC_BASE + 0x68);
iomemdef(INTC_ITR_BASE, INTC_BASE + 0x80);
iomemdef(INTC_MIR_BASE, INTC_BASE + 0x84);
iomemdef(INTC_MIR_CLEAR_BASE, INTC_BASE + 0x88);
iomemdef(INTC_MIR_SET_BASE, INTC_BASE + 0x8c);
iomemdef(INTC_ISR_SET_BASE, INTC_BASE + 0x90);
iomemdef(INTC_ISR_CLEAR_BASE, INTC_BASE + 0x94);
iomemdef(INTC_PENDING_IRQ_BASE, INTC_BASE + 0x98);
iomemdef(INTC_ILR_BASE, INTC_BASE + 0x100);

#define NUM_IRQ_LINES   128
#define NEWIRQAGR       0x1

#define irq_enable() do { \
    unsigned long _temp;  \
    __asm__ __volatile__ ("mrs %0,cpsr\n\t" \
                          "bic %0,%0,#0x80\n\t" \
                          "msr cpsr_c,%0\n\t"  \
                        : "=r" (_temp) \
                        : : "memory"); \
} while (0)

#define irq_disable() do { \
    unsigned long _temp;  \
    __asm__ __volatile__ ("mrs %0,cpsr\n\t" \
                          "orr %0,%0,#0x80\n\t" \
                          "msr cpsr_c,%0\n\t"  \
                        : "=r" (_temp) \
                        : : "memory"); \
} while (0)

#define data_sync_barrier() do { \
    unsigned long _temp; \
    __asm__ __volatile__ ("mcr p15,0,%0,c7,c10,4\n" \
                        : "=r" (_temp) \
                        : : "memory"); \
} while (0)
