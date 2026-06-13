.text
.global _bootstrap
.arm

// Bootstrap code,
// @notes
// - do not try this code on real hardware unless you want to destroy your
// batteries ' life ...
// - this code is located right after the CARTRIDGE header
// - no interruption handler setup ... So, aggressively mask all possible
// interrupt to avoid hardware crash
// - no stack setup, be careful

_bootstrap:
    bl disable_irq

disable_irq:
    mov r0, #0 // 
    ldr r1, =IME
    strh r0, [r1]
    bx lr


// ---
// Data area
// ---
.balign 4

.equ IME, 0x04000208 // define IME register address