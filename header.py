import click

BYTE_LEN = 4

# def debug(raw):
#     address = get_address(raw)
#     for add in address:
#         click.echo(f"{add:08x}")

def get_address(raw) -> list[int]:
    address = []
    for i in range(0, len(raw), 4):
        chunk = raw[i : i + 4]
        if len(chunk) == 4:
            address.append(int.from_bytes(chunk, "little"))
    return address


def get_opcode(entry, PC) -> str:
    family = (entry >> 25) & 0x7
    instruction = str()
    if family == 0b101:
        instruction = "b"
    offset = entry & 0xFFFFFF
    if offset & 0x8000000:
        offset |= 0xFF0000000
    target = PC + 8 + (offset << 2)
    return f"{instruction} 0x{target:02x}"


def is_valid_entry(entry) -> bool:
    cond = (entry >> 28) & 0xF
    family = (entry >> 25) & 0x7
    return cond == 0xE and family == 0b101

def is_valid_nintendo_logo(entry: list[int]) -> bool:
    NINTENDO_LOGO = bytes([
        0x24, 0xFF, 0xAE, 0x51, 0x69, 0x9A, 0xA2, 0x21,
        0x3D, 0x84, 0x82, 0x0A, 0x84, 0xE4, 0x09, 0xAD,
        0x11, 0x24, 0x8B, 0x98, 0xC0, 0x81, 0x7F, 0x21,
        0xA3, 0x52, 0xBE, 0x19, 0x93, 0x09, 0xCE, 0x20,
        0x10, 0x46, 0x4A, 0x4A, 0xF8, 0x27, 0x31, 0xEC,
        0x58, 0xC7, 0xE8, 0x33, 0x82, 0xE3, 0xCE, 0xBF,
        0x85, 0xF4, 0xDF, 0x94, 0xCE, 0x4B, 0x09, 0xC1,
        0x94, 0x56, 0x8A, 0xC0, 0x13, 0x72, 0xA7, 0xFC,
        0x9F, 0x84, 0x4D, 0x73, 0xA3, 0xCA, 0x9A, 0x61,
        0x58, 0x97, 0xA3, 0x27, 0xFC, 0x03, 0x98, 0x76,
        0x23, 0x1D, 0xC7, 0x61, 0x03, 0x04, 0xAE, 0x56,
        0xBF, 0x38, 0x84, 0x00, 0x40, 0xA7, 0x0E, 0xFD,
        0xFF, 0x52, 0xFE, 0x03, 0x6F, 0x95, 0x30, 0xF1,
        0x97, 0xFB, 0xC0, 0x85, 0x60, 0xD6, 0x80, 0x25,
        0xA9, 0x63, 0xBE, 0x03, 0x01, 0x4E, 0x38, 0xE2,
        0xF9, 0xA2, 0x34, 0xFF, 0xBB, 0x3E, 0x03, 0x44,
        0x78, 0x00, 0x90, 0xCB, 0x88, 0x11, 0x3A, 0x94,
        0x65, 0xC0, 0x7C, 0x63, 0x87, 0xF0, 0x3C, 0xAF,
        0xD6, 0x25, 0xE4, 0x8B, 0x38, 0x0A, 0xAC, 0x72,
        0x21, 0xD4, 0xF8, 0x07,
    ])
    raw_bytes = b''
    for hex in entry:
        raw_bytes += hex.to_bytes(4, byteorder="little") # todo: verif bit 2, 7 on 0x21h if debugging or not -> https://mgba-emu.github.io/gbatek/#gbacartridgeheader

    return raw_bytes == NINTENDO_LOGO

def is_debugging(entry: int) -> bool:
    address = list(entry.to_bytes(4))
    is_debug = (address[3] & 0b00100001) == 0b00100001
    
    return is_debug

def get_game_title(entry: list[int]) -> str:
    listByte = b""
    for addr in entry:
        listByte += addr.to_bytes(4, byteorder="little")
    result: str = str(listByte.decode(encoding="UTF-8"))
    return result

def get_code(entry: int) -> str:
    code = entry.to_bytes(4, byteorder="little")
    return str(code.decode(encoding="UTF-8"))

def get_date(entry: int) -> str:
    code = get_code(entry)
    if code[0] == "A":
        return "2001..2003 (old)"
    if code[0] == "B":
        return "2003.. (new)"
    return ""

def get_language(entry: int) -> str:
    code = get_code(entry)
    if code[3] == "E":
        return "USA/English"
    if code[3] == "J":
        return "Japan"
    if code[3] == "P":
        return "Europe/Elsewhere"
    if code[3] == "D":
        return "German"
    if code[3] == "F":
        return "French"
    if code[3] == "I":
        return "Italian"
    if code[3] == "S":
        return "Spanish"
    return ""

def get_marker_id(entry: int) -> str:
    hexa = hex(entry)[4:]
    n1 = hexa[2:]
    ascii1 = chr((int(n1[0]) ** 1) * 16 + (int(n1[1]) * 16 ** 0))
    n2 = hexa[:2]
    ascii2 = chr((int(n2[0]) ** 1) * 16 + (int(n2[1]) * 16 ** 0))
    return f"{ascii1}{ascii2}"

def get_developer(entry: int) -> str:
    if get_marker_id(entry) == "01":
        return "Nintendo"
    return ""

def get_valid_fixed(entry: int) -> str:
    hexa = hex(entry)[2:4]
    return hexa

def is_valid_fixed(entry: int) -> str:
    if get_valid_fixed(entry) == "96":
        return "valid"
    return "unvalid"

def get_unit_code(entry: int) -> str:
    return "0"+hex(entry)[2:4]

def check_header(gba_file):
    with open(gba_file, "rb") as fd:
        click.echo(f"{gba_file}:")

        raw = fd.read()
        addresses = get_address(raw)
        pc: int = 0
        click.echo("|-- entry")
        click.echo(f"|   |-- valid: {is_valid_entry(addresses[pc])}")
        click.echo(f"|   |-- raw: 0x{addresses[pc]:08x}")
        click.echo(f"|   `-- opcode: {get_opcode(addresses[pc], pc)}")
        pc += int(BYTE_LEN / BYTE_LEN)
        click.echo("|-- nintendo logo:")
        click.echo(f"|   |-- status: {is_valid_nintendo_logo(addresses[pc:pc + int(156 / BYTE_LEN)])}")
        pc += int(156 / BYTE_LEN)
        click.echo(f"|   `-- debugging: {is_debugging(addresses[pc - 1])}")
        click.echo(f"|-- game title: {get_game_title(addresses[pc:pc + 3])}")
        pc += int(12 / BYTE_LEN)
        click.echo("|-- game code:")
        click.echo(f"|   |-- code: {get_code(addresses[pc])}")
        click.echo(f"|   |-- date: {get_date(addresses[pc])}")
        click.echo(f"|   `-- language: {get_language(addresses[pc])}")
        pc += int(BYTE_LEN / BYTE_LEN)
        click.echo("|-- marker code:")
        click.echo(f"|   |-- id: {get_marker_id(addresses[pc])}")
        click.echo(f"|   `-- developer: {get_developer(addresses[pc])}")
        click.echo(f"|-- fixed value: {is_valid_fixed(addresses[pc])} ({get_valid_fixed(addresses[pc])}h)")
        pc += int(BYTE_LEN / BYTE_LEN)
        click.echo(f"|-- unit code: {get_unit_code(addresses[pc])}h")
        # click.echo(f"|-- device type: {}h")