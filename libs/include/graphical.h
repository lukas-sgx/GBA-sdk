#ifndef GRAPHICAL_H
    #define GRAPHICAL_H

    #include <stdint.h>

void dinit(void);
void dclear(uint16_t color);
void dpixel(uint16_t x, uint16_t y, uint16_t color);
#endif