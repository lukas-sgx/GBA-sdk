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

def check_header(gba_file):
    with open(gba_file, 'rb') as fd:
        click.echo(f"{gba_file}:")

        raw = fd.read()
        click.echo("|-- entry")
        debug(raw)