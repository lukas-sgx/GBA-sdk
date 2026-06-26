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

    with urllib.request.urlopen(req) as response:
        tar_data = io.BytesIO(response.read())

        with tarfile.open(fileobj=tar_data, mode="r:gz") as tar:
            extracted_count = 0

            for member in tar.getmembers():
                parts = member.name.split("/", 1)
                if len(parts) < 2:
                    continue

                relative_path = parts[1]
                if relative_path.startswith(("sandbox/")) and not member.isdir():
                    member.name = relative_path
                    tar.extract(member, path=".")
                    extracted_count += 1