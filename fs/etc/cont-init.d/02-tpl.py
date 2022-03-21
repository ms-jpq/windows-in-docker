#!/usr/bin/env python3

from os import altsep, environ, sep
from pathlib import Path, PurePosixPath
from string import Template

root = Path(sep)
srv = root / "srv"

p_root = PurePosixPath(altsep or sep)
path_prefix = p_root / environ["PATH_PREFIX"]
socket_prefix = path_prefix.as_posix().lstrip(p_root.as_posix())


nginx = Template((srv / "nginx.conf").read_text())
ng = nginx.safe_substitute(
    PATH_PREFIX=path_prefix,
    SOCKET_PREFIX=socket_prefix,
)
(root / "etc" / "nginx" / "nginx.conf").write_text(ng)

html = Template((srv / "index.html").read_text())
ht = html.substitute(
    PATH_PREFIX=path_prefix,
    SOCKET_PREFIX=socket_prefix,
    PAGE_TITLE=environ["PAGE_TITLE"],
    VNC_RESIZE=environ["VNC_RESIZE"],
)
(root / "usr" / "share" / "novnc" / "index.html").write_text(ht)
