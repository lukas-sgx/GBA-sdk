import click
from PIL import Image
from cartridge.services.conversion import Conversion

@click.command(help="Convert font asset into raw C file")
@click.option("-o", "--output", required=True, type=click.Path(exists=False), help="Path to the generated C file")
@click.option("-w", "--width", required=True, type=click.INT, help="Character width in pixels")
@click.option("-h", "--height", required=True, type=click.INT, help="Character height in pixels")
@click.option("-m", "--margin", required=True, type=click.INT, help="Margin between characters in pixels")
@click.option("-l", "--line-height", required=True, type=click.INT, help="Virtual alignment line height in pixels")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
@click.argument("ASSET_PATH", required=True, type=click.STRING, nargs=1)
def conv(asset_path: str, output: str, width: int, height: int, margin: int, line_height: int, debug) -> None:
    img = Image.open(asset_path, mode="r").convert("L")
    dimension = (height, width, line_height, margin)
    convert = Conversion(img, dimension, debug)

    with open(output, mode="w") as file:
        file.write(convert.get_content())