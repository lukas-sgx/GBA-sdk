#include "graphical.h"
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

extern void main(uint32_t CPSR, uint32_t IME)
{
    gba_font_t font = {0};
    uint32_t rom_size = 0;
    uint32_t code_size = 0;
    uint32_t const_size = 0;
    uint32_t stack_addr = 0;
    uint32_t cpsr = 0;
    uint32_t ime = 0;
    
    rom_size = (uint32_t)&__rom_end - (uint32_t)&__rom_start;
    code_size = (uint32_t)&__code_end - (uint32_t)&__code_start;
    const_size = (uint32_t)&__const_end - (uint32_t)&__const_start;
    stack_addr = get_stack();
    dinit();
    init_font(&font, PROPORTIONAL);
    wait_vblank();
    dclear(0xDE7B);
    dtext_opt(&font, 240 / 2, 12, 0x7FFF, C_NONE, DTEXT_HALIGN_MIDDLE, DTEXT_VALIGN_CENTER, "Welcolme !");
    dprint(&font, 10, 20, C_BLACK, "ROM: %do", rom_size);
    dprint(&font, 10, 32, C_BLACK, "Code: %do", code_size);
    dprint(&font, 10, 44, C_BLACK, "read-only data: %do", const_size);
    dprint(&font, 10, 56, C_BLACK, "stack: %p", stack_addr);
    dprint(&font, 10, 68, C_BLACK, "CPSR: %08x", CPSR);
    dprint(&font, 10, 80, C_BLACK, "IME: %08x", IME);
}