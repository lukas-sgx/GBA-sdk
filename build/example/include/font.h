#ifndef FONT_H
    #define FONT_H

    #include <stddef.h>
    #include <stdint.h>

typedef struct glyph_s {
    size_t width;
    size_t height;
} glyph_t;

typedef struct gba_font_s {
    uint8_t type;
    const glyph_t *glyphs;
    const glyph_t *global;
    const uint8_t *bitmap;
} gba_font_t;

void init_font(gba_font_t *font, uint8_t type);

#endif
