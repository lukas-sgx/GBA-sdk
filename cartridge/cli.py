import click
from cartridge.modules.build import build
from cartridge.modules.hdr import hdr
from cartridge.modules.conv import conv

@click.group(help="Cartridge SDK CLI entry")
def cli():
    pass

cli.add_command(build)
cli.add_command(hdr)
cli.add_command(conv)

def main():
    cli()