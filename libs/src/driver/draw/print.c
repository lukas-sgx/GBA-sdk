#include "font.h"
#include <stdarg.h>
#include <stdio.h>

void dprint_opt(gba_font_t *font, int32_t x, int32_t y,
    uint16_t fg, int16_t bg, enum halign halign,
    enum valign valign, char const *format, ...)
{
    char buffer[64];
    va_list args;

    va_start(args, format);
    vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    dtext_opt(font, x, y, fg, bg, halign, valign, buffer);
}

void dprint(gba_font_t *font, int32_t x, int32_t y,
    int16_t fg, char const *format, ...)
{
    char buffer[64];
    va_list args;

    va_start(args, format);
    vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    dtext(font, x, y, fg, buffer);
}
