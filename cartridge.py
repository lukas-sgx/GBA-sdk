import click
import os
from header import Header

@click.group()
def cli():
    pass

@click.group()
def hdr():
    pass

@click.command()
@click.argument("GBA_FILES", required=False, nargs=-1)
def dump(gba_files):
    for file in gba_files:
        header = Header(file)
        header.display_header()

@click.command()
def build():
    command = ["make", "-C", "build"]
    os.execvp(command[0], command)
    
cli.add_command(hdr)
cli.add_command(build)
hdr.add_command(dump)

def main():
    cli()

if __name__ == "__main__":
    main()