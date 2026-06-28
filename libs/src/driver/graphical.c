#include "graphical.h"
#include <stdint.h>

void dinit(void)
{
    DISPCNT_ADDR = MODE_3 | BG2_ENABLE;
}

void dpixel(uint16_t x, uint16_t y, uint16_t color)
{
    if (x >= 240 || y >= 160)
        return;
    (VRAM_ADDR)[y * 240 + x] = color;
}

void dclear(uint16_t color)
{
    uint32_t color32 = color << 16 | color;
    volatile uint32_t* vram32 = (volatile uint32_t*)VRAM_ADDR;
    
    for (int32_t i = 0; i < 240 * 160 / 2; i++)
        (vram32)[i] = color32;
}

void wait_vblank(void)
{
    while (DISPSTAT_ADDR & 1);
    while (!(DISPSTAT_ADDR & 1));
}