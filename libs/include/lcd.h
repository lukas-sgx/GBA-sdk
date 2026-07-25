#ifndef GRAPHICAL_H
#define GRAPHICAL_H

    #include "align.h"
    #include <stdint.h>

//     #define DISPCNT_ADDR (*(volatile uint16_t*)0x4000000)
//     #define VRAM_ADDR (volatile uint16_t*)0x06000000
//     #define DISPSTAT_ADDR (*(volatile uint16_t*)0x4000004)

//     #define MODE_3 0x0003
//     #define BG2_ENABLE 0x0400

// void dinit(void);
// void dclear(uint16_t color);
// void dpixel(uint16_t x, uint16_t y, uint16_t color);

// ---
// Low - level driver interface
// ---


// ---
// GBA LCD peripheral. Refer to:
// "GBATEK: LCD I/O Interrupts and Status"
// ---
typedef volatile struct {
  // I/O configuraton
  word_union(DISPCNT,
             uint16_t BG_MODE : 3; // Video Mode
             uint16_t : 1;         // reserved
             uint16_t DFS : 1;     // Display Frame Select
             uint16_t HBIF : 1;    // H - Blank Interval Free
             uint16_t OCVM : 1;    // OBJ Character VRAM Mapping
             uint16_t FB : 1;      // Force Blank
             uint16_t BG0 : 1;     // Enable Screen Display Background 0
             uint16_t BG1 : 1;     // Enable Screen Display Background 1
             uint16_t BG2 : 1;     // Enable Screen Display Background 2
             uint16_t BG3 : 1;     // Enable Screen Display Background 3
             uint16_t OBJ : 1;     // Enable Screen Display OBJ
             uint16_t WDF0 : 1;    // Window Display Flag 0
             uint16_t WDF1 : 1;    // Window Display Flag 1
             uint16_t WDFOBJ : 1;  // Window Display Flag OBJ
  );

  // DISPGW : Green - swap ( undocumented register )
  word_union(DISPGW,
             uint16_t SWAP : 1; // Enable green SWAP
             uint16_t : 15;     // reserved
  );

  // General LCD Status
  word_union(DISPSTAT,
             uint16_t const VBF : 1; // V - Blank Flag
             uint16_t const HBF : 1; // H - Blank Flag
             uint16_t const VCF : 1; // V - Counter Flag
             uint16_t VBIE : 1;      // V - Blank IRQ Enable
             uint16_t HBIE : 1;      // H - Blank IRQ Enable
             uint16_t VCIE : 1;      // V - Counter IRQ Enable
             uint16_t const : 1;     // reserved
             uint16_t const : 1;     // reserved
             uint16_t VCSET : 8;     // V - Count Setting
  );
  // todo: all other register
} WPACKED(2) GBA_lcd_t;

    /* In order to avoid manipulating raw pointers all the time , use a
    generic define instead */
    #define GBA_LCD (*(volatile GBA_lcd_t *)0x04000000)

    /* Generic Video RAM address */
    #define GBA_LCD_VRAM ((volatile uint16_t *)0x06000000)

//
void gba_lcd_driver_init(void);

// gba_lcd_vram_clear(): clear vram
void gba_lcd_vram_clear(uint16_t color);

// gba_lcd_vram_dpixel(): draw a pixel
void gba_lcd_vram_dpixel(uint16_t color, uint32_t x, uint32_t y);

// lcd_wait_vblank(): wait vblank
void gba_lcd_wait_vblank(void);
#endif
