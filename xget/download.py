import hashlib
import os
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import httpx
from print_err import print_err
from tqdm import tqdm


def download(url: str, checksum: str, overwrite: bool):

    assert len(checksum) == 64
    url_parts = urlparse(url)
    targat_filename = url_parts.path.split("/")[-1]
    hasher = hashlib.sha256()

    download_file = tempfile.NamedTemporaryFile(delete=False)
    with httpx.stream("GET", url) as response:
        total = int(response.headers["Content-Length"])

        with tqdm(
            total=total, unit_scale=True, unit_divisor=1024, unit="B"
        ) as progress:
            num_bytes_downloaded = response.num_bytes_downloaded
            for chunk in response.iter_bytes():
                download_file.write(chunk)
                hasher.update(chunk)
                progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                num_bytes_downloaded = response.num_bytes_downloaded
    download_file.close()

    if checksum != hasher.hexdigest():
        os.unlink(download_file.name)
        print_err(
            "ERROR: File content does not match the expected checksum!", exit_code=2
        )
    if overwrite and Path(targat_filename).exists:
        os.unlink(targat_filename)
    os.rename(download_file.name, targat_filename)
    print(f"File save to {targat_filename}")

    return download_file.name, hasher.hexdigest()
