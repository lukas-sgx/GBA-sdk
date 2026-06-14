/* custom linker script in order to generate a GameBoyAdvance binary */
OUTPUT_FORMAT("elf32-littlearm", "elf32-bigarm", "elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(_bootstrap)
/* address only the cartridge memory area
* @notes:
* - skip the cartridge header
* - other memory area will be cover soon .. */
MEMORY {
    game_pack(rx): ORIGIN = 0x080000c0, LENGTH = 32M
}
/* aggressively keep code binary and force it to be located at the start of the ROM */
SECTIONS {
    .text : {
        KEEP (*(.text));
    } > game_pack
}
