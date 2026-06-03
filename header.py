import click

BYTE_LEN = 4
LOGO_BYTE_LEN = 156
GAME_TITLE_BYTE_LEN = 12

class Header:
    def __init__(self, gba_file: str) -> None:
        self.gba_file = gba_file
        self.raw: bytes
        self.address = []
        self.pc = 0

        with open(gba_file, "rb") as fd:    
            self.raw = fd.read()
            self.stock_address()

    def debug(self):
        for addr in self.address:
            click.echo(f"{addr:08x}")
    
    def stock_address(self):
        for i in range(0, len(self.raw), 4):
            chunk = self.raw[i : i + 4]
            if len(chunk) == 4:
                self.address.append(int.from_bytes(chunk, "little"))

    def get_opcode_branch(self, addr) -> str:
        family = (addr >> 25) & 0x7
        instruction = ""

        if family == 0b101:
            instruction = "b"
        offset = addr & 0xFFFFFF
        if offset & 0x8000000:
            offset |= 0xFF0000000
        target = self.pc + (BYTE_LEN * 2) + (offset << 2)
        return f"{instruction} 0x{target:02x}"
    
    def is_valid_entry(self, addr) -> bool:
        cond = (addr >> 28) & 0xF
        family = (addr >> 25) & 0x7
        return cond == 0xE and family == 0b101

    def is_valid_nintendo_logo(self, addresses: list[int]) -> bool:
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
        for hexAddr in addresses:
            raw_bytes += hexAddr.to_bytes(4, byteorder="little") # todo: verif bit 2, 7 on 0x21h if debugging or not -> https://mgba-emu.github.io/gbatek/#gbacartridgeheader

        return raw_bytes == NINTENDO_LOGO

    def is_debugging(self, addr: int) -> bool:
        address = list(addr.to_bytes(4))
        return (address[3] & 0b00100001) == 0b00100001

    def get_game_title(self, addresses: list[int]) -> str:
        listByte = b""
        for addr in addresses:
            listByte += addr.to_bytes(4, byteorder="little")
        result: str = str(listByte.decode(encoding="UTF-8"))
        return result
    
    def get_code(self, addr: int) -> str:
        code = addr.to_bytes(4, byteorder="little")
        return str(code.decode(encoding="UTF-8"))

    def get_date(self, addr: int) -> str:
        code = self.get_code(addr)
        if code[0] == "A":
            return "2001..2003 (old)"
        if code[0] == "B":
            return "2003.. (new)"
        return ""

    def get_language(self, addr: int) -> str:
        code = self.get_code(addr)
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

    def get_marker_id(self, addr: int) -> str:
        hexa = hex(addr)[4:]
        n1 = hexa[2:]
        ascii1 = chr((int(n1[0]) ** 1) * 16 + (int(n1[1]) * 16 ** 0))
        n2 = hexa[:2]
        ascii2 = chr((int(n2[0]) ** 1) * 16 + (int(n2[1]) * 16 ** 0))
        return f"{ascii1}{ascii2}"

    def get_developer(self, addr: int) -> str:
        if self.get_marker_id(addr) == "01":
            return "Nintendo"
        return ""

    def get_valid_fixed(self, addr: int) -> str:
        return hex(addr)[2:4]

    def is_valid_fixed(self, addr: int) -> str:
        if self.get_valid_fixed(addr) == "96":
            return "valid"
        return "unvalid"

    def get_unit_code(self, addr: int) -> str:
        return "0" + hex(addr)[2:4]


    def display_header(self):
        is_valid_entry = self.is_valid_entry(self.address[self.pc])
        raw_entry = self.address[self.pc]
        op_code_entry = self.get_opcode_branch(self.address[self.pc])
        self.pc += int(BYTE_LEN / BYTE_LEN)
        is_valid_nintendo_logo = self.is_valid_nintendo_logo(self.address[self.pc:self.pc + int(LOGO_BYTE_LEN / BYTE_LEN)])
        self.pc += int(LOGO_BYTE_LEN / BYTE_LEN)
        is_debuging = self.is_debugging(self.address[self.pc - 1])
        title_game = self.get_game_title(self.address[self.pc:self.pc + 3])
        self.pc += int(GAME_TITLE_BYTE_LEN / BYTE_LEN)
        game_code = self.get_code(self.address[self.pc])
        game_release = self.get_date(self.address[self.pc])
        game_language = self.get_language(self.address[self.pc])
        self.pc += int(BYTE_LEN / BYTE_LEN)
        marker_id = self.get_marker_id(self.address[self.pc])
        developer = self.get_developer(self.address[self.pc])
        is_valid_fixed = self.is_valid_fixed(self.address[self.pc])
        valid_fixed = self.get_valid_fixed(self.address[self.pc])
        self.pc += int(BYTE_LEN / BYTE_LEN)
        unit_code = self.get_unit_code(self.address[self.pc])
        
        click.echo(self.gba_file + ":")
        click.echo("|-- entry")
        click.echo(f"|   |-- valid: {is_valid_entry}")
        click.echo(f"|   |-- raw: 0x{raw_entry:08x}")
        click.echo(f"|   `-- opcode: {op_code_entry}")
        click.echo("|-- nintendo logo:")
        click.echo(f"|   |-- status: {is_valid_nintendo_logo}")
        click.echo(f"|   `-- debugging: {is_debuging}")
        click.echo(f"|-- game title: {title_game}")
        click.echo("|-- game code:")
        click.echo(f"|   |-- code: {game_code}")
        click.echo(f"|   |-- date: {game_release}")
        click.echo(f"|   `-- language: {game_language}")
        click.echo("|-- marker code:")
        click.echo(f"|   |-- id: {marker_id}")
        click.echo(f"|   `-- developer: {developer}")
        click.echo(f"|-- fixed value: {is_valid_fixed} ({valid_fixed}h)")
        click.echo(f"|-- unit code: {unit_code}h")
