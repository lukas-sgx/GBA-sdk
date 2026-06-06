import click
from cartridge.modules.build import build
from cartridge.modules.hdr import hdr


@click.group(help="Cartridge SDK CLI entry")
def cli():
    pass


cli.add_command(build)
cli.add_command(hdr)

def main():
    cli()