#!/usr/bin/env python3

from os import sep
from pathlib import Path

sock = Path(sep) / "var" / "run" / "libvirt" / "libvirt-sock"
assert sock.is_socket(), sock
