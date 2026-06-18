#include <stdint.h>

extern void dinit(void);
extern void dclear(uint16_t color);

extern void main(void)
{
    dinit();
    while (1) {
        dclear(31);
        dclear(28);
        dclear(20);
    }
}