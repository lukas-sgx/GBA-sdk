import click
from cartridge.services.generation import Generation
from typing import BinaryIO

@click.command(help="Insert the header into a binary")
@click.option("-b", "--binary", required=True, nargs=1, type=click.File("rb"), help="input binary file")
@click.option("-o", "--output", required=True, nargs=1, type=click.File("wb"), help="output filename")
@click.option("-n", "--name", nargs=1, type=click.STRING, help="internal cartridge name", show_default=True, default="filename")
def gen(binary: click.File, output: BinaryIO, name: str):
    Generation(binary.name, output, name, "BXXE")
