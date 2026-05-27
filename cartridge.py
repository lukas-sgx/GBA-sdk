import click
import header

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
        header.check_header(file)
    
cli.add_command(hdr)
hdr.add_command(dump)

def main():
    cli()

if __name__ == "__main__":
    main()