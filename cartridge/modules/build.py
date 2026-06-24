import click
import subprocess
import os
import glob
from cartridge.services.generation import Generation

def listBin() -> list[str]:
    return glob.glob("bin/*.bin")

@click.command(help="Craft cartridge ROM (GBA)")
@click.option("-s", "--source", required=True, type=click.Path(exists=True), help="set CMake dir")
def build(source: str) -> None:
    os.makedirs("bin", exist_ok=True)
    os.makedirs("build", exist_ok=True)

    PREV_DIR = os.getcwd()
    
    os.chdir(source)

    subprocess.run([
        "cmake",
        "."
    ], check=True)

    os.chdir(PREV_DIR)

    subprocess.run([
        "cmake",
        "--build",
        source
    ], check=True)

    for binary in listBin():
        project = binary.split(".")[0]
        output_path = f"{project}.gba"
        
        with open(output_path, "wb") as output_file:
            Generation(binary, output_file, project.split("/")[1], "BXXE")