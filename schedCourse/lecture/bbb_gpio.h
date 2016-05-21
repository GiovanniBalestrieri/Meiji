#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

#define GPIO1_BASE            0x4804c000

iomemdef(GPIO1_IRQSTATUS_CLR_0, GPIO1_BASE + 0x3c);
iomemdef(GPIO1_IRQSTATUS_CLR_1, GPIO1_BASE + 0x40);
iomemdef(GPIO1_OE, GPIO1_BASE + 0x134);
iomemdef(GPIO1_DATAOUT, GPIO1_BASE + 0x13c);

/* TRM 25.3.4 */

iomemdef(GPIO1_CLEARDATAOUT, GPIO1_BASE + 0x190);
iomemdef(GPIO1_SETDATAOUT, GPIO1_BASE + 0x194);

#define gpio1_mask(V) do { \
                            iomem(GPIO1_DATAOUT) = (V); \
                      } while (0)

#define gpio1_toggle_mask(V) do { \
                            iomem(GPIO1_DATAOUT) ^= (V); \
                      } while (0)

#define gpio1_on_mask(V) do { \
                            iomem(GPIO1_SETDATAOUT) = (V); \
                         } while (0)

#define gpio1_off_mask(V) do { \
                            iomem(GPIO1_CLEARDATAOUT) = (V); \
                        } while (0)

#define gpio1_on(V)     gpio1_on_mask(1<<(V))
#define gpio1_off(V)    gpio1_off_mask(1<<(V))
