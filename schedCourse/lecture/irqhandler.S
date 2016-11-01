/* Shamelessy "inspired" by "Building bare-metal ARM Systems with GNU",
   by Miro Samek of Quantum Leaps, LLC */

	.equ NO_IRQ, 0x80
	.equ NO_FIQ, 0x40
	.equ NO_INT, (NO_IRQ | NO_FIQ)
	.equ FIQ_MODE, 0x11
	.equ IRQ_MODE, 0x12
	.equ SYS_MODE, 0x1f

	.section .text
	.code 32
	.globl _irq_handler

 _irq_handler:

	mov r13, r0							/* save r0 in r13_IRQ */
	sub r0, lr, #4						/* put return address in r0_SYS */
	mov lr, r1							/* save r1 in r14_IRQ (lr) */
	mrs r1, spsr						/* put the spsr in r1_SYS */
	msr cpsr_c, #(SYS_MODE|NO_IRQ)		/* SYSTEM mode, IRQ disabled */
	stmfd sp !, {r0, r1}				/* save spsr and pc on SYS stack */
	stmfd sp !, {r2-r3, r12, lr}		/* save AAPCS-clobbered regs on SYS stack */
	mov r0, sp							/* make sp_SYS visible to IRQ mode */
	sub sp, sp, #(2*4)					/* make room for the stacking (r0_SYS,r1_SYS) */
	msr cpsr_c, #(IRQ_MODE|NO_IRQ)		/* IRQ mode, IRQ disabled */
	stmfd r0 !, {r13, r14}				/* finish saving the context (r0_SYS,r1_SYS) */
	msr cpsr_c, #(SYS_MODE|NO_IRQ)		/* SYSTEM mode, IRQ disabled */
	ldr r12, = _bsp_irq					/* address of middle level C IRQ-handler */
	mov lr, pc							/* copy return address to link register */
	bx r12								/* call the C IRQ-handler */
	msr cpsr_c, #(SYS_MODE|NO_INT)		/* SYSTEM mode, IRQ/FIQ disabled */
	mov r0, sp							/* make sp_SYS visible to IRQ mode */
	add sp, sp, #(8*4)					/* fake unstacking 8 registers from the stack */
	msr cpsr_c, #(IRQ_MODE|NO_INT)		/* IRQ mode, IRQ/FIQ disabled */
	mov sp, r0							/* copy sp_SYS to sp_IRQ */
	ldr r0,[sp, #(7*4)]					/* load the saved spsr from the stack */
	msr spsr_cxsf, r0					/* copy the saved spsr to spsr_IRQ */

/* Support for preemptible jobs -- begin */

	and r0, r0, #SYS_MODE				/* mask unwanted flags */
	teq r0, #SYS_MODE					/* if returning to non-SYSTEM mode */
	bne .Lnosched						/*    then jump to label .Lnosched to finish */
	ldr r0, =trigger_schedule			/* load the address of trigger_schedule */
	ldr r0,[r0]							/* load the contents of trigger_schedule */
	tst r0, r0							/* if trigger_schedule == 0 */
	beq .Lnosched						/*    then jump to label .Lnosched to finish */
	ldr lr, =_irq_schedule				/* when returning into SYSTEM mode, jump there */
	movs pc, lr							/* jump to _irq_schedule() in SYSTEM mode */

.Lnosched:
/* Support for preemptible jobs -- end */

	ldmfd sp, {r0-r3, r12, lr}^			/* unstack all saved SYSTEM registers */
										/* "^" here means: use SYSTEM/USER registers */
	nop									/* can't access banked registers immediately */
	ldr lr,[sp, #(6*4)]					/* load return address from the stack */
	movs pc, lr							/* return restoring cpsr from spsr */


_irq_schedule:
	sub sp, sp, #32						/* values to be preserved already on the stack */
.Lnosub32:
	ldr r12, =schedule					/* load the address of the scheduler function */
	mov lr, pc							/* copy return address to the link register */
	bx r12								/* call schedule() -- return value in r0 */

	tst r0, r0							/* if return value is NULL */
	beq .Lnoswitch						/*    then jump to label .Lnoswitch to finish */
	ldr r12, =_switch_to				/* load the address of the _switch_to function */
	mov lr, pc							/* copy return address to the link register */
	bx r12								/* call _switch_to() */

/*	When _switch_to() returns here, the stack has been changed.
	The new stack contains the values suited for the job to be executed right now.
	Now the registers of the current job are restored to their saved values */

.Lnoswitch:
	ldr r0,[sp, #(7*4)]					/* load saved cpsr value */
	msr cpsr_f, r0						/* restore the flags */
	ldmfd sp !, {r0-r3, r12, lr}		/* restore (SYSTEM) registers from the stack */
	ldr pc,[sp], #(2*4)					/* terminate by jumping to the return address */

/*	The last instruction:
		(1) loads in r15/pc the return address saved on the current stack top
		(2) removes return address and saved flags from the top of the stack
		(3) does not modify any other register */


 .globl _sys_schedule

_sys_schedule:

	str lr,[sp, #-(4*2)]!				/* push the return address skipping cpsr's slot */
	mrs lr,cpsr							/* read special register cpsr */
	str lr,[sp, #4]						/* store the value of cpsr in its slot */
	ldr lr,[sp]							/* load in r14/lr the return address */
	stmfd sp !, {r0-r3, r12, lr}		/* save the AACS-clobbered registers */
	b .Lnosub32							/* jump into the _irq_schedule() function, 
										   bypassing the adjustment of the stack top */

