#!/usr/bin/env python3

from os import sep
from pathlib import Path

sockets = Path(sep) / "var" / "run" / "libvirt"

for name in (
    "libvirt-admin-sock",
    "libvirt-sock",
    "libvirt-sock-ro",
    "virtlockd-admin-sock",
    "virtlockd-sock",
    "virtlogd-admin-sock",
    "virtlogd-sock",
):
    sock = sockets / name
    assert sock.is_socket(), sock
