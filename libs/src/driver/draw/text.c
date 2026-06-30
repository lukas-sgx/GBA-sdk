#include "font.h"
#include "color.h"
#include "graphical.h"
#include <stddef.h>
#include <stdint.h>

const uint8_t *extract_pointer_monospaced(gba_font_t *font, uint8_t ascii)
{
    return &(font->monospaced.bitmap[ascii * 12]);
}

const uint8_t *extract_pointer_proportional(gba_font_t *font, uint8_t ascii)
{
    size_t offset = 0;

    for (uint8_t i = 0; i < ascii; i++)
        offset += font->proportional.glyphs[i].height;
    return &(font->proportional.bitmap[offset]);
}

const uint8_t *char_to_pointer(gba_font_t *font, char ch)
{
    uint8_t ascii = ch - ' ';

    if (ch < ' ' || ch > '~') {
        ch = ' ';
        ascii = ch - ' ';
    }
    if (font->type == MONOSPACED)
        return extract_pointer_monospaced(font, ascii);
    else
        return extract_pointer_proportional(font, ascii);
}

static glyph_t char_glyph(gba_font_t *font, char ch)
{
    uint8_t ascii = ch - ' ';

    if (ch < ' ' || ch > '~') {
        ch = ' ';
        ascii = ch - ' ';
    } 
    if (font->type == MONOSPACED)
        return font->monospaced.glyphs[0];
    else
        return font->proportional.glyphs[ascii];
}

void draw_char(const uint8_t *bitmap, glyph_t dimension, int32_t x, int32_t y,
               uint16_t fg, int16_t bg, int32_t letter_spacing)
{
    uint8_t byte = 0;
    int32_t bit = 0x0;
    int32_t total_width = dimension.width + letter_spacing;

    for (uint8_t row = 0; row < FONT_MAX_HEIGHT; row++) {
        if (row < dimension.height)
            byte = bitmap[row];
        else
            byte = 0;
        for (int32_t col = 0; col < total_width; col++) {
            if (col < dimension.width)
                bit = (byte >> (dimension.width - 1 - col)) & 1;
            else
                bit = 0;
            if (!bit && bg == C_NONE)
                continue;
            else
                dpixel(x + col, y + row, bit ? fg : bg);
        }
    }
}

int32_t get_total_width(gba_font_t *font, const char *str)
{
    glyph_t dimension = {0};
    int32_t total_width = 0;
    
    for (size_t i = 0; str[i] != '\0'; i++) {
        dimension = char_glyph(font, str[i]);
        total_width += dimension.width;
        if (str[i + 1] != '\0') {
            if (font->type == MONOSPACED)
                total_width += LETTER_SPACING_MONOSPACED;
            else
                total_width += LETTER_SPACING_PROPORTIONAL;
        }
    }
    return total_width;
}

int32_t get_valign(enum valign valign, int32_t x, int32_t total_width)
{
    int32_t cursor_x = 0;

    switch (valign) {
        case DTEXT_VALIGN_CENTER:
            cursor_x = x - total_width / 2;
            break;
        case DTEXT_VALIGN_RIGHT:
            cursor_x = x + total_width;
            break;
        case DTEXT_VALIGN_LEFT:
        default:
            cursor_x = x;
            break;
    }
    return cursor_x;
}

int32_t get_halign(enum halign halign, int32_t y)
{
    int32_t cursor_y = 0;

    switch (halign) {
        case DTEXT_HALIGN_MIDDLE:
            cursor_y = y - FONT_MAX_HEIGHT / 2;
            break;
        case DTEXT_HALIGN_BOTTOM:
            cursor_y = y + FONT_MAX_HEIGHT;
            break;
        case DTEXT_HALIGN_TOP:
        default:
            cursor_y = y;
            break;
    }
    return cursor_y;
}

void dtext_opt(gba_font_t *font, int32_t x, int32_t y, uint16_t fg, int16_t bg,
    enum halign halign, enum valign valign, char const *str)
{
    glyph_t dimension = {0};
    int32_t cursor_x = 0;
    int32_t cursor_y = 0;
    int32_t spacing = 0;
    int32_t total_width = get_total_width(font, str);

    cursor_x = get_valign(valign, x, total_width);
    cursor_y = get_halign(halign, y);
    
    for (size_t i = 0; str[i] != '\0'; i++) {
        dimension = char_glyph(font, str[i]);
        if (font->type == MONOSPACED)
            spacing = (str[i + 1] != '\0') ? LETTER_SPACING_MONOSPACED : 0;
        else
            spacing = (str[i + 1] != '\0') ? LETTER_SPACING_PROPORTIONAL : 0;
        draw_char(char_to_pointer(font, str[i]), dimension, cursor_x, cursor_y, fg, bg, spacing);
        cursor_x += dimension.width + spacing;
    }
}

void dtext(gba_font_t *font, int32_t x, int32_t y, uint16_t fg, char const *text)
{
    dtext_opt(font, x, y, fg, C_NONE, DTEXT_HALIGN_TOP, DTEXT_VALIGN_LEFT, text);
}