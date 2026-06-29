class Conversion:
    def __init__(self, img, attributes, debug) -> None:
        self.img = img
        self.height = attributes[0]
        self.width = attributes[1]
        self.attributes = attributes
        self.is_debug = debug

    def get_content(self):
        content = "// Auto Generated font asset file - CARTRIDGE\n\n"
        content += "#include <stdint.h>\n"
        content += '#include "font.h"\n\n'

        content += "void init_font(gba_font_t *font, enum font_type type) {\n"
        content += "\tstatic const uint8_t font_bitmap_monospaced[] = {\n"

        for ascii in range(32, 128):
            pixels_bytes = self.get_pixels_bitmap_glyph(ascii)

            row_values = ", ".join(self.get_monospace_glyph(pixels_bytes, ascii))
            printable = (
                chr(ascii) if chr(ascii) not in ("\\", "'") else f"\\{chr(ascii)}"
            )
            content += f"\t\t{row_values}, // {ascii}: '{printable}'\n"

        content += "\t};\n\n"

        content += "\tstatic const glyph_t glyphs_monospaced[] = {\n\t\t{"
        content += f" .width = {self.width}, .height = {self.height} "
        content += "},\n\t\t{ .width = 0, .height = 0 }\n"
        content += "\t};\n\n"

        content += "\tstatic const uint8_t font_bitmap_proportional[] = {\n"
        for ascii in range(32, 128):
            pixels_bytes = self.get_pixels_bitmap_glyph(ascii)
            proporitonal_glyph = self.get_proportional_glyph(pixels_bytes)
            content += "\t\t"
            content += ", ".join(proporitonal_glyph)
            content += ",\n"
        content += "\t};\n\n"

        content += "\tstatic const glyph_t glyphs_proportional[] = {\n"
        for ascii in range(32, 128):
            pixels_bytes = self.get_pixels_bitmap_glyph(ascii)
            proporitonal_glyph = self.get_proportional_glyph(pixels_bytes)
            content += "\t\t{"
            content += f".height = {len(proporitonal_glyph)}, "
            content += f".width = {self.get_max_width_proportional(proporitonal_glyph)}, "
            content += "},\n"
        content += "\t};\n\n"

        content += "\tfont->type = type;\n"
        content += "\tif (font->type == MONOSPACED) {\n"
        content += "\t\tfont->monospaced.bitmap = font_bitmap_monospaced;\n"
        content += "\t\tfont->monospaced.glyphs = glyphs_monospaced;\n"
        content += "\t} else {\n"
        content += "\t\tfont->proportional.bitmap = font_bitmap_proportional;\n"
        content += "\t\tfont->proportional.glyphs = glyphs_proportional;\n"
        content += "\t}\n"
        content += "}\n"

        return content

    def get_glyph_list(self, pixel_bytes: bytes) -> list[str]:
        glyph_list: list[str] = []

        for y in range(self.height):
            row = str()
            for x in range(self.width):
                row += "1" if pixel_bytes[y * self.width + x] > 200 else "0"
            glyph_list.append(f"0x{(int(row, 2)):02X}")

        return glyph_list

    def get_monospace_glyph(self, pixel_bytes: bytes, ascii: int) -> list[str]:
        glyph_list: list[str] = self.get_glyph_list(pixel_bytes)

        if self.is_debug:
            print(f"{ascii}:")
            print(format("~" * 28))
            for glyph in glyph_list:
                bytes_glyph = bytes.fromhex(glyph[2:])
                row = "".join(f"{b:08b}" for b in bytes_glyph)
                print(
                    f"{''.join('#' if r == '1' else '-' for r in row)} -> {row} -> 0x{int(row, 2):02x}"
                )
            print(format("~" * 28) + "\n")

        return glyph_list

    def get_max_width_proportional(self, glyph_list: list[str]) -> int:
        min_x = None
        max_x = None
    
        for glyph in glyph_list:
            bytes_glyph = bytes.fromhex(glyph[2:])
            row = "".join(f"{b:08b}" for b in bytes_glyph)
            start_idx = row.find("1")
            end_idx = row.rfind("1")

            if start_idx != -1:
                min_x = start_idx if min_x is None else min(min_x, start_idx)
                current_max = end_idx + 1
                max_x = current_max if max_x is None else max(max_x, current_max)
    
        if min_x is None or max_x is None:
            return 3
        
        return max_x - min_x

    def get_proportional_glyph(self, pixel_bytes: bytes) -> list[str]:
        glyph_list: list[str] = self.get_glyph_list(pixel_bytes)
        min_x = None
        max_x = None
        idx = 0

        for glyph in glyph_list:
            bytes_glyph = bytes.fromhex(glyph[2:])
            glyph = "".join(f"{b:08b}" for b in bytes_glyph)
            start_idx = glyph.find("1")
            end_idx = glyph.rfind("1")
            if start_idx != -1:
                if min_x is None:
                    min_x = start_idx
                else:
                    min_x = min(min_x, start_idx)
                current_max = end_idx + 1
                if max_x is None:
                    max_x = current_max
                else:
                    max_x = max(max_x, current_max)
            idx += 1

        glyph_list = glyph_list[0:11]

        idx = 0
        for glyph in glyph_list:
            bytes_glyph = bytes.fromhex(glyph[2:])
            row = "".join(f"{b:08b}" for b in bytes_glyph)
            row = row[min_x:max_x]
            glyph_list[idx] = f"0x{(int(row, 2)):02X}"
            idx += 1

        return glyph_list

    def get_pixels_bitmap_glyph(self, ascii):
        index = ascii - 32
        top = index // 16 * (self.attributes[0] + self.attributes[2])
        left = index % 16 * (self.attributes[1] + self.attributes[3])
        glyph = self.img.crop(
            (left, top, left + self.attributes[1], top + self.attributes[0])
        )

        return glyph.tobytes()
