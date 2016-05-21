#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

#define Timer1_Freq 32768	/* Hz */

#define Timer1_IRQ 67
#define Timer1_IRQ_Bank (Timer1_IRQ/32)
#define Timer1_IRQ_Bit  (Timer1_IRQ%32)
#define Timer1_IRQ_Mask (1u<<Timer1_IRQ_Bit)

#define DMTIMER1_BASE           0x44e31000

iomemdef(DMTIMER1_TIDR,			DMTIMER1_BASE + 0x00);
iomemdef(DMTIMER1_TIOCP_CFG,	DMTIMER1_BASE + 0x10);
iomemdef(DMTIMER1_TISTAT,		DMTIMER1_BASE + 0x14);
iomemdef(DMTIMER1_TISR,			DMTIMER1_BASE + 0x18);
iomemdef(DMTIMER1_TIER,			DMTIMER1_BASE + 0x1c);
iomemdef(DMTIMER1_TWER,			DMTIMER1_BASE + 0x20);
iomemdef(DMTIMER1_TCLR,			DMTIMER1_BASE + 0x24);
iomemdef(DMTIMER1_TCRR,			DMTIMER1_BASE + 0x28);
iomemdef(DMTIMER1_TLDR,			DMTIMER1_BASE + 0x2c);
iomemdef(DMTIMER1_TTGR,			DMTIMER1_BASE + 0x30);
iomemdef(DMTIMER1_TWPS,			DMTIMER1_BASE + 0x34);
iomemdef(DMTIMER1_TMAR,			DMTIMER1_BASE + 0x38);
iomemdef(DMTIMER1_TCAR1,		DMTIMER1_BASE + 0x3c);
iomemdef(DMTIMER1_TSICR,		DMTIMER1_BASE + 0x40);
iomemdef(DMTIMER1_TCAR2,		DMTIMER1_BASE + 0x44);
iomemdef(DMTIMER1_TPIR,			DMTIMER1_BASE + 0x48);
iomemdef(DMTIMER1_TNIR,			DMTIMER1_BASE + 0x4c);
iomemdef(DMTIMER1_TCVR,			DMTIMER1_BASE + 0x50);
iomemdef(DMTIMER1_TOCR,			DMTIMER1_BASE + 0x54);
iomemdef(DMTIMER1_TOWR,			DMTIMER1_BASE + 0x58);

#define DMT1_TCAR_IT_FLAG    0x4
#define DMT1_OVF_IT_FLAG     0x2
#define DMT1_MAT_IT_FLAG     0x1
