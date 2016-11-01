#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

#define Timer0_Freq 41000	/* Hz , rev. B board */

#define Timer0_IRQ  66
#define Timer0_IRQ_Bank (Timer0_IRQ/32)
#define Timer0_IRQ_Bit  (Timer0_IRQ%32)
#define Timer0_IRQ_Mask (1u<<Timer0_IRQ_Bit)

#define DMTIMER0_BASE           0x44e05000

iomemdef(DMTIMER0_IRQSTATUS, DMTIMER0_BASE + 0x28);
iomemdef(DMTIMER0_IRQENABLE_SET, DMTIMER0_BASE + 0x2c);
iomemdef(DMTIMER0_IRQENABLE_CLR, DMTIMER0_BASE + 0x30);
iomemdef(DMTIMER0_TCLR, DMTIMER0_BASE + 0x38);
iomemdef(DMTIMER0_TLDR, DMTIMER0_BASE + 0x40);
iomemdef(DMTIMER0_TTGR, DMTIMER0_BASE + 0x44);

#define DMT0_TCAR_IT_FLAG    0x4
#define DMT0_OVF_IT_FLAG     0x2
#define DMT0_MAT_IT_FLAG     0x1
