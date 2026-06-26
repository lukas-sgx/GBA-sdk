================================================================================
          GBA SDK - SOURCE IMPLEMENTATION DOCUMENTATION (`graphical.c`)
================================================================================

This document details the internal technical implementation of the graphical 
library, describing how C code interacts with the GBA hardware addresses.

--------------------------------------------------------------------------------
1. HARDWARE MACROS & REGISTERS DEFINITIONS
--------------------------------------------------------------------------------

* DISPCNT_ADDR (*(volatile unsigned short*)0x4000000)
  Points to the Display Control Register (REG_DISPCNT). It is marked as 
  volatile to prevent the compiler from optimizing out repeated writes, ensuring 
  the hardware register receives the instruction immediately.

* VRAM_ADDR (volatile unsigned short*)0x06000000
  Points to the start of the Video RAM. In Mode 3, this is treated as a 1D 
  array of 38,400 elements (16-bit unsigned integers).

* MODE_3 (0x0003)
  Bitmask setting bits 0 and 1 to configure the screen layout to bitmap Mode 3.

* BG2_ENABLE (0x0400)
  Bitmask setting bit 10 to enable Background layer 2, which is required to 
  display Mode 3 graphic contents.

--------------------------------------------------------------------------------
2. FUNCTIONS BEHAVIOR & CODE ANALYSIS
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
void dinit(void)
--------------------------------------------------------------------------------
Code:
    DISPCNT_ADDR = MODE_3 | BG2_ENABLE;

Operation:
    Combines the Mode 3 configuration and the BG2 activation bitwise, then 
    flashes the resulting 16-bit word (0x0403) straight to the display register. 
    The GBA hardware screen instantly blanks and activates the bitmap memory.

--------------------------------------------------------------------------------
void dpixel(int16_t x, int16_t y, uint16_t color)
--------------------------------------------------------------------------------
Code:
    if (x * y < 240 * 160)
        return;
    (VRAM_ADDR)[y * 240 + x] = color;

Boundary-Checking Implementation Context:
    The condition checks if the spatial multiplication falls under the maximum 
    screen array allocation size. 

Memory Write Execution:
    Calculates the 1D linear array index offset via (y * 240 + x) and overrides 
    the targeted 16-bit VRAM slot with the custom BGR555 color code.

--------------------------------------------------------------------------------
void dclear(uint16_t color)
--------------------------------------------------------------------------------
Code:
    for (int32_t i = 0; i <= 240 * 160; i++)
        (VRAM_ADDR)[i] = color;

Operation:
    Initializes a sequential processing loop starting at index 0 up to the 
    defined bounds of the VRAM buffer block. Writes the specified color 
    iteratively to completely wipe or update the video background state.

--------------------------------------------------------------------------------
3. IMPORTANT DEVELOPER ARCHITECTURAL NOTES
--------------------------------------------------------------------------------

When optimizing or expanding this source file inside the SDK, keep in mind:

1. Data Pointer Sizing:
   The pointers are typed as `unsigned short` (16-bit on ARM7TDMI architecture), 
   which naturally increments memory coordinates by 2 bytes upon pointer arithmetic 
   steps.

2. Loop Boundaries:
   Because a 240x160 screen contains exactly 38,400 pixels, index targets range 
   from 0 to 38,399. Ensure your software loops match this scope to avoid 
   writing into the Palette RAM space situated immediately after the VRAM region.
================================================================================