from pathlib import Path
from stat import S_IRGRP, S_IROTH, S_IRUSR, S_IWUSR, S_IXGRP, S_IXOTH, S_IXUSR

RWXR_XR_X = (S_IRUSR | S_IWUSR | S_IXUSR) | (S_IRGRP | S_IXGRP) | (S_IROTH | S_IXOTH)
RW_R__R__ = (S_IRUSR | S_IWUSR) | (S_IRGRP) | (S_IROTH)


def chmod(path: Path) -> None:
    path.chmod(RWXR_XR_X if path.is_dir() else RW_R__R__)
