import click
import os
from header import Header

@click.group(help="Cartridge SDK CLI entry")
def cli():
    pass

@click.group(help="Cartridge header interface")
def hdr():
    pass

@click.command(help="dump / display cartridge header information")
@click.argument("GBA_FILES", required=False, nargs=-1)
def dump(gba_files):
    for file in gba_files:
        header = Header(file)
        header.display_header()

@click.command(help="build / build cartridge ROM")
def build():
    command = ["make", "-C", "build"]
    os.execvp(command[0], command)

@click.command(help="gen / generate cartridge ROM")
@click.option("-b", "--binary", required=True, nargs=1, type=click.File('rb'), help="input binary file")
@click.option("-o", "--output", required=True, nargs=1, type=click.File('wb'), help="output filename")
def gen():
    pass
    
cli.add_command(hdr)
hdr.add_command(build)
hdr.add_command(dump)
hdr.add_command(gen)

def main():
    cli()

if __name__ == "__main__":
    main()