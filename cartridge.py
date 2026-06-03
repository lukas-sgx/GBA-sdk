import click
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
    
cli.add_command(hdr)
hdr.add_command(dump)

def main():
    cli()

if __name__ == "__main__":
    main()