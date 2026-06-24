class Convertion:
    def __init__(self, img, attributes, debug) -> None:
        self.img = img
        self.height = attributes[0]
        self.width = attributes[1]
        self.attributes = attributes
        self.is_debug = debug

    def get_content(self):
        content = "// Auto Generated font asset file - CARTRIDGE\n\n"
        content += "#include <stdint.h>\n"
        content += "#include \"font.h\"\n\n"
    
        content += "void init_font(gba_font_t *font, uint8_t type) {\n"
        content += "\tstatic const uint8_t font_bitmap[] = {\n"

        for ascii in range(32, 128):
            pixels_bytes = self.get_pixels_bitmap_glyph(ascii)
    
            (monospace, proportional) = self.get_fonts(pixels_bytes)
            
            row_values = ", ".join(monospace)
            printable = chr(ascii) if chr(ascii) not in ("\\", "'") else f"\\{chr(ascii)}"
            content += f"\t\t{row_values}, // {ascii}: '{printable}'\n"
            
        content += "\t};\n\n"
    
        content += f"\tglyph_t global = {{ .width = {self.width}, .height = {self.height} }};\n\n"
        
        content += "\tfont->type = type;\n"
        content += "\tfont->bitmap = font_bitmap;\n"
        content += "\tfont->global = &global;\n"
        content += "}\n"

        return content
            
    def monospace_glyph(self, pixel_bytes: bytes) -> list[str]:
        glyph_list: list[str] = []

        if self.is_debug:
            print(f"{ascii}:")
    
        for y in range(self.height):
            row = str()
            for x in range(self.width):
                row += ('1' if pixel_bytes[y * self.width + x] > 200 else '0')
            if self.is_debug:
                print(f"{''.join('#' if r == '1' else '-' for r in row)} -> {row} -> 0x{int(row, 2):02x}")
            glyph_list.append(hex(int(row, 2)))
        if self.is_debug:
            print(format("-" * 28)+"\n")
    
        return glyph_list
    
    def proportional_glyph(self, pixel_bytes: bytes):
        pass
    
    def get_pixels_bitmap_glyph(self, ascii):
        index = ascii - 32
        top = index // 16 * (self.attributes[0] + self.attributes[2])
        left = index % 16 * (self.attributes[1] + self.attributes[3])
        glyph = self.img.crop((left, top, left + self.attributes[1], top + self.attributes[0]))
    
        return glyph.tobytes()
    
    def get_fonts(self, pixel_bytes):
        monospace = self.monospace_glyph(pixel_bytes)
        proportional = self.proportional_glyph(pixel_bytes)
    
        return (monospace, proportional)
