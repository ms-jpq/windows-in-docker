FROM fedora:36


ARG S6_OVERLAY_VERSION=3.0.0.2-2
SHELL ["/bin/bash", "-o", "pipefail", "-c"]


RUN dnf --setopt=install_weak_deps=False install -y -- \
    xz \
    curl \
    dbus-daemon \
    virt-manager && \
    dnf clean all && \
    curl --location --output /tmp/s6-overlay-noarch.tar.xz -- \
         https://github.com/just-containers/s6-overlay/releases/download/v"$S6_OVERLAY_VERSION"/s6-overlay-noarch-"$S6_OVERLAY_VERSION".tar.xz && \
    curl --location --output /tmp/s6-overlay-some-arch.tar.xz -- \
         https://github.com/just-containers/s6-overlay/releases/download/v"$S6_OVERLAY_VERSION"/s6-overlay-"$(arch)"-"$S6_OVERLAY_VERSION".tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-some-arch.tar.xz
ENV TERM=xterm-256color\
    S6_KEEP_ENV=1 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_SERVICES_GRACETIME=0 \
    S6_KILL_GRACETIME=0
ENTRYPOINT [ "/init" ]


COPY ./fs /
ENV GDK_BACKEND=broadway \
    NO_AT_BRIDGE=1 \
    BROADWAY_PORT=8080 \
    VIRT_CONN=qemu:///system \
    DATA_DIR=/data \
    WIN_DRIVER='https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso'
EXPOSE 8080
VOLUME [ "/data" ]
