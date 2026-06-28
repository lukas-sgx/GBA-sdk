#include "graphical.h"
#include "font.h"

extern void main(void)
{
    gba_font_t font;

    dinit();
    init_font(&font, MONOSPACED);
    wait_vblank();
    dclear(0xDE7B);
    dtext_opt(&font, 240 / 2, 160 / 2, 31, BG_NONE, DTEXT_HALIGN_MIDDLE, DTEXT_VALIGN_CENTER, "Hello World !");
    while (1)
        wait_vblank();
}