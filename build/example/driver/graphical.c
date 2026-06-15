#include <stdint.h>

#define DISPCNT (*(volatile unsigned short*)0x4000000)

#define MODE_3      0x0003
#define BG2_ENABLE  0x0400

extern void dinit(void)
{
    DISPCNT = MODE_3 | BG2_ENABLE;
}

extern void dclear(uint16_t color)
{
    
}