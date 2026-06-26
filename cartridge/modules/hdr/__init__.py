import click
from cartridge.modules.hdr.dump import dump
from cartridge.modules.hdr.gen import gen

@click.group(help="Manage the cartridge header")
def hdr():
    pass

hdr.add_command(dump)
hdr.add_command(gen)