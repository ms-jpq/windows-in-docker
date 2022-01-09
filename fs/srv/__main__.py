from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import sleep
from typing import Callable, Iterator

from .backup import backup
from .download import download
from .log import log

_DRIVER_URI = "https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso"


def _cycle(period: int, fn: Callable[[], None]) -> None:
    while True:
        try:
            fn()
        except Exception as e:
            log.exception("%s", e)

        if period := max(0, period):
            sleep(period)
        else:
            break


def _exec(*stream: Callable[[], None]) -> None:
    with ThreadPoolExecutor() as pool:
        tuple(pool.map(lambda fn: fn(), stream))


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("destination")
    parser.add_argument("--daemon", type=int, default=0)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--driver", default=_DRIVER_URI)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    root = Path(args.destination).resolve(strict=True)

    def tasks() -> Iterator[Callable[[], None]]:
        yield lambda: _cycle(
            args.daemon,
            fn=lambda: backup(root),
        )

        if args.download:
            yield lambda: _cycle(
                args.daemon,
                fn=lambda: download(root, src=args.driver),
            )

    _exec(*tasks())


main()
