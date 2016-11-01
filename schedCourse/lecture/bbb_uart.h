#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

#define UART0_BASE      0x44e09000

iomemdef(UART0_THR, UART0_BASE + 0);	/* O:RW [7:0]=THR */

iomemdef(UART0_LSR, UART0_BASE + 0x14);	/* AO:R */
#define LSR_RXFIFOE         (1u<<0)
#define LSR_RXOE            (1u<<1)
#define LSR_RXPE            (1u<<2)
#define LSR_RXFE            (1u<<3)
#define LSR_RXBI            (1u<<4)
#define LSR_TXFIFOE         (1u<<5)
#define LSR_TXSRE           (1u<<6)
#define LSR_RXFIFOSTS       (1u<<7)
