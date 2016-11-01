    .text
    .code 32
    
    .equ    MODE_BITS,  0x1f
    .equ    USER_MODE,  0x10
    .equ    FIQ_MODE,   0x11
    .equ    IRQ_MODE,   0x12
    .equ    SVC_MODE,   0x13
    .equ    MON_MODE,   0x16
    .equ    ABORT_MODE, 0x17
    .equ    HYPER_MODE, 0x1a
    .equ    UNDEF_MODE, 0x1b
    .equ    SYS_MODE,   0x1f
    .equ    IRQ_BIT,    0x80
    .equ    FIQ_BIT,    0x40
    
    .global _reset
_reset:
    /* Force System mode, IRQ/FIQ masked */
    mrs     r0,cpsr
    bic     r0,r0,#MODE_BITS
    orr     r0,r0,#(SYS_MODE|IRQ_BIT|FIQ_BIT)
    msr     cpsr,r0

    /* load stack pointer */
    ldr     sp,=stack0_top
    ldr     sp,[sp]
    
    /* goto to C function _init() */
    b       _init
