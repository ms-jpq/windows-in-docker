from logging import INFO, StreamHandler, getLogger

log = getLogger()
log.setLevel(INFO)
log.addHandler(StreamHandler())
