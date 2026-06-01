import click


def get_address(raw):
    address = []
    for i in range(0, len(raw), 4):
        chunk = raw[i : i + 4]
        if len(chunk) == 4:
            address.append(int.from_bytes(chunk, "little"))
    return address


def get_opcode(entry, PC):
    family = (entry >> 25) & 0x7
    instruction = str()
    if family == 0b101:
        instruction = "b"
    offset = entry & 0xFFFFFF
    if offset & 0x8000000:
        offset |= 0xFF0000000
    target = PC + 8 + (offset << 2)
    return f"{instruction} 0x{target:02x}"

def debug(raw):
    address = get_address(raw)
    for add in address:
        click.echo(f"{add:08x}")


def is_valid_entry(entry):
    cond = (entry >> 28) & 0xF
    family = (entry >> 25) & 0x7
    return cond == 0xE and family == 0b101

def check_header(gba_file):
    with open(gba_file, "rb") as fd:
        click.echo(f"{gba_file}:")

        raw = fd.read()
        addresses = get_address(raw)
        PC = 0
        click.echo("|-- entry")
        click.echo(f"|   |-- valid: {is_valid_entry(addresses[0])}")
        click.echo(f"|   |-- raw: 0x{addresses[0]:08x}")
        click.echo(f"|   `-- opcode: {get_opcode(addresses[0], PC)}")
        # debug(raw)
