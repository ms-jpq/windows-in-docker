from contextlib import suppress
from datetime import timezone
from email.utils import parsedate_to_datetime
from http.client import HTTPResponse
from os import utime
from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile
from typing import Iterator, Tuple, cast
from urllib.parse import unquote, urlsplit
from urllib.request import Request, build_opener

from .log import log

_MB = 10 ** 6
_OPEN = build_opener()


def _meta(uri: str) -> Tuple[int, float]:
    req = Request(url=uri, method="HEAD")
    with _OPEN.open(req) as resp:
        resp = cast(HTTPResponse, resp)
        tot, mtime = 0, 0.0
        for key, val in resp.headers.items():
            match = key.casefold()
            if match == "content-length":
                tot = int(val)
            elif match == "last-modified":
                if req_mtime := parsedate_to_datetime(val):
                    mtime = req_mtime.replace(tzinfo=timezone.utc).timestamp()

        return tot, mtime


def _fetch(uri: str) -> Iterator[bytes]:
    with _OPEN.open(uri) as resp:
        resp = cast(HTTPResponse, resp)
        while buf := resp.read(_MB):
            yield buf


def download(root: Path, src: str) -> None:
    path = PurePosixPath(unquote(urlsplit(src).path))
    dest = root / path.name

    size, mtime = _meta(src)
    with suppress(FileNotFoundError):
        stat = dest.stat()
        if size == stat.st_size and mtime == stat.st_mtime:
            return

    stream = _fetch(src)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=dest.parent, prefix=dest.name, delete=False) as fd:
        for chunk in stream:
            fd.write(chunk)

    Path(fd.name).replace(dest)
    utime(dest, (mtime, mtime))
    log.info("%s", f"downloaded -- {src}")
