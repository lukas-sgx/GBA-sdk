import click

class Generation:
    def __init__(self, binary: click.File, output: click.File, name: str) -> None:
        click.echo(f"[GEN] {binary.name} -> {output.name}")

    def header_fill(self):
        pass