#!/usr/bin/env python3

from os import environ, sep
from pathlib import Path

sock = Path(sep) / "var" / "run" / "libvirt" / "libvirt-sock"

if "DEV" not in environ:
    assert sock.is_socket(), sock
