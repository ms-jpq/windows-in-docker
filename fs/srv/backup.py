from contextlib import closing
from datetime import datetime
from itertools import repeat
from pathlib import Path
from typing import Any, Iterable, Iterator, Tuple

from libvirt import openReadOnly

from .log import log
from .stat import RW_R__R__, RWXR_XR_X


def _ls_domains(conn: Any) -> Iterator[Tuple[str, str]]:
    for domain in conn.listAllDomains():
        yield domain.name(), domain.XMLDesc()


def _ls_storage(conn: Any) -> Iterator[Tuple[str, str]]:
    for domain in conn.listAllStoragePools():
        yield domain.name(), domain.XMLDesc()


def _ls_networks(conn: Any) -> Iterator[Tuple[str, str]]:
    for network in conn.listAllNetworks():
        yield network.name(), network.XMLDesc()


def _backup(
    time: datetime, state: Iterable[Tuple[Path, Tuple[str, str]]]
) -> Iterator[str]:
    stub = time.isoformat().replace(":", ".") + ".xml"

    for kind, (name, xml) in state:
        base = kind / name
        path = base / stub

        base.mkdir(parents=True, exist_ok=True, mode=RWXR_XR_X)
        if prev := sorted(
            base.iterdir(),
            key=lambda p: datetime.fromisoformat(p.stem.replace(".", ":")),
            reverse=True,
        ):
            most_recent, *_ = prev
            if xml != most_recent.read_text():
                path.write_text(xml)
                path.chmod(RW_R__R__)
                yield name
        else:
            path.write_text(xml)
            path.chmod(RW_R__R__)
            yield name


def backup(root: Path) -> None:
    now = datetime.utcnow().replace(microsecond=0)

    with closing(openReadOnly()) as conn:
        state = (
            *zip(repeat(root / "domains"), _ls_domains(conn)),
            *zip(repeat(root / "storage"), _ls_storage(conn)),
            *zip(repeat(root / "networks"), _ls_networks(conn)),
        )

    root.chmod(RWXR_XR_X)
    for name in _backup(now, state=state):
        log.info("%s", f"backed up -- {name}")
