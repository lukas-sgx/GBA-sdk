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
    os.makedirs("build", exist_ok=True)

    for file in source:
            ext = file.split(".")[-1]
            if ext == "c":
                label = "CC] "
            elif ext == "S":
                label = "ASM]"
            else:
                click.echo(click.style(f"[ERR] unsupported file: {file}", fg="red"), err=True)
                exit(1)
    
            click.echo(
                click.style(f"[{label} ", fg="blue", bold=True) +
                click.style(file, bold=True) +
                click.style(f" -> build/{name}.elf", fg="cyan")
            )

    subprocess.run([
        "arm-none-eabi-gcc",
        "-mcpu=arm7tdmi", "-mlittle-endian",
        "-nostdlib",
        "-o", f"build/{name}.elf",
        *source,
        "-T", "./build/linker/gba.ld"
    ], check=True)

    click.echo(
        click.style("[BIN] ", fg="blue", bold=True) +
        click.style(f"build/{name}.elf " , bold=True) +
        click.style(f"-> bin/{name}.bin", fg="cyan")
    )
    subprocess.run([
        "arm-none-eabi-objcopy",
        "-O", "binary",
        f"build/{name}.elf",
        f"./bin/{name}.bin"
    ], check=True)

    Generation(f"./bin/{name}.bin", output, "filename", "BXXE")
        