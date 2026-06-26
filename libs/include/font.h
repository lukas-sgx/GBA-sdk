#ifndef FONT_H
    #define FONT_H

    #include <stddef.h>
    #include <stdint.h>

enum font_type {
    MONOSPACED,
    PROPORTIONAL
};

typedef struct glyph_s {
    size_t width;
    size_t height;
} glyph_t;

typedef struct gba_font_packed_s {
    const uint8_t *bitmap;
    const glyph_t *glyphs;
} gba_font_packed_t;

typedef struct gba_font_s {
    enum font_type type;
    union {
        gba_font_packed_t monospaced;
        gba_font_packed_t proportional;
    };
} gba_font_t;

enum {
    /* Horizontal settings : default in dtext () is DTEXT_LEFT */
    DTEXT_VALIGN_LEFT,
    DTEXT_VALIGN_CENTER,
    DTEXT_VALIGN_RIGHT,
};

enum {
    /* Vertical settings : default in dtext () is DTEXT_TOP */
    DTEXT_HALIGN_TOP,
    DTEXT_HALIGN_MIDDLE,
    DTEXT_HALIGN_BOTTOM,
};

void dtext_opt(
    gba_font_t *font,
    int32_t x, int32_t y,
    uint16_t fg, uint16_t bg,
    uint8_t halign,
    uint8_t valign,
    char const *str
);

void dtext(gba_font_t *font, int32_t x, int32_t y, uint16_t fg, char const *text);

void dprint_opt(
    gba_font_t *font,
    int32_t x, int32_t y,
    uint16_t fg, uint16_t bg,
    uint8_t valign,
    char const *format,
    ...
);

void dprint(gba_font_t *font, int x, int y, int fg, char const *format, ...);

void dtext_size (
    gba_font_t *font,
    int32_t *width,
    int32_t *height,
    char const *str
);

void dprint_size(
    gba_font_t *font,
    int32_t *width,
    int32_t * height,
    char const *format,
    ...
);

void init_font(gba_font_t *font, enum font_type type);

#endif
