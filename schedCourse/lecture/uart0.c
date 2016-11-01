#include "beagleboneblack.h"

int putc(int ch)
{
	while (!(iomem(UART0_LSR) & LSR_TXFIFOE))
		/* do nothing */ ;
	iomem(UART0_THR) = ch;
	return 1;
}

int puts(const char *st)
{
	int v = 0;
	while (*st) {
		v += putc(*st);
		if (*st++ == '\n')
			v += putc('\r');
	}
	return v;
}

int putnl(void)
{
	putc('\n');
	putc('\r');
	return 2;
}

int puth(unsigned long v)
{
	int i, d, w = 0;
	u32 mask;

	mask = 0xf0000000;
	for (i = 0; mask != 0; i += 4, mask >>= 4) {
		d = (v & mask) >> (28 - i);
		w += putc(d + (d > 9 ? 'a' - 10 : '0'));
	}
	return w;
}

int putu(unsigned long v)
{
	char buf[11];
	int i, r, w = 0;

	if (v < 10ul) {
		w += putc(v + '0');
		return w;
	}
	i = 10;
	buf[i] = '\0';
	while (v != 0) {
		unsigned long w = v / 10;
		r = v - w * 10;
		v = w;
		buf[--i] = (char)(r + '0');
	}
	w += puts(buf + i);
	return w;
}

int putd(long v)
{
	int w = 0;
	if (v < 0) {
		w += putc('-');
		v = -v;
	}
	w += putu(v);
	return w;
}

int putf(double v, int prec)
{
	int i, w = 0;
	if (v < 0.0) {
		w += putc('-');
		v = -v;
	}
	w += putu(v);
	w += putc('.');
	for (i = 0; i < prec; ++i) {
		v = v - (int)v;
		v = v * 10;
		w += putc('0' + (int)v + (i + 1 == prec && v - (int)v > .5));
	}
	return w;
}

int putcn(int ch, int n)
{
	int i;

	if (n <= 0)
		return 0;
	for (i = 0; i < n; ++i)
		putc(ch);
	return n;
}
