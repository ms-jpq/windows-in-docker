FROM ubuntu:jammy


ARG S6_OVERLAY_VERSION=3.0.0.2-2
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV TERM=xterm-256color


RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends -- \
    xz-utils \
    libgtk-3-bin \
    dbus-x11 \
    curl \
    socat \
    virt-manager \
    gir1.2-spiceclientgtk-3.0


ADD https://github.com/just-containers/s6-overlay/releases/download/v"$S6_OVERLAY_VERSION"/s6-overlay-noarch-"$S6_OVERLAY_VERSION".tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v"$S6_OVERLAY_VERSION"/s6-overlay-x86_64-"$S6_OVERLAY_VERSION".tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch-"$S6_OVERLAY_VERSION".tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-x86_64-"$S6_OVERLAY_VERSION".tar.xz && \
    rm -rf -- /tmp/**
ENV S6_KEEP_ENV=1 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_SERVICES_GRACETIME=0 \
    S6_KILL_GRACETIME=0
ENTRYPOINT [ "/init" ]


COPY ./fs /
ENV GDK_BACKEND=broadway \
    VIRT_CONN=qemu:///system \
    DATA_DIR=/data \
    WIN_DRIVER='https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso'
EXPOSE 8080
VOLUME [ "/data" ]
