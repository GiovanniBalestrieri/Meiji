#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

#define WDT1_BASE       0x44e35000

iomemdef(WDT1_WTGR, WDT1_BASE + 0x30);
