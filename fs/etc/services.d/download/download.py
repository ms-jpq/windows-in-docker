#!/usr/bin/env python3

from contextlib import suppress
from datetime import timedelta, timezone
from email.utils import parsedate_to_datetime
from http.client import HTTPResponse
from os import environ, sep, utime
from pathlib import Path, PurePosixPath
from stat import S_IRGRP, S_IROTH, S_IRUSR, S_IWUSR, S_IXGRP, S_IXOTH, S_IXUSR
from sys import stderr
from tempfile import NamedTemporaryFile
from time import sleep
from typing import Iterator, Tuple, cast
from urllib.parse import unquote, urlsplit
from urllib.request import Request, build_opener

_RWXR_XR_X = (S_IRUSR | S_IWUSR | S_IXUSR) | (S_IRGRP | S_IXGRP) | (S_IROTH | S_IXOTH)
_RW_R__R__ = (S_IRUSR | S_IWUSR) | (S_IRGRP) | (S_IROTH)
_MB = 10**6
_OPEN = build_opener()
_SLEEP = timedelta(days=1)


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


def _download(root: Path, src: str) -> None:
    root.mkdir(parents=True, exist_ok=True, mode=_RWXR_XR_X)

    path = PurePosixPath(unquote(urlsplit(src).path))
    dest = root / path.name

    size, mtime = _meta(src)
    with suppress(FileNotFoundError):
        stat = dest.stat()
        if size == stat.st_size and mtime == stat.st_mtime:
            return

    stream = _fetch(src)
    with NamedTemporaryFile(dir=dest.parent, prefix=dest.name, delete=False) as fd:
        for chunk in stream:
            fd.write(chunk)

    Path(fd.name).replace(dest)
    dest.chmod(_RW_R__R__)
    utime(dest, (mtime, mtime))


while True:
    try:
        if src := environ.get("WIN_DRIVER"):
            _download(Path(sep) / environ["DATA_DIR"], src=src)
    except Exception as e:
        stderr.write(repr(e))
    finally:
        sleep(_SLEEP.total_seconds())
