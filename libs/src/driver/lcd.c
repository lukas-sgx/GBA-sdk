#include "lcd.h"
#include <stdint.h>

void gba_lcd_driver_init(void)
{
    GBA_LCD.DISPCNT.BG2 = 1;
    GBA_LCD.DISPCNT.BG_MODE = 3;
}

void gba_lcd_vram_dpixel(uint16_t color, uint32_t x, uint32_t y)
{
    if (x >= 240 || y >= 160)
        return;
    (GBA_LCD_VRAM)[y * 240 + x] = color;
}

void gba_lcd_vram_clear(uint16_t color)
{
    uint32_t color32 = color << 16 | color;
    volatile uint32_t* vram32 = (volatile uint32_t*)GBA_LCD_VRAM;
    
    for (int32_t i = 0; i < 240 * 160 / 2; i++)
        (vram32)[i] = color32;
}

void gba_lcd_wait_vblank(void)
{
    while (GBA_LCD.DISPSTAT.VBF & 1);
    while (!(GBA_LCD.DISPSTAT.VBF & 1));
}