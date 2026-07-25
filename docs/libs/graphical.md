# GBA SDK - LCD DRIVER ARCHITECTURE & IMPLEMENTATION

This technical document serves as both the API specification and implementation
reference for the low-level Mode 3 LCD driver included in `cartridge-sdk`, and
for the `wired_drivers` mechanism used to register and initialize it.

--------------------------------------------------------------------------------
 1. HARDWARE LAYER & MEMORY MAP
--------------------------------------------------------------------------------

The driver directly manipulates the GameBoy Advance display architecture by
targeting Video Mode 3 (a single 16-bit high-color bitmap frame buffer).

```text
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
```

--------------------------------------------------------------------------------
 2. DRIVER REGISTRATION: THE `wired_drivers` MECHANISM
--------------------------------------------------------------------------------

Drivers are not called directly from `main()`. Instead, they self-register at
compile time into a linker-managed array, and are configured automatically by
`kernel_init()` before the program's entry point runs.

### 2.1 The driver structure (`driver.h`)

```c
typedef struct {
    /* Driver name */
    char const *name;
    /* Initialize the hardware for the driver. Usually installs
       interrupt handlers and configures registers. May be NULL. */
    void (*configure)(void);
} wired_drv_t;
```

### 2.2 Declaring a driver

```c
#define WIRED_DECLARE_DRIVER(level, name, ...) \
    __attribute__((used, section(".wired.drivers." #level))) \
    static const wired_drv_t __wired_drv_##name = { __VA_ARGS__ }
```

Each call to `WIRED_DECLARE_DRIVER` places a `wired_drv_t` instance into a
dedicated linker section named `.wired.drivers.<level>`. The `level` argument
sets the priority: lower numbers are initialized first. Because section names
are sorted lexicographically by the linker, `level` must be written as a
zero-padded literal (`01`, `02`, ... `10`) so that numeric and alphabetic
ordering agree.

`used` prevents the compiler from discarding the (seemingly unreferenced)
static object before the linker has a chance to collect it.

### 2.3 Linker script contribution

The linker script is responsible for creating the symbols consumed by
`driver.h`, since no `.c` file defines them:

```ld
. = ALIGN(4);
__wired_drivers = .;
KEEP(*(SORT(.wired.drivers.*)))
__wired_drivers_end = .;
```

* `SORT(.wired.drivers.*)` collects every driver section and orders them by
  priority level.
* `KEEP(...)` prevents the linker's garbage collector from dropping the
  section, since it is only ever referenced indirectly through the bounding
  symbols below.
* `__wired_drivers` / `__wired_drivers_end` mark the start and end of the
  resulting array in ROM.

### 2.4 Runtime access (`driver.h`)

```c
/* Drivers in order of increasing priority level, provided by linker script */
extern wired_drv_t __wired_drivers[];
/* End of array; see also wired_driver_count() */
extern wired_drv_t __wired_drivers_end[];

/* Number of drivers in the (wired_drivers) array */
#define wired_driver_count() \
    ((wired_drv_t *)&__wired_drivers_end - (wired_drv_t *)&__wired_drivers)
```

### 2.5 Startup sequence (`kernel_init.c`)

```c
extern void main();

__attribute__((section(".text.kernel_init")))
void kernel_init(void)
{
    for (int i = 0; i < wired_driver_count(); i++) {
        wired_drv_t *driver = &__wired_drivers[i];
        if (driver->configure)
            driver->configure();
    }
    main();
    while (1);
}
```

`kernel_init` is the ROM entry point (see `ENTRY(kernel_init)` in the linker
script). It walks the wired drivers array in priority order, calling
`configure()` on each entry that provides one, then hands control to `main()`.

--------------------------------------------------------------------------------
 3. SOURCE CODE REFERENCE (`gba_lcd.c`)
--------------------------------------------------------------------------------

Below is the concrete implementation used to drive the LCD in Mode 3.

```c
#include "lcd.h"
#include "driver.h"
#include <stdint.h>

/**
 * @brief Initializes the GBA display subsystem.
 * Confirms Video Mode 3 operation and activates background layer 2.
 */
void gba_lcd_driver_init(void)
{
    GBA_LCD.DISPCNT.BG2 = 1;
    GBA_LCD.DISPCNT.BG_MODE = 3;
}

/**
 * @brief Plots a color pixel onto explicit screen coordinates.
 * Includes security checks to avoid VRAM pointer overflows.
 */
void gba_lcd_vram_dpixel(uint16_t color, uint32_t x, uint32_t y)
{
    /* Safety check against hardware out-of-bounds corruption */
    if (x >= 240 || y >= 160)
        return;
    /* Matrix conversion: Base + (Y * Width + X) */
    (GBA_LCD_VRAM)[y * 240 + x] = color;
}

/**
 * @brief Floods the active frame buffer with a single uniform color.
 * Effectively cleans or refreshes the viewport interface.
 * Writes are done 32 bits at a time (two pixels per iteration) for speed.
 */
void gba_lcd_vram_clear(uint16_t color)
{
    uint32_t color32 = color << 16 | color;
    volatile uint32_t *vram32 = (volatile uint32_t *)GBA_LCD_VRAM;

    for (int32_t i = 0; i < 240 * 160 / 2; i++)
        (vram32)[i] = color32;
}

/**
 * @brief Blocks until a full vertical blank cycle has occurred.
 * Used to synchronize VRAM writes with the display refresh.
 */
void gba_lcd_wait_vblank(void)
{
    while (GBA_LCD.DISPSTAT.VBF & 1);
    while (!(GBA_LCD.DISPSTAT.VBF & 1));
}

WIRED_DECLARE_DRIVER(01, gba_lcd, .name = " LCD ",
    .configure = &gba_lcd_driver_init,
);
```

--------------------------------------------------------------------------------
 4. API SUMMARY
--------------------------------------------------------------------------------

| Function                 | Description                                             |
|---------------------------|----------------------------------------------------------|
| `gba_lcd_driver_init`     | Configures Mode 3 + BG2. Registered via `wired_drivers`, called automatically by `kernel_init`. Not meant to be called manually. |
| `gba_lcd_vram_dpixel`     | Writes a single BGR555 pixel at `(x, y)`, bounds-checked. |
| `gba_lcd_vram_clear`      | Fills the entire frame buffer with one color.             |
| `gba_lcd_wait_vblank`     | Busy-waits for the next VBlank window, for tear-free VRAM updates. |

--------------------------------------------------------------------------------
 5. NOTES
--------------------------------------------------------------------------------

* `gba_lcd_driver_init` must never be called directly from application code:
  it is invoked once by `kernel_init`, before `main()`, as part of the wired
  drivers initialization loop.
* VRAM writes outside of VBlank are visible but may produce tearing on real
  hardware; use `gba_lcd_wait_vblank()` before bulk updates when visual
  consistency matters.
* Driver priority level `01` was chosen for `gba_lcd` since no other
  currently declared driver depends on it; drivers depending on LCD being
  configured first must use a strictly higher level.