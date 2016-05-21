#ifndef _BEAGLEBONEBLACK_H_
#error "You must not include this sub-header file directly"
#endif

#define CONTROL_MODULE_BASE		0x44e10000

iomemdef(CM_CONF_GPMC_AD2, CONTROL_MODULE_BASE + 0x808); /* gpio1[6], P8-3 */
iomemdef(CM_CONF_GPMC_AD3, CONTROL_MODULE_BASE + 0x80c); /* gpio1[7], P8-4 */
iomemdef(CM_CONF_GPMC_AD6, CONTROL_MODULE_BASE + 0x818); /* gpio1[2], P8-5 */
iomemdef(CM_CONF_GPMC_AD7, CONTROL_MODULE_BASE + 0x81c); /* gpio1[3], P8-6 */

#define CM_PER					0x44e00000
iomemdef(CM_PER_GPIO1_CLKCTRL, CM_PER + 0xac);

#define CM_WKUP                                        0x44e00400
iomemdef(CM_WKUP_CLKSTCTRL,                    CM_WKUP + 0x00);
iomemdef(CM_WKUP_TIMER1_CLKCTRL,       CM_WKUP + 0xc4);

#define CM_DPLL                                        0x44e00500
iomemdef(CM_DPLL_CLKSEL_TIMER1MS_CLK,  CM_DPLL + 0x28);
