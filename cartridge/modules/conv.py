import click
from PIL import Image

def monospace_glyph(height: int, width: int, pixel_bytes: bytes) -> list[str]:
    glyph_list: list[str] = []

    for y in range(height):
        row = str()
        for x in range(width):
            row += ('1' if pixel_bytes[y * width + x] > 200 else '0')
        glyph_list.append(hex(int(row, 2)))

    return glyph_list

def proportional_glyph(height: int, width: int, pixel_bytes: bytes) -> list[str]:
    glyph_list: list[str] = []

    for y in range(height):
        row = str()
        for x in range(width):
            row += ('1' if pixel_bytes[y * width + x] > 200 else '0')
        print(f"{''.join('#' if r == '1' else '-' for r in row)} -> {row} -> 0x{int(row, 2):02x}")
        glyph_list.append(f"0x{int(row, 2):02x}")

    return glyph_list

@click.command(help="Convert a font asset into a raw C file")
@click.option("-o", "--output", required=True, type=click.Path(exists=False), help="generated C file")
@click.option("-w", "--width", required=True, type=click.INT, help="width size of char in pixel")
@click.option("-h", "--height", required=True, type=click.INT, help="height size of char in pixel")
@click.option("-m", "--margin", required=True, type=click.INT, help="margin between of char in pixel")
@click.option("-l", "--line-height", required=True, type=click.INT, help="virtual alignement line height in pixel")
@click.argument("ASSET_PATH", required=True, type=click.STRING, nargs=1)
def conv(asset_path: str, output: str, width: int, height: int, margin: int, line_height: int) -> None:
    img = Image.open(asset_path, mode="r").convert("L")
    
    content = "// Auto Generated font asset file - CARTRIDGE\n\n"
    content += "#include <stdint.h>\n"
    content += "#include \"font.h\"\n\n"

    content += f"const int WIDTH = {width};\n"
    content += f"const int HEIGHT = {height};\n\n"

    content += "void init_font(gba_font_t *font, uint8_t type) {\n"
    content += "\tstatic const uint8_t font_bitmap[] = {\n"

    for ascii in range(32, 128):
        index = ascii - 32
        top = index // 16 * (height + line_height)
        left = index % 16 * (width + margin)

        glyph = img.crop((left, top, left + width, top + height))
        pixel_bytes = glyph.tobytes()

        monospace = monospace_glyph(height, width, pixel_bytes)

        print(f"{ascii}:")
        proportional = proportional_glyph(height, width, pixel_bytes)
        print(format("-" * 28)+"\n")
        
        row_values = ", ".join(monospace)
        printable = chr(ascii) if chr(ascii) not in ("\\", "'") else f"\\{chr(ascii)}"
        content += f"\t\t{row_values}, // {ascii}: '{printable}'\n"

    content += "\t};\n\n"
    
    content += "\tfont->type = type;\n"
    content += "\tfont->bitmap = font_bitmap;\n"
    content += "}\n"


    with open(output, mode="w") as file:
        file.write(content)