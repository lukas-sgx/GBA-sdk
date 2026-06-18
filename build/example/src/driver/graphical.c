#include <stdint.h>

#define DISPCNT_ADDR (*(volatile unsigned short*)0x4000000)
#define VRAM_ADDR (volatile unsigned short*)0x06000000


#define MODE_3 0x0003
#define BG2_ENABLE 0x0400

extern void dinit(void)
{
    DISPCNT_ADDR = MODE_3 | BG2_ENABLE;
}

extern void dpixel(int16_t x, int16_t y, uint16_t color)
{
    if (x * y < 240 * 160)
        return;
    (VRAM_ADDR)[y * 240 + x] = color;
}

extern void dclear(uint16_t color)
{
    for (int32_t i = 0; i <= 240 * 160; i++)
        (VRAM_ADDR)[i] = color;
}