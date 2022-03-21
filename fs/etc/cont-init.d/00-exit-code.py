#!/usr/bin/env python3

from os import sep
from pathlib import Path

path = Path(sep) / "run" / "s6-linux-init-container-results" / "exitcode"
path.write_text("1")
