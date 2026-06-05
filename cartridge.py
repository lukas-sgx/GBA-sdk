import click
import os
import subprocess
from header import Header
from generation import Generation

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

def _gen(binary, output, name):
    # generation = Generation(binary, output, name)
    pass
        
@click.command(help="craft cartridge ROM (GBA)")
@click.option("-s", "--source", required=True, type=click.STRING, multiple=True, help="input source(s) file(s)")
@click.option("-o", "--output", required=True, nargs=1, type=click.File('wb'), help="output filename")
def build(source: tuple, output: click.File):
    name = output.name.split(".")[0]

    os.makedirs("bin", exist_ok=True)
    
    click.echo(f"[CC] ARM7TDMI source(s) file(s): {' '.join(source)}")
    command = [
        "arm-none-eabi-gcc",
        "-mcpu=arm7tdmi", "-mlittle-endian",
        "-nostdlib",
        "-o", f"build/{name}.elf",
        *source,
        "-T", "./build/gba.ld"
    ]
    subprocess.run(command, check=True)

    click.echo(f"[BIN] extract {name}.elf -> {name}.bin")
    command = [
        "arm-none-eabi-objcopy",
        "-O", "binary",
        f"build/{name}.elf",
        f"./bin/{name}.bin"
    ]
    subprocess.run(command, check=True)

    with open(f"bin/{name}.bin", "rb") as bin_file:
        _gen(bin_file, output, "filename")

@click.command(help="gen / generate cartridge ROM")
@click.option("-b", "--binary", required=True, nargs=1, type=click.File("rb"), help="input binary file")
@click.option("-o", "--output", required=True, nargs=1, type=click.File("wb"), help="output filename")
@click.option("-n", "--name", nargs=1, type=click.STRING, help="internal cartridge name", show_default=True, default="filename")
def gen(binary: click.File, output: click.File, name: str):
    _gen(binary, output, name)
    
cli.add_command(hdr)
cli.add_command(build)
hdr.add_command(dump)
hdr.add_command(gen)

def main():
    cli()

if __name__ == "__main__":
    main()