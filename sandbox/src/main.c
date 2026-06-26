#include "graphical.h"
#include "font.h"

extern void main(void)
{
    gba_font_t font;

    dinit();
    init_font(&font, 0);
    while (1) {
        dclear(31);
        dclear(28);
        dclear(20);
    }
}