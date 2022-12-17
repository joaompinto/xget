import typer
from download import download
from print_err import print_err


def main(url: str, checksum: str, force: bool = False):

    if len(checksum) != 64:
        print_err("ERROR: Checksum must be a sha256 checksum (64 chars)!", exit_code=1)

    print(f"Downloading {url}")
    download(url, checksum, force)


if __name__ == "__main__":
    typer.run(main)
