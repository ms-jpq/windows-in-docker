FROM ubuntu:latest

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends -- \
    python3-libvirt

WORKDIR /srv
COPY ./fs /

VOLUME [ "/var/run/libvirt/libvirt-sock-ro", "/data" ]

ENTRYPOINT [ "/srv/main.py" ]
CMD [ "/data", "--daemon", "60" ]
