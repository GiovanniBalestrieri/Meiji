ENTRY(_reset)

mem_start = 0x80000000;
mem_end   = mem_start + 512*1024*1024;

SECTIONS
{
    . = mem_start;
    .text : {
        startup.o(.text)
        . = ALIGN(4);
        *(.text)
        . = ALIGN(4);
    }
    .rodata : {
        *(.rodata)
        . = ALIGN(4);
    }
    .data : {
        *(.data)
        . = ALIGN(4);
    }
    .bss : {
        /* special case for stacks: in .bss but not initialized */
        *(.bss.stack)
        _bss_start = .;
        *(.bss)
        *(COMMON)
        . = ALIGN(4);
        _bss_end = .;
    }
}
