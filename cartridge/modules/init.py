import click
import urllib.request
import io
import tarfile
from cartridge import __version__

@click.command(help="Initialize project with default build")
def init():
    url = f"https://api.github.com/repos/lukas-sgx/GBA-sdk/tarball/v{__version__}"
    headers = {"User-Agent": "Python-Cartridge"}
    req = urllib.request.Request(url, headers=headers)

    click.echo(
        click.style("Downloading ", fg="green", bold=True) +
        click.style(f"GBA-sdk v{__version__}\n") +
        click.style(f"\t    {url}", fg=(138,138,138))
    )

    with urllib.request.urlopen(req) as response:
        tar_data = io.BytesIO(response.read())

        extracted_count = 0
        with tarfile.open(fileobj=tar_data, mode="r:gz") as tar:

            for member in tar.getmembers():
                parts = member.name.split("/", 1)
                if len(parts) < 2:
                    continue

                relative_path = parts[1]
                if relative_path.startswith(("sandbox/", "libs/")) and not member.isdir():
                    member.name = relative_path
                    click.echo(
                        click.style("Extracting  ", fg="green", bold=True) +
                        click.style(f"{member.name} -> .")
                    )
                    tar.extract(member, path=".")
                    extracted_count += 1
        click.echo(
            click.style("Finished", fg="green", bold=True) +
            click.style(f"    {extracted_count} dir(s) extracted\n")
        )