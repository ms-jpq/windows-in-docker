FROM ubuntu:latest

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends -- \
    dumb-init \
    python3-libvirt

WORKDIR /
COPY ./fs /

VOLUME [ "/var/run/libvirt", "/data" ]

ENTRYPOINT [ "dumb-init", "--" ]
CMD [ "python3", "-m", "srv", "--", "/data", "--daemon", "60", "--download" ]
