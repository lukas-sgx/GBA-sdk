/* custom linker script in order to generate a GameBoyAdvance binary */
OUTPUT_FORMAT("elf32-littlearm", "elf32-bigarm", "elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(kernel_init)
/* address only the cartridge memory area
* @notes:
* - skip the cartridge header
* - other memory area will be cover soon .. */
MEMORY {
    game_pack(rx): ORIGIN = 0x080000c0, LENGTH = 32M
}
/* aggressively keep code binary and force it to be located at the start of the ROM */
SECTIONS {
    __rom_start = ORIGIN(game_pack);
    .text : {
        __code_start = .;
        *(.text.kernel_init)
		*(.text*)
		__code_end = .;
		__const_start = .;
        *(.rodata*)

        . = ALIGN(4);
        __wired_drivers = .;
        KEEP(*(SORT(.wired.drivers.*)))
        __wired_drivers_end = .;

        __const_end = .;
    } > game_pack

    PROVIDE(end = .); /* define end address if not define */
    __rom_end = .;
}
