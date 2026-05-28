import click

def get_address(raw):
    address = []
    for i in range(0, len(raw), 4):
        chunk = raw[i:i + 4]
        if len(chunk) == 4:
            address.append(int.from_bytes(chunk, 'little'))
    return address

def debug(raw):
    address = get_address(raw)
    for add in address:
        click.echo(f"{add:08x}")

def is_valid_entry(entry):
    cond = (entry >> 28) & 0xF
    family = (entry >> 25) & 0x7
    return cond == 0xE and family == 0b101

def check_header(gba_file):
    with open(gba_file, 'rb') as fd:
        click.echo(f"{gba_file}:")

        raw = fd.read()
        addresses = get_address(raw)
        click.echo("|-- entry")
        click.echo(f"|   |-- valid: {is_valid_entry(addresses[0])}")
        click.echo(f"|   |-- raw: 0x{addresses[0]:08x}")
        # debug(raw)