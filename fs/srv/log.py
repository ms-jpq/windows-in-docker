from logging import INFO, Formatter, Logger, StreamHandler, getLogger

_FMT = """
%(levelname)s\t%(asctime)s
%(message)s
"""
_TIME_FMT = "%x %X"


def _log() -> Logger:
    log = getLogger()
    log.setLevel(INFO)
    handler = StreamHandler()
    fmt = Formatter(_FMT, datefmt=_TIME_FMT)
    handler.setFormatter(fmt)
    log.addHandler(handler)
    return log


log = _log()
