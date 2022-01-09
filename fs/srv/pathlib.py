from pathlib import Path
from stat import S_IRGRP, S_IROTH, S_IRUSR, S_IWUSR, S_IXGRP, S_IXOTH, S_IXUSR

FOLDER_MODE = (S_IRUSR | S_IWUSR | S_IXUSR) | (S_IRGRP | S_IXGRP) | (S_IROTH | S_IXOTH)
FILE_MODE = (S_IRUSR | S_IWUSR) | (S_IRGRP) | (S_IROTH)


def chmod(path: Path) -> None:
    path.chmod(FOLDER_MODE if path.is_dir() else FILE_MODE)
