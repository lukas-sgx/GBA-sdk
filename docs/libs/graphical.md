# GBA SDK - GRAPHICAL COMPONENT ARCHITECTURE & IMPLEMENTATION

This technical document serves as both the API specification and implementation 
reference for the low-level Mode 3 graphical library included in `cartridge-sdk`.

--------------------------------------------------------------------------------
 1. HARDWARE LAYER & MEMORY MAP
--------------------------------------------------------------------------------

The library directly manipulates the GameBoy Advance display architecture by 
targeting Video Mode 3 (a single 16-bit high-color bitmap frame buffer).

* Memory Geometry : 240 columns x 160 rows (38,400 pixels total)
* Color Depth     : 15-bit color encapsulated inside a 16-bit word (BGR555)
* VRAM Boundary   : Starts at 0x06000000 and ends at 0x06012BFF

  [0,0]-------------------------------------------------------[239,0]
    |                                                            |
    |                                                            |
    |                         GBA SCREEN                         |
    |                      (240 x 160 px)                        |
    |                                                            |
    |                                                            |
  [0,159]-----------------------------------------------------[239,159]

--------------------------------------------------------------------------------
 2. SOURCE CODE REFERENCE (`graphical.c`)
--------------------------------------------------------------------------------

Below is the concrete implementation used to drive the graphics processing unit.

```c
#include <stdint.h>

/* --- Hardware Register Definitions --- */
#define DISPCNT_ADDR (*(volatile unsigned short*)0x4000000)
#define VRAM_ADDR    (volatile unsigned short*)0x06000000

/* --- Video Control Flags --- */
#define MODE_3       0x0003
#define BG2_ENABLE   0x0400

/**
 * @brief Initializes the GBA display subsystem.
 * Confirms Video Mode 3 operation and activates background layer 2.
 */
void dinit(void)
{
    DISPCNT_ADDR = MODE_3 | BG2_ENABLE;
}

/**
 * @brief Plots a color pixel onto explicit screen coordinates.
 * Includes security checks to avoid VRAM pointer overflows.
 */
void dpixel(int16_t x, int16_t y, uint16_t color)
{
    /* Safety check against hardware out-of-bounds corruption */
    if (x < 0 || x >= 240 || y < 0 || y >= 160)
        return;

    /* Matrix conversion: Base + (Y * Width + X) */
    (VRAM_ADDR)[y * 240 + x] = color;
}

/**
 * @brief Floods the active frame buffer with a single uniform color.
 * Effectively cleans or refreshes the viewport interface.
 */
void dclear(uint16_t color)
{
    /* Loop over exactly 38,400 pixels (0 to 38399) */
    for (int32_t i = 0; i < 240 * 160; i++)
    {
        (VRAM_ADDR)[i] = color;
    }
}