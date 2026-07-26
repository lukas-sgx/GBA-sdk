#include "driver.h"
#include <stddef.h>

extern void main(void);

__attribute__((section(".text.kernel_init")))
void kernel_init(void)
{
    wired_drv_t *driver = NULL;

    for (size_t i = 0; i < wired_driver_count(); i++) {
        driver = &__wired_drivers[i];
        if (driver->configure)
            driver->configure();
    }

    main();

    while (1);
}