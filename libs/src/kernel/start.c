#include "lcd.h"

extern void main();

__attribute__((section(".text.kernel_init")))
void kernel_init(void)
{
    gba_lcd_driver_init();
    main();
    while (1);
}