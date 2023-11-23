# [Windows in Docker](https://ms-jpq.github.io/windows-in-docker)

[![Docker Pulls](https://img.shields.io/docker/pulls/msjpq/windows-in-docker.svg)](https://hub.docker.com/r/msjpq/windows-in-docker/)

You really can run any VM / container you want under this. But I made it specifically to make headless windows less of a PITA.

Technically this is more of a "manage Windows in Docker" type of project, you can shutdown `dockerd` and all of your VMs won't be effected.

## What It Does

### Download VirtIO Windows Drivers

Periodically dump latest `virtio-win.iso` into `/data`

[From latest stable release](https://github.com/virtio-win/virtio-win-pkg-scripts)

### Web GUI 4 Virt Manager

![virt man](https://raw.githubusercontent.com/ms-jpq/windows-in-docker/main/screenshots/virtman.png)

## Usage

1. Install `libvirt-daemon` under **linux host**, ie `apt install -- libvirt-daemon-system`.

2. Adjust the broadway_port variable to define your own port. Default is 8080

3. Run the following `docker-compose`.

```yaml
---
version: "3.9"

services:
  libvirt:
    restart: always
    image: msjpq/windows-in-docker:latest
    security_opt:
      - apparmor=unconfined
    environment:
      TZ:
      # Make sure DATA_DIR is the same across the three `${DATA_DIR}`s
      # The windows drivers are also downloaded under here.
      DATA_DIR: "${DATA_DIR}"
      BROADWAY_PORT: "${BROADWAY_PORT}"
  
    ports:
      - 80:${BROADWAY_PORT}
    volumes:
      - /var/run/libvirt/libvirt-sock:/var/run/libvirt/libvirt-sock:ro
      - "${DATA_DIR}:${DATA_DIR}"
```

3. Drag in some ISOs you want to install under `${DATA_DIR}`.

4. Go to port 80, follow the GUI, you are good to go.

## Wait A Minute

Libvirt doesn't run under Docker tho?

Well, I realized running `libvirt` under Docker was actually a stupid idea.

You can't say provision a ZFS storage pool for example.
