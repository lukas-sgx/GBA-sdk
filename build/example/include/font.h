#ifndef FONT_H
    #define FONT_H

    #include <stddef.h>
    #include <stdint.h>

typedef struct glyph_s {
    size_t width;
    size_t height;
} glyph_t;

typedef struct gba_font_packed_s {
    const uint8_t *bitmap;
    const glyph_t *glyphs;
} gba_font_packed_t;

typedef struct gba_font_s {
    uint8_t type;
    union {
        gba_font_packed_t monospaced;
        gba_font_packed_t proportional;
    };
} gba_font_t;

void init_font(gba_font_t *font, uint8_t type);

#endif
