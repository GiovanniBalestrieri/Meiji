How to load the image on the BBB:

1) connect the BBB to the host PC via the USB cable
2) connect the USB-serial cable (Header pins: 1=black (ground),
   4=orange, 5=yellow)
3) open minicom or other serial communication program on host PC
   (115200, 8N1)
3) reboot the BBB via switch S1
4) press a key on minicom to stop autobooting
5) load the image in memory at offset 0x80000000 with the command
   in U-Boot: "loadb 0x80000000"
6) start kermit data transfer on host PC (in minicom, Ctrl-A+S ...)
7) start image with the command
   in U-Boot: "go 0x80000000"
