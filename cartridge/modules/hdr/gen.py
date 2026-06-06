import click
from cartridge.services.generation import Generation

@click.command(help="gen / generate cartridge ROM")
@click.option("-b", "--binary", required=True, nargs=1, type=click.File("rb"), help="input binary file")
@click.option("-o", "--output", required=True, nargs=1, type=click.File("wb"), help="output filename")
@click.option("-n", "--name", nargs=1, type=click.STRING, help="internal cartridge name", show_default=True, default="filename")
def gen(binary: click.File, output: click.File, name: str):
    Generation(binary.name, output, name, "BXXE")
    