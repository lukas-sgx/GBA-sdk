#include "lcd.h"
#include "font.h"
#include "color.h"
#include <stdint.h>

extern uint8_t __rom_start;
extern uint8_t __rom_end;
extern uint8_t __rom_start;
extern uint8_t __code_start;
extern uint8_t __code_end;
extern uint8_t __const_start;
extern uint8_t __const_end;

uint32_t get_stack(void)
{
    uint32_t stack_ptr = 0;

    __asm__ volatile ("mov %0, sp" : "=r" (stack_ptr));
   return stack_ptr;
}

uint32_t get_cpsr(void)
{
    uint32_t cpsr = 0;

    __asm__ volatile ("mrs %0, cpsr" : "=r" (cpsr));
   return cpsr;
}

uint32_t get_ime(void)
{
    return *(volatile uint16_t*)0x4000208;
}

extern void main(void)
{
    gba_font_t font = {0};
    uint32_t rom_size = (uint32_t)&__rom_end - (uint32_t)&__rom_start;
    uint32_t code_size = (uint32_t)&__code_end - (uint32_t)&__code_start;
    uint32_t const_size = (uint32_t)&__const_end - (uint32_t)&__const_start;
    uint32_t stack_addr = get_stack();
    uint32_t cpsr = get_cpsr();
    uint32_t ime = get_ime();

    init_font(&font, PROPORTIONAL);
    
    gba_lcd_wait_vblank();
    gba_lcd_vram_clear(0xDE7B);
    dtext_opt(&font, 240 / 2, 12, 0x7FFF, C_NONE, DTEXT_HALIGN_MIDDLE, DTEXT_VALIGN_CENTER, "Welcolme !");
    dprint(&font, 10, 20, C_BLACK, "ROM: %do", rom_size);
    dprint(&font, 10, 32, C_BLACK, "Code: %do", code_size);
    dprint(&font, 10, 44, C_BLACK, "read-only data: %do", const_size);
    dprint(&font, 10, 56, C_BLACK, "stack: %p", stack_addr);
    dprint(&font, 10, 68, C_BLACK, "CPSR: %08x", cpsr);
    dprint(&font, 10, 80, C_BLACK, "IME: %08x", ime);
}