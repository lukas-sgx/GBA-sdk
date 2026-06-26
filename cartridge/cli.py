import click
from cartridge.modules.build import build
from cartridge.modules.hdr import hdr
from cartridge.modules.conv import conv
from cartridge.modules.init import init

@click.group(help="Cartridge SDK CLI entry")
def cli():
    pass

cli.add_command(build)
cli.add_command(hdr)
cli.add_command(conv)
cli.add_command(init)

def main():
    cli()