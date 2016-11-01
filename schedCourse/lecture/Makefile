# Marco Cesati, 23.10.2014
CROSSPATH?=/opt/x-tools/gcc-linaro-arm-linux-gnueabihf-4.9-2014.09_linux/bin
CROSSPFX=$(CROSSPATH)/arm-linux-gnueabihf-
CC=$(CROSSPFX)gcc
AS=$(CROSSPFX)as
LD=$(CROSSPFX)ld
NM=$(CROSSPFX)nm
OBJCOPY=$(CROSSPFX)objcopy
OBJDUMP=$(CROSSPFX)objdump
# Alternatively: -O2 || -O3 -fno-tree-vectorize
CFLAGS=-Wall -Wextra -O2 -ffreestanding -ffast-math
ARCHFLAGS=-mcpu=cortex-a8 -march=armv7-a -mfloat-abi=hard -mfpu=neon
CCARCHFLAGS=$(ARCHFLAGS) -marm
CFILES:=$(shell ls *.c 2>/dev/null)
SFILES:=$(shell ls *.S 2>/dev/null)
HFILES:=$(shell ls *.h 2>/dev/null)
AOBJS:=$(SFILES:%.S=%.o)
COBJS:=$(CFILES:%.c=%.o)
TARGET=sert
GCCLIB=$(shell $(CC) -print-libgcc-file-name)

all: $(TARGET).bin $(TARGET).lst $(TARGET).sym

%.bin: %.elf
	$(OBJCOPY) -S -O binary $< $@

$(TARGET).elf: $(AOBJS) $(COBJS) $(TARGET).lds
	$(LD) -nostdlib -T $(TARGET).lds -o $@ $(AOBJS) $(COBJS) $(GCCLIB)

$(COBJS): $(HFILES)

%.o: %.S
	$(AS) $(ARCHFLAGS) -o $@ $<

%.o: %.c 
	$(CC) $(CFLAGS) $(CCARCHFLAGS) -c $<

%.s: %.c
	$(CC) $(CFLAGS) $(CCARCHFLAGS) -S $<

%.lst: %.elf
	$(OBJDUMP) -d $^ > $@

%.sym: %.elf
	$(NM) $^ | sort > $@

.PRECIOUS: %.elf

.PHONY: clean

clean:
	rm -f *~ *.o *.s *.bin *.elf *.lst *.sym

