.text
.global _bootstrap
.arm // force use of arm mode 32bits

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
    bl setup_stack
    bl main
    b security_running

disable_irq:
    mov r0, #0
    ldr r1, =IME // load register IME on r1
    strh r0, [r1] // set r0 content in r1 in 16 bits
    bx lr // branch exchange: link register -> ret in asm x64

setup_stack:
    ldr sp, =USER_STACK
    bx lr

security_running:
    b security_running

// ---
// Data area
// ---
.balign 4

.equ IME, 0x04000208 // define IME register address
.equ USER_STACK, 0x03007F00