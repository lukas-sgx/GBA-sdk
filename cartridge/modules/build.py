import click
import subprocess
import os
from cartridge.services.generation import Generation

@click.command(help="craft cartridge ROM (GBA)")
@click.option("-s", "--source", required=True, type=click.STRING, multiple=True, help="input source(s) file(s)")
@click.option("-o", "--output", required=True, nargs=1, type=click.File('wb'), help="output filename")
def build(source: tuple, output: click.File):
    name = output.name.split(".")[0]

    os.makedirs("bin", exist_ok=True)
    
    click.echo(f"[CC]  {' '.join(source)}")
    command = [
        "arm-none-eabi-gcc",
        "-mcpu=arm7tdmi", "-mlittle-endian",
        "-nostdlib",
        "-o", f"build/{name}.elf",
        *source,
        "-T", "./build/example/gba.ld"
    ]
    subprocess.run(command, check=True)

    click.echo(f"[BIN] {name}.elf -> {name}.bin")
    command = [
        "arm-none-eabi-objcopy",
        "-O", "binary",
        f"build/{name}.elf",
        f"./bin/{name}.bin"
    ]
    subprocess.run(command, check=True)

    with open(f"bin/{name}.bin", "rb") as bin_file:
        generation = Generation(bin_file, output, "filename")
