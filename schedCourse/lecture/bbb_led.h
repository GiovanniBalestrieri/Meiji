#ifndef _BEAGLEBONEBLACK_H_
#error You must not include this sub-header file directly
#endif

/*** LEDs ***/

#define _led_on(V)      gpio1_on(21+(V))
#define _led_off(V)     gpio1_off(21+(V))

#define led0_on()       _led_on(0)
#define led0_off()      _led_off(0)
#define led1_on()       _led_on(1)
#define led1_off()      _led_off(1)
#define led2_on()       _led_on(2)
#define led2_off()      _led_off(2)
#define led3_on()       _led_on(3)
#define led3_off()      _led_off(3)

#define leds_mask(V)        gpio1_mask((V)<<21)
#define leds_toggle_mask(V) gpio1_toggle_mask((V)<<21)
#define leds_on_mask(V)     gpio1_on_mask((V)<<21)
#define leds_off_mask(V)    gpio1_off_mask((V)<<21)
