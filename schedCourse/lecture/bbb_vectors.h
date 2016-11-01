static inline u32 *get_vectors_address(void)
{
	u32 v;

	/* read SCTLR (ARM B4.1.130) */
	__asm__ __volatile__("mrc p15, 0, %0, c1, c0, 0\n":"=r"(v)::);
	if (v & (1 << 13))
		return (u32 *) 0xffff0000;
	/* read VBAR (ARM B4.1.156) */
	__asm__ __volatile__("mrc p15, 0, %0, c12, c0, 0\n":"=r"(v)::);
	return (u32 *) v;
}
