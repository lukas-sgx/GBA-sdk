#include "driver.h"
#include <stddef.h>

extern void main();

__attribute__((section(".text.kernel_init")))
void kernel_init(void)
{
    for (size_t i = 0; i < wired_driver_count(); i++) {
        wired_drv_t *driver = &__wired_drivers[i];
        if (driver->configure)
            driver->configure();
    }
    main();
    while (1);
}