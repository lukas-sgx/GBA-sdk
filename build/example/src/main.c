#include <stdint.h>

extern void dinit(void);
extern void dclear(uint16_t color);

extern void main(void)
{
    dinit();
    dclear(31);
}