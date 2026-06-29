# TEXT RENDERING SUBSYSTEM (Mode 3)

Text rendering in Mode 3 relies on directly manipulating framebuffer pixels using bitmap font data (gba_font_t). Unlike tile-based text modes (Tiles/Backgrounds), these functions compute the position of each glyph pixel by pixel and dynamically apply alignment transformations at runtime.

### Dependent Types and Enums

```c
typedef struct {
uint8_t width;       /* Fixed or maximum width of a glyph in pixels /
uint8_t height;      / Font height in pixels */
uint8_t const data; / Pointer to character bitmap data */
} gba_font_t;

enum halign {
HALIGN_LEFT,   /* Align left on the X coordinate /
HALIGN_CENTER, / Center horizontally relative to X /
HALIGN_RIGHT   / Align right on the X coordinate */
};

enum valign {
VALIGN_TOP,    /* Align top of the glyph on the Y coordinate /
VALIGN_CENTER, / Center vertically relative to Y /
VALIGN_BOTTOM  / Align bottom of the glyph on the Y coordinate */
};
```

### API Reference

#### `dtext_opt`
Draws a static string with advanced alignment and background management options.

```c
void dtext_opt(
gba_font_t *font,
int32_t x, int32_t y,
uint16_t fg, int16_t bg,
enum halign halign,
enum valign valign,
char const *str
);
```
* **Description:** Computes the exact origin of the text based on the dimensions of the `str` string and the `halign` and `valign` enums, then draws the characters.
* **Background Management (`bg`):**
* If `bg >= 0`, the function draws a solid rectangle behind the text using the specified BGR555 color (opaque mode).
* If `bg < 0` (e.g., `-1`), the background is treated as transparent; only the foreground pixels (`fg`) are written to VRAM.
* **Safety:** The coordinates of every computed pixel undergo the same out-of-bounds verification as `dpixel` to prevent VRAM corruption.

#### `dtext`
Draws a static string using standard defaults (Simplified variant).

```c
void dtext(gba_font_t *font, int32_t x, int32_t y, uint16_t fg, char const *text);
```
* **Description:** Strict equivalent to the following call:
`dtext_opt(font, x, y, fg, -1, HALIGN_LEFT, VALIGN_TOP, text);`
* **Behavior:** The text is anchored top-left relative to the provided `(x, y)` coordinates and rendered with a transparent background.

#### `dprint_opt`
Draws a formatted string (`printf` style) with alignment and background options.

```c
void dprint_opt(
gba_font_t *font,
int32_t x, int32_t y,
uint16_t fg, int16_t bg,
enum halign halign,
enum valign valign,
char const *format,
...
);
```
* **Description:** Uses an internal buffer to format the string via variadic arguments (`...`). Once the final string is generated, it invokes the underlying rendering engine of `dtext_opt`.
* **Warning (GBA Resources):** This function includes the standard C library format parser. It consumes significantly more CPU cycles and stack memory than `dtext_opt`. It is highly recommended to limit its use within critical rendering loops (V-Blank).

#### `dprint`
Draws a standard formatted string (Simplified variant).

```c
void dprint(gba_font_t *font, int32_t x, int32_t y, int16_t fg, char const *format, ...);
```
* **Description:** A simplified version of `dprint_opt` utilizing a transparent background and default top-left alignment (`HALIGN_LEFT`, `VALIGN_TOP`).
* **Note on `fg` type:** Although declared as an `int16_t` in the signature for interface compatibility reasons, the parameter is treated internally as an opaque `uint16_t` color (BGR555).