#ifndef GRAPHICAL_H
    #define GRAPHICAL_H

    #include <stdint.h>

    #define DISPCNT_ADDR (*(volatile uint16_t*)0x4000000)
    #define VRAM_ADDR (volatile uint16_t*)0x06000000
    #define DISPSTAT_ADDR (*(volatile uint16_t*)0x4000004)
    
    #define MODE_3 0x0003
    #define BG2_ENABLE 0x0400

void dinit(void);
void dclear(uint16_t color);
void dpixel(uint16_t x, uint16_t y, uint16_t color);
void wait_vblank(void);
#endif