#include "graphical.h"

extern void main();

__attribute__((section(".text.kernel_init")))
void kernel_init(void)
{
    dinit();
    main();
    while (1);
}