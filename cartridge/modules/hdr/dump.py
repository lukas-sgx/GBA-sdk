import click
from cartridge.services.header import Header

@click.command(help="dump / display cartridge header information")
@click.argument("GBA_FILES", required=False, nargs=-1)
def dump(gba_files):
    for file in gba_files:
        header = Header(file)
        header.display_header()